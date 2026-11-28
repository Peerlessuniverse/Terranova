"""Canonical catalog loader, alias resolver, paginated search, and quote engine.
Loads data/catalog_seed.json (282 materials, 307 machines = 288 canonical + 19 aliases, 15 crops, 4 staples).
"""
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = ROOT / "data" / "catalog_seed.json"
MANIFEST_PATH = ROOT / "data" / "asset_manifest.json"

_CACHE = None


def load_seed():
    global _CACHE
    if _CACHE is None:
        raw = json.loads(SEED_PATH.read_text(encoding="utf-8"))
        mat_by_id = {m["id"]: m for m in raw["materials"] + raw["outputs"]}
        mch_by_id = {m["id"]: m for m in raw["machines"]}
        crop_by_id = {c["id"]: c for c in raw["crops"]}
        food_by_id = {f["id"]: f for f in raw["staple_foods"]}
        raw["_mat_by_id"] = mat_by_id
        raw["_mch_by_id"] = mch_by_id
        raw["_crop_by_id"] = crop_by_id
        raw["_food_by_id"] = food_by_id
        _CACHE = raw
    return _CACHE


def resolve_machine_id(mid):
    seed = load_seed()
    return seed["machine_aliases"].get(mid, mid)


def get_machine(mid):
    seed = load_seed()
    cid = resolve_machine_id(mid)
    return seed["_mch_by_id"].get(cid)


def get_material(mid):
    return load_seed()["_mat_by_id"].get(mid)


def get_crop(cid):
    return load_seed()["_crop_by_id"].get(cid)


def get_food(fid):
    return load_seed()["_food_by_id"].get(fid)


