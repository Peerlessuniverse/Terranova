"""Build canonical seed JSON (data/catalog_seed.json) and asset manifest (data/asset_manifest.json)
from TERRA_NOVA_FEATURE_FREEZE markdown specifications.
Zero external dependencies (Python standard library only).
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FF = ROOT / "docs" / "TERRA_NOVA_FEATURE_FREEZE"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


def parse_int(val, default=0):
    s = str(val).strip().replace(".", "").replace(",", "")
    m = re.search(r"-?\d+", s)
    return int(m.group(0)) if m else default


def parse_materials():
    path = FF / "docs" / "catalogs" / "02_TERRA_NOVA_DWE_MATERIAL_DATABASE_v1.0.md"
    text = path.read_text(encoding="utf-8")
    section = None
    materials = []
    outputs = []
    seen_ids = set()

    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith("## A."):
            section = "A"
            continue
        if ls.startswith("## B."):
            section = "B"
            continue
        if ls.startswith("## C."):
            section = "C"
            continue
        if ls.startswith("## "):
            section = "OTHER"
            continue
        if not ls.startswith("|") or ls.startswith("|---") or ls.startswith("| ID"):
            continue
        cols = [c.strip() for c in ls.strip("|").split("|")]
        if section == "A" and len(cols) >= 7:
            mid = cols[0]
            if not re.match(r"^[A-Z0-9_-]{2,12}$", mid):
                continue
            bank = parse_int(cols[2])
            pengepul = parse_int(cols[3])
            bandar = parse_int(cols[4])
            out_id = cols[5]
            yld = parse_int(cols[6])
            # Categorize by prefix
            cat = "rongsok"
            if mid.startswith(("OR", "AG", "BIO", "FD")):
                cat = "organik"
            elif mid.startswith(("B3", "HZ", "EW", "MD")):
                cat = "b3"
            elif mid.startswith(("RS", "RE", "SL", "CN")):
                cat = "residu"
            elif mid.startswith(("PA", "KP")):
                cat = "kertas"
            elif mid.startswith(("GL", "KC", "MT", "AL", "FE", "CU")):
                cat = "logam_kaca"
            elif mid.startswith(("TX", "RB", "WD")):
                cat = "lainnya"
            hazardous = (cat == "b3") or (bank < 0) or (out_id == "NONE")
            item = {
                "id": mid,
                "nama": cols[1],
                "kind": "material",
                "category": cat,
                "bank_gc": bank,
                "pengepul_gc": pengepul,
                "bandar_gc": bandar,
                "output_id": out_id,
                "yield_pct": yld,
                "unit": "kg",
                "hazardous": hazardous,
                "tradable": not hazardous and (bandar > 0 or pengepul > 0 or bank > 0),
                "disposal_fee": abs(min(bank, pengepul, bandar)) if min(bank, pengepul, bandar) < 0 else 0,
            }
            if mid not in seen_ids:
                seen_ids.add(mid)
                materials.append(item)
        elif section == "B" and len(cols) >= 4:
            oid = cols[0]
            if not re.match(r"^[A-Z0-9_-]{2,12}$", oid):
                continue
            # Table B format: | ID | Produk | Harga GC/kg | ... or similar
            price = parse_int(cols[2])
            item = {
                "id": oid,
                "nama": cols[1],
                "kind": "output",
                "category": "produk",
                "bank_gc": int(round(price * 0.75)) if price > 0 else price,
                "pengepul_gc": int(round(price * 0.9)) if price > 0 else price,
                "bandar_gc": price,
                "output_id": oid,
                "yield_pct": 100,
                "unit": cols[3] if len(cols) > 3 and cols[3] in ("kg", "L", "kWh", "unit", "m3") else "kg",
                "hazardous": price < 0,
                "tradable": price > 0,
                "disposal_fee": abs(price) if price < 0 else 0,
            }
            if oid not in seen_ids:
                seen_ids.add(oid)
                outputs.append(item)
        elif section == "C" and len(cols) >= 8:
            cid = cols[0]
            if not re.match(r"^[A-Z0-9_-]{2,12}$", cid):
                continue
            bank = parse_int(cols[2])
            pengepul = parse_int(cols[3])
            bandar = parse_int(cols[4])
            unit = cols[5]
            ref_g = parse_int(cols[6], 1000)
            disp = cols[7]
            hazardous = (disp.lower() == "licensed")
            item = {
                "id": cid,
                "nama": cols[1],
                "kind": "special_unit",
                "category": "b3" if hazardous else "rongsok",
                "bank_gc": bank,
                "pengepul_gc": pengepul,
                "bandar_gc": bandar,
                "output_id": disp,
                "yield_pct": 85 if not hazardous else 0,
                "unit": unit,
                "ref_mass_g": ref_g,
                "hazardous": hazardous,
                "tradable": not hazardous and bandar > 0,
                "disposal_fee": 80000 if cid in ("FRIDGE", "AC") else (30000 if cid == "WASH" else 0),
            }
            if cid not in seen_ids:
                seen_ids.add(cid)
                materials.append(item)
    return materials, outputs


def parse_machines():
    path = FF / "docs" / "catalogs" / "09_TERRA_NOVA_MASTER_MACHINERY_ENERGY_CATALOG_v1.2.md"
    text = path.read_text(encoding="utf-8")
    in_master = False
    category = "Umum"
    rows = []
    aliases = {}

    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith("## 2.") or ls.startswith("## 10."):
            in_master = True
            if ls.startswith("## 10."):
                category = "Pelengkap Rumah Tangga (HME v1.2)"
            continue
        if ls.startswith("## 3.") or ls.startswith("## 4.") or ls.startswith("## 5.") or ls.startswith("## 11."):
            in_master = False
            continue
        if not in_master:
            continue
        if ls.startswith("### "):
            category = ls[4:].strip()
            continue
        if not ls.startswith("|") or ls.startswith("|---") or ls.startswith("| ID"):
            continue
        cols = [c.strip() for c in ls.strip("|").split("|")]
        if len(cols) < 10:
            continue
        mid, cid = cols[0], cols[1]
        if not re.match(r"^[A-Z]{2,5}-\d{3}[A-Z]?$", mid):
            continue
        is_alias = (mid != cid)
        if is_alias:
            aliases[mid] = cid
        f_stage = parse_int(cols[3], 1)
        price = parse_int(cols[4], 0)
        area = parse_int(cols[7], 0)
        mode = cols[8].lower()
        # Determine energy/domain class
        domain = "machinery"
        if mid.startswith("WTE-"):
            domain = "wte"
        elif mid.startswith("DRE-"):
            domain = "dres"
        rows.append({
            "id": mid,
            "canonical_id": cid,
            "is_alias": is_alias,
            "nama": cols[2],
            "category": category,
            "domain": domain,
            "f_stage": f_stage,
            "harga_gc": price,
            "kapasitas": cols[5],
            "opex": cols[6],
            "area_m2": area,
            "mode": mode,
            "fungsi": cols[9],
            "status": "locked_pending_validation",
            "validated_recipe": False,
        })

    # Activate ONLY the validated Genesis/local minimal playable subset (household + starter + small renewable/WtE)
    # WTE-001 (educational risk incinerator) and HME-001..006 remain locked/display_only per catalog v1.2!
    VALIDATED_ACTIVE = {
        "MCH-001", "MCH-002", "MCH-003", "MCH-005", "MCH-006", "MCH-007",
        "MCH-021", "MCH-022", "MCH-023", "MCH-024",
        "MCH-044",  # Pencacah plastik mini
        "WTE-002",  # Digester biogas rumah tangga
        "WTE-015",  # Genset biogas mikro (sewa/beli rumah tangga)
        "DRE-001", "DRE-002", "DRE-003", "DRE-004", "DRE-005",  # Solar kit & PLTS atap
        "DRE-030",  # Turbin angin/mikrohidro kecil
        "DRE-075", "DRE-076", "DRE-077",  # Baterai LFP pico/1kWh/5kWh
    }
    for r in rows:
        nm = r["nama"].lower()
        cid = r["canonical_id"]
        if "edukasi risiko" in nm or "display" in r["mode"] or "riset" in r["mode"]:
            r["status"] = "display_only"
            r["validated_recipe"] = False
        elif cid in VALIDATED_ACTIVE:
            r["status"] = "active"
            r["validated_recipe"] = True
        else:
            r["status"] = "locked_pending_validation"
            r["validated_recipe"] = False

    return rows, aliases


def build_crops():
    # Exact 15 crops from 12_FOOD_AND_SEED_DATABASE_v1.0.md
    return [
        {"id": "CR01", "nama": "Kangkung", "detik": 30, "benih_gc": 500, "hasil_g": 200, "gc_per_kg": 6000, "vitality": 8, "bonus_sales_pct": 0, "rare": False, "group": "sayur", "daily_demand_g": 2000},
        {"id": "CR02", "nama": "Bayam", "detik": 40, "benih_gc": 500, "hasil_g": 200, "gc_per_kg": 8000, "vitality": 8, "bonus_sales_pct": 0, "rare": False, "group": "sayur", "daily_demand_g": 2000},
        {"id": "CR03", "nama": "Pakcoy", "detik": 50, "benih_gc": 750, "hasil_g": 250, "gc_per_kg": 12000, "vitality": 9, "bonus_sales_pct": 0, "rare": False, "group": "sayur", "daily_demand_g": 2000},
        {"id": "CR04", "nama": "Sawi hijau", "detik": 60, "benih_gc": 750, "hasil_g": 250, "gc_per_kg": 8000, "vitality": 9, "bonus_sales_pct": 0, "rare": False, "group": "sayur", "daily_demand_g": 2000},
        {"id": "CR05", "nama": "Selada", "detik": 75, "benih_gc": 1000, "hasil_g": 250, "gc_per_kg": 18000, "vitality": 10, "bonus_sales_pct": 0, "rare": False, "group": "sayur", "daily_demand_g": 2000},
        {"id": "CR06", "nama": "Kacang panjang", "detik": 90, "benih_gc": 1000, "hasil_g": 300, "gc_per_kg": 12000, "vitality": 10, "bonus_sales_pct": 0, "rare": False, "group": "protein", "daily_demand_g": 2000},
        {"id": "CR07", "nama": "Mentimun", "detik": 120, "benih_gc": 1200, "hasil_g": 500, "gc_per_kg": 7000, "vitality": 10, "bonus_sales_pct": 0, "rare": False, "group": "hidrasi", "daily_demand_g": 2000},
        {"id": "CR08", "nama": "Tomat", "detik": 135, "benih_gc": 1500, "hasil_g": 400, "gc_per_kg": 12000, "vitality": 11, "bonus_sales_pct": 0, "rare": False, "group": "vitamin", "daily_demand_g": 2000},
        {"id": "CR09", "nama": "Jagung manis", "detik": 150, "benih_gc": 1500, "hasil_g": 500, "gc_per_kg": 10000, "vitality": 12, "bonus_sales_pct": 0, "rare": False, "group": "energi", "daily_demand_g": 2000},
        {"id": "CR10", "nama": "Ubi jalar", "detik": 180, "benih_gc": 2000, "hasil_g": 750, "gc_per_kg": 8000, "vitality": 12, "bonus_sales_pct": 0, "rare": False, "group": "energi", "daily_demand_g": 2000},
        {"id": "CR11", "nama": "Romanesco", "detik": 300, "benih_gc": 5000, "hasil_g": 150, "gc_per_kg": 80000, "vitality": 25, "bonus_sales_pct": 5, "rare": True, "boost_sec": 600, "group": "vitamin", "daily_demand_g": 200},
        {"id": "CR12", "nama": "Asparagus ungu", "detik": 420, "benih_gc": 8000, "hasil_g": 150, "gc_per_kg": 100000, "vitality": 30, "bonus_sales_pct": 7, "rare": True, "boost_sec": 600, "group": "sayur", "daily_demand_g": 200},
        {"id": "CR13", "nama": "Wasabi Jepang", "detik": 600, "benih_gc": 30000, "hasil_g": 100, "gc_per_kg": 750000, "vitality": 35, "bonus_sales_pct": 10, "rare": True, "boost_sec": 600, "group": "vitamin", "daily_demand_g": 200},
        {"id": "CR14", "nama": "Pineberry", "detik": 720, "benih_gc": 20000, "hasil_g": 150, "gc_per_kg": 350000, "vitality": 40, "bonus_sales_pct": 12, "rare": True, "boost_sec": 600, "group": "vitamin", "daily_demand_g": 200},
        {"id": "CR15", "nama": "Ginseng", "detik": 900, "benih_gc": 50000, "hasil_g": 100, "gc_per_kg": 1500000, "vitality": 50, "bonus_sales_pct": 15, "rare": True, "boost_sec": 900, "group": "energi", "daily_demand_g": 200},
    ]


def build_asset_manifest():
    assets = []
    web_assets = ROOT / "web" / "assets"
    for p in sorted(web_assets.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT / "web").as_posix()
        data = p.read_bytes()
        h = hashlib.sha256(data).hexdigest()[:16]
        fam = p.parent.name
        assets.append({
            "asset_id": f"{fam}:{p.stem}",
            "family": fam,
            "version": "1.0",
            "path": "/" + rel,
            "source_license": "Kenney CC0" if fam == "sfx" or p.stem in ("crane", "dumpster1", "farmland", "farmland_empty", "fence", "hay", "house_small", "mill_factory", "pallet_full", "silo1", "treeRound_large", "treeRound_small", "windmill_complete") else "TERRA NOVA Original / fal.ai",
            "hash": h,
            "bytes": len(data),
            "alpha_mode": "transparent" if p.suffix == ".png" else "opaque",
            "fallback_icon": "♻️",
        })
    return assets


def main():
    mats, outs = parse_materials()
    machines, aliases = parse_machines()
    crops = build_crops()

    canon_machines = {m["canonical_id"] for m in machines}
    active_machines = [m for m in machines if m["status"] == "active" and not m["is_alias"]]

    seed = {
        "version": "feature-freeze-v1.0",
        "economy_mode": "realistic_v1",
        "stats": {
            "materials_raw": len(mats),
            "materials_output": len(outs),
            "materials_total": len(mats) + len(outs),
            "machines_rows": len(machines),
            "machines_canonical": len(canon_machines),
            "machines_aliases": len(aliases),
            "machines_active_validated": len(active_machines),
            "crops_total": len(crops),
        },
        "materials": mats,
        "outputs": outs,
        "machines": machines,
        "machine_aliases": aliases,
        "crops": crops,
        "staple_foods": [
            {"id": "FD_BERAS", "nama": "Beras lokal", "unit": "kg", "harga_gc": 15000, "porsi_g": 200, "vitality": 18, "group": "energi"},
            {"id": "FD_TEMPE", "nama": "Tempe segar", "unit": "kg", "harga_gc": 15000, "porsi_g": 200, "vitality": 16, "group": "protein"},
            {"id": "FD_TELUR", "nama": "Telur ayam", "unit": "kg", "harga_gc": 28000, "porsi_g": 150, "vitality": 20, "group": "protein"},
            {"id": "FD_AIR", "nama": "Air minum bersih", "unit": "L", "harga_gc": 3000, "porsi_g": 500, "vitality": 14, "group": "hidrasi"},
        ],
    }

    (DATA / "catalog_seed.json").write_text(json.dumps(seed, indent=1, ensure_ascii=False), encoding="utf-8")
    manifest = {"version": "1.0", "count": 0, "assets": build_asset_manifest()}
    manifest["count"] = len(manifest["assets"])
    (DATA / "asset_manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")

    print("Catalog seed built:", json.dumps(seed["stats"], indent=2))
    print("Active validated machines:", [(m["id"], m["nama"], m["harga_gc"]) for m in active_machines])
    print("Asset manifest built:", manifest["count"], "assets")


if __name__ == "__main__":
    main()
