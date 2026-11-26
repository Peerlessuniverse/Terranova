# TERRA NOVA — Playable Prototype: Feature Complete
27 November 2026 | Addendum 11 | Chapter I — The Calling of Gaia

[D] Arah pemilik: finalisasi scope ide prototipe lokal, bukan finalisasi angka atau kriteria Gaia's Chosen; mempertahankan visual sekarang, spawn sekarang, tambah sampah mengalir, misi level/lencana/angkut berkala, musik karya pemilik, dukungan sukarela, ekonomi realistis, kebun pangan, pasar NPC. Setelah pengujian dan dana cukup baru pertimbangkan server online. [U] Semua angka baru di sini adalah seed untuk balancing. Tidak ada deployment, pembelian aset atau perubahan DB yang disetujui melalui dokumen ini.

## 1. Baseline dan hierarki
GAME_SPEC v0.9 §17,30–36 dan DESIGN_SPEC v1.4 §19–25 mendeskripsikan prototipe aktual. Addendum 01–10 adalah rancangan, bukan fitur yang sudah aktif. Pertahankan ID katalog 02 dan 09 v1.2 (307 baris/288 canonical/19 alias menurut manifest), dan semua misi/lencana 03,06,07,10. Dokumen 11 melengkapi, bukan membuat katalog ganda. Realistic_v1 target ekonomi tunggal; 1 GC = Rp1 nominal simulasi tanpa penukaran tunai; modal 1 juta GC usulan utama, 100 ribu stress test. Starter gudang 500 kg, 3 benih, gerobak 25 kg/trip, area pilah, lahan berantakan, satu petak. Pembelian mesin nyata dalam simulasi, bukan uang nyata. Tidak mengubah saldo akun lama tanpa migrasi/backup/consent. Onboarding dan cinematic 120 detik tetap. Nav Pabrik/Kebun/Angkut/Pasar/Menu tetap. Kota/Bumi online terkunci; fixture lokal jelas diberi label.

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

## 6. Pasar NPC dan encyclopedia
Scene terpisah, ilustrasi pasar painted isometric statis, hotspot kios, list fallback. NPC kategori: Rongsok (plastik/logam/kertas/kaca), Organik, Tani, Benih, Mekanik, Surya, Bayu, Tirta, Energi WtE, Daur/industri, Logistik, Sehat, Researcher. Beli/Jual, search, filter, pagination 24, detail unit/grade, stok, bid/ask, fee, quote expiry, inventory and wallet, receipt. Harga material 02/01, mesin 09 v1.2, pangan §5; alias resolve canonical. Tidak hardcode harga di UI; semua katalog tampil, aksi hanya supported recipe/safety/stock. NPC buy/sell spread dan kuota 01; tidak jual B3 bebas. NPC fixed rules, no LLM. Pasar multiplayer nanti mengganti private NPC quota dengan shared ledger; NPC tetap sebagai fallback; tidak perlu realtime avatar. Tidak ada kewajiban menggunakan uang nyata.

## 7. Hybrid painted isometric modular
Pertahankan yard_iso.webp, jalan/sungai, kamera dan collision polygon koordinat 1672×941. Pada fase awal slot overlay untuk alat kecil di area tanah kosong. Untuk bangunan lama yang tertanam pada gambar, buat clean plate lokal dengan inpainting terbatas atau layer terrain terpisah; jangan tempel gudang baru di atas gudang lama. Gunakan original sebagai referensi; fal.ai (konfirmasi provider/model aktual repo) image-to-image/reference consistent style. Asset bible: sudut kamera, arah bayangan, skala objek, palet, anchor kaki, footprint polygon, z-sort, alpha edge, transparent WebP. Batch awal 25–40 keluarga aset hanya setelah budget approval, bukan 307 sprite. Reuse ikon/text card untuk sisanya. Variasi ukuran dan warna tidak menipu spesifikasi. Fixed slot → perluasan modular → free placement sesudah collision/route QA; jalan dan sungai tetap. Bangunan ekonomi validasi ownership, fee, overlap, utility dan batas lahan server. Jangan ubah renderer sekarang tanpa profiling. Tidak membuat aset fal.ai berbayar sebelum persetujuan biaya.

## 8. Selebrasi dan audio
Misi rutin CSS/overlay 1–2s, milestone coin 2–3s, badge 3–5s, tier 5–8s, God 10–15s. Reuse maksimal 22 template usulan (3 mission,3 coin,5 badge,8 ascension,3 special); MVP cukup 3 template. Milestone saldo 1M/10M/100M/1B/10B GC [U], starter tidak memicu 1M; pisahkan lifetime earned milestone. Queue priority God>tier>badge>coin>mission; merge burst; skip/mute/reduced motion; event_id once; reward sudah settle sebelum video; replay dari Jurnal tidak memberi hadiah. Video on-demand, fallback static, no preload. Aset opening budget 1.6MB, asset pabrik 1MB; ukur kualitas dan ukuran.

Gaia Radio: daftar lagu karya pemilik (metadata title, artist, duration, path, license, scene, loop); jangan mengarang judul atau menganggap file sudah ada. Pabrik playlist pengelolaan sampah; Kebun instrumental/natural atau lagu pilihan; Pasar upbeat; Angkut perjalanan; Menu/Jurnal tenang; cinematic audio sendiri. Pilihan Auto per scene / lagu manual / shuffle / mute; simpan preferensi lokal, satu audio player, crossfade pendek 0.5–1s, pause saat background opsional, duck saat VO/selebrasi, resume posisi; autoplay browser fallback. Stream audio compressed, bukan preload seluruh album; izin penggunaan dan hak cipta lagu/rekaman diverifikasi sebelum publikasi. Tidak ada biaya streaming pihak ketiga otomatis.

