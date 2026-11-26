"""TERRA NOVA — 90 & 180-Day Multi-Scenario Economy Simulation (Realistic_v1).
Runs actual engine/gameplay.py transitions across 6 player archetypes and exports raw CSVs.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.gameplay import (  # noqa: E402
    DEFAULT_CONFIG,
    aksi,
    daftar_gt,
    daftar_pr,
    evaluasi_chosen_provisional,
    hitung_gsg,
    settle_waktu,
    state_awal,
)


def safe_act(s, payload, t):
    try:
        aksi(s, payload, t, DEFAULT_CONFIG)
        return True
    except Exception:
        return False


def run_scenario(name, starter_gc, days=180, mode="modest", sandbox_topup=0):
    t = 1_795_700_000.0  # Fixed deterministic epoch
    s = state_awal(starter_gc)
    s["waktu"] = t
    safe_act(s, {"aksi": "terima", "nama": name, "gender": "pria", "kota": "Bandung"}, t)
    safe_act(s, {"aksi": "intro_selesai"}, t)

    if sandbox_topup > 0:
        safe_act(s, {"aksi": "sandbox_topup", "sku": "TOPUP_RECYCLER"}, t)
    if mode == "cash_exhaustion":
        # Simulate player spending down to near-zero cash by buying DRE-001 (450k) + MCH-006 (350k) + petak (150k)
        safe_act(s, {"aksi": "beli_mesin", "machine_id": "DRE-001"}, t)
        safe_act(s, {"aksi": "beli_mesin", "machine_id": "MCH-006"}, t)
        safe_act(s, {"aksi": "beli_petak"}, t)
        s["koin"] = 0  # forced edge-case stress!

    daily_rows = []
    deadlock_days = 0
    god_day = None
    snap_90 = None

    for day in range(1, days + 1):
        # Advance 1 simulated day in 4 chunks (6h each <= 8h lazy tick cap)
        for q in range(4):
            t += 6 * 3600
            settle_waktu(s, t)

        # Daily player actions based on archetype
        loops = 1 if mode == "low_activity" else (3 if mode == "industrial" else 2)

        # 1. Pick up free wild & river trash (always available, zero cash required!)
        for item in list(s["sampah_liar"])[: (2 if mode == "low_activity" else 5)]:
            safe_act(s, {"aksi": "pungut", "id": item["id"]}, t)
        for rv in list(s["sampah_sungai"])[:2]:
            safe_act(s, {"aksi": "pungut_sungai", "id": rv["id"]}, t)
        for ev in list(s["dle_events"])[:1]:
            safe_act(s, {"aksi": "ambil_dle", "event_id": ev["id"]}, t)

        # Cash recovery if low cash
        if s["koin"] < 2000 and mode == "cash_exhaustion":
            non_starter = [m for m in s["machines_owned"] if not m.get("starter")]
            if non_starter:
                safe_act(s, {"aksi": "jual_mesin_bekas", "uid": non_starter[0]["uid"]}, t)

        # 2. Transport from Pasar / Sungai
        for _ in range(loops):
            node = "pasar" if day % 2 == 0 else "sungai"
            if safe_act(s, {"aksi": "angkut_node", "node": node, "gram": 10_000, "_test_eta": 0}, t):
                t += 1
                settle_waktu(s, t)
                safe_act(s, {"aksi": "terima_kargo"}, t)

        # 3. Sort, B3 safe handover, Process (Compost, Plastic, Household Biogas)
        while s["campuran_g"] >= 1000:
            if not safe_act(s, {"aksi": "pilah"}, t):
                break
        if s["b3_g"] >= 10:
            safe_act(s, {"aksi": "serah_b3"}, t)

        # Household renewable solar kit purchase when affordable (for modest/energy/industrial)
        has_solar = any(m["canonical_id"] == "DRE-001" for m in s["machines_owned"])
        if not has_solar and s["koin"] >= 500_000 and mode != "low_activity":
            safe_act(s, {"aksi": "beli_mesin", "machine_id": "DRE-001"}, t)
        if mode == "industrial" and len(s["petak"]) < 3 and s["koin"] >= 600_000:
            safe_act(s, {"aksi": "beli_petak"}, t)

        # Biogas + renewable energy (household partner access or own)
        if s["organik_g"] >= 5000:
            safe_act(s, {"aksi": "olah_biogas"}, t)
            safe_act(s, {"aksi": "jalankan_energi", "sumber": "biogas"}, t)
        if s["energy"]["battery_renew_wh"] >= 200:
            safe_act(s, {"aksi": "jalankan_energi", "sumber": "renewable"}, t)
        if s["stat"]["audit_energi"] == 0 and (s["energy"]["waste_origin_used_wh"] > 0 or s["energy"]["renewable_used_wh"] > 0):
            safe_act(s, {"aksi": "audit_energi"}, t)

        # Compost & plastic processing
        for _ in range(3):
            if s["organik_g"] >= 2000:
                safe_act(s, {"aksi": "olah_kompos"}, t)
            if s["plastik_g"] >= 1000:
                safe_act(s, {"aksi": "daur" if day % 2 == 0 else "kreasi"}, t)

        # 4. Garden & Vitality
        if not s["ditanam"]:
            if s["benih_map"].get("CR01", 0) == 0 and s["koin"] >= 1000:
                safe_act(s, {"aksi": "beli_benih", "crop_id": "CR01", "qty": 2}, t)
            safe_act(s, {"aksi": "tanam_crop", "crop_id": "CR01", "petak": 0}, t)
        if s["ditanam"] and s["detik"] > 0 and not s["dipupuk"] and s["kompos_g"] >= 1000:
            safe_act(s, {"aksi": "pupuk", "petak": 0}, t)
        if s["ditanam"] and s["detik"] <= 0:
            safe_act(s, {"aksi": "panen", "petak": 0}, t)

        if s["vitality"] < 65:
            if s["pangan_map"].get("FD_AIR", 0) == 0 and s["koin"] >= 3000:
                safe_act(s, {"aksi": "beli_pangan", "food_id": "FD_AIR", "qty": 2}, t)
            safe_act(s, {"aksi": "makan", "item_id": "FD_AIR"}, t)

        # 5. Sell outputs
        for prod in ("kompos", "pelet", "pot", "kertas", "logam"):
            safe_act(s, {"aksi": f"jual_{prod}"}, t)
        for cid, gr in list(s["panen_map"].items()):
            if gr >= 200:
                safe_act(s, {"aksi": "jual_panen_crop", "crop_id": cid, "gram": min(gr, 400)}, t)

        # 6. Claim any eligible GT01-09 & PR01-10
        for gt in daftar_gt(s):
            if gt["can_claim"]:
                safe_act(s, {"aksi": "klaim_gt", "id": gt["id"]}, t)
        for pr in daftar_pr(s):
            if pr["can_claim"]:
                safe_act(s, {"aksi": "klaim_pr", "id": pr["id"]}, t)

        gsg = hitung_gsg(s)
        if gsg["passed"] and god_day is None:
            god_day = day
        if s["koin"] < 500 and s["total_masuk_g"] == 0:
            deadlock_days += 1

        row = {
            "scenario": name,
            "day": day,
            "koin_gc": s["koin"],
            "earned_gc": s["wallet"]["earned_gc"],
            "grant_gc": s["wallet"]["grant_gc"],
            "topup_gc": s["wallet"]["topup_sandbox_gc"],
            "tier": s["tier"],
            "pulih_kg": round(s["stat"]["pulih_unik_g"] / 1000, 2),
            "waste_kwh": round(s["energy"]["waste_origin_used_wh"] / 1000, 2),
            "renew_kwh": round(s["energy"]["renewable_used_wh"] / 1000, 2),
            "vitality": s["vitality"],
            "backlog_kg": round(s["backlog_tpa_g"] / 1000, 2),
            "gsg_passed": gsg["passed"],
            "self_made": s["wallet"]["self_made_provisional"],
        }
        daily_rows.append(row)
        if day == 90:
            snap_90 = dict(row)

    ch = evaluasi_chosen_provisional(s)
    summary = {
        "scenario": name,
        "starter_gc": starter_gc,
        "day90_koin": snap_90["koin_gc"],
        "day90_tier": snap_90["tier"],
        "day90_pulih_kg": snap_90["pulih_kg"],
        "day180_koin": s["koin"],
        "day180_earned_gc": s["wallet"]["earned_gc"],
        "day180_tier": s["tier"],
        "day180_pulih_kg": round(s["stat"]["pulih_unik_g"] / 1000, 2),
        "day180_waste_kwh": round(s["energy"]["waste_origin_used_wh"] / 1000, 2),
        "day180_renew_kwh": round(s["energy"]["renewable_used_wh"] / 1000, 2),
        "god_day": god_day or "NOT_REACHED",
        "deadlock_days": deadlock_days,
        "self_made": s["wallet"]["self_made_provisional"],
        "chosen_candidate_provisional": ch["candidate_provisional"],
        "chosen_final_active": ch["final_selection_active"],
    }
    return daily_rows, summary


def main():
    scenarios = [
        ("modest_1M_nopay", 1_000_000, "modest", 0),
        ("modest_100k_stress", 100_000, "modest", 0),
        ("industrial_1M_nopay", 1_000_000, "industrial", 0),
        ("paid_sandbox_1M_plus_5M", 1_000_000, "modest", 5_000_000),
        ("low_activity_1M", 1_000_000, "low_activity", 0),
        ("cash_exhaustion_recovery", 1_000_000, "cash_exhaustion", 0),
    ]
    all_daily = []
    summaries = []
    for name, starter, mode, topup in scenarios:
        drows, summ = run_scenario(name, starter, 180, mode, topup)
        all_daily.extend(drows)
        summaries.append(summ)
        print(f"[SIM] {name:26s} | D90: {summ['day90_tier']:9s} ({summ['day90_koin']:>10,} GC) | D180: {summ['day180_tier']:9s} ({summ['day180_koin']:>10,} GC) | God day={summ['god_day']} | Deadlock={summ['deadlock_days']}")

    out_dir = ROOT / "docs" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "sim_180d_daily.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_daily[0].keys()))
        w.writeheader()
        w.writerows(all_daily)
    with (out_dir / "sim_180d_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
        w.writeheader()
        w.writerows(summaries)
    print("Saved CSV reports to docs/reports/sim_180d_*.csv")


if __name__ == "__main__":
    main()
