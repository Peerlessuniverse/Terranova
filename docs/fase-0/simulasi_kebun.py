"""Uji pilihan panen per petak, terpisah dari model kota. Python 3."""
import csv
from pathlib import Path


def hasil(jeda, pupuk, kuota):
    # Satu petak. Tanam pada jam nol, lalu cek hanya saat pemain kembali.
    tumbuh = 3 if pupuk else 4
    kemajuan = terjual = panen = stok = 0
    tanam = 1
    sisa_kuota = kuota
    periode = 0
    for jam in range(jeda, 90 * 24 + 1, jeda):
        hari = (jam - 1) // 24  # penutupan hari dihitung sebelum reset kuota
        if hari != periode:
            periode, sisa_kuota = hari, kuota
        kemajuan += min(jeda, 8)
        if kemajuan >= tumbuh:
            stok += 1
            panen += 1
            kemajuan = 0
            if jam < 90 * 24:
                tanam += 1
        laku = min(stok, sisa_kuota)
        stok -= laku
        sisa_kuota -= laku
        terjual += laku
    biaya_benih = max(0, tanam - 3) * 2
    nilai_kompos = tanam * 5 if pupuk else 0
    return (jeda, kuota, pupuk, panen, stok, terjual, biaya_benih, nilai_kompos,
            terjual * 24 - biaya_benih - nilai_kompos)


if __name__ == "__main__":
    lokasi = Path(__file__).resolve().parent / "hasil" / "kebun.csv"
    with lokasi.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["jeda_jam", "kuota_porsi_hari", "pakai_kompos", "panen", "stok", "terjual",
                    "biaya_benih", "peluang_jual_kompos", "margin_ekonomi"])
        for jeda in (1, 4, 12, 24):
            for kuota in (0, 4, 8):
                for pupuk in (False, True):
                    baris = hasil(jeda, pupuk, kuota)
                    assert baris[3] == baris[4] + baris[5]
                    w.writerow(baris)