## 9. Dukungan sukarela
Menu → Dukung TERRA NOVA: Donasi/Apresiasi, Sponsor, Tentang & transparansi. Link Saweria/opsi pembayaran resmi yang pemilik berikan (support_url=null sampai diberikan); sponsor_contact_url=null sampai diberikan. Jangan menebak username atau link; tombol disabled 'segera hadir' jika kosong. External link allowlist HTTPS, tampil tujuan; tidak simpan data pembayaran, tidak menerima kartu di game. Dukungan tidak menambah GC, XP, spawn, rare chance, status God/Chosen atau produksi. Penghargaan kosmetik opsional, tidak mengekspos nama donor tanpa consent; sponsorship label jelas, tidak mengubah fakta edukasi/harga. Untuk usia muda jangan mendesak pembayaran; legal/privasi dan kebijakan platform ditinjau sebelum publik. Monetisasi tambahan: soundtrack/merch eksternal, kosmetik, kemitraan edukasi; hanya setelah scope approval. Dana server bukan janji jadwal rilis.

## 10. Ringan dan rencana implementasi
Server simulation data-driven, Lazy Tick dengan timestamp/receipt, satu scene aktif, no per-second job per item, no LLM, no WebSocket avatar. Catalog static paginated/cache version; snapshot <=20KB, shell JS <=250KB compressed, aset pabrik <=1MB, initial gameplay <=3MB, opening <=1.6MB, heap <=100MB, Eco 30FPS, API p95 <=500ms target; audio/video/katalog on-demand tidak masuk initial bundle. Profiling perangkat Android 2GB/iOS dan desktop; jangan mengklaim target tercapai sebelum tes. SQLite lokal loopback saja. Backup state; jangan ubah existing accounts otomatis. 

Urutan: (1) audit repo + dokumen, seed katalog canonical, migrasi economy dan neraca spawn; (2) pasar NPC + angkut + starter buy/rent; (3) 15 tanaman dan vitality; (4) progression/misi/badge, GSG dan jalur rumahan; (5) modular overlay, sungai, asset profiling; (6) celebration/audio/support links; (7) regression, ekonomi 90/180 hari, security/QA. Scope selesai bukan berarti semua 307 alat punya resep operasional; semua terlihat, yang belum validated terkunci. Untuk fitur aktif minimal jalur rumahan dari kompos/biogas/pembangkit kecil + solar/hydro sesuai site dan mitra wajib dapat diuji; industri besar tetap jalur opsional.

## 11. Acceptance dan keputusan terbuka
- Starter grant/receipt exactly once, saldo/stok tidak negatif; harga realistis konsisten seluruh transaksi; tidak ada arbitrase NPC/rare boost; jalur modal 100k/1M diuji.
- GT01–09 reachable tanpa forced factory; jalur rumahan 90/180 hari dan mitra, God GSG tidak bisa dibeli; no claim Gaia's Chosen final.
- 8 badge lama tidak hilang; 03/06/07/10 IDs tidak diduplikasi; reward idempotent multi-tab/reset/replay.
- Spawn 90/60/40 detik dan cap lama dipertahankan; river expiry/backlog gram conserved; no click teleport/farm; B3 safe.
- Angkut quote, reservation, deadlines, expiry, capacity, refund and cleanup ledger validated; no timezone exploit.
- 15 crops, 30–180s common, 300–900s rare; harvest once; no offline starvation; price/demand/cap test.
- Market NPC category and search all catalog entries, canonical alias, locks, quote stale handling, no hazardous trade; purchase/sell atomic.
- Existing visual remains recognizable, road/river unchanged, no overlap/blocked exit; before/after screenshots, mobile touch, asset budget.
- Celebration skip/replay/mute, queue, no double reward; radio scene transitions, manual selection, autoplay fallback, no duplicate audio players.
- Support URL empty safe; HTTPS whitelist, no payment privilege; no paid asset generation without approval.
- Simulate 90/180 days with modest, industrial, energy, no-pay, low activity and prevention scenarios; record inflation, cash deadlocks, mission completion, God feasibility, mass/energy balance, spawn supply and costs. No simulation run claimed here.
- K5 direction realistic decided, K6 recommendation integrate DWE before shared mode; K1–K4/K7 still owner decision unless explicit; Gaia's Chosen final criteria, actual song manifest, donation URL, budget, mission thresholds, and starter exact amount still to approve/test. Public launch blocked by age/privacy/auth/security/production infra and legal review. No live server procurement until funding and go/no-go.

## 12. Handoff
Antigravity: read GAME_SPEC v0.9, DESIGN_SPEC v1.4, README, 01–07, 08/09 v1.2, 10 and this addendum. Report conflict matrix and proposed GAME_SPEC v0.10 / DESIGN_SPEC v1.5, sync derivatives; preserve history. Implement incrementally in local branch with backups, test each feature and report exact failures; no external deployment, public payment, paid generation or irreversible migration without owner approval. Keep final Gaia's Chosen decision open. Deliver local playable build, screenshots, tests, simulation CSV, performance report and funding readiness checklist.
