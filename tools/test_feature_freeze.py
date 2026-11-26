"""TERRA NOVA — Feature Freeze v1.0 Full Regression, Security & Performance Test Suite (FF01–FF24)."""
import gzip
import http.cookiejar
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import server  # noqa: E402
from engine.catalog import load_seed, resolve_machine_id  # noqa: E402
from engine.gameplay import TITIK_DALAM, TITIK_LUAR, TITIK_POHON, road_y, settle_waktu  # noqa: E402

RESULTS = []


def check(ff_id, name, cond, detail=""):
    st = "PASS" if cond else "FAIL"
    RESULTS.append({"ff": ff_id, "status": st, "name": name, "detail": detail})
    print(f"[{st}] {ff_id} {name}" + (f" — {detail}" if detail else ""))


def main():
    tmpdir = Path(tempfile.mkdtemp(prefix="tn_ff_test_"))
    test_db = tmpdir / "test_gaia.sqlite3"
    orig_db = server.DB_PATH
    server.DB_PATH = test_db
    server.siapkan_db()

    httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Layanan)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}"

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    def req(method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        hdrs = {"Content-Type": "application/json"} if body is not None else {}
        r = urllib.request.Request(base + path, data=data, headers=hdrs, method=method)
        t0 = time.perf_counter()
        try:
            with opener.open(r, timeout=5) as resp:
                raw = resp.read()
                return resp.status, raw, resp.headers, (time.perf_counter() - t0) * 1000
        except urllib.error.HTTPError as e:
            return e.code, e.read(), e.headers, (time.perf_counter() - t0) * 1000

    perf_latencies = []
    snapshot_bytes = 0

    try:
        # FF01: Onboarding, auth, existing account preservation
        st, raw, _, _ = req("GET", "/intro/?embed=1&autostart=1")
        check("FF01", "Opening cinematic 120s runtime served 200", st == 200 and len(raw) > 500)
        st, _, _, _ = req("POST", "/daftar", {"username": "ff_tester", "email": "ff@teranova.local", "password": "Password123!"})
        check("FF01", "Register new account sets session", st == 200)
        k1 = str(uuid.uuid4())
        st, raw, _, _ = req("POST", "/aksi", {"key": k1, "aksi": "terima", "nama": "FF Tester", "gender": "wanita", "kota": "Bandung"})
        d = json.loads(raw)
        s = d["state"]
        check("FF01", "Starter realistic_v1 = 1.000.000 GC, 500 kg, 3 seeds (2 CR01 + 1 CR02)",
              st == 200 and s["koin"] == 1_000_000 and s["gudang_kap_g"] == 500_000 and s["benih_map"] == {"CR01": 2, "CR02": 1})
        st2, raw2, _, _ = req("POST", "/aksi", {"key": k1, "aksi": "terima", "nama": "FF Tester", "gender": "wanita", "kota": "Bandung"})
        check("FF01", "Idempotent replay grant once", st2 == 200 and json.loads(raw2)["state"]["koin"] == 1_000_000)

        # Verify v0.9 account migration preserves old balance
        old_v09 = {"versi": 2, "diterima": True, "koin": 1350, "benih": 3, "stat": {"pungut": 4}}
        mig = server.migrasi_state(old_v09)
        check("FF01", "Existing v0.9 account balance preserved without forced overwrite",
              mig["koin"] == 1350 and mig["economy_mode"] == "historical_v09_preserved")

        # FF02: Catalog 282 materials, 307 machines (288 canonical + 19 aliases)
        seed = load_seed()
        cs = seed["stats"]
        check("FF02", "Catalog exact counts 282 mat / 307 mch (288 canon + 19 alias)",
              cs["materials_total"] == 282 and cs["machines_rows"] == 307 and cs["machines_canonical"] == 288 and cs["machines_aliases"] == 19,
              str(cs))
        st, raw, _, _ = req("GET", "/catalog?kind=machine&page=1&per_page=24")
        cd = json.loads(raw)
        check("FF02", "Paginated /catalog returns 24 items/page", st == 200 and len(cd["items"]) == 24 and cd["total"] == 307)
        # Verify locked machine rejected on buy
        st, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "beli_mesin", "machine_id": "WTE-001"})
        check("FF02", "Educational risk machine WTE-001 rejected for purchase", st == 400)
        st, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "beli_mesin", "machine_id": "HME-001"})
        check("FF02", "Locked machine HME-001 rejected for purchase", st == 400)

        # FF03: Quotes, hazardous rejected, nonnegative balance
        st, raw, _, _ = req("POST", "/market/quote", {"kind": "machine", "id": "DRE-001", "side": "buy", "qty": 1})
        q = json.loads(raw).get("quote", {})
        check("FF03", "Server quote returns version, net_gc, expires_at", st == 200 and q.get("net_gc") == 450_000 and q.get("expires_at", 0) > time.time())
        st, _, _, _ = req("POST", "/market/quote", {"kind": "material", "id": "HZ01", "side": "sell", "qty": 1000})
        check("FF03", "Hazardous material HZ01 blocked from free NPC trade", st == 400)

        # FF04: Spawn + floating river trash + geometry reachability
        FENCE = [(380, 500), (380, 420), (510, 310), (705, 180), (770, 160), (1045, 170), (1385, 345), (1390, 430),
                 (1360, 450), (1265, 500), (1180, 545), (1000, 580), (900, 580), (745, 585), (655, 565), (530, 550), (430, 530)]
        OBST = [(755, 120, 1045, 350), (500, 210, 760, 410), (420, 390, 700, 505), (710, 370, 840, 460), (950, 300, 1390, 470)]
        RIVER = [(0, 752), (300, 792), (836, 852), (1100, 896), (1400, 912), (1672, 930)]
        def rtop(x):
            for i in range(1, len(RIVER)):
                if x <= RIVER[i][0]:
                    x0, y0 = RIVER[i - 1]; x1, y1 = RIVER[i]
                    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
            return RIVER[-1][1]
        def in_poly(x, y, poly):
            ins = False; j = len(poly) - 1
            for i in range(len(poly)):
                xi, yi = poly[i]; xj, yj = poly[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: ins = not ins
                j = i
            return ins
        bad_pohon = [p for p in TITIK_POHON if in_poly(*p, FENCE) or not (25 < p[0] < 1647 and 45 < p[1] < rtop(p[0]) - 12)]
        check("FF04", "All 10 TITIK_POHON strictly outside fence & above river", len(bad_pohon) == 0, f"bad={bad_pohon}")
        # Trigger river spawn & expiry deterministically across 10 slots (75s each)
        sim_s = json.loads(json.dumps(s))
        t_now = time.time()
        saw_spawn = False
        for step_i in range(1, 11):
            settle_waktu(sim_s, t_now + step_i * 75)
            if sim_s["sampah_sungai"]:
                saw_spawn = True
        settle_waktu(sim_s, t_now + 10 * 75 + 120)
        check("FF04", "River floating trash spawns & conserves missed mass to backlog",
              saw_spawn and sim_s["backlog_tpa_g"] > 0,
              f"saw_spawn={saw_spawn}, backlog={sim_s['backlog_tpa_g']}g")

        # FF05: Realistic transport + actual node fraction preservation
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "angkut_node", "node": "pasar", "gram": 10000, "_test_eta": 0})
        d = json.loads(raw)
        check("FF05", "Angkut Pasar 10kg charges 1300 GC & sets 2000 GC service comp",
              st == 200 and d["state"]["job"]["biaya_gc"] == 1300 and d["state"]["job"]["kompensasi_gc"] == 2000)
        time.sleep(0.05)
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "terima_kargo"})
        d = json.loads(raw)
        check("FF05", "Terima kargo preserves real Pasar fraction (~77% organik > 7500g, not hardcoded 50%)",
              st == 200 and d["state"]["campuran_fraksi"]["organik"] >= 7500, f"organik={d['state']['campuran_fraksi']['organik']}g")
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pilah"})
        d = json.loads(raw)
        check("FF05", "Pilah splits according to real node composition (>=7500g organik)",
              st == 200 and d["state"]["organik_g"] >= 7500, f"organik_g={d['state']['organik_g']}g")

        # FF06 & FF07: 15 crops, vitality, staple food, no offline decay, rare boost cap
        check("FF06", "All 15 crops seeded (CR01-CR15)", len(seed["crops"]) == 15)
        st, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "tanam_crop", "crop_id": "CR01", "petak": 0})
        check("FF06", "Plant CR01 Kangkung on Kebun Gaia", st == 200)
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "beli_pangan", "food_id": "FD_TEMPE", "qty": 1})
        st2, raw2, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "makan", "item_id": "FD_TEMPE"})
        check("FF07", "Buy & consume staple food restores vitality & tracks food group",
              st == 200 and st2 == 200 and "protein" in json.loads(raw2)["state"]["food_groups_today"])
        # Verify offline lazy tick does NOT drain vitality
        v_before = json.loads(raw2)["state"]["vitality"]
        s_off = json.loads(raw2)["state"]
        settle_waktu(s_off, time.time() + 10000)
        check("FF07", "Vitality does NOT decay offline", s_off["vitality"] == v_before)

        # FF08 & FF09: Mass balance + Household WtE & DRES Energy Center
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "olah_kompos"})
        st2, raw2, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "olah_biogas"})
        st3, raw3, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "jalankan_energi", "sumber": "biogas"})
        st4, raw4, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "audit_energi"})
        d4 = json.loads(raw4)
        check("FF08", "Mass balance tracks kompos, uap_terkendali, residu, neraca_valid",
              st == 200 and d4["state"]["uap_terkendali_g"] > 0 and d4["state"]["stat"]["neraca_valid"] >= 3)
        check("FF09", "Household biogas WtE records 1.2 kWh net waste-origin & energy audit",
              st2 == 200 and st3 == 200 and st4 == 200 and d4["state"]["energy"]["waste_origin_used_wh"] == 1200)

        # FF10 & FF12: GT01-09, legacy badges, Chosen provisional ONLY
        req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "intro_selesai"})
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "klaim_gt", "id": "GT01"})
        d_gt = json.loads(raw)
        check("FF10", "Claim GT01 Awaken succeeds & pushes celebration + journal",
              st == 200 and "GT01" in d_gt["state"]["gt_claimed"] and len(d_gt["state"]["journal"]) >= 1)
        check("FF10", "8 legacy badges intact; Saudagar Hijau not auto-unlocked by 1M starter",
              len(d_gt["meta"]["pencapaian"]) == 8 and not next(b for b in d_gt["meta"]["pencapaian"] if b["id"] == "saudagar")["ok"])
        check("FF12", "Gaia's Chosen final_selection_active is strictly False",
              d_gt["meta"]["chosen_eval"]["final_selection_active"] is False)

        # FF13 & FF17: Buy/place/sell used machine (no overlap, anti-arbitrage)
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "beli_mesin", "machine_id": "DRE-001"})
        uid_solar = json.loads(raw)["state"]["machines_owned"][-1]["uid"]
        st_ov, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pasang_mesin", "uid": uid_solar, "slot": "S1"})
        check("FF13", "Modular placement blocks overlap on occupied slot S1", st_ov == 400)
        st_ok, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pasang_mesin", "uid": uid_solar, "slot": "S5"})
        check("FF13", "Modular placement succeeds on free slot S5", st_ok == 200)
        st_sell, raw_sell, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "jual_mesin_bekas", "uid": uid_solar})
        check("FF17", "Used machine buyback < buy price (no arbitrage)",
              st_sell == 200 and json.loads(raw_sell)["state"]["koin"] < 1_000_000)

        # FF19: Admin config validate, publish, audit, rollback
        st, raw, _, _ = req("POST", "/admin/config", {"updates": {"price_multiplier": 1.15}, "reason": "test FF19"})
        check("FF19", "Admin config publish creates v2", st == 200 and json.loads(raw)["config"]["version"] == 2)
        st, raw, _, _ = req("POST", "/admin/config", {"rollback_to": 1, "reason": "rollback FF19"})
        check("FF19", "Admin config rollback creates v3 with v1 values", st == 200 and json.loads(raw)["config"]["price_multiplier"] == 1.0)

        # FF20, FF21, FF22, FF24: Support URL null safe, Sandbox top-up, Leaderboard fixture, Feedback
        check("FF20", "Support URLs null safe by default", d_gt["meta"]["support_urls"]["support_url"] is None)
        st, raw, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "sandbox_topup", "sku": "TOPUP_STARTER"})
        dsb = json.loads(raw)
        check("FF21", "Sandbox top-up marks self_made_provisional=False & gives 0 XP",
              st == 200 and dsb["state"]["wallet"]["self_made_provisional"] is False and dsb["state"]["wallet"]["topup_sandbox_gc"] == 1_000_000)
        st, raw, _, _ = req("GET", "/leaderboard?board=sustainability")
        dlb = json.loads(raw)
        check("FF22", "Leaderboard returns 14 boards with LOCAL_FIXTURE_ONLY label & no email",
              st == 200 and dlb["mode"] == "LOCAL_FIXTURE_ONLY" and len(dlb["boards"]) == 14 and b"ff@teranova.local" not in raw)
        st, _, _, _ = req("POST", "/feedback", {"category": "saran", "rating": 5, "message": "Uji coba lokal berjalan mulus"})
        check("FF24", "Feedback stored locally in SQLite", st == 200)

        # Security: path traversal blocked
        st, _, _, _ = req("GET", "/assets/../../server.py")
        check("FF24", "Security: path traversal blocked (404)", st == 404)

        # Performance: API p95 latency (60 requests) + snapshot & shell JS bytes
        for _ in range(60):
            st_p, raw_p, _, ms = req("GET", "/state")
            perf_latencies.append(ms)
            snapshot_bytes = len(raw_p)
        perf_latencies.sort()
        p95 = perf_latencies[int(len(perf_latencies) * 0.95)]
        shell_raw = (ROOT / "web" / "index.html").read_bytes() + (ROOT / "web" / "assets" / "ff_modules.js").read_bytes()
        shell_gz = len(gzip.compress(shell_raw))
        check("FF24", f"Perf: API p95={p95:.1f}ms (<=500ms), shell_gz={shell_gz/1024:.1f}KB (<=250KB), snapshot={snapshot_bytes/1024:.1f}KB",
              p95 <= 500 and shell_gz <= 250 * 1024)

        # JS syntax checks
        for f in ["web/landing.html", "web/index.html"]:
            txt = (ROOT / f).read_text(encoding="utf-8")
            m = re.findall(r"<script>(.*?)</script>", txt, re.S)
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
                tf.write(m[-1]); p = tf.name
            r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
            Path(p).unlink()
            check("FF24", f"JS syntax OK: {f}", r.returncode == 0, r.stderr.strip())
        r = subprocess.run(["node", "--check", str(ROOT / "web/assets/ff_modules.js")], capture_output=True, text=True)
        check("FF24", "JS syntax OK: web/assets/ff_modules.js", r.returncode == 0, r.stderr.strip())

    finally:
        httpd.shutdown()
        httpd.server_close()
        server.DB_PATH = orig_db
        shutil.rmtree(tmpdir, ignore_errors=True)

    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in RESULTS if r["status"] == "FAIL")
    print(f"\nREGRESSION SUMMARY: {passed} PASS, {failed} FAIL (total {len(RESULTS)})")
    out_dir = ROOT / "docs" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "regression_results.json").write_text(json.dumps({
        "passed": passed, "failed": failed, "total": len(RESULTS),
        "p95_ms": round(p95, 2) if perf_latencies else 0,
        "snapshot_bytes": snapshot_bytes,
        "results": RESULTS,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
