"""TERRA NOVA — Feature Freeze v1.0 Gameplay Engine (Realistic_v1 + GT01-09 + PR01-10 + TR01-05 + 15 Crops + Vitality + WtE/DRES + River Spawn).
Server-authoritative, integer grams / GC / Wh, Lazy Tick (cap 8h), deterministic slot spawns.
"""
import hashlib
import math
import random
import time
from datetime import datetime, timezone, timedelta

from .catalog import (
    get_crop,
    get_food,
    get_machine,
    get_material,
    load_seed,
    make_quote,
    resolve_machine_id,
)

WIB = timezone(timedelta(hours=7))

FRAKSI = ("organik", "plastik", "kertas", "logam_kaca", "residu", "B3")
KOTA_SAH = ("Bandung", "Jakarta", "Surabaya", "Yogyakarta", "Semarang", "Medan", "Makassar", "Kota lainnya")
AVATAR_ALLOW = {
    "rambut": ("pendek", "ikal", "panjang", "cepuk"),
    "baju": ("hijau", "biru", "coklat", "kuning"),
    "topi": ("tanpa", "rimba", "cap", "daun"),
    "aksesori": ("tanpa", "kacamata", "ransel", "syal"),
}

# Realistic_v1 Transport Nodes (Addendum 11 §4)
NODE_TEMPLATE = {
    "permukiman": {
        "nama": "Permukiman Warga",
        "kapasitas_g": 150_000,
        "laju_per_menit_g": 600,
        "jarak_km": 1.0,
        "fee_tetap": 500,
        "gc_per_km": 300,
        "handling_per_kg": 20,
        "kompensasi_per_kg": 150,
        "eta_detik": 30,
        "min_kg": 5,
        "max_kg": 25,
        "komposisi": {"organik": 50, "plastik": 20, "kertas": 15, "logam_kaca": 5, "residu": 9, "B3": 1},
    },
    "pasar": {
        "nama": "Pasar Tradisional",
        "kapasitas_g": 150_000,
        "laju_per_menit_g": 700,
        "jarak_km": 2.0,
        "fee_tetap": 500,
        "gc_per_km": 300,
        "handling_per_kg": 20,
        "kompensasi_per_kg": 200,
        "eta_detik": 45,
        "min_kg": 5,
        "max_kg": 25,
        "komposisi": {"organik": 78, "plastik": 12, "kertas": 5, "logam_kaca": 1, "residu": 4, "B3": 0},
    },
    "sungai": {
        "nama": "Tepi Sungai",
        "kapasitas_g": 100_000,
        "laju_per_menit_g": 250,
        "jarak_km": 0.5,
        "fee_tetap": 500,
        "gc_per_km": 300,
        "handling_per_kg": 20,
        "kompensasi_per_kg": 250,
        "eta_detik": 25,
        "min_kg": 2,
        "max_kg": 25,
        "komposisi": {"organik": 0, "plastik": 55, "kertas": 0, "logam_kaca": 15, "residu": 30, "B3": 0},
    },
    "sekolah": {
        "nama": "Sekolah & Kantor",
        "kapasitas_g": 120_000,
        "laju_per_menit_g": 400,
        "jarak_km": 3.0,
        "fee_tetap": 500,
        "gc_per_km": 300,
        "handling_per_kg": 20,
        "kompensasi_per_kg": 100,
        "eta_detik": 60,
        "min_kg": 5,
        "max_kg": 25,
        "komposisi": {"organik": 20, "plastik": 25, "kertas": 45, "logam_kaca": 5, "residu": 5, "B3": 0},
    },
    "restoran": {
        "nama": "Restoran & Kafe",
        "kapasitas_g": 120_000,
        "laju_per_menit_g": 500,
        "jarak_km": 2.0,
        "fee_tetap": 500,
        "gc_per_km": 300,
        "handling_per_kg": 20,
        "kompensasi_per_kg": 200,
        "eta_detik": 45,
        "min_kg": 5,
        "max_kg": 25,
        "komposisi": {"organik": 70, "plastik": 15, "kertas": 10, "logam_kaca": 2, "residu": 3, "B3": 0},
    },
}

# Periodic Transport Missions TR01-TR05 (Asia/Jakarta windows, Addendum 11 §4)
TR_MISSIONS = [
    {"id": "TR01", "nama": "Sisa Pasar Pagi", "start_h": 6, "end_h": 9, "weekend": False, "node": "pasar", "min_kg": 10, "bonus_gc": 500},
    {"id": "TR02", "nama": "Restoran Siang", "start_h": 11, "end_h": 14, "weekend": False, "node": "restoran", "min_kg": 5, "bonus_gc": 500},
    {"id": "TR03", "nama": "Kardus Toko", "start_h": 15, "end_h": 18, "weekend": False, "node": "sekolah", "min_kg": 5, "bonus_gc": 500},
    {"id": "TR04", "nama": "Bersih Tepi Sungai", "start_h": 18, "end_h": 21, "weekend": False, "node": "sungai", "min_kg": 2, "bonus_gc": 500},
    {"id": "TR05", "nama": "Kerja Bakti Akhir Pekan", "start_h": 8, "end_h": 20, "weekend": True, "node": "permukiman", "min_kg": 10, "bonus_gc": 1000},
]

# Spawn definitions (preserve §32 + fix (590,258) -> (465,255) + river floating trash)
JENIS_SAMPAH = {
    "botol": ("plastik_g", 300, 700), "kaleng": ("logam_kaca_g", 200, 500), "kardus": ("kertas_g", 400, 1000),
    "organik": ("organik_g", 600, 1500), "kaca": ("logam_kaca_g", 400, 900), "kantong": ("campuran_g", 1500, 3000),
    "baterai": ("b3_g", 80, 200), "sterofoam": ("residu_g", 150, 400),
    "daun": ("organik_g", 150, 400), "ranting": ("organik_g", 250, 700), "dahan": ("organik_g", 600, 1200),
    "buah": ("organik_g", 300, 700),
    "kemasan": ("campuran_g", 150, 400),
}
JENIS_UMUM = ("botol", "kaleng", "kardus", "organik", "kaca", "kantong", "baterai", "sterofoam")
JENIS_SUNGAI = ("botol", "kaleng", "kemasan", "organik")  # NO hazardous/sharp B3 for hand pickup!
LABEL_SAMPAH = {
    "botol": "Botol PET", "kaleng": "Kaleng", "kardus": "Kardus & kertas", "organik": "Sisa organik",
    "kaca": "Botol kaca", "kantong": "Kantong sampah campur", "baterai": "Baterai bekas (B3)",
    "sterofoam": "Sterofoam", "daun": "Daun kering", "ranting": "Ranting patah", "dahan": "Dahan patah",
    "buah": "Buah busuk", "kemasan": "Kemasan campur terapung",
}
TITIK_DALAM = [(700, 480), (780, 520), (880, 475), (925, 425), (895, 372), (665, 522), (1000, 505), (860, 548), (940, 482)]
TITIK_LUAR = [
    (300, 250), (480, 170), (620, 120), (1150, 110), (1300, 230), (200, 150), (1440, 330),
    (150, 470), (260, 420), (120, 560), (300, 540), (1620, 330), (1380, 620),
    (480, 582), (620, 592), (1050, 612), (1200, 622), (1330, 642),
    (150, 735), (450, 765), (700, 800), (1000, 835), (1250, 860), (1500, 880),
]
TITIK_SUNGAI = {(150, 735), (450, 765), (700, 800), (1000, 835), (1250, 860), (1500, 880)}
# Fixed (590, 258) -> (465, 255) so all 10 tree spots are strictly outside fence & outside Area Pilah OBST!
TITIK_POHON = [
    (190, 150), (440, 195), (465, 255), (280, 345), (140, 482),
    (700, 140), (1195, 152), (1560, 125), (1440, 270), (1630, 600),
]
SAMPAH_SLOT_DETIK, SAMPAH_MAKS_LUAR = 90, 16
POHON_SLOT_DETIK, POHON_MAKS = 60, 6
JALAN_SLOT_DETIK, JALAN_MAKS = 40, 5
SUNGAI_SLOT_DETIK, SUNGAI_MAKS, SUNGAI_LINTAS_DETIK = 75, 4, 90

KENDARAAN = {
    "pikap": ("RL", ("organik", "organik", "kardus")), "truk": ("RL", ("kardus", "kantong", "sterofoam")),
    "motor": ("RL", ("botol", "kaleng", "kantong")), "sepeda": ("RL", ("botol", "kardus")),
    "becak": ("RL", ("kardus", "organik", "sterofoam")), "delman": ("RL", ("organik", "daun")),
}

# Modular placement slots inside/right of yard (no overlap, road & river safe)
YARD_SLOTS = [
    {"id": "S1", "label": "Slot Komposter Kiri", "x": 620, "y": 530},
    {"id": "S2", "label": "Slot Alat Tengah", "x": 760, "y": 545},
    {"id": "S3", "label": "Slot Energi Kanan", "x": 1030, "y": 535},
    {"id": "S4", "label": "Slot Biogas Belakang", "x": 910, "y": 360},
    {"id": "S5", "label": "Slot Surya Atap", "x": 960, "y": 210},
    {"id": "S6", "label": "Slot Ekspansi Timur", "x": 1410, "y": 495},
]

# Realistic_v1 Prices for processed products (per kg, 1 GC = Rp1 nominal simulation)
HARGA_PRODUK_REALISTIS = {
    "kompos": ("kompos_g", 1000, 3500),       # 3.500 GC/kg
    "pelet": ("pelet_g", 850, 9500),          # ~11.176 GC/kg (850g = 9.500 GC)
    "pot": ("pot_g", 850, 14000),             # pot daur ulang
    "kertas": ("kertas_g", 1000, 2400),       # kardus OCC pengepul
    "logam": ("logam_kaca_g", 1000, 6500),    # campuran logam/kaca
}

HARGA_PETAK_REALISTIS = (150_000, 300_000, 500_000)
HARGA_GUDANG_REALISTIS = (350_000, 750_000)

# Sandbox Top-Up Packages (GME v1.0, local sandbox ONLY, no real money!)
SANDBOX_TOPUP_PACKAGES = [
    {"sku": "TOPUP_STARTER", "nama": "Starter (Sandbox)", "gc": 1_000_000, "idr": 10_000},
    {"sku": "TOPUP_EXPLORER", "nama": "Explorer (Sandbox)", "gc": 2_500_000, "idr": 25_000},
    {"sku": "TOPUP_RECYCLER", "nama": "Recycler (Sandbox)", "gc": 5_000_000, "idr": 50_000},
    {"sku": "TOPUP_GUARDIAN", "nama": "Guardian (Sandbox)", "gc": 10_000_000, "idr": 100_000},
    {"sku": "TOPUP_INDUSTRIALIST", "nama": "Industrialist (Sandbox)", "gc": 25_000_000, "idr": 250_000},
    {"sku": "TOPUP_CIVILIZATION", "nama": "Civilization (Sandbox)", "gc": 50_000_000, "idr": 500_000},
]