def query_catalog(kind="all", category="", search="", page=1, per_page=24, only_active=False):
    seed = load_seed()
    q = (search or "").strip().lower()
    cat = (category or "").strip().lower()
    # beberapa kategori sekaligus dipisah "|" (kios Pasar: mis. Bengkel = Pengumpulan|Organik|Plastik|...)
    cats = [c for c in cat.split("|") if c] if "|" in cat else None
    per_page = max(1, min(48, int(per_page or 24)))
    page = max(1, int(page or 1))

    items = []
    if kind in ("all", "material", "materials"):
        for m in seed["materials"] + seed["outputs"]:
            if cat and m["category"].lower() != cat and m["kind"].lower() != cat:
                continue
            if only_active and not m["tradable"]:
                continue
            if q and q not in m["id"].lower() and q not in m["nama"].lower():
                continue
            items.append({
                "catalog_kind": "material",
                "id": m["id"],
                "nama": m["nama"],
                "category": m["category"],
                "subkind": m["kind"],
                "unit": m["unit"],
                "bank_gc": m["bank_gc"],
                "pengepul_gc": m["pengepul_gc"],
                "bandar_gc": m["bandar_gc"],
                "output_id": m["output_id"],
                "yield_pct": m["yield_pct"],
                "hazardous": m["hazardous"],
                "tradable": m["tradable"],
                "disposal_fee": m["disposal_fee"],
                "status": "hazardous_licensed" if m["hazardous"] else ("active" if m["tradable"] else "reference_only"),
            })
    if kind in ("all", "machine", "machines"):
        for m in seed["machines"]:
            if cats is not None:
                if not any(c in m["category"].lower() for c in cats):
                    continue
            elif cat and cat not in m["category"].lower() and cat != m["domain"]:
                continue
            if only_active and m["status"] != "active":
                continue
            if q and q not in m["id"].lower() and q not in m["canonical_id"].lower() and q not in m["nama"].lower() and q not in m["fungsi"].lower():
                continue
            items.append({
                "catalog_kind": "machine",
                "id": m["id"],
                "canonical_id": m["canonical_id"],
                "is_alias": m["is_alias"],
                "nama": m["nama"],
                "category": m["category"],
                "domain": m["domain"],
                "f_stage": m["f_stage"],
                "harga_gc": m["harga_gc"],
                "kapasitas": m["kapasitas"],
                "opex": m["opex"],
                "area_m2": m["area_m2"],
                "fungsi": m["fungsi"],
                "status": m["status"],
                "validated_recipe": m["validated_recipe"],
            })
    if kind in ("all", "crop", "crops"):
        for c in seed["crops"]:
            if cat and cat not in ("tani", "benih", "kebun", c["group"]):
                continue
            if q and q not in c["id"].lower() and q not in c["nama"].lower():
                continue
            items.append({"catalog_kind": "crop", **c, "status": "active"})
    if kind in ("all", "food", "foods"):
        for f in seed["staple_foods"]:
            if cat and cat not in ("sehat", "pangan", f["group"]):
                continue
            if q and q not in f["id"].lower() and q not in f["nama"].lower():
                continue
            items.append({"catalog_kind": "food", **f, "status": "active"})

    total = len(items)
    pages = max(1, (total + per_page - 1) // per_page)
    page = min(page, pages)
    start = (page - 1) * per_page
    return {
        "version": seed["version"],
        "stats": seed["stats"],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": pages,
        "items": items[start:start + per_page],
    }


def make_quote(item_kind, item_id, side, qty, kini=None, price_mult=1.0):
    """Server-authoritative price quote with version and 120s expiry."""
    kini = kini or time.time()
    seed = load_seed()
    qty = int(qty)
    if qty <= 0:
        raise ValueError("Jumlah transaksi harus positif.")

    if item_kind == "material":
        m = get_material(item_id)
        if not m:
            raise ValueError(f"Material {item_id} tidak ditemukan di katalog.")
        if m["hazardous"]:
            raise ValueError(f"{m['nama']} adalah limbah B3/khusus; tidak diperdagangkan bebas di pasar NPC.")
        if side == "sell":
            unit_price = max(0, int(round(m["pengepul_gc"] * price_mult)))
            if unit_price <= 0:
                raise ValueError(f"{m['nama']} tidak memiliki harga jual positif (gunakan jalur disposal/olah).")
            total_gc = (unit_price * qty) // 1000 if m["unit"] == "kg" else unit_price * qty
            fee_gc = max(0, int(round(total_gc * 0.02)))
            net_gc = max(0, total_gc - fee_gc)
        else:
            unit_price = max(0, int(round(m["bandar_gc"] * 1.15 * price_mult)))
            if unit_price <= 0:
                raise ValueError(f"{m['nama']} tidak tersedia untuk dibeli.")
            total_gc = (unit_price * qty) // 1000 if m["unit"] == "kg" else unit_price * qty
            fee_gc = max(0, int(round(total_gc * 0.02)))
            net_gc = total_gc + fee_gc
        return {
            "version": seed["version"],
            "kind": "material",
            "id": m["id"],
            "nama": m["nama"],
            "side": side,
            "qty": qty,
            "unit": "g" if m["unit"] == "kg" else m["unit"],
            "unit_price_gc": unit_price,
            "gross_gc": total_gc,
            "fee_gc": fee_gc,
            "net_gc": net_gc,
            "expires_at": round(kini + 120, 1),
        }

    if item_kind == "machine":
        cid = resolve_machine_id(item_id)
        m = get_machine(cid)
        if not m:
            raise ValueError(f"Mesin {item_id} tidak ditemukan di katalog.")
        if m["status"] != "active":
            raise ValueError(f"{m['nama']} ({cid}) berstatus {m['status']} — hanya untuk dipelajari, belum dibuka untuk transaksi.")
        if m["harga_gc"] <= 0 and side == "buy":
            raise ValueError(f"{m['nama']} adalah aset starter/referensi, bukan item jual-beli.")
        if side == "buy":
            net_gc = int(round(m["harga_gc"] * price_mult))
            fee_gc = 0
        elif side == "rent":
            # Affordable daily/cycle rental for household/UMKM path (~4% of price, min 15.000 GC)
            net_gc = max(15000, int(round(m["harga_gc"] * 0.04 * price_mult)))
            fee_gc = 0
        elif side == "sell_used":
            # Anti-arbitrage: used buyback is 60% of the CURRENT market price minus 5% inspection fee
            # (gameplay additionally caps it at 57% of what the player actually paid)
            gross = int(round(m["harga_gc"] * 0.60 * price_mult))
            fee_gc = int(round(gross * 0.05))
            net_gc = max(0, gross - fee_gc)
        else:
            raise ValueError("Jenis transaksi mesin tidak valid.")
        return {
            "version": seed["version"],
            "kind": "machine",
            "id": cid,
            "requested_id": item_id,
            "nama": m["nama"],
            "side": side,
            "qty": 1,
            "unit": "unit",
            "unit_price_gc": m["harga_gc"],
            "gross_gc": net_gc + fee_gc if side == "sell_used" else net_gc,
            "fee_gc": fee_gc,
            "net_gc": net_gc,
            "expires_at": round(kini + 120, 1),
        }

    if item_kind == "crop_seed":
        c = get_crop(item_id)
        if not c:
            raise ValueError("Benih tanaman tidak dikenal.")
        net_gc = int(round(c["benih_gc"] * qty * price_mult))
        return {
            "version": seed["version"],
            "kind": "crop_seed",
            "id": c["id"],
            "nama": f"Benih {c['nama']}",
            "side": "buy",
            "qty": qty,
            "unit": "benih",
            "unit_price_gc": c["benih_gc"],
            "gross_gc": net_gc,
            "fee_gc": 0,
            "net_gc": net_gc,
            "expires_at": round(kini + 120, 1),
        }

    if item_kind == "food":
        f = get_food(item_id)
        if not f:
            raise ValueError("Bahan pangan tidak dikenal.")
        net_gc = int(round(f["harga_gc"] * qty * price_mult))
        return {
            "version": seed["version"],
            "kind": "food",
            "id": f["id"],
            "nama": f["nama"],
            "side": "buy",
            "qty": qty,
            "unit": f["unit"],
            "unit_price_gc": f["harga_gc"],
            "gross_gc": net_gc,
            "fee_gc": 0,
            "net_gc": net_gc,
            "expires_at": round(kini + 120, 1),
        }

    raise ValueError("Kategori quote tidak dikenal.")
