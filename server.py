"""Server lokal TERRA NOVA — Final Feature Freeze v1.0 (Chapter I: The Calling of Gaia).

Pustaka standar Python 3 + SQLite (WAL), transaksi atomik, UUID idempotency, Lazy Tick,
Realistic_v1, 282 material + 307 mesin (288 canonical + 19 alias), 15 tanaman + Vitalitas,
GT01–09 + PR01–10 + TR01–05 + GSG, WtE/DRES rumahan, sungai mengalir, pasar NPC,
sandbox top-up, fixture leaderboard, admin config audit, dan feedback lokal.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import threading
import time
import urllib.parse
import uuid
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from engine.catalog import load_seed, make_quote, query_catalog
from engine.gameplay import (
    DEFAULT_CONFIG,
    TITIK_DALAM,
    TITIK_LUAR,
    TITIK_POHON,
    aksi,
    efek_mesin,
    meta_statis,
    migrasi_state,
    perlu,
    ringkasan_ekstra,
    road_y,
    settle_waktu,
    state_awal,
)

ROOT = Path(__file__).resolve().parent
_RIBUAN = re.compile(r"(?<=\d),(?=\d{3}(?!\d))")


META_STATIS_CACHE = meta_statis()  # teks misi, geometri lahan, paket: tetap selama proses server hidup


def angka_id(teks):
    """Pesan engine memakai f"{x:,}" (450,000); tampilkan pemisah ribuan Indonesia (450.000)."""
    return _RIBUAN.sub(".", teks) if isinstance(teks, str) else teks
# TN_DB_PATH: on Fly.io the database lives on the mounted volume (/data) so it survives restarts and deploys
DB_PATH = Path(os.environ.get("TN_DB_PATH") or (ROOT / "gaia.sqlite3"))

# ---------------------------------------------------------------- akun & sesi
PBKDF2_ITER = 240_000
SESI_DETIK = 30 * 24 * 3600
COOKIE = "tn_sesi"
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]{3,24}$")
EMAIL_RE = re.compile(r"^[^@\s]{1,64}@[^@\s]+\.[^@\s]{2,}$")
GAGAL_LOGIN = {}
GAGAL_LOCK = threading.Lock()
# Admin Config hanya untuk akun pemilik. Atur lewat env TN_ADMIN_USERS="nama1,nama2" (tanpa beda huruf besar/kecil).
ADMIN_USERS = {u.strip().lower() for u in os.environ.get("TN_ADMIN_USERS", "Dewa_Penguji").split(",") if u.strip()}


def is_admin(akun):
    return bool(akun) and akun["username"].lower() in ADMIN_USERS


def hash_sandi(sandi, salt=None):
    salt = salt or os.urandom(16)
    return salt.hex(), hashlib.pbkdf2_hmac("sha256", sandi.encode("utf-8"), salt, PBKDF2_ITER).hex()


def cek_sandi(sandi, salt_hex, hash_hex):
    return hmac.compare_digest(hash_sandi(sandi, bytes.fromhex(salt_hex))[1], hash_hex)


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def buat_sesi(db, akun_id):
    token = secrets.token_urlsafe(32)
    db.execute("DELETE FROM sesi WHERE kedaluwarsa < ?", (time.time(),))
    db.execute("INSERT INTO sesi VALUES(?,?,?)", (hash_token(token), akun_id, time.time() + SESI_DETIK))
    return token


def akun_dari_token(token):
    if not token:
        return None
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute(
            "SELECT a.id, a.username FROM sesi s JOIN akun a ON a.id = s.akun_id "
            "WHERE s.token = ? AND s.kedaluwarsa > ?",
            (hash_token(token), time.time()),
        ).fetchone()
    return {"id": row[0], "username": row[1]} if row else None


def sudah_diterima(akun_id):
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute("SELECT data FROM pemain_akun WHERE akun_id=?", (akun_id,)).fetchone()
    return bool(row and json.loads(row[0]).get("diterima"))


def get_active_config():
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute("SELECT version, data FROM config_version ORDER BY version DESC LIMIT 1").fetchone()
    if not row:
        return dict(DEFAULT_CONFIG)
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(json.loads(row[1]))
    cfg["version"] = row[0]
    return cfg


def publish_config(updates, actor, reason):
    cfg = get_active_config()
    allowed_num = {
        "starter_gc": (100_000, 10_000_000),
        "pickup_reward_gc": (0, 5_000),
        "pickup_daily_cap_gc": (0, 50_000),
        "rare_boost_daily_cap_gc": (0, 50_000),
    }
    for k, (lo, hi) in allowed_num.items():
        if k in updates:
            v = int(updates[k])
            perlu(lo <= v <= hi, f"Parameter {k} harus di antara {lo} dan {hi}.")
            cfg[k] = v
    if "price_multiplier" in updates:
        pm = float(updates["price_multiplier"])
        perlu(0.5 <= pm <= 2.0, "price_multiplier harus antara 0.5 dan 2.0.")
        cfg["price_multiplier"] = round(pm, 2)
    for url_k in ("support_url", "sponsor_contact_url", "soundtrack_url"):
        if url_k in updates:
            val = updates[url_k]
            if val is None or str(val).strip() == "":
                cfg[url_k] = None
            else:
                sval = str(val).strip()
                perlu(sval.startswith("https://") and len(sval) <= 256, f"{url_k} wajib HTTPS valid.")
                cfg[url_k] = sval
    new_ver = int(cfg["version"]) + 1
    cfg["version"] = new_ver
    now = time.time()
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        db.execute("INSERT INTO config_version(version, data, created_at) VALUES(?,?,?)", (new_ver, json.dumps(cfg), now))
        db.execute("INSERT INTO admin_audit(version, actor, reason, created_at) VALUES(?,?,?,?)", (new_ver, actor[:40], reason[:200], now))
    return cfg


def rollback_config(target_ver, actor, reason):
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute("SELECT data FROM config_version WHERE version=?", (int(target_ver),)).fetchone()
        perlu(row is not None, f"Versi config {target_ver} tidak ditemukan.")
        old_data = json.loads(row[0])
        latest = db.execute("SELECT COALESCE(MAX(version), 1) FROM config_version").fetchone()[0]
        new_ver = latest + 1
        old_data["version"] = new_ver
        now = time.time()
        db.execute("INSERT INTO config_version(version, data, created_at) VALUES(?,?,?)", (new_ver, json.dumps(old_data), now))
        db.execute("INSERT INTO admin_audit(version, actor, reason, created_at) VALUES(?,?,?,?)", (new_ver, actor[:40], f"ROLLBACK to v{target_ver}: {reason[:160]}", now))
    return old_data


def daftar_akun(data):
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    sandi = str(data.get("password", ""))
    perlu(USERNAME_RE.match(username), "Nama pengguna 3–24 karakter: huruf, angka, titik atau garis bawah.")
    perlu(len(email) <= 254 and EMAIL_RE.match(email), "Alamat email tidak valid.")
    perlu(8 <= len(sandi) <= 128, "Kata sandi minimal 8 karakter.")
    salt, h = hash_sandi(sandi)
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        try:
            cur = db.execute(
                "INSERT INTO akun(username,email,salt,hash,dibuat) VALUES(?,?,?,?,?)",
                (username, email, salt, h, time.time()),
            )
        except sqlite3.IntegrityError:
            raise ValueError("Nama pengguna atau email sudah terdaftar. Silakan masuk.")
        return {"id": cur.lastrowid, "username": username}, buat_sesi(db, cur.lastrowid)


def masuk_akun(data, ip):
    kini = time.time()
    with GAGAL_LOCK:
        GAGAL_LOGIN[ip] = [t for t in GAGAL_LOGIN.get(ip, []) if kini - t < 600]
        perlu(len(GAGAL_LOGIN[ip]) < 8, "Terlalu banyak percobaan masuk. Coba lagi dalam 10 menit.")
    login = str(data.get("login", "")).strip()
    sandi = str(data.get("password", ""))
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute(
            "SELECT id, username, salt, hash FROM akun WHERE username = ? OR email = ?",
            (login, login.lower()),
        ).fetchone()
        if not row or not cek_sandi(sandi, row[2], row[3]):
            with GAGAL_LOCK:
                GAGAL_LOGIN.setdefault(ip, []).append(kini)
            raise ValueError("Nama pengguna/email atau kata sandi salah.")
        return {"id": row[0], "username": row[1]}, buat_sesi(db, row[0])


def transaksi(akun_id, payload=None, key=None):
    cfg = get_active_config()
    db = sqlite3.connect(DB_PATH, timeout=10)
    try:
        with db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT data FROM pemain_akun WHERE akun_id=?", (akun_id,)).fetchone()
            s = migrasi_state(json.loads(row[0]), cfg) if row else state_awal(cfg["starter_gc"])
            kini = time.time()
            settle_waktu(s, kini)
            pesan = ""
            if payload:
                kanonik = json.dumps(payload, sort_keys=True)
                rkey = f"{akun_id}:{key}"
                lama = db.execute("SELECT aksi,kota,pesan FROM receipt WHERE id=?", (rkey,)).fetchone()
                if lama:
                    perlu(lama[0] == payload.get("aksi") and lama[1] == kanonik, "Kunci aksi berbeda isi.")
                    pesan = lama[2]
                else:
                    pesan = aksi(s, payload, kini, cfg)
                    db.execute("INSERT INTO receipt VALUES(?,?,?,?)", (rkey, payload.get("aksi", ""), kanonik, pesan))
            db.execute("INSERT OR REPLACE INTO pemain_akun VALUES(?,?)", (akun_id, json.dumps(s)))
            return {"state": s, "meta": ringkasan_ekstra(s, kini, cfg), "pesan": angka_id(pesan)}
    finally:
        db.close()


def baca_state(akun_id):
    """Baca state tanpa menulis ke DB (untuk endpoint GET yang hanya menampilkan)."""
    cfg = get_active_config()
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute("SELECT data FROM pemain_akun WHERE akun_id=?", (akun_id,)).fetchone()
    if not row:
        return None
    s = migrasi_state(json.loads(row[0]), cfg)
    settle_waktu(s, time.time())
    return s


def build_leaderboard_fixture(board="sustainability", my_state=None):
    """Local clearly-labeled fixture for all 14 GGL boards (no PII, no real global import)."""
    BOARDS = {
        "wealthiest": ("Wealthiest", "Net Worth (GC)"),
        "industrial_titans": ("Industrial Titans", "Kapasitas Aktif"),
        "waste_masters": ("Waste Masters", "Massa Terpulihkan (kg)"),
        "circular_masters": ("Circular Masters", "Rasio Pemulihan (%)"),
        "energy_masters": ("Energy Masters", "Listrik Waste-Origin (kWh)"),
        "renewable_masters": ("Renewable Masters", "Energi Terbarukan (kWh)"),
        "independence": ("Independence", "Kemandirian Energi (%)"),
        "food_guardians": ("Food Guardians", "Panen Pangan (varietas)"),
        "river_guardians": ("River Guardians", "Lot Sungai Aman"),
        "sustainability": ("Sustainability", "Skor Keberlanjutan"),
        "badge_collectors": ("Badge Collectors", "Lencana Unik"),
        "path_of_enough": ("Path of Enough", "Provisional (Bukan Chosen)"),
        "community_heroes": ("Community Heroes", "Kontribusi Komunitas"),
        "hall_of_fame": ("Hall of Fame", "Histori God"),
    }
    if board not in BOARDS:
        board = "sustainability"
    title, metric = BOARDS[board]
    rows = [
        {"public_id": "TN-FX-01", "nama": "Raka Nusantara", "kota": "Bandung", "tier": "Guardian", "self_made": True, "score": 84, "note": "Fixture"},
        {"public_id": "TN-FX-02", "nama": "Sari Lestari", "kota": "Yogyakarta", "tier": "Ascendant", "self_made": True, "score": 91, "note": "Fixture"},
        {"public_id": "TN-FX-03", "nama": "Bima Pesisir", "kota": "Surabaya", "tier": "Recycler", "self_made": True, "score": 68, "note": "Fixture"},
    ]
    if my_state:
        st = my_state["stat"]
        en = my_state["energy"]
        val_map = {
            "wealthiest": my_state["koin"],
            "waste_masters": round(st["pulih_unik_g"] / 1000, 1),
            "energy_masters": round(en["waste_origin_used_wh"] / 1000, 2),
            "renewable_masters": round(en["renewable_used_wh"] / 1000, 2),
            "food_guardians": len(st["varietas_panen"]),
            "river_guardians": st["sungai"] + st["sungai_apung"],
            "badge_collectors": len(my_state.get("gt_claimed", [])) + len(my_state.get("pr_claimed", [])),
            "sustainability": min(100, 30 + st["neraca_valid"] * 4 + len(st["hari_bersih"]) * 5),
        }
        rows.append({
            "public_id": "LOCAL-YOU",
            "nama": my_state["nama"] + " (Anda · Lokal)",
            "kota": my_state["kota"],
            "tier": my_state["tier"],
            "self_made": my_state["wallet"].get("self_made_provisional", True),
            "score": val_map.get(board, st["pungut"]),
            "note": "Akun Lokal",
        })
    rows.sort(key=lambda r: (-r["score"], r["public_id"]))
    return {
        "mode": "LOCAL_FIXTURE_ONLY",
        "label": "FIXTURE LOKAL — bukan ranking publik beta",
        "board": board,
        "title": title,
        "metric": metric,
        "boards": [{"id": k, "title": v[0], "metric": v[1]} for k, v in BOARDS.items()],
        "rows": rows,
    }


INTRO_MIME = {
    ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8", ".json": "application/json", ".webp": "image/webp",
    ".m4a": "audio/mp4", ".ogg": "audio/ogg", ".vtt": "text/vtt; charset=utf-8", ".md": "text/markdown; charset=utf-8",
}


class Layanan(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def kirim(self, isi, mime, kode=200, cache="no-store", header=None):
        self.send_response(kode)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (header or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(isi)

    def kirim_media(self, isi, mime, cache="no-cache"):
        """Audio dengan dukungan satu rentang byte (Range) agar browser bisa seek/stream Opus & AAC."""
        total = len(isi)
        rng = self.headers.get("Range", "")
        m = re.match(r"bytes=(\d*)-(\d*)$", rng.strip()) if rng else None
        if not m or (not m.group(1) and not m.group(2)):
            self.kirim(isi, mime, cache=cache, header={"Accept-Ranges": "bytes"})
            return
        if m.group(1):
            awal = int(m.group(1)); akhir = int(m.group(2)) if m.group(2) else total - 1
        else:
            awal = max(0, total - int(m.group(2))); akhir = total - 1
        akhir = min(akhir, total - 1)
        if awal > akhir or awal >= total:
            self.kirim(b"", mime, kode=416, cache=cache, header={"Content-Range": f"bytes */{total}"})
            return
        self.kirim(isi[awal:akhir + 1], mime, kode=206, cache=cache,
                   header={"Accept-Ranges": "bytes", "Content-Range": f"bytes {awal}-{akhir}/{total}"})

    def kirim_json(self, obj, kode=200, header=None):
        self.kirim(json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", kode, header=header)

    def token(self):
        c = SimpleCookie()
        try:
            c.load(self.headers.get("Cookie", ""))
        except Exception:
            return None
        return c[COOKIE].value if COOKIE in c else None

    def akun(self):
        return akun_dari_token(self.token())

    def cookie(self, token, umur=SESI_DETIK):
        aman = "; Secure" if self.headers.get("X-Forwarded-Proto", "").lower() == "https" else ""
        return {"Set-Cookie": f"{COOKIE}={token}; Max-Age={umur}; Path=/; HttpOnly; SameSite=Lax{aman}"}

    def ip(self):
        return self.client_address[0]

    def do_GET(self):
        parsed = urllib.parse.urlsplit(self.path)
        jalan = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if jalan == "/":
            akun = self.akun()
            halaman = "web/index.html" if akun and sudah_diterima(akun["id"]) else "web/landing.html"
            self.kirim((ROOT / halaman).read_bytes(), "text/html; charset=utf-8")
        elif jalan == "/akun":
            akun = self.akun()
            self.kirim_json({"masuk": bool(akun), "username": akun["username"] if akun else None, "diterima": sudah_diterima(akun["id"]) if akun else False})
        elif jalan == "/state":
            akun = self.akun()
            if not akun:
                return self.kirim_json({"pesan": "Silakan masuk terlebih dahulu."}, 401)
            hasil = transaksi(akun["id"])
            hasil["akun"] = {"username": akun["username"], "admin": is_admin(akun)}
            self.kirim_json(hasil)
        elif jalan == "/meta-statis":
            self.kirim_json(META_STATIS_CACHE)
        elif jalan == "/catalog":
            res = query_catalog(
                kind=qs.get("kind", ["all"])[0],
                category=qs.get("cat", [""])[0],
                search=qs.get("q", [""])[0],
                page=qs.get("page", ["1"])[0],
                per_page=qs.get("per_page", ["24"])[0],
                only_active=qs.get("active", ["0"])[0] in ("1", "true"),
            )
            seed = load_seed()
            kind = qs.get("kind", ["all"])[0]
            sumber = seed["machines"] if kind == "machine" else seed["materials"] if kind == "material" else []
            res["categories"] = sorted({x.get("category") for x in sumber if x.get("category")})
            for it in res.get("items", []):
                if it.get("catalog_kind") == "machine":
                    it["efek"] = efek_mesin(it.get("canonical_id") or it["id"])
            self.kirim_json(res)
        elif jalan == "/leaderboard":
            akun = self.akun()
            st = baca_state(akun["id"]) if akun else None
            if st and not st.get("diterima"):
                st = None
            board = qs.get("board", ["sustainability"])[0]
            self.kirim_json(build_leaderboard_fixture(board, st))
        elif jalan == "/admin/config":
            akun = self.akun()
            if not akun:
                return self.kirim_json({"pesan": "Login diperlukan."}, 401)
            with sqlite3.connect(DB_PATH, timeout=10) as db:
                audits = [
                    {"version": r[0], "actor": r[1], "reason": r[2], "created_at": r[3]}
                    for r in db.execute("SELECT version, actor, reason, created_at FROM admin_audit ORDER BY id DESC LIMIT 15").fetchall()
                ] if is_admin(akun) else []
            self.kirim_json({"config": get_active_config(), "audit": audits, "is_admin": is_admin(akun)})
        elif jalan == "/feedback":
            akun = self.akun()
            if not akun:
                return self.kirim_json({"pesan": "Login diperlukan."}, 401)
            with sqlite3.connect(DB_PATH, timeout=10) as db:
                rows = [
                    {"id": r[0], "category": r[1], "rating": r[2], "message": r[3], "created_at": r[4]}
                    for r in db.execute("SELECT id, category, rating, message, created_at FROM feedback WHERE akun_id=? ORDER BY id DESC LIMIT 20", (akun["id"],)).fetchall()
                ]
            self.kirim_json({"items": rows})
        elif jalan.startswith("/assets/") and ".." not in jalan:
            f = (ROOT / "web" / jalan[1:]).resolve()
            tipe = {
                ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp",
                ".wav": "audio/wav", ".txt": "text/plain", ".json": "application/json",
                ".svg": "image/svg+xml", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                ".m4a": "audio/mp4",
            }.get(f.suffix.lower())
            if tipe and f.is_file() and (ROOT / "web" / "assets") in f.parents:
                if tipe == "audio/mp4":   # songs: Range support so the browser streams/seeks instead of downloading all
                    self.kirim_media(f.read_bytes(), tipe, cache="public, max-age=86400")
                else:
                    self.kirim(f.read_bytes(), tipe, cache="public, max-age=3600")
            else:
                self.send_error(404)
        elif jalan == "/intro":
            self.send_response(301)
            self.send_header("Location", "/intro/" + (("?" + parsed.query) if parsed.query else ""))
            self.end_headers()
        elif jalan.startswith("/intro/") and ".." not in jalan:
            base = (ROOT / "cinematic-web" / "runtime").resolve()
            rel = jalan[len("/intro/"):] or "index.html"
            f = (base / rel).resolve()
            tipe = INTRO_MIME.get(f.suffix.lower())
            if tipe and f.is_file() and base in f.parents:
                if tipe.startswith("audio/"):
                    self.kirim_media(f.read_bytes(), tipe)
                else:
                    self.kirim(f.read_bytes(), tipe, cache="no-cache")
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        try:
            perlu("application/json" in self.headers.get("Content-Type", ""), "Permintaan tidak valid.")
            n = int(self.headers.get("Content-Length", "0"))
            perlu(0 <= n <= 8192, "Ukuran permintaan tidak valid.")
            data = json.loads(self.rfile.read(n) or b"{}")
            perlu(isinstance(data, dict), "Permintaan tidak valid.")

            if self.path == "/daftar":
                akun, token = daftar_akun(data)
                return self.kirim_json({"ok": True, "username": akun["username"], "diterima": False}, header=self.cookie(token))
            if self.path == "/masuk":
                akun, token = masuk_akun(data, self.ip())
                return self.kirim_json({"ok": True, "username": akun["username"], "diterima": sudah_diterima(akun["id"])}, header=self.cookie(token))
            if self.path == "/keluar":
                tok = self.token()
                if tok:
                    with sqlite3.connect(DB_PATH, timeout=10) as db:
                        db.execute("DELETE FROM sesi WHERE token = ?", (hash_token(tok),))
                return self.kirim_json({"ok": True}, header=self.cookie("", 0))

            akun = self.akun()
            if not akun:
                return self.kirim_json({"pesan": "Sesi berakhir. Silakan masuk kembali."}, 401)

            if self.path == "/market/quote":
                cfg = get_active_config()
                q = make_quote(str(data.get("kind", "")), str(data.get("id", "")), str(data.get("side", "buy")), data.get("qty", 1), time.time(), cfg["price_multiplier"])
                return self.kirim_json({"quote": q})

            if self.path == "/admin/config":
                if not is_admin(akun):
                    return self.kirim_json({"pesan": "Admin Config hanya untuk akun pemilik."}, 403)
                perlu(isinstance(data.get("updates", {}), dict), "Format pembaruan config tidak valid.")
                if "rollback_to" in data:
                    cfg = rollback_config(data["rollback_to"], akun["username"], str(data.get("reason", "rollback lokal")))
                    return self.kirim_json({"ok": True, "config": cfg, "pesan": f"Config di-rollback ke versi baru v{cfg['version']}."})
                cfg = publish_config(data.get("updates", {}), akun["username"], str(data.get("reason", "pembaruan lokal")))
                return self.kirim_json({"ok": True, "config": cfg, "pesan": f"Config v{cfg['version']} diterbitkan."})

            if self.path == "/feedback":
                cat = str(data.get("category", "saran"))[:32]
                rating = max(1, min(5, int(data.get("rating", 5) or 5)))
                msg = str(data.get("message", "")).strip()[:1000]
                perlu(len(msg) >= 3, "Tulis masukan minimal 3 karakter.")
                with sqlite3.connect(DB_PATH, timeout=10) as db:
                    db.execute(
                        "INSERT INTO feedback(akun_id, category, rating, message, consent, created_at) VALUES(?,?,?,?,?,?)",
                        (akun["id"], cat, rating, msg, int(bool(data.get("consent", True))), time.time()),
                    )
                return self.kirim_json({"ok": True, "pesan": "Terima kasih! Masukan tersimpan di log lokal."})

            perlu(self.path == "/aksi", "Permintaan tidak valid.")
            key = str(uuid.UUID(data["key"]))
            payload = {k: v for k, v in data.items() if k != "key"}
            hasil = transaksi(akun["id"], payload, key)
            self.kirim_json(hasil)
        except (ValueError, TypeError, KeyError) as e:
            self.kirim_json({"pesan": angka_id(str(e))}, 400)
        except Exception:  # jangan pernah memutus koneksi tanpa jawaban
            import traceback
            traceback.print_exc()
            self.kirim_json({"pesan": "Terjadi kesalahan di server lokal. Coba lagi."}, 500)


def siapkan_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("PRAGMA journal_mode=WAL;")
        db.execute("PRAGMA foreign_keys=ON;")
        db.executescript(
            "CREATE TABLE IF NOT EXISTS pemain(id INTEGER PRIMARY KEY,data TEXT);"
            "CREATE TABLE IF NOT EXISTS receipt(id TEXT PRIMARY KEY,aksi TEXT,kota TEXT,pesan TEXT);"
            "CREATE TABLE IF NOT EXISTS akun(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " username TEXT NOT NULL UNIQUE COLLATE NOCASE, email TEXT NOT NULL UNIQUE COLLATE NOCASE,"
            " salt TEXT NOT NULL, hash TEXT NOT NULL, dibuat REAL NOT NULL);"
            "CREATE TABLE IF NOT EXISTS sesi(token TEXT PRIMARY KEY, akun_id INTEGER NOT NULL"
            " REFERENCES akun(id), kedaluwarsa REAL NOT NULL);"
            "CREATE TABLE IF NOT EXISTS pemain_akun(akun_id INTEGER PRIMARY KEY REFERENCES akun(id), data TEXT);"
            "CREATE TABLE IF NOT EXISTS config_version(version INTEGER PRIMARY KEY, data TEXT NOT NULL, created_at REAL NOT NULL);"
            "CREATE TABLE IF NOT EXISTS admin_audit(id INTEGER PRIMARY KEY AUTOINCREMENT, version INTEGER NOT NULL, actor TEXT NOT NULL, reason TEXT NOT NULL, created_at REAL NOT NULL);"
            "CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY AUTOINCREMENT, akun_id INTEGER NOT NULL, category TEXT NOT NULL, rating INTEGER NOT NULL, message TEXT NOT NULL, consent INTEGER NOT NULL, created_at REAL NOT NULL);"
        )
        if not db.execute("SELECT 1 FROM config_version LIMIT 1").fetchone():
            db.execute("INSERT INTO config_version(version, data, created_at) VALUES(1, ?, ?)", (json.dumps(DEFAULT_CONFIG), time.time()))
            db.execute("INSERT INTO admin_audit(version, actor, reason, created_at) VALUES(1, 'system', 'initial feature freeze v1.0 seed', ?)", (time.time(),))


if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    siapkan_db()
    load_seed()  # warm catalog cache
    host = os.environ.get("TN_HOST", "127.0.0.1")   # hosting (Fly.io): TN_HOST=0.0.0.0 and PORT from the platform
    port = int(os.environ.get("PORT", "8765"))
    print(f"Buka http://{host}:{port}", flush=True)
    ThreadingHTTPServer((host, port), Layanan).serve_forever()