# Earned GC Milestones (separate from starter & topup!)
EARNED_MILESTONES = [1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000]

# Default runtime config (editable via local Admin Config with audit & rollback)
DEFAULT_CONFIG = {
    "version": 1,
    "starter_gc": 1_000_000,
    "stress_starter_gc": 100_000,
    "pickup_reward_gc": 100,
    "pickup_daily_cap_gc": 2000,
    "rare_boost_daily_cap_gc": 5000,
    "price_multiplier": 1.0,
    "support_url": None,
    "sponsor_contact_url": None,
    "soundtrack_url": None,
}


def road_y(x):
    return 611 + 0.0962 * x


def perlu(syarat, pesan):
    if not syarat:
        raise ValueError(pesan)


def bagi_g(total_g, komp):
    out = {}
    sisa = int(total_g)
    aktif = [f for f in FRAKSI if komp.get(f, 0) > 0]
    tot_w = sum(komp.get(f, 0) for f in FRAKSI) or 100
    for f in FRAKSI:
        v = (int(total_g) * komp.get(f, 0)) // tot_w
        out[f] = v
        sisa -= v
    if sisa > 0 and aktif:
        out[aktif[0]] += sisa
    return out


def stat_awal():
    return {
        "pungut": 0, "pungut_dalam": 0, "sungai": 0, "sungai_apung": 0,
        "pilah_g": 0, "kompos": 0, "daur": 0, "kreasi": 0, "biogas": 0,
        "panen": 0, "panen_langka": 0, "koin_jual": 0, "lot_jual_sah": 0,
        "lot_jual_laba": 0, "pulih_unik_g": 0, "neraca_valid": 0, "audit_energi": 0,
        "angkut_tepat": 0, "resep_dipakai": [], "varietas_panen": [], "fraksi_terpilah": [],
        "hari_bersih": [], "energi_sumber_dipakai": [],
    }


def state_awal(starter_gc=1_000_000):
    nodes = {}
    for kode, tpl in NODE_TEMPLATE.items():
        nodes[kode] = {
            "stok": bagi_g(60_000 if kode != "sungai" else 25_000, tpl["komposisi"]),
            "kapasitas_g": tpl["kapasitas_g"],
        }
    return {
        "versi": 3,
        "economy_mode": "realistic_v1",
        "diterima": False,
        "nama": "Penjaga Bumi",
        "gender": "pria",
        "avatar": {"rambut": "pendek", "baju": "hijau", "topi": "rimba", "aksesori": "tanpa"},
        "kota": "Bandung",
        "koin": int(starter_gc),
        "starter_gc_initial": int(starter_gc),
        "peak_wealth_gc": int(starter_gc),
        "poin": 0,
        "karma": 0.0,
        "tier": "Awaken",
        "tier_idx": 0,
        "gudang_kap_g": 500_000,
        # Raw material inventory (grams)
        "campuran_g": 0,
        "campuran_fraksi": {f: 0 for f in FRAKSI},
        "organik_g": 0,
        "plastik_g": 0,
        "kertas_g": 0,
        "logam_kaca_g": 0,
        "residu_g": 0,
        "b3_g": 0,
        # Processed outputs (grams) & mass balance
        "kompos_g": 0,
        "pelet_g": 0,
        "pot_g": 0,
        "uap_terkendali_g": 0,
        "b3_serah_g": 0,
        "terjual_g": 0,
        "dipakai_kebun_g": 0,
        "biomassa_panen_g": 0,
        "backlog_tpa_g": 0,
        "total_masuk_g": 0,
        "env_ledger_debit_g": 0,
        # Wallet ledger (earned vs topup vs grants)
        "wallet": {
            "earned_gc": 0,
            "operating_profit_gc": 0,
            "grant_gc": 0,
            "topup_sandbox_gc": 0,
            "expenses_gc": 0,
            "self_made_provisional": True,
        },
        # DWE nodes & WCS active job
        "nodes": nodes,
        "job": None,
        # DLE & spawns
        "dle_events": [],
        "dle_cursor_slot": 0,
        "dle_utc_day": "",
        "dle_daily_count": 0,
        "dle_daily_bonus_g": 0,
        "dle_tutorial_done": False,
        "intro_selesai": False,
        "sampah_liar": [],
        "sampah_sungai": [],  # floating river trash
        "sampah_seq": 0,
        "sampah_slot": 0,
        "pohon_slot": 0,
        "jalan_slot": 0,
        "sungai_slot": 0,
        "pickup_day": "",
        "pickup_daily_gc": 0,
        # 15-Crop Garden & Vitality
        "benih": 3,  # legacy mirror (sum of CR01+CR02)
        "benih_map": {"CR01": 2, "CR02": 1},  # Feature Freeze: 2 kangkung, 1 bayam
        "panen_map": {},  # crop_id -> grams
        "pangan_map": {"FD_AIR": 2},  # staple food units
        "rare_seed_week": "",
        "rare_seed_bought": {},
        "crop_sell_day": "",
        "crop_sold_today_g": {},
        "rare_boost": None,  # {crop_id, pct, expires_at}
        "rare_boost_day": "",
        "rare_boost_today_gc": 0,
        "vitality": 100,
        "food_groups_day": "",
        "food_groups_today": [],
        "stok_langka": 0,
        "ditanam": False,
        "tanaman": "",
        "tanaman_id": "",
        "detik": 0.0,
        "dipupuk": False,
        "panen": 0,
        "panen_langka": 0,
        "misi": False,
        "varietas": "",
        "pernah_jual": False,
        "waktu": 0.0,
        "petak": [],
        "gudang_upgrade": 0,
        # Machinery, Modular Placement & Leases
        "machines_owned": [
            {"uid": "starter-gerobak", "canonical_id": "MCH-002", "condition": 100, "slot": None, "starter": True},
            {"uid": "starter-meja", "canonical_id": "MCH-005", "condition": 100, "slot": None, "starter": True},
            {"uid": "starter-kompos", "canonical_id": "MCH-021", "condition": 100, "slot": "S1", "starter": True},
        ],
        "machines_leased": [],  # {uid, canonical_id, expires_at, partner}
        # Energy Center (Wh integer, strict provenance)
        "energy": {
            "battery_wh": 0,
            "battery_cap_wh": 1000,  # starter small buffer 1 kWh
            "battery_waste_wh": 0,
            "battery_renew_wh": 0,
            "waste_origin_used_wh": 0,
            "renewable_used_wh": 0,
            "battery_loss_wh": 0,
            "biogas_m3_x100": 0,
            "last_audit_ts": 0,
        },
        # Progression, Grants, Celebrations, Journal, Periodic Missions
        "gt_claimed": [],
        "pr_claimed": [],
        "tr_claimed_windows": [],
        "milestones_claimed": [],
        "celebrations": [],
        "journal": [],
        "public_profile": {"opt_in": False, "quote": "Merawat Bumi dari lahan kecil."},
        "stat": stat_awal(),
    }


def migrasi_state(raw, cfg=None):
    """Non-destructive migration: preserves existing v0.9 accounts & balances without forced overwrite!"""
    base = state_awal((cfg or DEFAULT_CONFIG).get("starter_gc", 1_000_000))
    if not isinstance(raw, dict):
        return base
    v = raw.get("versi", 1)
    if v >= 2:
        was_v2 = (v == 2)
        for k, val in base.items():
            if k not in raw:
                raw[k] = val
        for k, val in stat_awal().items():
            raw["stat"].setdefault(k, val)
        for k, val in base["wallet"].items():
            raw["wallet"].setdefault(k, val)
        for k, val in base["energy"].items():
            raw["energy"].setdefault(k, val)
        for k, val in base["nodes"].items():
            raw["nodes"].setdefault(k, val)
        if was_v2:
            # Preserve existing v0.9 account balance & flag it as historical_v09 so we NEVER overwrite old balances!
            raw["versi"] = 3
            if raw.get("diterima"):
                raw["economy_mode"] = "historical_v09_preserved"
                raw["starter_gc_initial"] = raw.get("koin", 1000)
                if "CR01" not in raw["benih_map"] and raw.get("benih", 0) > 0:
                    raw["benih_map"]["CR01"] = raw["benih"]
        return raw
    return base


def gudang_terpakai_g(s):
    panen_g = sum(s.get("panen_map", {}).values())
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
        + panen_g
    )


def vitality_multiplier(s):
    """Vitality 0-100 affects manual efficiency 60%-110% (Addendum 11 §5)."""
    v = max(0, min(100, int(s.get("vitality", 100))))
    return 0.60 + (v / 100.0) * 0.50


def drain_vitality(s, amount):
    """Vitality drains ONLY on active manual actions, never offline, never causes death/asset loss."""
    s["vitality"] = max(5, int(s.get("vitality", 100)) - int(amount))


def push_celebration(s, ctype, title, subtitle, priority, kini):
    """Priority: God(5) > tier(4) > badge(3) > coin(2) > mission(1)."""
    ev_id = f"cel-{ctype}-{len(s['journal'])+1}-{int(kini)}"
    item = {"id": ev_id, "type": ctype, "title": title, "subtitle": subtitle, "priority": priority, "ts": round(kini, 1)}
    s["celebrations"].append(item)
    s["celebrations"].sort(key=lambda x: (-x["priority"], x["ts"]))
    s["celebrations"] = s["celebrations"][:12]
    s["journal"].append({"id": ev_id, "type": ctype, "title": title, "subtitle": subtitle, "ts": round(kini, 1)})
    s["journal"] = s["journal"][-60:]


def record_clean_day(s, kini):
    day = datetime.fromtimestamp(kini, tz=WIB).strftime("%Y-%m-%d")
    if s["b3_g"] == 0 and day not in s["stat"]["hari_bersih"]:
        s["stat"]["hari_bersih"].append(day)


def update_wealth_and_milestones(s, kini):
    # Estimate net worth = cash + depreciated owned machines
    m_val = 0
    for m in s.get("machines_owned", []):
        if m.get("starter"):
            continue
        info = get_machine(m["canonical_id"])
        if info:
            m_val += int(info["harga_gc"] * (m.get("condition", 100) / 100.0) * 0.6)
    net_worth = s["koin"] + m_val
    if net_worth > s.get("peak_wealth_gc", 0):
        s["peak_wealth_gc"] = net_worth
    earned = s["wallet"]["earned_gc"]
    for ms in EARNED_MILESTONES:
        if earned >= ms and ms not in s["milestones_claimed"]:
            s["milestones_claimed"].append(ms)
            push_celebration(s, "coin", f"Tonggak {ms:,} GC Diperoleh!", "Pencapaian hasil usaha murni (terpisah dari modal/sandbox).", 2, kini)


