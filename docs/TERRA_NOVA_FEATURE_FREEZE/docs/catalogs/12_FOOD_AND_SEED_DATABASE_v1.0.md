# Food and Seed Database v1.0

Seed [U], extracted from Addendum 11, not additional IDs or grants.

## 5. Kebun, pangan, vitalitas
Seed 10 umum dan 5 langka sesuai brainstorming; unit benih per petak, hasil gram, harga jual referensi per kg, waktu game detik. Semua dapat dijual di NPC pasar jika stok/demand memungkinkan. Waktu bukan agronomi nyata. Pangan langka = langka dalam game, bonus fiktif, bukan manfaat kesehatan dunia nyata.

| ID | Tanaman | detik | benih GC | hasil g | GC/kg | bonus vitality game | bonus sales % |
|---|---|---:|---:|---:|---:|---:|---:|
| CR01 | Kangkung | 30 | 500 | 200 | 6000 | 8 | 0 |
| CR02 | Bayam | 40 | 500 | 200 | 8000 | 8 | 0 |
| CR03 | Pakcoy | 50 | 750 | 250 | 12000 | 9 | 0 |
| CR04 | Sawi hijau | 60 | 750 | 250 | 8000 | 9 | 0 |
| CR05 | Selada | 75 | 1000 | 250 | 18000 | 10 | 0 |
| CR06 | Kacang panjang | 90 | 1000 | 300 | 12000 | 10 | 0 |
| CR07 | Mentimun | 120 | 1200 | 500 | 7000 | 10 | 0 |
| CR08 | Tomat | 135 | 1500 | 400 | 12000 | 11 | 0 |
| CR09 | Jagung manis | 150 | 1500 | 500 | 10000 | 12 | 0 |
| CR10 | Ubi jalar | 180 | 2000 | 750 | 8000 | 12 | 0 |
| CR11 | Romanesco | 300 | 5000 | 150 | 80000 | 25 | 5 |
| CR12 | Asparagus ungu | 420 | 8000 | 150 | 100000 | 30 | 7 |
| CR13 | Wasabi Jepang | 600 | 30000 | 100 | 750000 | 35 | 10 |
| CR14 | Pineberry | 720 | 20000 | 150 | 350000 | 40 | 12 |
| CR15 | Ginseng | 900 | 50000 | 100 | 1500000 | 50 | 15 |

Rare boost 10 menit, ginseng 15; tidak stack, cap bonus 5000 GC/hari [U], berlaku penjualan hasil produksi sendiri, bukan resale/transfer/reward. Dana bonus dicatat grant sink/source; tidak mengubah harga pasar. Stok langka max1 benih/varietas/minggu per player fixture; unlock misi non-paid, tidak ada lootbox. Demand umum awal 2kg/jenis/hari, langka 0.2kg/jenis/hari [U], uji supaya panen cepat tidak mencetak uang. Satu panen per plant receipt, tidak auto-replant. Pupuk kompos -25% sisa waktu sekali, gunakan aturan massa 03/01; hasil tanaman masuk ledger biomassa dari input tumbuh simulasi, bukan kredit sampah. Vitality 0–100, turun hanya aksi aktif, tidak offline, tidak mati/hilang aset; pemulihan konsumsi pangan, air. Tahap awal satu bar, kemudian kategori energi, hidrasi, protein, vitamin, serat. NPC jual beras 15000/kg, tempe 15000/kg, telur 28000/kg, air 3000/liter [U]. Makan mengurangi inventaris. Efek manual 60–110% berdasarkan vitality, tidak pada mesin otomatis. Pangan langka tidak wajib untuk God.



## Integration
Use integer grams, GC integer, mature_at server. Crop requires seed and plot; compost consumed once; harvest settles once and storage capacity checked. Food NPC inventory includes staples, tempe, eggs and water; prices not yet seeded/verified. Vitality is fictional, no starvation offline, no paid rare lottery. Demand caps and cooldowns prevent rapid-harvest/boost arbitrage. Test full 15 crops and low cash recovery.
