"""Konversi sprite sumber (PNG, Asset/sumber_web/sprites_png) ke WebP ringan untuk web/assets/sprites.

Anggaran PERFORMANCE_BUDGET: aset pabrik awal <=1 MB, gameplay awal <=3 MB. PNG asli tetap disimpan di
Asset/ (tidak dilayani server) agar bisa diedit/dikonversi ulang. Jalankan: python tools/optimize_sprites.py
"""
import glob
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Asset", "sumber_web", "sprites_png")
OUT = os.path.join(ROOT, "web", "assets", "sprites")
# Sprite yang tidak dipakai game/landing (tetap ada di sumber, tidak dikirim ke browser)
TIDAK_DIPAKAI = {
    "player_3", "player_7", "playerf_3", "npc_7",
    "vehicles_1", "vehicles_2", "vehicles_3",
    "vehicles2_1", "vehicles2_2", "vehicles2_3", "vehicles2_4", "vehicles2_5", "vehicles2_6", "vehicles2_7",  # 2_3/2_4 diganti veh_motor/veh_sepeda (tampak samping)
    "pedagang_3", "pedagang_6",   # kembar / diganti pedagang2_1 (warung) & pedagang2_2 (energi)
    "pedagang2_3", "pedagang2_4",               # potongan sendok & mangkuk lepas dari lembar pedagang2
}
KUALITAS = 85


def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.png")))
    if not files:
        sys.exit(f"Tidak ada PNG sumber di {SRC}")
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0
    for p in files:
        nama = os.path.splitext(os.path.basename(p))[0]
        if nama in TIDAK_DIPAKAI:
            continue
        im = Image.open(p).convert("RGBA")
        dst = os.path.join(OUT, nama + ".webp")
        im.save(dst, "WEBP", quality=KUALITAS, alpha_quality=100, method=6, exact=False)
        total_in += os.path.getsize(p)
        total_out += os.path.getsize(dst)
    print(f"{total_in / 1024:.0f} KB PNG -> {total_out / 1024:.0f} KB WebP ({OUT})")


if __name__ == "__main__":
    main()