def active_tr_window(kini):
    """Return active TR01-TR05 mission for Asia/Jakarta time, plus 3-hour rotating fallback."""
    dt = datetime.fromtimestamp(kini, tz=WIB)
    h = dt.hour
    wd = dt.weekday()  # 5=Sat, 6=Sun
    day_key = dt.strftime("%Y-%m-%d")
    for m in TR_MISSIONS:
        if m["weekend"] and wd >= 5 and m["start_h"] <= h < m["end_h"]:
            return {**m, "window_key": f"{m['id']}:{day_key}", "fallback": False}
        if not m["weekend"] and m["start_h"] <= h < m["end_h"]:
            return {**m, "window_key": f"{m['id']}:{day_key}", "fallback": False}
    # 3-hour rotating alternative for busy players (no stacking, no punishment!)
    slot_3h = int(kini // (3 * 3600))
    alt = TR_MISSIONS[slot_3h % 4]
    return {**alt, "nama": f"{alt['nama']} (Jadwal Alternatif 3 Jam)", "window_key": f"ALT-{alt['id']}:{slot_3h}", "fallback": True}


def active_dynamic_event(kini):
    """Deterministic daily world/weather event (Addendum 11 + TECHNICAL_DESIGN_SYNC)."""
    day = datetime.fromtimestamp(kini, tz=WIB).strftime("%Y-%m-%d")
    seed = int.from_bytes(hashlib.sha256(f"tn-event:{day}".encode()).digest()[:4], "big")
    events = [
        {"id": "EV_CERAH", "nama": "Hari Cerah Nusantara", "efek": "Output panel surya +15% hari ini.", "solar_mult": 1.15, "hydro_mult": 1.0},
        {"id": "EV_HUJAN", "nama": "Hujan Tropis Ringan", "efek": "Debit mikrohidro +20%, kebun segar.", "solar_mult": 0.90, "hydro_mult": 1.20},
        {"id": "EV_BAKTI", "nama": "Gerakan Komunitas Hijau", "efek": "Suasana kota kondusif, kesadaran warga meningkat.", "solar_mult": 1.0, "hydro_mult": 1.0},
    ]
    return {**events[seed % len(events)], "day": day}


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


def buat_sampah(s, x, y, rng, zona):
    jenis = rng.choice(JENIS_UMUM)
    if zona == "dalam" and jenis == "baterai" and rng.random() < 0.5:
        jenis = "kantong"
    _, lo, hi = JENIS_SAMPAH[jenis]
    g_val = rng.randint(lo, hi) // 10 * 10
    s["sampah_seq"] += 1
    s["env_ledger_debit_g"] += g_val
    s["sampah_liar"].append({"id": f"s{s['sampah_seq']}", "jenis": jenis, "x": x, "y": y, "g": g_val, "zona": zona})


def sebar_sampah_awal(s, kini):
    rng = random.Random(f"awal:{kini:.0f}")
    for x, y in TITIK_DALAM:
        buat_sampah(s, x, y, rng, "dalam")
    for x, y in rng.sample(TITIK_LUAR, 12):
        buat_sampah(s, x, y, rng, "luar")
    s["sampah_slot"] = int(kini // SAMPAH_SLOT_DETIK)
    s["pohon_slot"] = int(kini // POHON_SLOT_DETIK)
    s["jalan_slot"] = int(kini // JALAN_SLOT_DETIK)
    s["sungai_slot"] = int(kini // SUNGAI_SLOT_DETIK)


def tambah_item(s, jenis, x, y, rng, kini, **extra):
    _, lo, hi = JENIS_SAMPAH[jenis]
    g_val = rng.randint(lo, hi) // 10 * 10
    s["sampah_seq"] += 1
    s["env_ledger_debit_g"] += g_val
    item = {"id": f"s{s['sampah_seq']}", "jenis": jenis, "x": int(x), "y": int(y), "g": g_val, "zona": "luar", "t": round(kini, 1)}
    item.update(extra)
    s["sampah_liar"].append(item)


def tumbuh_sampah(s, kini):
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


def jatuh_pohon(s, kini):
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
        for _ in range(8):
            x = rng.randrange(120, 1560, 10)
            y = road_y(x) - 48 if arah == "R" else road_y(x) + 68
            if all(abs(t["x"] - x) + abs(t["y"] - y) > 70 for t in s["sampah_liar"]):
                break
        else:
            continue
        tambah_item(s, rng.choice(isi), x, y, rng, kini if sl == slot else sl * JALAN_SLOT_DETIK, sumber="jalan", kendaraan=jenis_kend, arah=arah)
    s["jalan_slot"] = slot


def jatuh_sungai(s, kini):
    """Floating river trash: slot 75s, 50% chance, max 4, 90s transit; missed -> downstream backlog (conserved!)."""
    masih = []
    for ev in s.get("sampah_sungai", []):
        if kini >= ev["end_at"]:
            s["backlog_tpa_g"] += ev["g"]
        else:
            masih.append(ev)
    s["sampah_sungai"] = masih

    slot = int(kini // SUNGAI_SLOT_DETIK)
    if not s["diterima"] or slot <= s.get("sungai_slot", 0):
        return
    for sl in range(max(s.get("sungai_slot", 0) + 1, slot - 2), slot + 1):
        if len(s["sampah_sungai"]) >= SUNGAI_MAKS:
            break
        rng = random.Random(f"sungai:{sl}:{s['sampah_seq']}")
        if rng.random() > 0.50:
            continue
        jenis = rng.choice(JENIS_SUNGAI)
        _, lo, hi = JENIS_SAMPAH[jenis]
        g_val = rng.randint(lo, hi) // 10 * 10
        s["sampah_seq"] += 1
        s["env_ledger_debit_g"] += g_val
        start_t = kini if sl == slot else sl * SUNGAI_SLOT_DETIK
        s["sampah_sungai"].append({
            "id": f"riv{s['sampah_seq']}",
            "jenis": jenis,
            "g": g_val,
            "start_at": round(start_t, 1),
            "end_at": round(start_t + SUNGAI_LINTAS_DETIK, 1),
        })
    s["sungai_slot"] = slot


def settle_waktu(s, kini):
    if s["waktu"] <= 0:
        s["waktu"] = kini
    selang_raw = max(0.0, kini - s["waktu"])
    selang_cap = min(28800.0, selang_raw)  # max 8h lazy tick

    # 1. Garden plots (lazy tick)
    for pt in [s] + s["petak"]:
        if pt["ditanam"] and pt["detik"] > 0:
            pt["detik"] = max(0.0, pt["detik"] - selang_cap)

    # 2. Spawns (wild, tree, vehicle, floating river)
    tumbuh_sampah(s, kini)
    jatuh_pohon(s, kini)
    jatuh_kendaraan(s, kini)
    jatuh_sungai(s, kini)

    # 3. Expire rare boost & leases
    if s.get("rare_boost") and kini >= s["rare_boost"]["expires_at"]:
        s["rare_boost"] = None
    s["machines_leased"] = [ls for ls in s.get("machines_leased", []) if kini < ls["expires_at"]]

    # 4. Passive DRES renewable generation (solar / pico-hydro, capped to battery capacity, NO perpetual energy!)
    if s["diterima"] and selang_cap >= 10:
        ev = active_dynamic_event(kini)
        watts = 0
        for m in s.get("machines_owned", []):
            cid = m["canonical_id"]
            if cid == "DRE-001": watts += int(50 * ev["solar_mult"])
            elif cid == "DRE-002": watts += int(150 * ev["solar_mult"])
            elif cid == "DRE-003": watts += int(500 * ev["solar_mult"])
            elif cid == "DRE-004": watts += int(1000 * ev["solar_mult"])
            elif cid == "DRE-005": watts += int(3000 * ev["solar_mult"])
            elif cid == "DRE-030": watts += int(100 * ev["hydro_mult"])
        # Cap total DRES household-UMKM at 100 kW per freeze parameter
        watts = min(100_000, watts)
        if watts > 0:
            # Accelerated game clock (1s real ~ 1 min sim for energy preview -> watts * selang_cap / 60 Wh)
            gen_wh = int((watts * selang_cap) // 3600)
            if gen_wh > 0:
                en = s["energy"]
                space = max(0, en["battery_cap_wh"] - en["battery_wh"])
                stored = min(space, gen_wh)
                if stored > 0:
                    en["battery_wh"] += stored
                    en["battery_renew_wh"] += stored

    # 5. WCS job arrival
    if s["job"] and s["job"]["status"] == "in_transit" and kini >= s["job"]["tiba_pada"]:
        s["job"]["status"] = "arrived"

    # 6. DWE node accumulation (max 60 min catch-up)
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

    # 7. DLE expiry & UTC slot evaluation (§28)
    utc_day = datetime.fromtimestamp(kini, tz=timezone.utc).strftime("%Y-%m-%d")
    if s["dle_utc_day"] != utc_day:
        s["dle_utc_day"] = utc_day
        s["dle_daily_count"] = 0
        s["dle_daily_bonus_g"] = 0

    masih = []
    for ev in s["dle_events"]:
        if ev["status"] == "available" and kini >= ev["expires_at"]:
            s["backlog_tpa_g"] += ev["mass_g"]
            ev["status"] = "expired"
        if ev["status"] == "available":
            masih.append(ev)
    s["dle_events"] = masih

    slot_kini = int(kini // 180)
    if s["diterima"] and slot_kini > s["dle_cursor_slot"]:
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
                            "id": f"dle-{sl}-riv", "jenis": "npc_litter_river", "judul": "Kemasan di Tepi Sungai",
                            "pesan": "Seorang pejalan kaki membuang botol di tepi sungai. Bersihkan agar tidak hanyut!",
                            "anchor": "river_bank", "source_node": "permukiman", "fraksi": fr, "mass_g": got,
                            "status": "available", "expires_at": kini + 900,
                        })
                        s["dle_daily_count"] += 1
                else:
                    target = min(rng.randint(1000, 3000), sisa_cap)
                    fr, got = ambil_dari_node_g(s["nodes"]["pasar"]["stok"], target, ("organik",))
                    if got > 0:
                        s["dle_events"].append({
                            "id": f"dle-{sl}-veg", "jenis": "vegetable_spill", "judul": "Sayuran Tercecer di Bahu Jalan",
                            "pesan": "Mobil pengangkut sayur menjatuhkan muatan di depan gerbangmu. Manfaatkan organiknya!",
                            "anchor": "road_shoulder", "source_node": "pasar", "fraksi": fr, "mass_g": got,
                            "status": "available", "expires_at": kini + 900,
                        })
                        s["dle_daily_count"] += 1
        s["dle_cursor_slot"] = slot_kini

    s["waktu"] = max(s["waktu"], kini)


def buat_insiden_tutorial(s, kini):
    if s["dle_tutorial_done"] or len(s["dle_events"]) >= 3:
        return
    fr, got = ambil_dari_node_g(s["nodes"]["pasar"]["stok"], 2000, ("organik",))
    if got > 0:
        s["dle_events"].append({
            "id": "dle-tutorial-veg", "jenis": "vegetable_spill", "judul": "Sayuran Tercecer di Depan Gerbang",
            "pesan": "Ada sayuran tercecer di depan gerbangmu. Bersihkan jalan dan manfaatkan bahan organiknya.",
            "anchor": "road_shoulder", "source_node": "pasar", "fraksi": fr, "mass_g": got,
            "status": "available", "expires_at": kini + 900,
        })
        s["dle_daily_count"] += 1
        s["dle_tutorial_done"] = True


def hitung_gsg(s):
    """Gaia Sustainability Gate (GSG) for God tier — equal for household/modest and industrial paths."""
    st = s["stat"]
    en = s["energy"]
    pulih_kg = st["pulih_unik_g"] / 1000.0
    waste_kwh = en["waste_origin_used_wh"] / 1000.0
    days = len(st["hari_bersih"])
    checks = {
        "pulih_200kg": pulih_kg >= 200.0,
        "waste_energy_10kwh": waste_kwh >= 10.0,
        "clean_days_10": days >= 10,
        "mass_audit": st["neraca_valid"] >= 1,
        "energy_audit": st["audit_energi"] >= 1,
        "b3_safe": s["b3_g"] == 0,
    }
    return {"passed": all(checks.values()), "checks": checks, "pulih_kg": round(pulih_kg, 2), "waste_kwh": round(waste_kwh, 2), "clean_days": days}


def evaluasi_chosen_provisional(s):
    """Internal provisional candidate evaluation ONLY. NEVER awards Gaia's Chosen automatically!"""
    gsg = hitung_gsg(s)
    has_f3_plus = any((get_machine(m["canonical_id"]) or {}).get("f_stage", 1) >= 3 for m in s.get("machines_owned", []))
    en = s["energy"]
    has_household_wte = en["waste_origin_used_wh"] > 0
    has_renewable = en["renewable_used_wh"] > 0
    wealth_ok = s.get("peak_wealth_gc", 0) <= 1_000_000_000
    eligible = gsg["passed"] and (not has_f3_plus) and wealth_ok and has_household_wte and has_renewable
    return {
        "status": "PROVISIONAL_EVALUATION_ONLY",
        "final_selection_active": False,
        "candidate_provisional": eligible,
        "note": "Evaluasi internal sementara. Seleksi akhir Gaia's Chosen sengaja belum diaktifkan (menunggu keputusan pemilik).",
    }


def daftar_gt(s):
    st = s["stat"]
    en = s["energy"]
    pulih_kg = st["pulih_unik_g"] // 1000
    waste_kwh = en["waste_origin_used_wh"] // 1000
    days = len(st["hari_bersih"])
    gsg = hitung_gsg(s)
    claimed = set(s.get("gt_claimed", []))

    defs = [
        ("GT01", "Awaken", "BT01", 0, "Terima panggilan Gaia & selesaikan intro lahan.", bool(s["diterima"] and s["intro_selesai"])),
        ("GT02", "Seeker", "BT02", 5000, "Pungut 5 sampah, jual 1 lot sah, pulihkan 2 kg.", st["pungut"] >= 5 and st["lot_jual_sah"] >= 1 and pulih_kg >= 2),
        ("GT03", "Sorter", "BT03", 15000, "Pilah 10 kg campuran, 3 fraksi, 1 audit neraca valid.", st["pilah_g"] >= 10000 and len(st["fraksi_terpilah"]) >= 3 and st["neraca_valid"] >= 1),
        ("GT04", "Recycler", "BT04", 40000, "Pulihkan 25 kg, 2 resep berbeda, panen pertama.", pulih_kg >= 25 and len(st["resep_dipakai"]) >= 2 and st["panen"] >= 1),
        ("GT05", "Guardian", "BT05", 100000, "Pulihkan 50 kg, 5 bersih sungai, 3 hari operasi bersih.", pulih_kg >= 50 and (st["sungai"] + st["sungai_apung"]) >= 5 and days >= 3),
        ("GT06", "Ascendant", "BT06", 250000, "Pulihkan 100 kg, 1 kWh energi waste-origin, 1 audit energi.", pulih_kg >= 100 and waste_kwh >= 1 and st["audit_energi"] >= 1),
        ("GT07", "Titan", "BT07", 500000, "Pulihkan 150 kg, 5 kWh waste-origin, 7 hari bersih, B3 aman.", pulih_kg >= 150 and waste_kwh >= 5 and days >= 7 and s["b3_g"] == 0),
        ("GT08", "Archon", "BT08", 1000000, "Pulihkan 200 kg, 10 kWh waste-origin, 10 hari bersih, audit neraca.", pulih_kg >= 200 and waste_kwh >= 10 and days >= 10 and st["neraca_valid"] >= 1),
        ("GT09", "God", "BT09", 2500000, "Lulus Gaia Sustainability Gate (GSG) — tanpa syarat kekayaan/pabrik besar.", gsg["passed"]),
    ]
    out = []
    prev_claimed = True
    for gid, tier, badge, gc, desc, met in defs:
        is_claimed = gid in claimed
        can_claim = (not is_claimed) and prev_claimed and met
        out.append({"id": gid, "tier": tier, "badge": badge, "grant_gc": gc, "desc": desc, "met": met, "claimed": is_claimed, "can_claim": can_claim})
        prev_claimed = is_claimed
    return out


def daftar_pr(s):
    st = s["stat"]
    claimed = set(s.get("pr_claimed", []))
    placed = sum(1 for m in s.get("machines_owned", []) if m.get("slot"))
    defs = [
        ("PR01", "Arus Pertama", "River Catcher", 500, "Ambil 1 sampah sungai terapung dengan aman.", st["sungai_apung"] >= 1),
        ("PR02", "Sungai Lestari", "Flow Guardian", 2000, "Tangani 10 lot sampah sungai terapung.", st["sungai_apung"] >= 10),
        ("PR03", "Angkut Tepat Waktu", "Green Carrier", 2500, "Selesaikan 5 kontrak angkut sesuai jadwal.", st["angkut_tepat"] >= 5),
        ("PR04", "Pangan Sendiri", "Food Keeper", 3000, "Panen 5 varietas tanaman berbeda.", len(st["varietas_panen"]) >= 5),
        ("PR05", "Kebun Keajaiban", "Rare Gardener", 2000, "Panen 1 varietas tanaman langka.", st["panen_langka"] >= 1),
        ("PR06", "Makan Beragam", "Balanced Life", 1000, "Konsumsi 3 kelompok pangan berbeda dalam 1 hari.", len(s.get("food_groups_today", [])) >= 3),
        ("PR07", "Usaha Mandiri", "Circular Trader", 3000, "10 penjualan produksi sendiri dengan laba positif.", st["lot_jual_laba"] >= 10),
        ("PR08", "Daya Campuran", "Hybrid Keeper", 4000, "2 sumber energi berbeda menyuplai beban sah.", len(st["energi_sumber_dipakai"]) >= 2),
        ("PR09", "Tata Lahan", "Eco Builder", 1000, "Tempatkan 3 alat sah tanpa tumpang tindih.", placed >= 3),
        ("PR10", "Tidak Terbuang", "Matter Keeper", 2000, "Catat 10 batch neraca massa valid.", st["neraca_valid"] >= 10),
    ]
    return [{"id": pid, "judul": j, "badge": b, "grant_gc": gc, "desc": d, "met": met, "claimed": pid in claimed, "can_claim": (pid not in claimed) and met} for pid, j, b, gc, d, met in defs]


def daftar_pencapaian(s):
    """Preserve all 8 §34 legacy badges; Saudagar Hijau uses operating_profit_gc >= 2000 for realistic_v1."""
    st = s["stat"]
    dalam_sisa = sum(1 for t in s["sampah_liar"] if t["zona"] == "dalam")
    saudagar_val = s["wallet"]["operating_profit_gc"] if s.get("economy_mode") == "realistic_v1" else s["koin"]
    saudagar_desc = "Raih laba operasi kumulatif 2.000 GC." if s.get("economy_mode") == "realistic_v1" else "Kumpulkan 2.000 Gaia Coin."
    data = [
        ("pungut", 1, "Tangan Pertama", "Pungut sampah pertamamu.", st["pungut"], 1),
        ("pilah", 2, "Pemilah Andal", "Pilah 10 kg bahan campuran di Area Pilah.", st["pilah_g"] // 1000, 10),
        ("kompos", 3, "Penyubur Tanah", "Buat kompos pertamamu.", st["kompos"], 1),
        ("panen", 4, "Panen Perdana", "Panen sayur dari kebunmu.", st["panen"], 1),
        ("saudagar", 5, "Saudagar Hijau", saudagar_desc, min(max(0, saudagar_val), 2000), 2000),
        ("sungai", 6, "Penjaga Sungai", "Bersihkan 5 sampah di tepi/aliran sungai.", st["sungai"] + st["sungai_apung"], 5),
        ("petani", 7, "Petani Kota", "Miliki petak tanam tambahan.", len(s["petak"]), 1),
        ("bersih", 8, "Lahan Bersih", "Bersihkan semua sampah di dalam pagar.", len(TITIK_DALAM) - dalam_sisa if s["diterima"] else 0, len(TITIK_DALAM)),
    ]
    return [{"id": i, "ikon": f"badges_{ik}.png", "judul": j, "desk": d, "nilai": min(n, t), "target": t, "ok": n >= t} for i, ik, j, d, n, t in data]


def petak_dari(s, payload):
    i = int(payload.get("petak", 0) or 0)
    if i == 0:
        return s
    perlu(1 <= i <= len(s["petak"]), "Petak tanam tidak ditemukan.")
    return s["petak"][i - 1]


def aksi(s, payload, kini, cfg=None):
    cfg = cfg or DEFAULT_CONFIG
    nama = payload.get("aksi", "")
    wib_day = datetime.fromtimestamp(kini, tz=WIB).strftime("%Y-%m-%d")
    wib_week = datetime.fromtimestamp(kini, tz=WIB).strftime("%Y-W%W")

    if nama == "reset_sim":
        starter = int(payload.get("starter_gc") or cfg.get("starter_gc", 1_000_000))
        if starter not in (100_000, 1_000_000):
            starter = cfg.get("starter_gc", 1_000_000)
        baru = state_awal(starter)
        baru["waktu"] = kini
        s.clear()
        s.update(baru)
        return f"Simulasi lokal direset ke Realistic_v1 (modal {starter:,} GC)."

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

    if nama == "ganti_kota":
        kota = payload.get("kota", "")
        perlu(kota in KOTA_SAH, "Pilih kota yang tersedia di daftar.")
        s["kota"] = kota
        return f"Lokasi lahan diperbarui ke {kota} (mode lokal)."

    if nama == "intro_selesai":
        s["intro_selesai"] = True
        return "Selamat bekerja, Penjaga Bumi. Bersihkan lahanmu!"

    if nama == "tutup_selebrasi":
        cid = str(payload.get("id", ""))
        if cid:
            s["celebrations"] = [c for c in s["celebrations"] if c["id"] != cid]
        else:
            s["celebrations"] = []
        return "Selebrasi ditutup."

    if nama == "update_profil_publik":
        s["public_profile"]["opt_in"] = bool(payload.get("opt_in", False))
        s["public_profile"]["quote"] = str(payload.get("quote", ""))[:120]
        return "Preferensi profil lokal diperbarui."

    # ---- Pickup wild litter
    if nama == "pungut":
        sid = str(payload.get("id", ""))
        item = next((t for t in s["sampah_liar"] if t["id"] == sid), None)
        perlu(item is not None, "Sampah itu sudah dipungut.")
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= item["g"], "Gudang penuh — olah atau jual isi gudang terlebih dahulu.")
        kunci = JENIS_SAMPAH[item["jenis"]][0]
        s[kunci] += item["g"]
        if kunci == "campuran_g":
            bg = bagi_g(item["g"], {"organik": 50, "plastik": 18, "kertas": 10, "logam_kaca": 7, "residu": 14, "B3": 1})
            for f in FRAKSI:
                s["campuran_fraksi"][f] += bg[f]
        s["total_masuk_g"] += item["g"]
        s["sampah_liar"].remove(item)
        # Service compensation with daily cap (2.000 GC/day)
        if s["pickup_day"] != wib_day:
            s["pickup_day"] = wib_day
            s["pickup_daily_gc"] = 0
        reward_gc = min(cfg["pickup_reward_gc"], max(0, cfg["pickup_daily_cap_gc"] - s["pickup_daily_gc"]))
        s["pickup_daily_gc"] += reward_gc
        s["koin"] += reward_gc
        s["wallet"]["earned_gc"] += reward_gc
        s["wallet"]["operating_profit_gc"] += reward_gc
        s["poin"] += 3
        s["stat"]["pungut"] += 1
        if item["zona"] == "dalam":
            s["stat"]["pungut_dalam"] += 1
        if (item["x"], item["y"]) in TITIK_SUNGAI:
            s["stat"]["sungai"] += 1
        drain_vitality(s, 1)
        record_clean_day(s, kini)
        update_wealth_and_milestones(s, kini)
        tujuan = "Area Pilah (perlu dipilah)" if kunci == "campuran_g" else "gudang"
        return f"{LABEL_SAMPAH[item['jenis']]} {item['g']} g dipungut → {tujuan} (+{reward_gc} GC kompensasi)."

    # ---- Pickup floating river trash (safe bank access, no B3)
    if nama == "pungut_sungai":
        rid = str(payload.get("id", ""))
        ev = next((e for e in s.get("sampah_sungai", []) if e["id"] == rid), None)
        perlu(ev is not None, "Sampah sungai sudah hanyut ke hilir atau sudah diambil.")
        perlu(kini < ev["end_at"], "Sampah sudah melewati tepi sungai dan tercatat di backlog hilir.")
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= ev["g"], "Gudang penuh — kosongkan ruang gudang terlebih dahulu.")
        kunci = JENIS_SAMPAH[ev["jenis"]][0]
        s[kunci] += ev["g"]
        if kunci == "campuran_g":
            bg = bagi_g(ev["g"], {"organik": 20, "plastik": 50, "kertas": 10, "logam_kaca": 10, "residu": 10, "B3": 0})
            for f in FRAKSI:
                s["campuran_fraksi"][f] += bg[f]
        s["total_masuk_g"] += ev["g"]
        s["sampah_sungai"].remove(ev)
        if s["pickup_day"] != wib_day:
            s["pickup_day"] = wib_day
            s["pickup_daily_gc"] = 0
        reward_gc = min(cfg["pickup_reward_gc"], max(0, cfg["pickup_daily_cap_gc"] - s["pickup_daily_gc"]))
        s["pickup_daily_gc"] += reward_gc
        s["koin"] += reward_gc
        s["wallet"]["earned_gc"] += reward_gc
        s["wallet"]["operating_profit_gc"] += reward_gc
        s["stat"]["sungai_apung"] += 1
        s["stat"]["pungut"] += 1
        s["poin"] += 5
        drain_vitality(s, 1)
        update_wealth_and_milestones(s, kini)
        return f"{LABEL_SAMPAH[ev['jenis']]} ({ev['g']} g) diamankan dari tepi sungai (+{reward_gc} GC)."

    # ---- Land expansion (Realistic_v1 prices)
    if nama == "beli_petak":
        n = len(s["petak"])
        perlu(n < len(HARGA_PETAK_REALISTIS), "Semua petak tanam tambahan sudah dimiliki.")
        harga = HARGA_PETAK_REALISTIS[n]
        perlu(s["koin"] >= harga, f"Petak tanam baru seharga {harga:,} GC. Saldo belum mencukupi.")
        s["koin"] -= harga
        s["wallet"]["expenses_gc"] += harga
        s["petak"].append({"ditanam": False, "tanaman": "", "tanaman_id": "", "detik": 0.0, "dipupuk": False})
        return f"Petak tanam ke-{n + 2} dibangun di sisi kanan lahan (-{harga:,} GC)."

    if nama == "tambah_gudang":
        n = s["gudang_upgrade"]
        perlu(n < len(HARGA_GUDANG_REALISTIS), "Gudang sudah diperluas maksimal.")
        harga = HARGA_GUDANG_REALISTIS[n]
        perlu(s["koin"] >= harga, f"Perluasan gudang seharga {harga:,} GC.")
        s["koin"] -= harga
        s["wallet"]["expenses_gc"] += harga
        s["gudang_upgrade"] += 1
        s["gudang_kap_g"] += 250_000
        return f"Gudang diperluas +250 kg (-{harga:,} GC)."

    # ---- Realistic Transport (WCS + 5 Nodes + TR01-05)
    if nama in ("angkut_node", "angkut"):
        perlu(s["job"] is None, "Gerobak sedang beroperasi. Terima kargo terlebih dahulu.")
        node_id = payload.get("node", "pasar")
        perlu(node_id in NODE_TEMPLATE, "Sumber sampah tidak dikenal.")
        tpl = NODE_TEMPLATE[node_id]
        muat_g = int(payload.get("gram", 10_000))
        kg = muat_g // 1000
        perlu(tpl["min_kg"] <= kg <= tpl["max_kg"], f"Kapasitas gerobak MCH-002 untuk {tpl['nama']}: {tpl['min_kg']}–{tpl['max_kg']} kg.")
        biaya = int(round(tpl["fee_tetap"] + tpl["jarak_km"] * tpl["gc_per_km"] + kg * tpl["handling_per_kg"]))
        kompensasi = int(kg * tpl["kompensasi_per_kg"])
        perlu(s["koin"] >= biaya, f"Biaya angkut {biaya:,} GC tidak mencukupi. Pungut sampah sekitar atau jual stok untuk recovery kas.")
        ns = s["nodes"][node_id]["stok"]
        tot_node = sum(ns.values())
        perlu(tot_node >= muat_g, f"Stok {tpl['nama']} belum mencukupi ({tot_node // 1000} kg tersedia).")
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= muat_g, "Ruang gudang tidak cukup untuk menerima muatan ini.")
        s["koin"] -= biaya
        s["wallet"]["expenses_gc"] += biaya
        s["wallet"]["operating_profit_gc"] -= biaya
        diambil = {f: 0 for f in FRAKSI}
        sisa = muat_g
        for f in FRAKSI:
            if f == "B3":
                continue  # B3 never transported via mixed starter cart!
            porsi = (ns[f] * muat_g) // tot_node
            pot = min(ns[f], porsi, sisa)
            ns[f] -= pot
            diambil[f] += pot
            sisa -= pot
        for f in FRAKSI:
            if f == "B3" or sisa <= 0:
                continue
            pot = min(ns[f], sisa)
            ns[f] -= pot
            diambil[f] += pot
            sisa -= pot
        tr_win = active_tr_window(kini)
        tr_match = tr_win["window_key"] if (tr_win["node"] == node_id and kg >= tr_win["min_kg"] and tr_win["window_key"] not in s["tr_claimed_windows"]) else None
        eta = int(payload.get("_test_eta", tpl["eta_detik"])) if "_test_eta" in payload else tpl["eta_detik"]
        s["job"] = {
            "node": node_id, "nama_node": tpl["nama"], "muat_g": muat_g, "fraksi": diambil,
            "biaya_gc": biaya, "kompensasi_gc": kompensasi, "tr_window": tr_match,
            "tr_bonus_gc": tr_win["bonus_gc"] if tr_match else 0,
            "status": "in_transit", "tiba_pada": kini + eta, "deadline": kini + eta + 600,
        }
        return f"Gerobak MCH-002 ke {tpl['nama']} ({kg} kg, biaya {biaya:,} GC, kompensasi jasa {kompensasi:,} GC). Tiba dalam {eta} dtk."

    if nama == "terima_kargo":
        perlu(s["job"] is not None, "Tidak ada kargo aktif.")
        perlu(s["job"]["status"] == "arrived", "Gerobak masih dalam perjalanan.")
        muat_g = s["job"]["muat_g"]
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= muat_g, "Gudang penuh — kosongkan ruang terlebih dahulu.")
        # Preserve ACTUAL node fraction composition!
        s["campuran_g"] += muat_g
        for f in FRAKSI:
            s["campuran_fraksi"][f] += s["job"]["fraksi"].get(f, 0)
        s["total_masuk_g"] += muat_g
        komp = s["job"].get("kompensasi_gc", 0)
        on_time = kini <= s["job"].get("deadline", kini + 1)
        bonus_msg = ""
        if on_time:
            s["koin"] += komp
            s["wallet"]["earned_gc"] += komp
            s["wallet"]["operating_profit_gc"] += komp
            s["stat"]["angkut_tepat"] += 1
            trw = s["job"].get("tr_window")
            trb = s["job"].get("tr_bonus_gc", 0)
            if trw and trb > 0 and trw not in s["tr_claimed_windows"]:
                s["tr_claimed_windows"].append(trw)
                s["koin"] += trb
                s["wallet"]["grant_gc"] += trb
                bonus_msg = f" + bonus misi berkala {trb:,} GC!"
        asal = s["job"]["nama_node"]
        s["job"] = None
        update_wealth_and_milestones(s, kini)
        return f"Kargo {muat_g // 1000} kg dari {asal} diterima (+{komp:,} GC kompensasi jasa{bonus_msg})."

    # ---- DLE claim (§28)
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
        for f, g_val in ev["fraksi"].items():
            if f == "organik": s["organik_g"] += g_val
            elif f == "plastik": s["plastik_g"] += g_val
            elif f == "logam_kaca": s["logam_kaca_g"] += g_val
            else:
                s["campuran_g"] += g_val
                s["campuran_fraksi"][f] += g_val
        s["total_masuk_g"] += ev["mass_g"]
        s["dle_daily_bonus_g"] += ev["mass_g"]
        if ev["anchor"] == "river_bank":
            s["stat"]["sungai"] += 1
        s["poin"] += 15
        drain_vitality(s, 2)
        return f"+{ev['mass_g']} g material dari {ev['judul']} masuk gudang (+15 Poin Misi)."

    # ---- Sorting 6 fractions (uses REAL accumulated node composition!)
    if nama == "pilah":
        perlu(s["campuran_g"] >= 1000, "Belum ada bahan campuran di area pilah (minimal 1 kg).")
        batch_g = min(10_000, s["campuran_g"])
        tot_cf = sum(s["campuran_fraksi"].values())
        if tot_cf > 0:
            bagian = bagi_g(batch_g, s["campuran_fraksi"])
            for f in FRAKSI:
                s["campuran_fraksi"][f] = max(0, s["campuran_fraksi"][f] - bagian[f])
        else:
            bagian = bagi_g(batch_g, {"organik": 50, "plastik": 18, "kertas": 10, "logam_kaca": 7, "residu": 14, "B3": 1})
        s["campuran_g"] -= batch_g
        s["stat"]["pilah_g"] += batch_g
        for f, col in (("organik", "organik_g"), ("plastik", "plastik_g"), ("kertas", "kertas_g"), ("logam_kaca", "logam_kaca_g"), ("residu", "residu_g"), ("B3", "b3_g")):
            s[col] += bagian[f]
            if bagian[f] > 0 and f not in s["stat"]["fraksi_terpilah"]:
                s["stat"]["fraksi_terpilah"].append(f)
        s["stat"]["neraca_valid"] += 1
        drain_vitality(s, 2)
        record_clean_day(s, kini)
        return f"Dipilah {batch_g} g sesuai komposisi asal → {bagian['organik']}g organik, {bagian['plastik']}g plastik, {bagian['kertas']}g kertas, {bagian['logam_kaca']}g logam/kaca, {bagian['residu']}g residu, {bagian['B3']}g B3."

    # ---- Processing: Compost, Plastic Pellet, Plastic Pot
    if nama in ("olah", "olah_kompos"):
        perlu(s["organik_g"] >= 2000, "Perlu minimal 2 kg bahan organik.")
        s["organik_g"] -= 2000
        # Manual efficiency affected gently by vitality on bonus speed/points, mass strictly conserved!
        s["kompos_g"] += 1000
        s["uap_terkendali_g"] += 900
        s["residu_g"] += 100
        s["stat"]["kompos"] += 1
        s["stat"]["pulih_unik_g"] += 1000
        s["stat"]["neraca_valid"] += 1
        if "kompos" not in s["stat"]["resep_dipakai"]:
            s["stat"]["resep_dipakai"].append("kompos")
        s["poin"] += int(round(40 * vitality_multiplier(s)))
        s["karma"] = max(0.0, round(s["karma"] - 0.1, 2))
        drain_vitality(s, 2)
        record_clean_day(s, kini)
        return "2.000 g organik → 1.000 g kompos, 900 g uap/air terkendali, 100 g residu (neraca valid)."

    if nama in ("daur", "kreasi"):
        perlu(s["plastik_g"] >= 1000, "Perlu minimal 1 kg plastik terpilah.")
        s["plastik_g"] -= 1000
        target = "pot_g" if nama == "kreasi" else "pelet_g"
        s[target] += 850
        s["uap_terkendali_g"] += 100
        s["residu_g"] += 50
        s["stat"][nama] = s["stat"].get(nama, 0) + 1
        s["stat"]["pulih_unik_g"] += 850
        s["stat"]["neraca_valid"] += 1
        if nama not in s["stat"]["resep_dipakai"]:
            s["stat"]["resep_dipakai"].append(nama)
        s["poin"] += int(round(60 * vitality_multiplier(s)))
        s["karma"] = max(0.0, round(s["karma"] - 0.1, 2))
        drain_vitality(s, 2)
        record_clean_day(s, kini)
        label = "pot daur ulang" if nama == "kreasi" else "pelet plastik"
        return f"1.000 g plastik → 850 g {label}, 100 g terkendali, 50 g residu (neraca valid)."

    # ---- B3 licensed handover (D03)
    if nama == "serah_b3":
        perlu(s["b3_g"] >= 10, "Belum ada fraksi B3 untuk diserahkan.")
        jml = s["b3_g"]
        s["b3_g"] = 0
        s["b3_serah_g"] += jml
        s["stat"]["neraca_valid"] += 1
        s["poin"] += max(10, (jml * 8) // 100)
        record_clean_day(s, kini)
        return f"{jml} g B3 diserahkan ke pengolah berizin (aman, tidak masuk pengolahan umum)."

    # ---- Formal Mass Balance Audit (for GT03/GT08/PR10)
    if nama == "audit_neraca":
        s["stat"]["neraca_valid"] += 1
        record_clean_day(s, kini)
        return "Audit Neraca Massa selesai: seluruh gram masuk, olahan, uap terkendali, B3, dan backlog tercatat seimbang."

    # ---- Household WtE & DRES Energy Center (strict Wh provenance, no double count!)
    if nama == "olah_biogas":
        has_digester = any(m["canonical_id"] == "WTE-002" for m in s["machines_owned"]) or any(l["canonical_id"] == "WTE-002" for l in s["machines_leased"])
        partner_fee = 0 if has_digester else 2500
        perlu(s["organik_g"] >= 5000, "Perlu minimal 5 kg bahan organik untuk digester biogas.")
        perlu(s["koin"] >= partner_fee, f"Biaya akses mitra digester biogas {partner_fee:,} GC tidak mencukupi.")
        if partner_fee > 0:
            s["koin"] -= partner_fee
            s["wallet"]["expenses_gc"] += partner_fee
            s["wallet"]["operating_profit_gc"] -= partner_fee
        s["organik_g"] -= 5000
        # 5 kg organic -> 1.5 kg digestat/kompos + 3.2 kg gas/air terkendali + 300 g residu + 1.25 kWh waste-origin potential
        s["kompos_g"] += 1500
        s["uap_terkendali_g"] += 3200
        s["residu_g"] += 300
        s["energy"]["biogas_m3_x100"] += 50  # 0.50 m3 biogas
        s["stat"]["biogas"] += 1
        s["stat"]["pulih_unik_g"] += 1500
        s["stat"]["neraca_valid"] += 1
        if "biogas" not in s["stat"]["resep_dipakai"]:
            s["stat"]["resep_dipakai"].append("biogas")
        record_clean_day(s, kini)
        return f"5 kg organik → 0,50 m³ biogas + 1,5 kg digestat kompos" + (f" (akses mitra -{partner_fee:,} GC)." if partner_fee else " (digester milik sendiri).")

    if nama == "jalankan_energi":
        # Convert stored biogas into net waste-origin electricity (Wh) OR discharge renewable battery to supply yard load
        sumber = payload.get("sumber", "biogas")
        en = s["energy"]
        if sumber == "biogas":
            perlu(en["biogas_m3_x100"] >= 50, "Belum ada stok biogas (minimal 0,50 m³). Olah organik di Digester Biogas dahulu.")
            has_gen = any(m["canonical_id"] == "WTE-015" for m in s["machines_owned"]) or any(l["canonical_id"] == "WTE-015" for l in s["machines_leased"])
            fee = 0 if has_gen else 2000  # affordable micro-genset partner access for household path
            perlu(s["koin"] >= fee, f"Biaya sewa pakai genset biogas mitra {fee:,} GC tidak cukup.")
            if fee:
                s["koin"] -= fee
                s["wallet"]["expenses_gc"] += fee
            en["biogas_m3_x100"] -= 50
            # Net 1.200 Wh (1.2 kWh) waste-origin electricity used directly for yard load (counted ONCE!)
            en["waste_origin_used_wh"] += 1200
            if "waste_biogas" not in s["stat"]["energi_sumber_dipakai"]:
                s["stat"]["energi_sumber_dipakai"].append("waste_biogas")
            return f"1,20 kWh listrik net waste-origin (biogas) menyuplai beban lahan" + (f" (mitra -{fee:,} GC)." if fee else ".")
        elif sumber == "renewable":
            perlu(en["battery_renew_wh"] >= 200, "Muatan baterai energi terbarukan minimal 200 Wh. Pasang Solar Kit/PLTS atau tunggu pengisian.")
            gross = en["battery_renew_wh"]
            loss = gross // 10  # 10% battery round-trip loss
            net = gross - loss
            en["battery_wh"] = max(0, en["battery_wh"] - gross)
            en["battery_renew_wh"] = 0
            en["battery_loss_wh"] += loss
            en["renewable_used_wh"] += net
            if "renewable_dres" not in s["stat"]["energi_sumber_dipakai"]:
                s["stat"]["energi_sumber_dipakai"].append("renewable_dres")
            return f"{net/1000:.2f} kWh listrik terbarukan disalurkan ke beban lahan (rugi baterai {loss} Wh tercatat)."
        raise ValueError("Sumber energi harus 'biogas' atau 'renewable'.")

    if nama == "audit_energi":
        en = s["energy"]
        perlu(en["waste_origin_used_wh"] > 0 or en["renewable_used_wh"] > 0, "Gunakan minimal 1 sumber energi terlebih dahulu sebelum audit energi.")
        en["last_audit_ts"] = round(kini, 1)
        s["stat"]["audit_energi"] += 1
        return f"Audit energi tercatat: {en['waste_origin_used_wh']/1000:.2f} kWh waste-origin, {en['renewable_used_wh']/1000:.2f} kWh terbarukan, rugi baterai {en['battery_loss_wh']} Wh."

    # ---- 15-Crop Garden & Vitality
    if nama in ("beli", "beli_langka", "beli_benih"):
        cid = payload.get("crop_id") or ("CR11" if nama == "beli_langka" else "CR01")
        crop = get_crop(cid)
        perlu(crop is not None, "Varietas benih tidak dikenal.")
        qty = max(1, min(10, int(payload.get("qty", 1) or 1)))
        if crop["rare"]:
            perlu(s["misi"] or s["stat"]["panen"] >= 1, "Selesaikan panen berpupuk pertama (Misi Siklus Gaia) untuk membuka benih langka.")
            if s["rare_seed_week"] != wib_week:
                s["rare_seed_week"] = wib_week
                s["rare_seed_bought"] = {}
            bought = s["rare_seed_bought"].get(cid, 0)
            perlu(bought + qty <= 1, f"Stok benih langka {crop['nama']} dibatasi maks 1 benih/minggu (anti-arbitrase).")
            s["rare_seed_bought"][cid] = bought + qty
        harga = crop["benih_gc"] * qty
        perlu(s["koin"] >= harga, f"Harga {qty} benih {crop['nama']} adalah {harga:,} GC.")
        s["koin"] -= harga
        s["wallet"]["expenses_gc"] += harga
        s["benih_map"][cid] = s["benih_map"].get(cid, 0) + qty
        s["benih"] = sum(v for k, v in s["benih_map"].items() if not get_crop(k)["rare"])
        s["stok_langka"] = sum(v for k, v in s["benih_map"].items() if get_crop(k)["rare"])
        return f"Membeli {qty} benih {crop['nama']} (-{harga:,} GC)."

    if nama in ("tanam", "tanam_langka", "tanam_crop"):
        pt = petak_dari(s, payload)
        perlu(not pt["ditanam"], "Petak sudah terisi tanaman.")
        cid = payload.get("crop_id")
        if not cid:
            if nama == "tanam_langka":
                cid = next((k for k, v in s["benih_map"].items() if v > 0 and get_crop(k)["rare"]), "CR11")
            else:
                cid = next((k for k, v in s["benih_map"].items() if v > 0 and not get_crop(k)["rare"]), "CR01")
        crop = get_crop(cid)
        perlu(crop is not None and s["benih_map"].get(cid, 0) > 0, f"Stok benih {crop['nama'] if crop else cid} kosong.")
        s["benih_map"][cid] -= 1
        s["benih"] = sum(v for k, v in s["benih_map"].items() if not get_crop(k)["rare"])
        s["stok_langka"] = sum(v for k, v in s["benih_map"].items() if get_crop(k)["rare"])
        pt.update(ditanam=True, tanaman=crop["nama"], tanaman_id=cid, detik=float(crop["detik"]), dipupuk=False)
        drain_vitality(s, 1)
        return f"Menanam {crop['nama']} (matang dalam {crop['detik']} detik uji)."

    if nama == "pupuk":
        pt = petak_dari(s, payload)
        perlu(pt["ditanam"] and pt["detik"] > 0 and not pt["dipupuk"] and s["kompos_g"] >= 1000,
              "Perlu tanaman tumbuh dan 1 kg kompos (satu dosis per siklus).")
        s["kompos_g"] -= 1000
        s["dipakai_kebun_g"] += 1000
        pt["detik"] = round(pt["detik"] * 0.75, 2)
        pt["dipupuk"] = True
        return "1 kg kompos dipakai di kebun (-25% sisa waktu; tercatat di Neraca Massa, tanpa kredit lingkungan ganda)."

    if nama == "panen":
        pt = petak_dari(s, payload)
        perlu(pt["ditanam"] and pt["detik"] <= 0, "Tanaman belum siap dipanen.")
        cid = pt.get("tanaman_id") or "CR01"
        crop = get_crop(cid) or get_crop("CR01")
        ruang = s["gudang_kap_g"] - gudang_terpakai_g(s)
        perlu(ruang >= crop["hasil_g"], "Gudang penuh — kosongkan ruang sebelum panen.")
        s["panen_map"][cid] = s["panen_map"].get(cid, 0) + crop["hasil_g"]
        s["biomassa_panen_g"] += crop["hasil_g"]
        s["panen_langka" if crop["rare"] else "panen"] += 1
        s["stat"]["panen"] += 1
        if crop["rare"]:
            s["stat"]["panen_langka"] += 1
        if cid not in s["stat"]["varietas_panen"]:
            s["stat"]["varietas_panen"].append(cid)
        extra = ""
        if pt["dipupuk"] and not s["misi"]:
            s["misi"] = True
            s["varietas"] = "Romanesco"
            s["benih_map"]["CR11"] = s["benih_map"].get("CR11", 0) + 1
            s["stok_langka"] = sum(v for k, v in s["benih_map"].items() if get_crop(k)["rare"])
            extra = " Misi Siklus Pertama Gaia selesai! Benih langka Romanesco terbuka."
        pt.update(ditanam=False, tanaman="", tanaman_id="", detik=0.0, dipupuk=False)
        drain_vitality(s, 1)
        return f"Panen {crop['hasil_g']} g {crop['nama']} masuk gudang.{extra}"

    # ---- Food & Vitality Consumption
    if nama == "beli_pangan":
        fid = payload.get("food_id", "FD_AIR")
        qty = max(1, min(10, int(payload.get("qty", 1) or 1)))
        food = get_food(fid)
        perlu(food is not None, "Bahan pangan NPC tidak dikenal.")
        harga = food["harga_gc"] * qty
        perlu(s["koin"] >= harga, f"Biaya {qty} {food['unit']} {food['nama']} ({harga:,} GC) melebihi saldo.")
        s["koin"] -= harga
        s["wallet"]["expenses_gc"] += harga
        s["pangan_map"][fid] = s["pangan_map"].get(fid, 0) + qty
        return f"Membeli {qty} {food['unit']} {food['nama']} (-{harga:,} GC)."

    if nama == "makan":
        item_id = payload.get("item_id", "")
        if s["food_groups_day"] != wib_day:
            s["food_groups_day"] = wib_day
            s["food_groups_today"] = []
        food = get_food(item_id)
        if food:
            perlu(s["pangan_map"].get(item_id, 0) >= 1, f"Stok {food['nama']} kosong. Beli di Pasar Sehat dahulu.")
            s["pangan_map"][item_id] -= 1
            s["vitality"] = min(100, s["vitality"] + food["vitality"])
            if food["group"] not in s["food_groups_today"]:
                s["food_groups_today"].append(food["group"])
            return f"Konsumsi {food['nama']} (+{food['vitality']} Vitalitas → {s['vitality']}%)."
        crop = get_crop(item_id)
        perlu(crop is not None, "Item pangan tidak dikenal.")
        porsi = crop["hasil_g"]
        perlu(s["panen_map"].get(item_id, 0) >= porsi, f"Stok panen {crop['nama']} tidak cukup (butuh {porsi} g).")
        s["panen_map"][item_id] -= porsi
        s["vitality"] = min(100, s["vitality"] + crop["vitality"])
        if crop["group"] not in s["food_groups_today"]:
            s["food_groups_today"].append(crop["group"])
        boost_txt = ""
        if crop["rare"] and crop["bonus_sales_pct"] > 0:
            dur = crop.get("boost_sec", 600)
            s["rare_boost"] = {"crop_id": item_id, "nama": crop["nama"], "pct": crop["bonus_sales_pct"], "expires_at": round(kini + dur, 1)}
            boost_txt = f" Bonus jual +{crop['bonus_sales_pct']}% aktif {dur // 60} menit (cap 5.000 GC/hari)."
        return f"Konsumsi {porsi} g {crop['nama']} (+{crop['vitality']} Vitalitas → {s['vitality']}%).{boost_txt}"

    # ---- Machinery: Buy, Rent/Lease, Sell Used, Modular Place/Remove
    if nama in ("beli_mesin", "sewa_mesin"):
        req_id = str(payload.get("machine_id", ""))
        side = "buy" if nama == "beli_mesin" else "rent"
        q = make_quote("machine", req_id, side, 1, kini, cfg["price_multiplier"])
        perlu(s["koin"] >= q["net_gc"], f"Saldo tidak cukup untuk {q['nama']} ({q['net_gc']:,} GC).")
        s["koin"] -= q["net_gc"]
        s["wallet"]["expenses_gc"] += q["net_gc"]
        cid = q["id"]
        uid = f"m-{cid}-{int(kini)}-{len(s['machines_owned'])+len(s['machines_leased'])}"
        if side == "buy":
            s["machines_owned"].append({"uid": uid, "canonical_id": cid, "condition": 100, "slot": None, "starter": False})
            # Expand battery capacity if LFP battery purchased
            if cid == "DRE-075": s["energy"]["battery_cap_wh"] = min(200_000, s["energy"]["battery_cap_wh"] + 500)
            elif cid == "DRE-076": s["energy"]["battery_cap_wh"] = min(200_000, s["energy"]["battery_cap_wh"] + 1000)
            elif cid == "DRE-077": s["energy"]["battery_cap_wh"] = min(200_000, s["energy"]["battery_cap_wh"] + 5000)
            return f"Membeli {q['nama']} ({cid}) seharga {q['net_gc']:,} GC."
        else:
            s["machines_leased"].append({"uid": uid, "canonical_id": cid, "expires_at": round(kini + 24 * 3600, 1), "partner": "Mitra UMKM Lokal"})
            return f"Menyewa {q['nama']} ({cid}) 24 jam seharga {q['net_gc']:,} GC."

    if nama == "jual_mesin_bekas":
        uid = str(payload.get("uid", ""))
        inst = next((m for m in s["machines_owned"] if m["uid"] == uid), None)
        perlu(inst is not None, "Mesin tidak ditemukan di inventaris.")
        perlu(not inst.get("starter"), "Aset starter tidak dapat dijual (anti-deadlock).")
        q = make_quote("machine", inst["canonical_id"], "sell_used", 1, kini)
        s["machines_owned"].remove(inst)
        s["koin"] += q["net_gc"]
        return f"Menjual bekas {q['nama']} (+{q['net_gc']:,} GC setelah depresiasi & biaya inspeksi)."

    if nama == "pasang_mesin":
        uid = str(payload.get("uid", ""))
        slot_id = str(payload.get("slot", ""))
        perlu(any(sl["id"] == slot_id for sl in YARD_SLOTS), "Slot penempatan tidak valid.")
        inst = next((m for m in s["machines_owned"] if m["uid"] == uid), None)
        perlu(inst is not None, "Mesin tidak ditemukan.")
        occupied = next((m for m in s["machines_owned"] if m.get("slot") == slot_id and m["uid"] != uid), None)
        perlu(occupied is None, f"Slot {slot_id} sudah ditempati mesin lain (anti-overlap).")
        inst["slot"] = slot_id
        return f"Mesin ditempatkan di {slot_id} (jalan & sungai tetap aman)."

    # ---- Market Selling (Products, Crops with Daily Demand Cap + Rare Boost Cap)
    if nama == "jual_panen_crop":
        cid = str(payload.get("crop_id", "CR01"))
        crop = get_crop(cid)
        perlu(crop is not None, "Varietas panen tidak dikenal.")
        have_g = s["panen_map"].get(cid, 0)
        qty_g = int(payload.get("gram") or have_g)
        perlu(qty_g > 0 and have_g >= qty_g, f"Stok panen {crop['nama']} belum mencukupi.")
        if s["crop_sell_day"] != wib_day:
            s["crop_sell_day"] = wib_day
            s["crop_sold_today_g"] = {}
        sold_today = s["crop_sold_today_g"].get(cid, 0)
        rem_demand = max(0, crop["daily_demand_g"] - sold_today)
        perlu(rem_demand >= qty_g, f"Permintaan harian NPC untuk {crop['nama']} tersisa {rem_demand} g hari ini (anti-inflasi).")
        base_gc = max(1, (crop["gc_per_kg"] * qty_g) // 1000)
        bonus_gc = 0
        if s.get("rare_boost") and kini < s["rare_boost"]["expires_at"]:
            if s["rare_boost_day"] != wib_day:
                s["rare_boost_day"] = wib_day
                s["rare_boost_today_gc"] = 0
            raw_bonus = (base_gc * s["rare_boost"]["pct"]) // 100
            bonus_gc = min(raw_bonus, max(0, cfg["rare_boost_daily_cap_gc"] - s["rare_boost_today_gc"]))
            s["rare_boost_today_gc"] += bonus_gc
        s["panen_map"][cid] -= qty_g
        s["terjual_g"] += qty_g
        s["crop_sold_today_g"][cid] = sold_today + qty_g
        tot = base_gc + bonus_gc
        s["koin"] += tot
        s["wallet"]["earned_gc"] += base_gc
        s["wallet"]["operating_profit_gc"] += base_gc
        s["wallet"]["grant_gc"] += bonus_gc
        s["stat"]["koin_jual"] += tot
        s["stat"]["lot_jual_sah"] += 1
        s["stat"]["lot_jual_laba"] += 1
        s["pernah_jual"] = True
        update_wealth_and_milestones(s, kini)
        return f"Menjual {qty_g} g {crop['nama']} (+{base_gc:,} GC" + (f" + {bonus_gc:,} GC bonus langka" if bonus_gc else "") + ")."

    if nama.startswith("jual_"):
        barang = nama.removeprefix("jual_")
        if barang in ("panen", "panen_langka"):
            # Backward-compatible shortcut: sell first available common/rare harvested crop
            cid = next((k for k, v in s["panen_map"].items() if v > 0 and get_crop(k)["rare"] == (barang == "panen_langka")), None)
            if cid:
                return aksi(s, {"aksi": "jual_panen_crop", "crop_id": cid, "gram": min(s["panen_map"][cid], get_crop(cid)["hasil_g"])}, kini, cfg)
            perlu(s[barang] >= 1, "Stok sayur belum tersedia.")
            s[barang] -= 1
            s["koin"] += 1200
            s["wallet"]["earned_gc"] += 1200
            s["wallet"]["operating_profit_gc"] += 1200
            s["stat"]["koin_jual"] += 1200
            s["stat"]["lot_jual_sah"] += 1
            s["stat"]["lot_jual_laba"] += 1
            s["pernah_jual"] = True
            return "Penjualan 1 ikat sayur berhasil (+1.200 GC)."
        perlu(barang in HARGA_PRODUK_REALISTIS, "Produk pasar tidak dikenal.")
        kunci, min_g, harga = HARGA_PRODUK_REALISTIS[barang]
        harga = int(round(harga * cfg["price_multiplier"]))
        perlu(s[kunci] >= min_g, f"Perlu minimal {min_g} g untuk menjual {barang}.")
        bonus_gc = 0
        if s.get("rare_boost") and kini < s["rare_boost"]["expires_at"]:
            if s["rare_boost_day"] != wib_day:
                s["rare_boost_day"] = wib_day
                s["rare_boost_today_gc"] = 0
            raw_bonus = (harga * s["rare_boost"]["pct"]) // 100
            bonus_gc = min(raw_bonus, max(0, cfg["rare_boost_daily_cap_gc"] - s["rare_boost_today_gc"]))
            s["rare_boost_today_gc"] += bonus_gc
        s[kunci] -= min_g
        s["terjual_g"] += min_g
        tot = harga + bonus_gc
        s["koin"] += tot
        s["wallet"]["earned_gc"] += harga
        s["wallet"]["operating_profit_gc"] += harga
        s["wallet"]["grant_gc"] += bonus_gc
        s["stat"]["koin_jual"] += tot
        s["stat"]["lot_jual_sah"] += 1
        s["stat"]["lot_jual_laba"] += 1
        s["pernah_jual"] = True
        update_wealth_and_milestones(s, kini)
        return f"Penjualan {min_g} g {barang} berhasil (+{harga:,} GC" + (f" + {bonus_gc:,} GC bonus" if bonus_gc else "") + ")."

    # ---- Claim GT01-09 & PR01-10 (one-time idempotent)
    if nama == "klaim_gt":
        gid = str(payload.get("id", ""))
        item = next((x for x in daftar_gt(s) if x["id"] == gid), None)
        perlu(item is not None, "Misi tier tidak dikenal.")
        perlu(not item["claimed"], f"{gid} sudah pernah diklaim.")
        perlu(item["can_claim"], f"Syarat {gid} ({item['tier']}) belum terpenuhi atau tier sebelumnya belum diklaim.")
        s["gt_claimed"].append(gid)
        s["tier"] = item["tier"]
        s["tier_idx"] = int(gid[2:]) - 1
        if item["grant_gc"] > 0:
            s["koin"] += item["grant_gc"]
            s["wallet"]["grant_gc"] += item["grant_gc"]
        prio = 5 if gid == "GT09" else 4
        push_celebration(s, "god" if gid == "GT09" else "tier", f"Naik Tier: {item['tier']} ({item['badge']})", item["desc"], prio, kini)
        update_wealth_and_milestones(s, kini)
        return f"Selamat! Tier {item['tier']} ({gid}) tercapai (+{item['grant_gc']:,} GC hibah sekali)."

    if nama == "klaim_pr":
        pid = str(payload.get("id", ""))
        item = next((x for x in daftar_pr(s) if x["id"] == pid), None)
        perlu(item is not None, "Misi tambahan tidak dikenal.")
        perlu(not item["claimed"], f"{pid} sudah pernah diklaim.")
        perlu(item["can_claim"], f"Syarat {pid} ({item['judul']}) belum terpenuhi.")
        s["pr_claimed"].append(pid)
        s["koin"] += item["grant_gc"]
        s["wallet"]["grant_gc"] += item["grant_gc"]
        push_celebration(s, "badge", f"Lencana: {item['badge']}", f"{item['judul']} (+{item['grant_gc']:,} GC)", 3, kini)
        update_wealth_and_milestones(s, kini)
        return f"Misi {item['judul']} selesai! Lencana {item['badge']} terbuka (+{item['grant_gc']:,} GC)."

    # ---- Local Sandbox Top-Up (GME v1.0: clearly sandbox, NO XP/God/badge, disqualifies Self-Made!)
    if nama == "sandbox_topup":
        sku = str(payload.get("sku", ""))
        pkg = next((p for p in SANDBOX_TOPUP_PACKAGES if p["sku"] == sku), None)
        perlu(pkg is not None, "Paket sandbox tidak dikenal.")
        s["koin"] += pkg["gc"]
        s["wallet"]["topup_sandbox_gc"] += pkg["gc"]
        s["wallet"]["self_made_provisional"] = False
        update_wealth_and_milestones(s, kini)
        return f"[SANDBOX LOKAL] +{pkg['gc']:,} GC uji ditambahkan (bukan uang nyata; tidak memberi XP/God/lencana)."

    raise ValueError("Aksi tidak dikenal.")


def ringkasan_ekstra(s, kini, cfg=None):
    cfg = cfg or DEFAULT_CONFIG
    terpakai = gudang_terpakai_g(s)
    total_basis = max(100_000, s["total_masuk_g"] + s["backlog_tpa_g"])
    rasio_limbah = min(1.0, (s["residu_g"] + s["backlog_tpa_g"]) / total_basis)
    bhi = max(10, min(100, int(round(100 - 55 * rasio_limbah))))
    nodes_info = {}
    for kode, tpl in NODE_TEMPLATE.items():
        ns = s["nodes"][kode]["stok"]
        biaya_10 = int(round(tpl["fee_tetap"] + tpl["jarak_km"] * tpl["gc_per_km"] + 10 * tpl["handling_per_kg"]))
        nodes_info[kode] = {
            "nama": tpl["nama"], "tersedia_g": sum(ns.values()), "kapasitas_g": tpl["kapasitas_g"],
            "jarak_km": tpl["jarak_km"], "tarif_10kg": biaya_10, "kompensasi_per_kg": tpl["kompensasi_per_kg"],
            "eta_detik": tpl["eta_detik"], "min_kg": tpl["min_kg"], "max_kg": tpl["max_kg"], "stok": ns,
        }
    return {
        "gudang_terpakai_g": terpakai,
        "gudang_bebas_g": max(0, s["gudang_kap_g"] - terpakai),
        "bhi": bhi,
        "bhi_label": "Snapshot lokal (simulasi)",
        "server_time": kini,
        "nodes_info": nodes_info,
        "tr_aktif": active_tr_window(kini),
        "event_aktif": active_dynamic_event(kini),
        "gt_missions": daftar_gt(s),
        "pr_missions": daftar_pr(s),
        "gsg": hitung_gsg(s),
        "chosen_eval": evaluasi_chosen_provisional(s),
        "pencapaian": daftar_pencapaian(s),
        "harga_petak": HARGA_PETAK_REALISTIS[len(s["petak"])] if len(s["petak"]) < len(HARGA_PETAK_REALISTIS) else None,
        "harga_gudang": HARGA_GUDANG_REALISTIS[s["gudang_upgrade"]] if s["gudang_upgrade"] < len(HARGA_GUDANG_REALISTIS) else None,
        "harga_produk": {k: {"min_g": v[1], "gc": int(round(v[2] * cfg["price_multiplier"]))} for k, v in HARGA_PRODUK_REALISTIS.items()},
        "yard_slots": YARD_SLOTS,
        "label_sampah": LABEL_SAMPAH,
        "sandbox_packages": SANDBOX_TOPUP_PACKAGES,
        "support_urls": {
            "support_url": cfg.get("support_url"),
            "sponsor_contact_url": cfg.get("sponsor_contact_url"),
            "soundtrack_url": cfg.get("soundtrack_url"),
        },
        "config_version": cfg.get("version", 1),
        "catalog_stats": load_seed()["stats"],
    }
