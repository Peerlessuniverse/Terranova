# Missions and Achievements — integration v1.1

Preserve catalog 03 and 06/07/10; this is an overlay.

## 2. Misi inti tiap tier — usulan jalur ringan dan industri setara
Misi GT01–GT09 baru, serial, satu kali; tidak mensyaratkan mesin milik sendiri atau upgrade F3. Bukti dari receipt server. Nilai berat adalah lot unik final, bukan stok berpindah. Misi lama tetap tersedia sebagai opsional dengan dependency dan feature flag; jangan paksa ST11–ST20 yang bergantung industri untuk jalur rumahan. Ambang poin 03 untuk tier 2–8 adalah baseline historis yang perlu diganti setelah uji jika menghalangi jalur kecil; target tabel adalah usulan gate baru berbasis aksi, bukan tambahan ke ambang lama. God memakai GSG 06/10 setelah kalibrasi; Gaia's Chosen tetap terbuka untuk keputusan pemilik. Tidak mengunci hidden gem atau upacara lama tanpa audit.

| ID | Tier | Kondisi kumulatif kecuali disebut | Hibah GC sekali (reuse grant 03) | Lencana (reuse ID) |
|---|---|---|---:|---|
| GT01 | Awaken | terima panggilan, intro selesai | 0 | BT01 |
| GT02 | Seeker | pungut 5; jual 1 lot sah; pulihkan 2 kg | 5000 | BT02 |
| GT03 | Sorter | pilah 10 kg; 3 fraksi; 1 neraca valid | 15000 | BT03 |
| GT04 | Recycler | 25 kg pulih; 2 resep berbeda (mitra boleh); panen pertama | 40000 | BT04 |
| GT05 | Guardian | 50 kg pulih; 5 pembersihan sungai; 3 hari operasi bersih | 100000 | BT05 |
| GT06 | Ascendant | 100 kg pulih; 1 kWh net waste-origin digunakan; 1 audit energi | 250000 | BT06 |
| GT07 | Titan | 150 kg pulih; 5 kWh net waste-origin; 7 hari bersih; residu aman | 500000 | BT07 |
| GT08 | Archon | 200 kg pulih; 10 kWh net waste-origin; 10 hari bersih; audit neraca | 1000000 | BT08 |
| GT09 | God | GSG 06/10 lulus, tidak ada syarat kekayaan/pabrik | 2500000 | BT09 |

Hibah bukan tambahan di atas hibah tier 03, evaluasi inflasi sebelum aktif. Seluruh threshold termasuk energi awal harus diuji untuk akses rumahan, akses mitra berbayar GC diperbolehkan tanpa kredit ganda. UI misi menampilkan kondisi, progress, hadiah, lock reason, alternatif, receipt. Badge hanya kosmetik. Pertahankan 8 badge §34: Tangan Pertama, Pemilah Andal, Penyubur Tanah, Panen Perdana, Saudagar Hijau, Penjaga Sungai, Petani Kota, Lahan Bersih; Saudagar Hijau lama 2000 GC akan otomatis terpenuhi dengan starter baru, usulan ganti trigger laba operasi kumulatif 2000 GC untuk akun baru, histori tidak dicabut. Alias badge semantik hanya jika kondisi benar-benar sama. God dan Chosen jangan disamakan; batas kekayaan/tonase Chosen 10 tetap proposal dan kriteria akhir belum selesai.

| ID | Misi tambahan | Kondisi | GC | Badge baru (kosmetik) |
|---|---|---|---:|---|
| PR01 | Arus pertama | 1 sampah sungai terapung diambil aman | 500 | River Catcher |
| PR02 | Sungai lestari | 10 lot terapung ditangani akhir | 2000 | Flow Guardian (reuse bila cocok) |
| PR03 | Angkut tepat waktu | 5 kontrak diterima sesuai deadline | 2500 | Green Carrier |
| PR04 | Pangan sendiri | panen 5 varietas | 3000 | Food Keeper |
| PR05 | Kebun keajaiban | panen 1 varietas langka | 2000 | Rare Gardener |
| PR06 | Makan beragam | konsumsi 3 kelompok pangan dalam satu hari aktif | 1000 | Balanced Life |
| PR07 | Usaha mandiri | 10 penjualan produksi sendiri dengan laba positif | 3000 | Circular Trader |
| PR08 | Daya campuran | 2 sumber energi berbeda menyuplai beban sah | 4000 | Hybrid Keeper |
| PR09 | Tata lahan | tempatkan 3 alat sah tanpa overlap | 1000 | Eco Builder |
| PR10 | Tidak terbuang | 10 batch balance valid | 2000 | Matter Keeper |

PR satu kali, tidak mengganti katalog 03. Katalog lama seluruhnya tampil, fitur unavailable LOCKED, bukan progress palsu. Claim idempotent. Daily/weekly caps mengikuti 03 sampai recalibration, tidak bertambah karena event baru. Badge tidak memberikan cash langsung.



