"""Server lokal untuk review Fase 0/1 TERRA NOVA (v0.8 · DWE + DLE + Kebun Gaia).

Akun pemain (daftar/masuk, sesi cookie), progres per akun, pustaka standar Python 3, transaksi SQLite atomik,
kunci permintaan UUID idempotent, dan evaluasi Lazy Tick + DLE deterministik.
"""
import hashlib
import hmac
import json
import os
import random
import re
import secrets
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "gaia.sqlite3"

FRAKSI = ("organik", "plastik", "kertas", "logam_kaca", "residu", "B3")
LANGKA = ["Bayam Fajar Gaia", "Kangkung Embun", "Sawi Cahaya"]
KOTA_SAH = ("Bandung", "Jakarta", "Surabaya", "Kota lainnya")
AVATAR_ALLOW = {
    "rambut": ("pendek", "ikal", "panjang", "cepuk"),
    "baju": ("hijau", "biru", "coklat", "kuning"),
    "topi": ("tanpa", "rimba", "cap", "daun"),
    "aksesori": ("tanpa", "kacamata", "ransel", "syal"),
}

NODE_TEMPLATE = {
    "permukiman": {
        "nama": "Permukiman Warga",
        "kapasitas_g": 150_000,
        "laju_per_menit_g": 600,
        "jarak_km": 2,
        "tarif": 4,
        "komposisi": {"organik": 50, "plastik": 20, "kertas": 15, "logam_kaca": 5, "residu": 9, "B3": 1},
    },
    "pasar": {
        "nama": "Pasar Tradisional",
        "kapasitas_g": 150_000,
        "laju_per_menit_g": 700,
        "jarak_km": 4,
        "tarif": 6,
        "komposisi": {"organik": 78, "plastik": 12, "kertas": 5, "logam_kaca": 1, "residu": 4, "B3": 0},
    },
    "sungai": {
        "nama": "Tepi Sungai",
        "kapasitas_g": 100_000,
        "laju_per_menit_g": 250,
        "jarak_km": 1,
        "tarif": 2,
        "komposisi": {"organik": 0, "plastik": 55, "kertas": 0, "logam_kaca": 15, "residu": 30, "B3": 0},
    },
}

TIERS = [
    (0, "Awaken"),
    (500, "Seeker"),
    (2000, "Sorter"),
    (6000, "Recycler"),
    (15000, "Guardian"),
    (35000, "Ascendant"),
    (80000, "Titan"),
    (180000, "Archon"),
    (400000, "God"),
]


def bagi_g(total_g, komp):
    out = {}
    sisa = int(total_g)
    aktif = [f for f in FRAKSI if komp.get(f, 0) > 0]
    for f in FRAKSI:
        v = (int(total_g) * komp.get(f, 0)) // 100
        out[f] = v
        sisa -= v
    if sisa > 0 and aktif:
        out[aktif[0]] += sisa
    return out


# ---------------------------------------------------------------- Evaluasi 1: sampah liar, lahan, pencapaian
# Litter lying in and around the starter yard (image coordinates of web/assets/img/yard_iso.webp).
# jenis -> (inventory key, min g, max g). Black bags are unsorted (campuran), batteries are B3.
JENIS_SAMPAH = {
    "botol": ("plastik_g", 300, 700), "kaleng": ("logam_kaca_g", 200, 500), "kardus": ("kertas_g", 400, 1000),
    "organik": ("organik_g", 600, 1500), "kaca": ("logam_kaca_g", 400, 900), "kantong": ("campuran_g", 1500, 3000),
    "baterai": ("b3_g", 80, 200), "sterofoam": ("residu_g", 150, 400),
    # organic litter from the trees around the yard
    "daun": ("organik_g", 150, 400), "ranting": ("organik_g", 250, 700), "dahan": ("organik_g", 600, 1200),
    "buah": ("organik_g", 300, 700),
}
JENIS_UMUM = ("botol", "kaleng", "kardus", "organik", "kaca", "kantong", "baterai", "sterofoam")
LABEL_SAMPAH = {"botol": "Botol plastik", "kaleng": "Kaleng", "kardus": "Kardus & kertas", "organik": "Sisa organik",
                "kaca": "Botol kaca", "kantong": "Kantong sampah campur", "baterai": "Baterai bekas (B3)",
                "sterofoam": "Sterofoam", "daun": "Daun kering", "ranting": "Ranting patah", "dahan": "Dahan patah",
                "buah": "Buah busuk"}
TITIK_DALAM = [(700, 480), (780, 520), (880, 475), (925, 425), (895, 372), (665, 522), (1000, 505), (860, 548), (940, 482)]
TITIK_LUAR = [  # top grass, left grass, right grass, strip in front of the fence, river bank
    (300, 250), (480, 170), (620, 120), (1150, 110), (1300, 230), (200, 150), (1440, 330),
    (150, 470), (260, 420), (120, 560), (300, 540), (1620, 330), (1380, 620),
    (480, 582), (620, 592), (1050, 612), (1200, 622), (1330, 642),
    (150, 735), (450, 765), (700, 800), (1000, 835), (1250, 860), (1500, 880),
]
TITIK_SUNGAI = {(150, 735), (450, 765), (700, 800), (1000, 835), (1250, 860), (1500, 880)}
SAMPAH_MAKS_LUAR = 16
# trees around the yard: litter spot near each trunk (the client knows the matching crown for the leaf animation)
TITIK_POHON = [(190, 150), (440, 195), (590, 258), (280, 345), (140, 482), (700, 140), (1195, 152), (1560, 125),
               (1440, 270), (1630, 600)]
POHON_SLOT_DETIK, POHON_MAKS = 60, 6
# passing vehicles that may drop litter: kind -> (lanes, possible litter)
KENDARAAN = {
    "pikap": ("RL", ("organik", "organik", "kardus")), "truk": ("RL", ("kardus", "kantong", "sterofoam")),
    "motor": ("RL", ("botol", "kaleng", "kantong")), "sepeda": ("RL", ("botol", "kardus")),
    "becak": ("RL", ("kardus", "organik", "sterofoam")), "delman": ("RL", ("organik", "daun")),
}
JALAN_SLOT_DETIK, JALAN_MAKS = 40, 5


def road_y(x):
    return 611 + 0.0962 * x   # road centre line (regression on the lane markings)
SAMPAH_SLOT_DETIK = 90          # one new piece of litter outside the fence every 90 s (if a spot is free)
HARGA_PETAK = (250, 500, 750)   # extra planting plots (max 3)
HARGA_GUDANG = (400, 800)       # +250 kg storage, twice


