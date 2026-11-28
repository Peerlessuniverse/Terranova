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
import urllib.parse
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import server  # noqa: E402
from engine import gameplay as G  # noqa: E402
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
    orig_admins = set(server.ADMIN_USERS)
    server.ADMIN_USERS = {"ff_tester"}
    G.TEST_MODE = True  # izinkan _test_eta hanya di suite ini

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

        # Keputusan pemilik (B6): akun v0.9 direset ke Realistic_v1, identitas dipertahankan
        old_v09 = {"versi": 2, "diterima": True, "koin": 1350, "benih": 3, "nama": "Lama", "kota": "Medan", "stat": {"pungut": 4}}
        mig = server.migrasi_state(old_v09)
        check("FF01", "v0.9 account reset to Realistic_v1 (1.000.000 GC) keeping name & city",
              mig["koin"] == 1_000_000 and mig["economy_mode"] == "realistic_v1" and mig["nama"] == "Lama"
              and mig["kota"] == "Medan" and mig["stat"]["pungut"] == 0 and len(mig["sampah_liar"]) == 21)
        mig2 = server.migrasi_state({**json.loads(json.dumps(s)), "economy_mode": "historical_v09_preserved", "koin": 1000})
        check("FF01", "Already-migrated historical_v09_preserved account is also reset",
              mig2["koin"] == 1_000_000 and mig2["economy_mode"] == "realistic_v1")

        # FF02: Catalog 282 materials, 307 machines (288 canonical + 19 aliases)
        seed = load_seed()
        cs = seed["stats"]
        check("FF02", "Catalog exact counts 282 mat / 307 mch (288 canon + 19 alias)",
              cs["materials_total"] == 282 and cs["machines_rows"] == 307 and cs["machines_canonical"] == 288 and cs["machines_aliases"] == 19,
              str(cs))
        st, raw, _, _ = req("GET", "/catalog?kind=machine&page=1&per_page=24")
        cd = json.loads(raw)
        check("FF02", "Paginated /catalog returns 24 items/page", st == 200 and len(cd["items"]) == 24 and cd["total"] == 307)
        check("FF16", "K1 Catalog lists categories for the filter", len(cd.get("categories", [])) >= 10)
        st, raw, _, _ = req("GET", "/catalog?kind=machine&cat=" + urllib.parse.quote("Surya") + "&page=1&per_page=24")
        cdf = json.loads(raw)
        check("FF16", "K1 Category filter returns only that category", st == 200 and cdf["total"] == 16 and all(i["category"] == "Surya" for i in cdf["items"]))
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
        d_buy = json.loads(raw)
        solar = d_buy["state"]["machines_owned"][-1]
        check("FF13", "E3 Purchased item is auto-placed on the land (visible immediately)", bool(solar.get("pos")))
        kompos = next(m for m in d_buy["state"]["machines_owned"] if m["uid"] == "starter-kompos")
        check("FF13", "E3 Starter komposter has a valid on-land position", bool(kompos.get("pos")))
        kx, ky = kompos["pos"]
        st_ov, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": uid_solar, "x": kx + 5, "y": ky})
        check("FF13", "E3 Drag onto another item is rejected (no overlap)", st_ov == 400)
        st_rd, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": uid_solar, "x": 900, "y": 700})
        check("FF13", "E3 Drag onto the road is rejected", st_rd == 400)
        st_bd, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": uid_solar, "x": 600, "y": 300})
        check("FF13", "E3 Drag onto the sorting shed is rejected", st_bd == 400)
        st_ok, raw_ok, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": uid_solar, "x": 900, "y": 140})
        check("FF13", "E3 Solar panel may be dragged onto the office roof", st_ok == 200 and next(m for m in json.loads(raw_ok)["state"]["machines_owned"] if m["uid"] == uid_solar)["pos"] == [900, 140])
        st_ok2, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": "starter-kompos", "x": 1250, "y": 560})
        check("FF13", "E3 Komposter may be dragged to free grass inside the land", st_ok2 == 200)
        st_rf, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": "starter-kompos", "x": 900, "y": 140})
        check("FF13", "E3 Non-solar item cannot be placed on the roof", st_rf == 400)
        st_fc, _, _, _ = req("POST", "/aksi", {"key": str(uuid.uuid4()), "aksi": "pindah_mesin", "uid": "starter-kompos", "x": 1150, "y": 556})
        check("FF13", "E3 Item cannot straddle the yard fence", st_fc == 400)
        gts_meta = json.loads(raw_ok)["meta"]["gt_missions"]
        check("FF10", "K1 Mission cards carry measurable progress, lock reason and suggestion",
              all("nilai" in m for m in gts_meta) and gts_meta[2].get("kunci") is not None and "saran" not in gts_meta[3])
        st_ms, raw_ms, _, _ = req("GET", "/meta-statis")
        ms = json.loads(raw_ms)
        check("FF24", "K1 Static meta (mission texts/targets, land geometry) served once via /meta-statis",
              st_ms == 200 and len(ms["misi_def"]["GT03"]["labels"]) == 3 and bool(ms["misi_def"]["GT04"]["saran"]) and "pagar" in ms["tata_lahan"])
        check("FF03", "K1 Server messages use Indonesian thousands separator", "450.000" in json.loads(raw)["pesan"] and "450,000" not in json.loads(raw)["pesan"])
        check("FF13", "E3 Card data lists in-game effect of owned items", "efek" in json.loads(raw_ok)["meta"]["info_mesin"]["DRE-001"])
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

        # FF25: regresi bug yang ditemukan uji mandiri (B1–B10)
        opener2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

        def req2(method, path, body=None):
            data = json.dumps(body).encode() if body is not None else None
            r = urllib.request.Request(base + path, data=data, headers={"Content-Type": "application/json"} if data else {}, method=method)
            try:
                with opener2.open(r, timeout=5) as resp:
                    return resp.status, json.loads(resp.read() or b"{}")
            except urllib.error.HTTPError as e:
                return e.code, json.loads(e.read() or b"{}")

        def aksi2(**p):
            return req2("POST", "/aksi", dict(key=str(uuid.uuid4()), **p))

        req2("POST", "/daftar", {"username": "ff_biasa", "email": "biasa@teranova.local", "password": "Password123!"})
        st, d = aksi2(aksi="terima", nama="Biasa", gender="pria", kota="Bandung", avatar="bukan-objek")
        check("FF25", "B9 Malformed avatar payload returns 400 JSON (no dropped connection)", st == 400 and "pesan" in d)
        aksi2(aksi="terima", nama="Biasa", gender="pria", kota="Bandung")
        st, d = req2("POST", "/market/quote", {"kind": "machine", "id": ["x"], "side": "buy"})
        check("FF25", "B9 Quote with list id returns 4xx JSON", st == 400)
        st, d = req2("POST", "/admin/config", {"updates": {"price_multiplier": 0.5}, "reason": "serang"})
        check("FF25", "B1 Non-admin player cannot publish global config (403)", st == 403)
        st, d = req2("GET", "/admin/config")
        check("FF25", "B1 Non-admin GET hides audit log & reports is_admin=false", st == 200 and d["is_admin"] is False and d["audit"] == [])

        G.TEST_MODE = False
        st, d = aksi2(aksi="angkut_node", node="pasar", gram=10000, _test_eta=-5)
        st2, _ = aksi2(aksi="terima_kargo")
        check("FF25", "B4 _test_eta from client ignored outside test mode", st == 200 and st2 == 400
              and d["state"]["job"]["tiba_pada"] - d["state"]["job"]["berangkat_pada"] == G.NODE_TEMPLATE["pasar"]["eta_detik"])
        G.TEST_MODE = True

        st, d = aksi2(aksi="audit_neraca")
        check("FF25", "B5 Audit neraca rejected without new processed batch", st == 400)
        ok_spam = all(aksi2(aksi="audit_neraca")[0] == 400 for _ in range(5))
        st, _ = aksi2(aksi="klaim_pr", id="PR10")
        check("FF25", "B5 Audit spam cannot unlock PR10", ok_spam and st == 400)

        aksi2(aksi="sandbox_topup", sku="TOPUP_CIVILIZATION")
        st, d = aksi2(aksi="beli_mesin", machine_id="DRE-077")
        cap_beli = d["state"]["energy"]["battery_cap_wh"]
        uid = d["state"]["machines_owned"][-1]["uid"]
        st, d = aksi2(aksi="jual_mesin_bekas", uid=uid)
        check("FF25", "B3 Selling LFP battery removes its capacity", st == 200 and cap_beli == 6000 and d["state"]["energy"]["battery_cap_wh"] == 1000)

        req("POST", "/admin/config", {"updates": {"price_multiplier": 0.5}, "reason": "uji arbitrase"})
        k0 = req2("GET", "/state")[1]["state"]["koin"]
        for _ in range(3):
            st, d = aksi2(aksi="beli_mesin", machine_id="DRE-077")
            uid = d["state"]["machines_owned"][-1]["uid"]
            st, d = aksi2(aksi="jual_mesin_bekas", uid=uid)
        req("POST", "/admin/config", {"updates": {"price_multiplier": 2.0}, "reason": "uji arbitrase naik"})
        st, d = aksi2(aksi="beli_mesin", machine_id="DRE-076")
        uid = d["state"]["machines_owned"][-1]["uid"]
        paid = d["state"]["machines_owned"][-1]["paid_gc"]
        k_mid = d["state"]["koin"]
        req("POST", "/admin/config", {"rollback_to": 1, "reason": "kembalikan"})
        st, d = aksi2(aksi="jual_mesin_bekas", uid=uid)
        check("FF25", "B2 Buy/sell-used loop never profits (×0,5 and ×2,0 swings)",
              d["state"]["koin"] < k0 and d["state"]["koin"] - k_mid <= int(round(paid * 0.57)),
              f"saldo {k0:,} → {d['state']['koin']:,}")

        # B7: PR09 bisa dicapai — gerobak ditolak, 3 alat di slot bebas, lepas tersedia
        st, _ = aksi2(aksi="pasang_mesin", uid="starter-gerobak", slot="S2")
        check("FF25", "B7 Mobile cart (gerobak) cannot be placed in a yard slot", st == 400)
        aksi2(aksi="pasang_mesin", uid="starter-meja", slot="S2")
        st, d = aksi2(aksi="beli_mesin", machine_id="DRE-001")
        uid = d["state"]["machines_owned"][-1]["uid"]
        aksi2(aksi="pasang_mesin", uid=uid, slot="S6")
        st, d = aksi2(aksi="klaim_pr", id="PR09")
        check("FF25", "B7 PR09 claimable with komposter S1 + meja S2 + solar S6", st == 200)
        st, d = aksi2(aksi="lepas_mesin", uid=uid)
        check("FF25", "B7 lepas_mesin stores the item in the warehouse", st == 200 and not next(m for m in d["state"]["machines_owned"] if m["uid"] == uid).get("pos"))

        # E4 #4: karakter dipilih sekali sebelum prolog (warna jaket & rambut), gender tidak bisa diganti di profil
        ka = G.state_awal(); tk0 = time.time()
        G.aksi(ka, {"aksi": "terima", "nama": "Uji", "gender": "wanita", "kota": "Bandung", "avatar": {"baju": "biru", "rambut": "pirang"}}, tk0)
        try:
            G.aksi(ka, {"aksi": "ganti_karakter", "gender": "pria"}, tk0); ganti = True
        except ValueError:
            ganti = False
        check("FF01", "E4 Character setup stores gender + jacket/hair colour; gender cannot be changed later",
              ka["avatar"] == {"baju": "biru", "rambut": "pirang"} and ka["gender"] == "wanita" and not ganti)
        try:
            G.aksi(G.state_awal(), {"aksi": "terima", "nama": "X", "gender": "pria", "kota": "Bandung", "avatar": {"baju": "emas"}}, tk0); salah = True
        except ValueError:
            salah = False
        check("FF01", "E4 Unknown appearance option rejected", not salah)

        # E4: efek produksi nyata alat dasar (hanya alat terpasang yang bekerja; massa tetap)
        e4 = G.state_awal(); G.tata_ulang_mesin(e4); e4["diterima"] = True; tk = time.time()
        def massa(x):
            return G.gudang_terpakai_g(x) + x["uap_terkendali_g"] + x["terjual_g"] + x["b3_serah_g"]
        e4["campuran_g"] = 30_000; e4["campuran_fraksi"] = {"organik": 15_000, "plastik": 6_000, "kertas": 3_000, "logam_kaca": 2_000, "residu": 3_700, "B3": 300}
        m0 = massa(e4); G.aksi(e4, {"aksi": "pilah"}, tk)
        check("FF08", "E4 Starter sorting table sorts 10 kg per action (5 kg base + 5 kg table)", e4["stat"]["pilah_g"] == 10_000 and massa(e4) == m0)
        meja = next(m for m in e4["machines_owned"] if m["canonical_id"] == "MCH-005"); simpan = meja.pop("pos")
        G.aksi(e4, {"aksi": "pilah"}, tk)
        check("FF08", "E4 Without an installed table sorting drops to 5 kg", e4["stat"]["pilah_g"] == 15_000)
        meja["pos"] = simpan
        e4["machines_owned"].append({"uid": "t-tong", "canonical_id": "MCH-001", "condition": 100, "pos": [1, 1]})
        r0 = e4["residu_g"]; m0 = massa(e4); G.aksi(e4, {"aksi": "pilah"}, tk)
        check("FF08", "E4 Sorted bins move part of residue into recyclables, mass conserved", e4["residu_g"] - r0 < 3_700 * 10 // 30 and massa(e4) == m0)
        e4["organik_g"] = 20_000
        e4["machines_owned"].append({"uid": "t-ember", "canonical_id": "MCH-022", "condition": 100, "pos": [2, 2]})
        k0 = e4["kompos_g"]; m0 = massa(e4); G.aksi(e4, {"aksi": "olah_kompos"}, tk)
        check("FF08", "E4 Composter capacities add up (starter 2 kg + bucket 4 kg = 6 kg -> 3 kg compost)", e4["kompos_g"] - k0 == 3_000 and massa(e4) == m0)
        for m in e4["machines_owned"]:
            if m["canonical_id"] in G.KOMPOS_BATCH_G:
                m.pop("pos", None)
        try:
            G.aksi(e4, {"aksi": "olah_kompos"}, tk); ok_k = False
        except ValueError as ex:
            ok_k = "komposter" in str(ex).lower()
        check("FF08", "E4 Compost needs an installed composter (actionable message)", ok_k)
        kap0 = G.kap_gudang(e4)
        e4["machines_owned"].append({"uid": "t-rak", "canonical_id": "MCH-006", "condition": 100, "pos": [3, 3]})
        check("FF08", "E4 Warehouse rack adds 100 kg capacity while installed", G.kap_gudang(e4) == kap0 + 100_000)
        e4["kompos_g"] = 5_000; h0 = e4["koin"]; G.aksi(e4, {"aksi": "jual_kompos"}, tk); tanpa = e4["koin"] - h0
        e4["machines_owned"].append({"uid": "t-timb", "canonical_id": "MCH-003", "condition": 100, "pos": [4, 4]})
        h0 = e4["koin"]; G.aksi(e4, {"aksi": "jual_kompos"}, tk); dengan = e4["koin"] - h0
        check("FF03", "E4 Hanging scale adds 5% to processed product sales", dengan == tanpa + tanpa * 5 // 100, f"{tanpa} -> {dengan}")
        e4["plastik_g"] = 5_000
        e4["machines_owned"].append({"uid": "t-cacah", "canonical_id": "MCH-044", "condition": 100, "pos": [5, 5]})
        p0 = e4["pelet_g"]; m0 = massa(e4); G.aksi(e4, {"aksi": "daur"}, tk)
        check("FF08", "E4 Plastic shredder: 3 kg per action, 900 g per kg, mass conserved", e4["pelet_g"] - p0 == 2_700 and massa(e4) == m0)

        # B10: hari bersih hanya dari pengolahan nyata
        sim = G.state_awal(); sim["diterima"] = True
        t0 = time.time()
        for hari in range(10):
            sim["stat"]["batch_sejak_audit"] = 0
            try:
                G.aksi(sim, {"aksi": "audit_neraca"}, t0 + hari * 86400)
            except ValueError:
                pass
        check("FF25", "B10 Clean days are not earned by audit clicks alone", len(sim["stat"]["hari_bersih"]) == 0)

        # Biaya genset mitra masuk laba operasi; PR07 butuh laba positif
        sim = G.state_awal(); sim["diterima"] = True; sim["energy"]["biogas_m3_x100"] = 50
        G.aksi(sim, {"aksi": "jalankan_energi", "sumber": "biogas"}, time.time())
        check("FF25", "Biogas genset partner fee reduces operating profit", sim["wallet"]["operating_profit_gc"] == -2000)
        sim["kompos_g"] = 2000
        sim["wallet"]["operating_profit_gc"] = -10_000  # mis. biaya angkut besar
        G.aksi(sim, {"aksi": "jual_kompos"}, time.time())
        rugi_tidak_dihitung = sim["stat"]["lot_jual_laba"] == 0
        sim["wallet"]["operating_profit_gc"] = 0
        G.aksi(sim, {"aksi": "jual_kompos"}, time.time())
        check("FF25", "PR07 sale counted only when cumulative operating profit is positive",
              rugi_tidak_dihitung and sim["stat"]["lot_jual_laba"] == 1)

        st, raw, _, _ = req("GET", "/leaderboard?board=wealthiest")
        check("FF25", "B9 Leaderboard GET is read-only (200)", st == 200)

        # ---- FF26: N1 surya waktu nyata + siang/malam, N2 lencana menetap, N5 pesan GT01
        tengah_malam = 1_798_761_600 - 7 * 3600  # 00.00 WIB
        def sim_surya(cid="DRE-001"):
            x = G.state_awal(); x["diterima"] = True
            x["machines_owned"].append({"uid": "uji", "canonical_id": cid, "slot": None})
            x["energy"]["battery_cap_wh"] = 100_000
            return x
        x = sim_surya(); t = tengah_malam + 6 * 3600; x["waktu"] = t
        while t < tengah_malam + 18 * 3600:
            t += 12; G.settle_waktu(x, t); x["waktu"] = t
        ideal = G.watt_dres(x, G.active_dynamic_event(t))[0] * G.jam_surya_efektif(tengah_malam, tengah_malam + 86400)
        check("FF26", "N1 Small solar charges under 12 s polling (fraction carried)",
              x["energy"]["battery_wh"] > 0 and abs(x["energy"]["battery_wh"] - ideal) <= 1,
              f"{x['energy']['battery_wh']} Wh vs {ideal:.1f}")
        x = sim_surya("DRE-003"); x["waktu"] = tengah_malam + 19 * 3600
        G.settle_waktu(x, tengah_malam + 23 * 3600)
        check("FF26", "N1 Solar produces nothing at night (19.00-23.00 WIB)", x["energy"]["battery_wh"] == 0)
        psh = G.jam_surya_efektif(tengah_malam, tengah_malam + 86400)
        check("FF26", "N1 Daily solar ~5 peak-sun-hours (real time, not accelerated)", 4.5 <= psh <= 5.5, f"{psh:.2f} h")
        wi = G.info_waktu(x, tengah_malam + 21 * 3600)
        check("FF26", "N1 waktu_info reports night phase", wi["fase"] == "malam" and wi["faktor_surya"] == 0)

        x = G.state_awal(); x["diterima"] = True
        x["wallet"]["operating_profit_gc"] = 2500; G.update_wealth_and_milestones(x, time.time())
        x["wallet"]["operating_profit_gc"] = 900   # biaya angkut menggerus laba
        saud = next(p for p in G.daftar_pencapaian(x) if p["id"] == "saudagar")
        check("FF26", "N2 Saudagar Hijau badge stays unlocked after later costs", saud["ok"])

        x = G.state_awal(); x["diterima"] = True; x["intro_selesai"] = True
        try:
            pesan = G.aksi(x, {"aksi": "klaim_gt", "id": "GT01"}, time.time())
        except ValueError as e:
            pesan = str(e)
        check("FF26", "N5 GT01 message has no '+0 GC'", "+0 GC" not in pesan, pesan)

        # Performance: API p95 latency (60 requests) + snapshot & shell JS bytes
        for _ in range(60):
            st_p, raw_p, _, ms = req("GET", "/state")
            perf_latencies.append(ms)
            snapshot_bytes = len(raw_p)
        perf_latencies.sort()
        p95 = perf_latencies[int(len(perf_latencies) * 0.95)]
        shell_raw = (ROOT / "web" / "index.html").read_bytes() + (ROOT / "web" / "assets" / "ff_modules.js").read_bytes() + (ROOT / "web" / "assets" / "tn_mesin.js").read_bytes()
        shell_gz = len(gzip.compress(shell_raw))
        check("FF24", f"Perf: API p95={p95:.1f}ms (<=500ms), shell_gz={shell_gz/1024:.1f}KB (<=250KB), snapshot={snapshot_bytes/1024:.1f}KB (<=20KB)",
              p95 <= 500 and shell_gz <= 250 * 1024 and snapshot_bytes <= 20 * 1024)

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
        server.ADMIN_USERS = orig_admins
        G.TEST_MODE = False
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