## 3. Spawn dan sungai
Pertahankan §32: awal 9 dalam pagar +12 luar sekali; liar 90 detik maks16 luar; pohon 60 detik peluang60% maks6; kendaraan 40 detik peluang45% maks5; DLE lama terpisah sesuai §28. Berat 12 jenis mengikuti tabel §32; tidak menaikkan frekuensi otomatis karena level atau kekayaan. Slot deterministic seed; catch-up max3, tanpa offline farming. Usulan river: slot 75 detik, peluang 50%, maks4 objek terapung, masa lintasan 90 detik, spawn upstream; botol PET 300–700g, kaleng 200–500g, kemasan campur 150–400g, organik 300–700g. Tidak ada B3 tajam/berbahaya untuk aksi tangan; lapor mitra. Sprite mengalir pada polyline sungai yang sudah ada, posisi client interpolated; server menentukan event_id, start/end, accessible bank window, claim; avatar tidak masuk air. Jika lewat, pindah ke backlog hilir, tidak dihapus dari neraca. Capture memakai akses tepi sah atau alat penangkap terpasang; tanpa prosedur teknis sungai dunia nyata.

Sumber baru harus debit node/fixture environment ledger; pohon menghasilkan lot biologis tercatat, kendaraan debit kargo, sampah liar debit stok lingkungan; transfer ke gudang sekali; no new mass on click. Cap global per source dan jarak minimum; client animasi kosmetik tidak menciptakan reward. Spawn tidak dipercepat untuk mengejar badge; misi dihitung terhadap supply yang tersedia dan bisa diberi alternatif Angkut. Reward pungut lama +2 GC/+3 poin histori; usulan kompensasi layanan 100 GC/event dengan cap 2000 GC/hari gabungan event, poin final recovery sekali; tidak menganggap material pickup sudah terpulihkan. Uji ekonomi sebelum ganti. Gudang penuh mempertahankan event sampai expiry, tidak kehilangan massa.

## 4. Angkut realistis dan misi berkala
Gunakan rate 01 sumber dan fee pembeli; biaya kendaraan berbeda dari fee pembeli. Gerobak starter MCH-002 25kg/trip, kendaraan lain dari canonical catalog, jangan buat ID mesin baru. Rumus biaya = tarif tetap + jarak PP km × tarif/km + kg × handling; material dibeli bila kontrak beli, kompensasi bila jasa, tidak keduanya otomatis. Waktu game dipercepat dan diberi label. Seed lokal:

| Node | Jarak PP km | Lot kg | Fee tetap GC | GC/km | Handling GC/kg | Kompensasi jasa GC/kg | ETA game |
|---|---:|---|---:|---:|---:|---:|---|
| Permukiman | 1 | 5–25 | 500 | 300 | 20 | 150 | 30 s |
| Pasar | 2 | 5–25 | 500 | 300 | 20 | 200 | 45 s |
| Sungai | 0.5 | 2–25 | 500 | 300 | 20 | 250 | 25 s |
| Sekolah/kantor | 3 | 5–25 | 500 | 300 | 20 | 100 | 60 s |
| Restoran | 2 | 5–25 | 500 | 300 | 20 | 200 | 45 s |

Contoh 10kg pasar: biaya 1300 GC; jasa 2000 GC; surplus jasa 700 GC sebelum penanganan akhir, material sale terpisah. Kompensasi hanya setelah receipt sah sesuai kontrak; transport masuk ledger. No negative balance, reserve stock+capacity+cash atomik; expiry kembali ke stok asal; cap 8h offline sesuai engine lama, tidak membuat kontrak baru saat offline. B3 melalui mitra sah, bukan gerobak campur. Node tambahan hanya setelah seed tersedia. Kendaraan sewa mengikuti katalog dan kapasitas aktual, tidak wajib dibeli.

| ID | Window server Asia/Jakarta | Misi | Lot | Bonus GC sekali/window |
|---|---|---|---|---:|
| TR01 | 06–09 | Sisa pasar pagi | 10–25 kg organik | 500 |
| TR02 | 11–14 | Restoran siang | 5–15 kg organik | 500 |
| TR03 | 15–18 | Kardus toko | 5–20 kg kertas | 500 |
| TR04 | 18–21 | Bersih tepi sungai | 2–10 kg campur | 500 |
| TR05 | Sabtu/Minggu 08–20 | Kerja bakti | 10–25 kg campur | 1000 |

Window alternatif untuk pemain sibuk: misi setara rotasi setiap 3 jam, tanpa stacking reward; tidak menghukum absen; jangan mengirim push wajib. Bonus masuk cap misi 03. Prototype waktu lokal deterministik; test clock injection bukan client clock. Offer → reserved → in_transit → arrived → received → processed/settled. Kontrak menunjukkan komposisi, grade, harga/fee, jarak, ETA, deadline, stok dan sisa kapasitas.



## Claim and ceremony
Unique (player, grant_key); map GT reward to existing tier reward, no double award. Retain existing eight badge history. Server event -> eligibility -> transactional grant -> celebration queue -> journal/card; skip/replay does not grant. Milestone based on earned GC separate from topup. Video templates from 11, optional longer Archon/God/Chosen narrative after approval. No final Chosen grant.