def stat_awal():
    return {"pungut": 0, "pungut_dalam": 0, "sungai": 0, "pilah_g": 0, "kompos": 0, "panen": 0, "koin_jual": 0}


def buat_sampah(s, x, y, rng, zona):
    jenis = rng.choice(JENIS_UMUM)
    if zona == "dalam" and jenis == "baterai" and rng.random() < 0.5:
        jenis = "kantong"
    _, lo, hi = JENIS_SAMPAH[jenis]
    s["sampah_seq"] += 1
    s["sampah_liar"].append({"id": f"s{s['sampah_seq']}", "jenis": jenis, "x": x, "y": y,
                             "g": rng.randint(lo, hi) // 10 * 10, "zona": zona})


def sebar_sampah_awal(s, kini):
    """The yard the player wakes up in is a mess: every inside spot plus 12 spots outside."""
    rng = random.Random(f"awal:{kini:.0f}")
    for x, y in TITIK_DALAM:
        buat_sampah(s, x, y, rng, "dalam")
    for x, y in rng.sample(TITIK_LUAR, 12):
        buat_sampah(s, x, y, rng, "luar")
    s["sampah_slot"] = int(kini // SAMPAH_SLOT_DETIK)
    s["pohon_slot"] = int(kini // POHON_SLOT_DETIK)
    s["jalan_slot"] = int(kini // JALAN_SLOT_DETIK)


def tumbuh_sampah(s, kini):
    """New litter keeps appearing outside the fence (deterministic per slot, max 3 catch-up slots)."""
    slot = int(kini // SAMPAH_SLOT_DETIK)
    if not s["diterima"] or slot <= s["sampah_slot"]:
        return
    for sl in range(max(s["sampah_slot"] + 1, slot - 2), slot + 1):
        luar = [t for t in s["sampah_liar"] if t["zona"] == "luar"]
        terpakai = {(t["x"], t["y"]) for t in s["sampah_liar"]}
        bebas = [t for t in TITIK_LUAR if t not in terpakai]
        if len(luar) >= SAMPAH_MAKS_LUAR or not bebas:
            break
        rng = random.Random(f"liar:{sl}:{s['sampah_seq']}")
        x, y = rng.choice(bebas)
        buat_sampah(s, x, y, rng, "luar")
    s["sampah_slot"] = slot


def tambah_item(s, jenis, x, y, rng, kini, **extra):
    _, lo, hi = JENIS_SAMPAH[jenis]
    s["sampah_seq"] += 1
    item = {"id": f"s{s['sampah_seq']}", "jenis": jenis, "x": int(x), "y": int(y),
            "g": rng.randint(lo, hi) // 10 * 10, "zona": "luar", "t": round(kini, 1)}
    item.update(extra)
    s["sampah_liar"].append(item)


def jatuh_pohon(s, kini):
    """Dry leaves, twigs, branches and rotten fruit fall from the trees around the yard."""
    slot = int(kini // POHON_SLOT_DETIK)
    if not s["diterima"] or slot <= s["pohon_slot"]:
        return
    for sl in range(max(s["pohon_slot"] + 1, slot - 2), slot + 1):
        rng = random.Random(f"pohon:{sl}:{s['sampah_seq']}")
        if rng.random() > 0.6:
            continue
        ada = [t for t in s["sampah_liar"] if t.get("sumber") == "pohon"]
        terpakai = {(t["x"], t["y"]) for t in s["sampah_liar"]}
        bebas = [t for t in TITIK_POHON if t not in terpakai]
        if len(ada) >= POHON_MAKS or not bebas:
            break
        x, y = rng.choice(bebas)
        jenis = rng.choices(("daun", "ranting", "dahan", "buah"), weights=(5, 3, 1, 2))[0]
        tambah_item(s, jenis, x, y, rng, kini if sl == slot else sl * POHON_SLOT_DETIK, sumber="pohon")
    s["pohon_slot"] = slot


def jatuh_kendaraan(s, kini):
    """Now and then a passing vehicle drops litter on the road shoulder (free material for the player)."""
    slot = int(kini // JALAN_SLOT_DETIK)
    if not s["diterima"] or slot <= s["jalan_slot"]:
        return
    for sl in range(max(s["jalan_slot"] + 1, slot - 2), slot + 1):
        rng = random.Random(f"jalan:{sl}:{s['sampah_seq']}")
        if rng.random() > 0.45:
            continue
        if sum(1 for t in s["sampah_liar"] if t.get("sumber") == "jalan") >= JALAN_MAKS:
            break
        jenis_kend = rng.choice(list(KENDARAAN))
        lajur, isi = KENDARAAN[jenis_kend]
        arah = rng.choice(lajur)
        for _ in range(8):   # keep drops apart from existing litter
            x = rng.randrange(120, 1560, 10)
            y = road_y(x) - 48 if arah == "R" else road_y(x) + 68   # upper shoulder / lower sidewalk
            if all(abs(t["x"] - x) + abs(t["y"] - y) > 70 for t in s["sampah_liar"]):
                break
        else:
            continue
        tambah_item(s, rng.choice(isi), x, y, rng, kini if sl == slot else sl * JALAN_SLOT_DETIK,
                    sumber="jalan", kendaraan=jenis_kend, arah=arah)
    s["jalan_slot"] = slot


def petak_dari(s, payload):
    """Planting plot addressed by payload['petak']: 0 = Kebun Gaia (top-level fields), 1..3 = extra plots."""
    i = int(payload.get("petak", 0) or 0)
    if i == 0:
        return s
    perlu(1 <= i <= len(s["petak"]), "Petak tanam tidak ditemukan.")
    return s["petak"][i - 1]


def daftar_pencapaian(s):
    st = s["stat"]
    dalam_sisa = sum(1 for t in s["sampah_liar"] if t["zona"] == "dalam")
    data = [
        ("pungut", 1, "Tangan Pertama", "Pungut sampah pertamamu.", st["pungut"], 1),
        ("pilah", 2, "Pemilah Andal", "Pilah 10 kg bahan campuran di Area Pilah.", st["pilah_g"] // 1000, 10),
        ("kompos", 3, "Penyubur Tanah", "Buat kompos pertamamu.", st["kompos"], 1),
        ("panen", 4, "Panen Perdana", "Panen sayur dari kebunmu.", st["panen"], 1),
        ("saudagar", 5, "Saudagar Hijau", "Kumpulkan 2.000 Gaia Coin.", min(s["koin"], 2000), 2000),
        ("sungai", 6, "Penjaga Sungai", "Bersihkan 5 sampah di tepi sungai.", st["sungai"], 5),
        ("petani", 7, "Petani Kota", "Miliki petak tanam tambahan.", len(s["petak"]), 1),
        ("bersih", 8, "Lahan Bersih", "Bersihkan semua sampah di dalam pagar.",
         len(TITIK_DALAM) - dalam_sisa if s["diterima"] else 0, len(TITIK_DALAM)),
    ]
    return [{"id": i, "ikon": f"badges_{ik}.png", "judul": j, "desk": d, "nilai": min(n, t), "target": t, "ok": n >= t}
            for i, ik, j, d, n, t in data]


def state_awal():
    nodes = {}
    for kode, tpl in NODE_TEMPLATE.items():
        nodes[kode] = {
            "stok": bagi_g(60_000 if kode != "sungai" else 25_000, tpl["komposisi"]),
            "kapasitas_g": tpl["kapasitas_g"],
        }
    return {
        "versi": 2,
        "diterima": False,
        "nama": "Penjaga Bumi",
        "gender": "pria",
        "avatar": {"rambut": "pendek", "baju": "hijau", "topi": "rimba", "aksesori": "tanpa"},
        "kota": "Bandung",
        "koin": 1000,  # Evaluasi 1: modal awal kecil, koin didapat dari memungut & mengolah sampah
        "poin": 0,
        "karma": 0.0,
        "tier": "Awaken",
        "gudang_kap_g": 500_000,  # 500 kg starter
        # Inventaris bahan mentah (gram)
        "campuran_g": 0,
        "organik_g": 0,
        "plastik_g": 0,
        "kertas_g": 0,
        "logam_kaca_g": 0,
        "residu_g": 0,
        "b3_g": 0,
        # Produk olahan (gram) & neraca terkendali
        "kompos_g": 0,
        "pelet_g": 0,
        "pot_g": 0,
        "uap_terkendali_g": 0,
        "b3_serah_g": 0,
        "backlog_tpa_g": 0,
        "total_masuk_g": 0,
        # DWE nodes & WCS active job
        "nodes": nodes,
        "job": None,  # {node, muat_g, fraksi, status: in_transit|arrived, tiba_pada}
        # DLE state (v0.8 §28)
        "dle_events": [],
        "dle_cursor_slot": 0,
        "dle_utc_day": "",
        "dle_daily_count": 0,
        "dle_daily_bonus_g": 0,
        "dle_tutorial_done": False,
        # Kebun Gaia (D14)
        "benih": 3,
        "stok_langka": 0,
        "ditanam": False,
        "tanaman": "",
        "detik": 0.0,
        "dipupuk": False,
        "panen": 0,
        "panen_langka": 0,
        "misi": False,
        "varietas": "",
        "pernah_jual": False,
        "waktu": 0.0,
        # Evaluasi 1
        "intro_selesai": False,
        "sampah_liar": [],
        "sampah_seq": 0,
        "sampah_slot": 0,
        "petak": [],          # extra planting plots: {ditanam, tanaman, detik, dipupuk}
        "gudang_upgrade": 0,
        "stat": stat_awal(),
        "pohon_slot": 0,
        "jalan_slot": 0,
    }


def migrasi_state(raw):
    """Gabungkan state lama v0.6 agar tetap kompatibel tanpa crash."""
    base = state_awal()
    if not isinstance(raw, dict):
        return base
    if raw.get("versi") == 2:
        sebelum_evaluasi1 = "intro_selesai" not in raw
        for k, v in base.items():
            raw.setdefault(k, v)
        for k, v in stat_awal().items():
            raw["stat"].setdefault(k, v)
        if sebelum_evaluasi1 and raw["diterima"]:
            raw["intro_selesai"] = True       # players who were already playing skip the new intro
        return raw
    # Migrasi dari state v0.6 lama (kg -> gram)
    base["diterima"] = bool(raw.get("diterima", False))
    base["kota"] = raw.get("kota") or "Bandung"
    base["koin"] = int(raw.get("koin", 10000))
    base["campuran_g"] = int(raw.get("campuran", 0)) * 1000
    base["organik_g"] = int(raw.get("organik", 0)) * 1000
    base["plastik_g"] = int(raw.get("botol", 0)) * 1000
    base["residu_g"] = int(raw.get("residu", 0)) * 1000
    base["kompos_g"] = int(raw.get("kompos", 0)) * 1000
    base["uap_terkendali_g"] = int(raw.get("uap", 0)) * 1000
    base["pelet_g"] = int(raw.get("pelet", 0)) * 1000
    base["pot_g"] = int(raw.get("pot", 0)) * 1000
    base["benih"] = int(raw.get("benih", 3))
    base["stok_langka"] = int(raw.get("stok_langka", 0))
    base["panen"] = int(raw.get("panen", 0))
    base["panen_langka"] = int(raw.get("panen_langka", 0))
    base["ditanam"] = bool(raw.get("ditanam", False))
    base["tanaman"] = raw.get("tanaman", "")
    base["detik"] = float(raw.get("detik", 0))
    base["dipupuk"] = bool(raw.get("dipupuk", False))
    base["misi"] = bool(raw.get("misi", False))
    base["varietas"] = raw.get("varietas", "")
    base["waktu"] = float(raw.get("waktu", 0))
    return base


def perlu(syarat, pesan):
    if not syarat:
        raise ValueError(pesan)


def hitung_tier(poin):
    nama = TIERS[0][1]
    for batas, label in TIERS:
        if poin >= batas:
            nama = label
    return nama


def gudang_terpakai_g(s):
    return (
        s["campuran_g"]
        + s["organik_g"]
        + s["plastik_g"]
        + s["kertas_g"]
        + s["logam_kaca_g"]
        + s["residu_g"]
        + s["b3_g"]
        + s["kompos_g"]
        + s["pelet_g"]
        + s["pot_g"]
    )


def ambil_dari_node_g(node_stok, target_g, prioritas):
    diambil = {f: 0 for f in FRAKSI}
    sisa = int(target_g)
    for f in prioritas:
        if f == "B3" or sisa <= 0:
            continue
        ada = node_stok[f]
        pot = min(ada, sisa)
        node_stok[f] -= pot
        diambil[f] += pot
        sisa -= pot
    return diambil, sum(diambil.values())


def settle_waktu(s, kini):
    """Lazy Tick: pertumbuhan kebun, timbulan DWE, tiba kargo WCS, dan slot DLE."""
    if s["waktu"] <= 0:
        s["waktu"] = kini
    selang_raw = max(0.0, kini - s["waktu"])
    selang_cap = min(28800.0, selang_raw)  # cap 8 jam untuk proses pribadi

    # 1. Kebun Gaia + petak tambahan (Lazy Tick pribadi)
    for pt in [s] + s["petak"]:
        if pt["ditanam"] and pt["detik"] > 0:
            pt["detik"] = max(0.0, pt["detik"] - selang_cap)
    tumbuh_sampah(s, kini)
    jatuh_pohon(s, kini)
    jatuh_kendaraan(s, kini)

    # 2. WCS job arrival
    if s["job"] and s["job"]["status"] == "in_transit" and kini >= s["job"]["tiba_pada"]:
        s["job"]["status"] = "arrived"

    # 3. DWE timbulan eksternal (maks 60 menit catch-up pada review lokal)
    menit = int(min(selang_raw, 3600.0) // 60)
    if menit > 0:
        for kode, tpl in NODE_TEMPLATE.items():
            tambah_g = tpl["laju_per_menit_g"] * menit
            bagian = bagi_g(tambah_g, tpl["komposisi"])
            ns = s["nodes"][kode]["stok"]
            for f in FRAKSI:
                ns[f] += bagian[f]
            tot = sum(ns.values())
            kap = s["nodes"][kode]["kapasitas_g"]
            if tot > kap:
                lebih = tot - kap
                for f in FRAKSI:
                    if lebih <= 0:
                        break
                    pot = min(ns[f], lebih)
                    ns[f] -= pot
                    s["backlog_tpa_g"] += pot
                    lebih -= pot

    # 4. DLE expiry & evaluasi slot UTC deterministik (§28.3-28.4)
    utc_day = datetime.fromtimestamp(kini, tz=timezone.utc).strftime("%Y-%m-%d")
    if s["dle_utc_day"] != utc_day:
        s["dle_utc_day"] = utc_day
        s["dle_daily_count"] = 0
        s["dle_daily_bonus_g"] = 0

    masih = []
    for ev in s["dle_events"]:
        if ev["status"] == "available" and kini >= ev["expires_at"]:
            # Expiry memindahkan massa ke backlog TPA, tidak menghapus gram
            s["backlog_tpa_g"] += ev["mass_g"]
            ev["status"] = "expired"
        if ev["status"] == "available":
            masih.append(ev)
    s["dle_events"] = masih

    slot_kini = int(kini // 180)  # slot 3 menit UTC
    if s["diterima"] and slot_kini > s["dle_cursor_slot"]:
        # Catch-up terbatas: evaluasi maksimal 3 slot terbaru (tanpa tumpukan offline)
        mulai = max(s["dle_cursor_slot"] + 1, slot_kini - 2)
        for sl in range(mulai, slot_kini + 1):
            if s["dle_daily_count"] >= 6 or len(s["dle_events"]) >= 3:
                break
            sisa_cap = 12_000 - s["dle_daily_bonus_g"]
            if sisa_cap < 200:
                break
            seed = int.from_bytes(hashlib.sha256(f"local:{sl}:v0.8".encode()).digest()[:8], "big")
            rng = random.Random(seed)
            if rng.random() < 0.20:
                if rng.random() < 0.5:
                    target = min(rng.randint(200, 1000), sisa_cap)
                    fr, got = ambil_dari_node_g(s["nodes"]["permukiman"]["stok"], target, ("plastik", "logam_kaca"))
                    if got > 0:
                        s["dle_events"].append({
                            "id": f"dle-{sl}-riv",
                            "jenis": "npc_litter_river",
                            "judul": "Kemasan di Tepi Sungai",
                            "pesan": "Seorang pejalan kaki membuang botol di tepi sungai. Bersihkan agar tidak hanyut!",
                            "anchor": "river_bank",
                            "source_node": "permukiman",
                            "fraksi": fr,
                            "mass_g": got,
                            "status": "available",
                            "expires_at": kini + 900,
                        })
                        s["dle_daily_count"] += 1
                else:
                    target = min(rng.randint(1000, 3000), sisa_cap)
                    fr, got = ambil_dari_node_g(s["nodes"]["pasar"]["stok"], target, ("organik",))
                    if got > 0:
                        s["dle_events"].append({
                            "id": f"dle-{sl}-veg",
                            "jenis": "vegetable_spill",
                            "judul": "Sayuran Tercecer di Bahu Jalan",
                            "pesan": "Mobil pengangkut sayur menjatuhkan muatan di depan gerbangmu. Manfaatkan organiknya!",
                            "anchor": "road_shoulder",
                            "source_node": "pasar",
                            "fraksi": fr,
                            "mass_g": got,
                            "status": "available",
                            "expires_at": kini + 900,
                        })
                        s["dle_daily_count"] += 1
        s["dle_cursor_slot"] = slot_kini

    s["waktu"] = max(s["waktu"], kini)
    s["tier"] = hitung_tier(s["poin"])


def buat_insiden_tutorial(s, kini):
    """Satu insiden tutorial terjamin sekali per akun (§28.3), tetap masuk kuota."""
    if s["dle_tutorial_done"] or len(s["dle_events"]) >= 3:
        return
    fr, got = ambil_dari_node_g(s["nodes"]["pasar"]["stok"], 2000, ("organik",))
    if got > 0:
        s["dle_events"].append({
            "id": "dle-tutorial-veg",
            "jenis": "vegetable_spill",
            "judul": "Sayuran Tercecer di Depan Gerbang",
            "pesan": "Ada sayuran tercecer di depan gerbangmu. Bersihkan jalan dan manfaatkan bahan organiknya.",
            "anchor": "road_shoulder",
            "source_node": "pasar",
            "fraksi": fr,
            "mass_g": got,
            "status": "available",
            "expires_at": kini + 900,
        })
        s["dle_daily_count"] += 1
        s["dle_tutorial_done"] = True


def aksi(s, payload, kini):
    nama = payload.get("aksi", "")
    if nama == "reset_sim":
        baru = state_awal()
        baru["waktu"] = kini
        s.clear()
        s.update(baru)
        return "Simulasi lokal direset ke awal untuk review."

    if nama == "terima":
        kota = payload.get("kota", "Bandung")
        perlu(not s["diterima"] and kota in KOTA_SAH, "Pilih kota awal yang valid.")
        nama_pl = str(payload.get("nama", "Penjaga Bumi")).strip()[:24] or "Penjaga Bumi"
        gender = payload.get("gender", "pria")
        perlu(gender in ("pria", "wanita"), "Pilihan karakter harus pria atau wanita.")
        av_in = payload.get("avatar") or {}
        av = {}
        for slot, daftar in AVATAR_ALLOW.items():
            val = av_in.get(slot, daftar[0])
            perlu(val in daftar, f"Pilihan kosmetik {slot} tidak valid.")
            av[slot] = val
        s.update(diterima=True, kota=kota, nama=nama_pl, gender=gender, avatar=av, dle_cursor_slot=int(kini // 180))
        sebar_sampah_awal(s, kini)
        buat_insiden_tutorial(s, kini)
        return f"Selamat datang, {nama_pl}. Dari lahan kecil di {kota} inilah perjalananmu dimulai."

    perlu(s["diterima"], "Terima panggilan Gaia dahulu.")

    if nama == "ganti_karakter":
        gender = payload.get("gender", "")
        perlu(gender in ("pria", "wanita"), "Pilihan karakter harus pria atau wanita.")
        s["gender"] = gender
        return "Karakter diganti menjadi " + ("Penjaga Bumi wanita." if gender == "wanita" else "Penjaga Bumi pria.")

    if nama == "intro_selesai":
        s["intro_selesai"] = True
        return "Selamat bekerja, Penjaga Bumi. Bersihkan lahanmu!"

    # Memungut sampah liar di dalam / luar pagar
    if nama == "pungut":
        sid = str(payload.get("id", ""))
        item = next((t for t in s["sampah_liar"] if t["id"] == sid), None)
        perlu(item is not None, "Sampah itu sudah dipungut.")
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= item["g"], "Gudang penuh — olah atau jual isi gudang terlebih dahulu.")
        kunci = JENIS_SAMPAH[item["jenis"]][0]
        s[kunci] += item["g"]
        s["total_masuk_g"] += item["g"]
        s["sampah_liar"].remove(item)
        s["koin"] += 2
        s["poin"] += 3
        s["stat"]["pungut"] += 1
        if item["zona"] == "dalam":
            s["stat"]["pungut_dalam"] += 1
        if (item["x"], item["y"]) in TITIK_SUNGAI:
            s["stat"]["sungai"] += 1
        s["tier"] = hitung_tier(s["poin"])
        tujuan = "Area Pilah (perlu dipilah)" if kunci == "campuran_g" else "gudang"
        return f"{LABEL_SAMPAH[item['jenis']]} {item['g']} g dipungut → {tujuan} (+2 koin, +3 poin)."

    # Pengembangan lahan
    if nama == "beli_petak":
        n = len(s["petak"])
        perlu(n < len(HARGA_PETAK), "Semua petak tanam tambahan sudah dimiliki.")
        harga = HARGA_PETAK[n]
        perlu(s["koin"] >= harga, f"Petak tanam baru seharga {harga} Gaia Coin. Kumpulkan koin dari sampah yang kamu olah.")
        s["koin"] -= harga
        s["petak"].append({"ditanam": False, "tanaman": "", "detik": 0.0, "dipupuk": False})
        return f"Petak tanam ke-{n + 2} dibangun di sisi kanan lahan (-{harga} Gaia Coin)."

    if nama == "tambah_gudang":
        n = s["gudang_upgrade"]
        perlu(n < len(HARGA_GUDANG), "Gudang sudah diperluas maksimal.")
        harga = HARGA_GUDANG[n]
        perlu(s["koin"] >= harga, f"Perluasan gudang seharga {harga} Gaia Coin.")
        s["koin"] -= harga
        s["gudang_upgrade"] += 1
        s["gudang_kap_g"] += 250_000
        return f"Gudang diperluas +250 kg (-{harga} Gaia Coin)."

    # DWE / WCS: kirim gerobak ke node (Permukiman / Pasar / Sungai)
    if nama in ("angkut_node", "angkut"):
        perlu(s["job"] is None, "Gerobak sedang beroperasi. Terima kargo terlebih dahulu.")
        node_id = payload.get("node", "pasar")
        perlu(node_id in NODE_TEMPLATE, "Sumber sampah tidak dikenal.")
        tpl = NODE_TEMPLATE[node_id]
        muat_g = int(payload.get("gram", 10_000))
        perlu(5_000 <= muat_g <= 50_000, "Kapasitas gerobak 5–50 kg per perjalanan.")
        biaya = tpl["tarif"]
        perlu(s["koin"] >= biaya, f"Biaya angkut {biaya} Gaia Coin tidak mencukupi.")
        ns = s["nodes"][node_id]["stok"]
        tot_node = sum(ns.values())
        perlu(tot_node >= muat_g, f"Stok {tpl['nama']} belum mencukupi ({tot_node // 1000} kg tersedia).")
        s["koin"] -= biaya
        diambil = {f: 0 for f in FRAKSI}
        sisa = muat_g
        for f in FRAKSI:
            porsi = (ns[f] * muat_g) // tot_node
            pot = min(ns[f], porsi, sisa)
            ns[f] -= pot
            diambil[f] += pot
            sisa -= pot
        for f in FRAKSI:
            if sisa <= 0:
                break
            pot = min(ns[f], sisa)
            ns[f] -= pot
            diambil[f] += pot
            sisa -= pot
        # Waktu perjalanan dipercepat 6 detik untuk review lokal
        s["job"] = {
            "node": node_id,
            "nama_node": tpl["nama"],
            "muat_g": muat_g,
            "fraksi": diambil,
            "status": "in_transit",
            "tiba_pada": kini + 6,
        }
        return f"Gerobak menuju {tpl['nama']} mengangkut {muat_g // 1000} kg (-{biaya} koin). Tiba dalam 6 detik uji."

    if nama == "terima_kargo":
        perlu(s["job"] is not None, "Tidak ada kargo aktif.")
        perlu(s["job"]["status"] == "arrived", "Gerobak masih dalam perjalanan.")
        muat_g = s["job"]["muat_g"]
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= muat_g, "Gudang penuh — kosongkan ruang terlebih dahulu.")
        # Simpan sebagai bahan campuran belum terpilah (atau simpan asal fraksi di campuran)
        s["campuran_g"] += muat_g
        s["total_masuk_g"] += muat_g
        asal = s["job"]["nama_node"]
        s["job"] = None
        return f"Kargo {muat_g // 1000} kg dari {asal} masuk ke area pilah."

    # DLE: klaim insiden jalan/sungai secara atomik (§28.4)
    if nama == "ambil_dle":
        ev_id = payload.get("event_id", "")
        ev = next((e for e in s["dle_events"] if e["id"] == ev_id and e["status"] == "available"), None)
        perlu(ev is not None, "Insiden sudah dibersihkan atau kedaluwarsa.")
        perlu(kini < ev["expires_at"], "Insiden sudah kedaluwarsa dan berpindah ke backlog lingkungan.")
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= ev["mass_g"], "Gudang penuh — kosongkan ruang terlebih dahulu.")
        perlu(s["dle_daily_bonus_g"] + ev["mass_g"] <= 12_000, "Batas bonus material DLE harian (12 kg) tercapai.")
        ev["status"] = "collected"
        s["dle_events"] = [e for e in s["dle_events"] if e["status"] == "available"]
        # Material masuk inventaris belum dipilah/mentah (tidak langsung jadi kompos!)
        for f, g_val in ev["fraksi"].items():
            if f == "organik":
                s["organik_g"] += g_val
            elif f == "plastik":
                s["plastik_g"] += g_val
            elif f == "logam_kaca":
                s["logam_kaca_g"] += g_val
            else:
                s["campuran_g"] += g_val
        s["total_masuk_g"] += ev["mass_g"]
        s["dle_daily_bonus_g"] += ev["mass_g"]
        if ev["anchor"] == "river_bank":
            s["stat"]["sungai"] += 1
        s["poin"] += 15  # poin misi pembersihan kecil, terpisah dari kredit olah
        s["tier"] = hitung_tier(s["poin"])
        return f"+{ev['mass_g']} g material dari {ev['judul']} masuk area pilah (+15 Poin Misi)."

    # Pemilahan 6 fraksi (10 kg atau semua campuran >= 1 kg)
    if nama == "pilah":
        perlu(s["campuran_g"] >= 1000, "Belum ada bahan campuran di area pilah (minimal 1 kg).")
        batch_g = min(10_000, s["campuran_g"])
        s["campuran_g"] -= batch_g
        s["stat"]["pilah_g"] += batch_g
        bagian = bagi_g(batch_g, {"organik": 50, "plastik": 18, "kertas": 10, "logam_kaca": 7, "residu": 14, "B3": 1})
        s["organik_g"] += bagian["organik"]
        s["plastik_g"] += bagian["plastik"]
        s["kertas_g"] += bagian["kertas"]
        s["logam_kaca_g"] += bagian["logam_kaca"]
        s["residu_g"] += bagian["residu"]
        s["b3_g"] += bagian["B3"]
        return (
            f"Dipilah {batch_g} g → {bagian['organik']} g organik, {bagian['plastik']} g plastik, "
            f"{bagian['kertas']} g kertas, {bagian['logam_kaca']} g logam/kaca, {bagian['residu']} g residu, {bagian['B3']} g B3."
        )

    # Olah kompos (konservatif gram: 2 kg organik -> 900 g kompos + 1000 g uap/air + 100 g residu)
    if nama in ("olah", "olah_kompos"):
        perlu(s["organik_g"] >= 2000, "Perlu minimal 2 kg bahan organik.")
        s["organik_g"] -= 2000
        s["kompos_g"] += 1000
        s["stat"]["kompos"] += 1
        s["uap_terkendali_g"] += 900
        s["residu_g"] += 100
        s["poin"] += 40
        s["karma"] = max(0.0, round(s["karma"] - 0.1, 2))
        s["tier"] = hitung_tier(s["poin"])
        return "2.000 g organik → 1.000 g kompos, 900 g aliran air/gas terkendali, 100 g residu (+40 Poin)."

    # Olah plastik -> pelet / pot (1 kg -> 850 g produk + 100 g terkendali + 50 g residu)
    if nama in ("daur", "kreasi"):
        perlu(s["plastik_g"] >= 1000, "Perlu minimal 1 kg plastik terpilah.")
        s["plastik_g"] -= 1000
        target = "pot_g" if nama == "kreasi" else "pelet_g"
        s[target] += 850
        s["uap_terkendali_g"] += 100
        s["residu_g"] += 50
        s["poin"] += 60
        s["karma"] = max(0.0, round(s["karma"] - 0.1, 2))
        s["tier"] = hitung_tier(s["poin"])
        label = "pot daur ulang" if nama == "kreasi" else "pelet plastik"
        return f"1.000 g plastik → 850 g {label}, 100 g aliran terkendali, 50 g residu (+60 Poin)."

    # Penyerahan B3 khusus (D03)
    if nama == "serah_b3":
        perlu(s["b3_g"] >= 100, "Belum ada fraksi B3 untuk diserahkan.")
        jml = s["b3_g"]
        s["b3_g"] = 0
        s["b3_serah_g"] += jml
        s["poin"] += max(10, (jml * 8) // 100)
        s["tier"] = hitung_tier(s["poin"])
        return f"{jml} g B3 diserahkan ke pengolah berizin (aman, tidak masuk pengolahan umum)."

    # Kebun Gaia (D14)
    if nama in ("tanam", "tanam_langka"):
        langka = nama == "tanam_langka"
        stok = "stok_langka" if langka else "benih"
        pt = petak_dari(s, payload)
        perlu(not pt["ditanam"] and s[stok] > 0, "Perlu petak kosong dan benih.")
        s[stok] -= 1
        pt.update(ditanam=True, tanaman=s["varietas"] if langka else "Kangkung Gaia", detik=40.0, dipupuk=False)
        return "Benih ditanam. Matang dalam 40 detik uji (4 jam simulasi)."

    if nama == "pupuk":
        pt = petak_dari(s, payload)
        perlu(pt["ditanam"] and pt["detik"] > 0 and not pt["dipupuk"] and s["kompos_g"] >= 1000,
              "Perlu tanaman tumbuh dan 1 kg kompos (satu dosis per siklus).")
        s["kompos_g"] -= 1000
        pt["detik"] = round(pt["detik"] * 0.75, 2)
        pt["dipupuk"] = True
        return "1 kg kompos dipakai di Kebun Gaia (sisa waktu dipangkas 25%; tanpa kredit lingkungan ganda)."

    if nama == "panen":
        pt = petak_dari(s, payload)
        perlu(pt["ditanam"] and pt["detik"] <= 0, "Tanaman belum siap dipanen.")
        langka = pt["tanaman"] in LANGKA
        s["panen_langka" if langka else "panen"] += 1
        s["stat"]["panen"] += 1
        extra = ""
        if pt["dipupuk"] and not s["misi"]:
            s["misi"] = True
            s["varietas"] = random.choice(LANGKA)
            s["stok_langka"] += 1
            extra = f" Misi Siklus Pertama Gaia selesai! Varietas langka terbuka: {s['varietas']}."
        pt.update(ditanam=False, tanaman="", detik=0.0, dipupuk=False)
        return "Panen 1 ikat sayur masuk gudang." + extra

    if nama in ("beli", "beli_langka"):
        if nama == "beli_langka":
            perlu(s["misi"], "Buka varietas langka dahulu melalui misi Siklus Pertama Gaia.")
        perlu(s["koin"] >= 2, "Harga benih 2 Gaia Coin.")
        s["koin"] -= 2
        s["stok_langka" if nama == "beli_langka" else "benih"] += 1
        return "Membeli 1 benih (-2 Gaia Coin)."

    # Pasar Kota
    if nama.startswith("jual_"):
        barang = nama.removeprefix("jual_")
        if barang in ("panen", "panen_langka"):
            perlu(s[barang] >= 1, "Stok sayur belum tersedia.")
            s[barang] -= 1
            s["koin"] += 24
            s["stat"]["koin_jual"] += 24
            s["pernah_jual"] = True
            return "Penjualan 1 ikat sayur berhasil (+24 Gaia Coin)."
        gram_map = {
            "kompos": ("kompos_g", 1000, 5),
            "pelet": ("pelet_g", 850, 12),
            "pot": ("pot_g", 850, 14),
            "kertas": ("kertas_g", 1000, 9),
            "logam": ("logam_kaca_g", 1000, 12),
        }
        perlu(barang in gram_map, "Produk pasar tidak dikenal.")
        kunci, min_g, harga = gram_map[barang]
        perlu(s[kunci] >= min_g, f"Perlu minimal {min_g} g untuk menjual {barang}.")
        s[kunci] -= min_g
        s["koin"] += harga
        s["stat"]["koin_jual"] += harga
        s["pernah_jual"] = True
        return f"Penjualan {min_g} g {barang} berhasil (+{harga} Gaia Coin)."

    raise ValueError("Aksi tidak dikenal.")


def ringkasan_ekstra(s, kini):
    """Tambahkan informasi turunan untuk UI (kapasitas, BHI terhitung, node info)."""
    terpakai = gudang_terpakai_g(s)
    # BHI dihitung dari rasio residu+backlog terhadap total massa (bukan 42% hardcoded!)
    total_basis = max(100_000, s["total_masuk_g"] + s["backlog_tpa_g"])
    rasio_limbah = min(1.0, (s["residu_g"] + s["backlog_tpa_g"]) / total_basis)
    bhi = max(10, min(100, int(round(100 - 55 * rasio_limbah))))
    nodes_info = {}
    for kode, tpl in NODE_TEMPLATE.items():
        ns = s["nodes"][kode]["stok"]
        nodes_info[kode] = {
            "nama": tpl["nama"],
            "tersedia_g": sum(ns.values()),
            "kapasitas_g": tpl["kapasitas_g"],
            "jarak_km": tpl["jarak_km"],
            "tarif": tpl["tarif"],
            "stok": ns,
        }
    return {
        "gudang_terpakai_g": terpakai,
        "gudang_bebas_g": max(0, s["gudang_kap_g"] - terpakai),
        "bhi": bhi,
        "bhi_label": "Snapshot lokal (simulasi)",
        "server_time": kini,
        "nodes_info": nodes_info,
        "pencapaian": daftar_pencapaian(s),
        "harga_petak": HARGA_PETAK[len(s["petak"])] if len(s["petak"]) < len(HARGA_PETAK) else None,
        "harga_gudang": HARGA_GUDANG[s["gudang_upgrade"]] if s["gudang_upgrade"] < len(HARGA_GUDANG) else None,
        "label_sampah": LABEL_SAMPAH,
    }


# ---------------------------------------------------------------- akun & sesi
# Accounts for the web build: username + email + password (PBKDF2-SHA256, per-account salt).
# Session tokens are random; only their SHA-256 is stored. Each account has its own game state.
PBKDF2_ITER = 240_000
SESI_DETIK = 30 * 24 * 3600
COOKIE = "tn_sesi"
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]{3,24}$")
EMAIL_RE = re.compile(r"^[^@\s]{1,64}@[^@\s]+\.[^@\s]{2,}$")
GAGAL_LOGIN = {}          # ip -> [timestamps of failed logins]
GAGAL_LOCK = threading.Lock()


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
        row = db.execute("SELECT a.id, a.username FROM sesi s JOIN akun a ON a.id = s.akun_id "
                         "WHERE s.token = ? AND s.kedaluwarsa > ?", (hash_token(token), time.time())).fetchone()
    return {"id": row[0], "username": row[1]} if row else None


def sudah_diterima(akun_id):
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        row = db.execute("SELECT data FROM pemain_akun WHERE akun_id=?", (akun_id,)).fetchone()
    return bool(row and json.loads(row[0]).get("diterima"))


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
            cur = db.execute("INSERT INTO akun(username,email,salt,hash,dibuat) VALUES(?,?,?,?,?)",
                             (username, email, salt, h, time.time()))
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
        row = db.execute("SELECT id, username, salt, hash FROM akun WHERE username = ? OR email = ?",
                         (login, login.lower())).fetchone()
        if not row or not cek_sandi(sandi, row[2], row[3]):
            with GAGAL_LOCK:
                GAGAL_LOGIN.setdefault(ip, []).append(kini)
            raise ValueError("Nama pengguna/email atau kata sandi salah.")
        return {"id": row[0], "username": row[1]}, buat_sesi(db, row[0])


def transaksi(akun_id, payload=None, key=None):
    db = sqlite3.connect(DB_PATH, timeout=10)
    try:
        with db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT data FROM pemain_akun WHERE akun_id=?", (akun_id,)).fetchone()
            s = migrasi_state(json.loads(row[0])) if row else state_awal()
            kini = time.time()
            settle_waktu(s, kini)
            pesan = ""
            if payload:
                kanonik = json.dumps(payload, sort_keys=True)
                rkey = f"{akun_id}:{key}"  # receipts are scoped to the account
                lama = db.execute("SELECT aksi,kota,pesan FROM receipt WHERE id=?", (rkey,)).fetchone()
                if lama:
                    perlu(lama[0] == payload.get("aksi") and lama[1] == kanonik, "Kunci aksi berbeda isi.")
                    pesan = lama[2]
                else:
                    pesan = aksi(s, payload, kini)
                    db.execute("INSERT INTO receipt VALUES(?,?,?,?)", (rkey, payload.get("aksi", ""), kanonik, pesan))
            db.execute("INSERT OR REPLACE INTO pemain_akun VALUES(?,?)", (akun_id, json.dumps(s)))
            return {"state": s, "meta": ringkasan_ekstra(s, kini), "pesan": pesan}
    finally:
        db.close()


INTRO_MIME = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
              ".css": "text/css; charset=utf-8", ".json": "application/json", ".webp": "image/webp",
              ".m4a": "audio/mp4", ".vtt": "text/vtt; charset=utf-8", ".md": "text/markdown; charset=utf-8"}


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

    def kirim_json(self, obj, kode=200, header=None):
        self.kirim(json.dumps(obj).encode(), "application/json", kode, header=header)

    # ---- session cookie
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
        # Secure is added when served over HTTPS behind a proxy (e.g. teranova.id); plain http stays usable locally
        aman = "; Secure" if self.headers.get("X-Forwarded-Proto", "").lower() == "https" else ""
        return {"Set-Cookie": f"{COOKIE}={token}; Max-Age={umur}; Path=/; HttpOnly; SameSite=Lax{aman}"}

    def ip(self):
        return (self.headers.get("X-Forwarded-For", "").split(",")[0].strip() or self.client_address[0])

    def do_GET(self):
        jalan = self.path.split("?")[0]
        if jalan == "/":
            # signed in and already accepted Gaia's call -> the game; otherwise the landing page
            # (the landing page itself plays the cinematic for a signed-in player who has not accepted yet)
            akun = self.akun()
            halaman = "web/index.html" if akun and sudah_diterima(akun["id"]) else "web/landing.html"
            self.kirim((ROOT / halaman).read_bytes(), "text/html; charset=utf-8")
        elif jalan == "/akun":
            akun = self.akun()
            self.kirim_json({"masuk": bool(akun), "username": akun["username"] if akun else None,
                             "diterima": sudah_diterima(akun["id"]) if akun else False})
        elif jalan == "/state":
            akun = self.akun()
            if not akun:
                return self.kirim_json({"pesan": "Silakan masuk terlebih dahulu."}, 401)
            hasil = transaksi(akun["id"])
            hasil["akun"] = {"username": akun["username"]}
            self.kirim_json(hasil)
        elif jalan.startswith("/assets/") and ".." not in jalan:
            f = (ROOT / "web" / jalan[1:]).resolve()
            tipe = {".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".wav": "audio/wav",
                    ".txt": "text/plain"}.get(f.suffix)
            if tipe and f.is_file() and (ROOT / "web" / "assets") in f.parents:
                self.kirim(f.read_bytes(), tipe, cache="no-cache")
            else:
                self.send_error(404)
        elif jalan == "/intro":
            self.send_response(301)
            self.send_header("Location", "/intro/" + (("?" + self.path.split("?", 1)[1]) if "?" in self.path else ""))
            self.end_headers()
        elif jalan.startswith("/intro/") and ".." not in jalan:
            # opening cinematic (cinematic-web/runtime), played right after sign-up
            base = (ROOT / "cinematic-web" / "runtime").resolve()
            rel = jalan[len("/intro/"):] or "index.html"
            f = (base / rel).resolve()
            tipe = INTRO_MIME.get(f.suffix)
            if tipe and f.is_file() and base in f.parents:
                self.kirim(f.read_bytes(), tipe, cache="no-cache")
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        try:
            perlu("application/json" in self.headers.get("Content-Type", ""), "Permintaan tidak valid.")
            n = int(self.headers.get("Content-Length", "0"))
            perlu(0 <= n <= 4096, "Ukuran tidak valid.")
            data = json.loads(self.rfile.read(n) or b"{}")
            perlu(isinstance(data, dict), "Permintaan tidak valid.")
            if self.path == "/daftar":
                akun, token = daftar_akun(data)
                return self.kirim_json({"ok": True, "username": akun["username"], "diterima": False},
                                       header=self.cookie(token))
            if self.path == "/masuk":
                akun, token = masuk_akun(data, self.ip())
                return self.kirim_json({"ok": True, "username": akun["username"],
                                        "diterima": sudah_diterima(akun["id"])}, header=self.cookie(token))
            if self.path == "/keluar":
                tok = self.token()
                if tok:
                    with sqlite3.connect(DB_PATH, timeout=10) as db:
                        db.execute("DELETE FROM sesi WHERE token = ?", (hash_token(tok),))
                return self.kirim_json({"ok": True}, header=self.cookie("", 0))
            perlu(self.path == "/aksi", "Permintaan tidak valid.")
            akun = self.akun()
            if not akun:
                return self.kirim_json({"pesan": "Sesi berakhir. Silakan masuk kembali."}, 401)
            key = str(uuid.UUID(data["key"]))
            payload = {k: v for k, v in data.items() if k != "key"}
            hasil = transaksi(akun["id"], payload, key)
            self.kirim_json(hasil)
        except (ValueError, TypeError, KeyError) as e:
            self.kirim_json({"pesan": str(e)}, 400)


def siapkan_db():
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(
            "CREATE TABLE IF NOT EXISTS pemain(id INTEGER PRIMARY KEY,data TEXT);"  # legacy single-player row
            "CREATE TABLE IF NOT EXISTS receipt(id TEXT PRIMARY KEY,aksi TEXT,kota TEXT,pesan TEXT);"
            "CREATE TABLE IF NOT EXISTS akun(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " username TEXT NOT NULL UNIQUE COLLATE NOCASE, email TEXT NOT NULL UNIQUE COLLATE NOCASE,"
            " salt TEXT NOT NULL, hash TEXT NOT NULL, dibuat REAL NOT NULL);"
            "CREATE TABLE IF NOT EXISTS sesi(token TEXT PRIMARY KEY, akun_id INTEGER NOT NULL"
            " REFERENCES akun(id), kedaluwarsa REAL NOT NULL);"
            "CREATE TABLE IF NOT EXISTS pemain_akun(akun_id INTEGER PRIMARY KEY REFERENCES akun(id), data TEXT);"
        )


if __name__ == "__main__":
    siapkan_db()
    print("Buka http://127.0.0.1:8765", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8765), Layanan).serve_forever()
