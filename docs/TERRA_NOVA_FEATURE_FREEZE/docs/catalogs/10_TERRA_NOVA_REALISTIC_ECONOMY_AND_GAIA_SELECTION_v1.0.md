# TERRA NOVA — Realistic Economy & Gaia Selection v1.0
**Addendum 10 | 26 November 2026 | GAME_SPEC v0.9 / DESIGN_SPEC v1.4 | Proposal for integration review**

[D] Arah pemilik: ganti ekonomi prototipe dengan ekonomi realistis; pemain membeli peralatan dari katalog, bebas mengejar industri atau cukup pada rumah tangga. God tidak mensyaratkan kekayaan. Kandidat pilihan Gaia dapat mencapai God tanpa pabrik, mengoptimalkan gabungan free energy dan waste-to-electricity rumah tangga, mempertahankan tonase secara konsisten, dan tidak mengumpulkan kekayaan melebihi 1 miliar GC. [U] Semua angka operasional di bawah, termasuk starter 1 juta (alternatif pemilik 100 ribu), jendela audit, ambang persentase, dan metode valuasi merupakan rekomendasi untuk uji, bukan hasil simulasi atau keputusan final angka. [P] Prototipe masih seperti §35 sampai implementasi selesai. K5 arah ekonomi diselesaikan; K1–K4/K6–K7 belum diputuskan otomatis.

## 1. Satu ekonomi resmi, bukan dua ekonomi pemain
`realistic_v1` menjadi target satu-satunya untuk settlement game; `prototype_v09` hanya histori, regression fixture dan rollback lokal. 1 GC merepresentasikan Rp1 nominal simulasi, bukan uang nyata. Katalog 02 (material), 05–07 (teknologi), 09 v1.2 (master) menjadi seed. Seluruh 301 baris sumber/282 canonical/19 alias lama dipertahankan; 6 pelengkap rumah tangga HME menambah total menjadi 307 entri/288 canonical/19 alias. alias tidak menjadi barang kedua. Harga master kanonik aktif untuk mesin yang sudah lolos mapping, safety, kapasitas, resep, utilitas dan QA. `active_price_gc=null` untuk yang belum lolos, bukan gratis. Semua kartu dapat dilihat. Tidak memakai satu pengali harga lama. Harga, kapasitas dan tarif adalah estimasi game, bukan quotation.

### Starter [U]
| Entitlement | Nilai |
|---|---|
| Saldo akun baru | 1.000.000 GC sekali |
| Lahan | 100 m²; kondisi berantakan mengikuti v0.9 |
| Gudang | 500 kg |
| Gerobak | starter MCH-002, harga pengganti 750.000 GC, kapasitas realistis 25 kg/trip |
| Area pilah | MCH-005 starter, 20 kg/jam, bukan mesin daur ulang |
| Kebun | 1 petak, 3 benih |
| Tier/Karma | Awaken/0% |

Entitlement awal tidak dapat dijual untuk menggandakan modal; replay dan reinkarnasi tidak mengulang grant. Tidak otomatis memberi komposter, mesin plastik, genset atau PLTS. Pemain bebas membeli dari toko atau mengakses layanan mitra. Alternatif 100.000 GC diuji sebagai stress test, bukan mode ekonomi publik kedua.

### Contoh keranjang awal (pilihan, bukan paket wajib)
| ID | Alat | GC |
|---|---|---:|
| MCH-001 | Tong sampah terpilah | 45.000 |
| MCH-003 | Timbangan gantung | 85.000 |
| MCH-022 | Komposter ember bertingkat | 85.000 |
| MCH-025 | Biopori | 35.000 |
| DRE-001 | Solar kit DC terintegrasi | 450.000 |
| TOTAL | Pembelian | 700.000 |
| SISA | Modal kerja | 300.000 |

Alternatif hemat: MCH-021 komposter starter 5.000; tong 45.000; timbangan 85.000 =135.000; sisa 865.000. Paket 100 ribu: tong 45.000 + komposter 5.000, sisa 50.000, timbang melalui fasilitas starter/mitra yang tervalidasi. Biaya pengiriman/instalasi tambahan tidak termasuk; kit DC bukan PLTS AC. Jangan memberikan listrik/kompos hanya karena sprite terlihat.

## 2. Transisi aksi prototipe §35
| Aksi | Target realistis |
|---|---|
| Pungut sampah liar | lot gram unik, nilai berasal dari jual/olah; +2 GC lama dihentikan; jasa kebersihan hanya bila kontrak beranggaran |
| Angkut | kapasitas kendaraan, jarak, biaya 01; tidak memakai 4/6/2 GC lama atau 6 detik sebagai waktu produksi nyata |
| Pilah | resep fraksi, grade dan kontaminasi; kategori campuran tidak otomatis menjadi grade termahal |
| Kompos | mesin dimiliki/disewa/mitra; batch matang, kapasitas dan rendemen resep tervalidasi; air/gas/residu tercatat |
| Plastik | tidak ada pelet/pot tanpa peralatan atau layanan yang sah; output sesuai grade, reject tercatat |
| B3 | drop-off khusus; tarif 02 D, kuota gratis terkontrol; tidak dijual bebas |
| Benih/petak | seed 01: 200 GC benih umum, 5.000 GC petak tambahan sebagai nilai uji; waktu tumbuh dan hasil dari resep; bukan 2 GC/40 detik |
| Gudang | perluasan melalui slot; biaya usulan +250 kg pertama 1.000.000, kedua 1.500.000 GC termasuk struktur, tidak sama dengan rak; belum aktif sampai layout/quote tervalidasi |
| Jual | 02 harga per unit, supply-demand, grade, volume dan quote server; bukan 5/9/12 GC lama |
| DLE | material dan poin tugas unik; tidak memberi koin tanpa anggaran |
| Lencana | 8 lencana prototipe dipertahankan; Saudagar Hijau ambang 2.000 historis untuk pemilik lama, usulan 2 juta untuk akun realistis; tidak memberi GC |

Contoh nilai kotor: 10 kg PET01 bersih dijual ke bank =30.000 GC, ke pengepul =45.000 GC jika grade/akses terpenuhi. 10 kg PA01 dijual ke bank =18.000 GC. Kompos COMP mengikuti harga seed 02; pembelian input, opex, residu dan logistik mengurangi margin. Pemasok/buyer dibatasi demand, kuota, kualitas dan stok. Tidak ada beli-jual instan pada grade sama tanpa biaya atau kuota untuk arbitrase. Settlement mencatat pihak pembayar, item, berat/unit, versi harga, biaya, kas neto.

### Pembiayaan dan pemulihan kas
- Mesin rumah tangga (WTE-002 4,5 juta; WTE-015 18 juta) tidak perlu dibeli pada hari pertama. Jalur sewa/jasa rumah tangga dengan kuota nyata; harga sewa usulan 0,1% CAPEX/hari aktif + opex, hanya jika mitra menyediakan alat. Jangan mendebit maintenance pemilik untuk aset sewa. Jalur berlangganan/dana komunitas tidak menjadi pay-to-win.
- Kontrak layanan kebersihan dibayar anggaran kota virtual, bukan uang tanpa batas; rescue 01: 5 kg material terpilah zero input cost, 500 GC setelah delivery, sekali/24 jam, dan drop-off publik 2 kg/hari. Uji apakah cukup dalam ekonomi realistis; tidak ada utang otomatis atau pembayaran uang nyata.
- Hadiah tier file 03 tetap seed untuk simulasi, bukan arus kas otomatis yang telah disahkan; uji inflasi dan kelayakan jalur hemat. Sumber grant dicatat, sekali per entitlement. Tidak mensyaratkan kekayaan untuk lencana lingkungan.
- Waktu server, offline cap 8 jam, tidak memaksa login nonstop. Produksi batch biologis tidak disamakan dengan kapasitas throughput; fix MCH-021 menjadi 10 kg aktif/batch sebagai parameter usulan setelah uji, bukan 2 kg kompos/jam; durasi matang resep harus tervalidasi.

## 3. God umum: tetap terbuka untuk semua jalur
Sembilan tier Awaken–God; F1–F5 terpisah. GSG file 06 menggantikan ambang 400.000 poin untuk God, setelah implementasi. Tidak ada batas harta, jumlah mesin atau jenis perusahaan bagi God. G01–G11 tetap berlaku: Archon naratif, massa dan listrik neto asal sampah, diversion, pemulihan material, potensi dan efisiensi energi, pemanfaatan, Karma, pengendalian emisi, disposition dan neraca, BHI lokal. Tidak boleh mengompensasi satu gate dengan gate lain. Semua angka seed.

### Perbaikan akses rumah tangga [U]
G02 100 kg/20 kWh pada 14 hari sulit untuk WTE-002: ER01 net seed 0,12×0,8=0,096 kWh/kg; 5 kg/hari ×14 =70 kg dan 6,72 kWh maksimal seed. Tidak memaksa membeli pabrik. Uji opsi jendela audit 60 hari bagi semua jalur dengan minimal 40 hari aktivitas settlement (atau 14 hari/10 aktif untuk jalur cepat). Kedua jendela sama-sama mensyaratkan 100 kg dan 20 kWh neto; 5 kg/hari ×60 ×0,096=28,8 kWh teoritis seed, sebelum kendala aktual. Tidak mengubah ambang keselamatan. Semua pelanggaran dalam jendela terpilih dihitung. Rasio G03–G11 memakai lot/energi pada window yang sama. Denominator nol = pending. Archon 180.000 poin juga wajib diuji; bila tidak realistis untuk lahan kecil, ajukan jalur mastery berbasis pencapaian lingkungan ke tier 1–8, bukan membeli XP atau menghapus gate. Jangan mengklaim target 90 hari sudah tercapai.

## 4. Hidden distinction: Gaia's Chosen — Jalan Kecukupan [U nama]
Pencapaian kedua, bukan tier ke-10, bukan syarat God umum, bukan larangan industri. Semua God tetap setara. Kandidat dipilih berdasarkan bukti keberlangsungan, bukan saldo terbesar/terkecil, gender, pembayaran atau undian. Kriteria final dan mekanisme upacara perlu review pemilik. Jangan mengganti hadiah cerita §7g yang lama diam-diam; bila terintegrasi ke upacara ZWM global, status kandidat personal tetap terpisah. Tidak ada keuntungan ekonomi, kapasitas atau XP dari gelar ini. Gunakan penghormatan netral usia, kosmetik/naratif saja.

| ID | Kondisi kandidat usulan |
|---|---|
| GC01 | God tercapai dan GSG tetap lulus pada evaluasi terbaru |
| GC02 | Tidak pernah memiliki/mengendalikan pabrik F3–F5 dalam seluruh riwayat realistis yang dapat diaudit, lintas musim dan reset; F1–F2 skala rumah tangga atau mikro sah; akses mitra untuk disposal aman tidak disamakan dengan kepemilikan |
| GC03 | Kekayaan neto tertinggi historis sepanjang riwayat realistis yang dapat diaudit ≤1.000.000.000 GC; current wealth juga ≤ batas; tepat 1 miliar lulus |
| GC04 | Listrik asal sampah dihasilkan dari alat rumah tangga dimiliki/disewa dan dioperasikan sendiri; WTE-002 + WTE-015 beserta seluruh dependensi tervalidasi adalah contoh; listrik industri mitra tidak menjadi kredit gate kandidat |
| GC05 | Minimal satu pembangkit non-waste terbarukan yang benar-benar menghasilkan listrik berguna, mis. PV, angin, hidro; gabungkan dengan WtE dan ledger microgrid; bukan sekadar punya alat |
| GC06 | ≥80% realisasi potensi energi layak, ≥85% listrik neto dimanfaatkan, GSG efisiensi tetap terpenuhi; hasil terpisah per asal; tidak menghitung ulang baterai |
| GC07 | ≥80% listrik kebutuhan operasional sah dipenuhi dari pembangkit sendiri/rumah tangga sewa pada window kandidat [U]; kebutuhan nol/alat palsu/curtail load penting = pending; tidak memaksa ekspor |
| GC08 | Konsistensi tonase: 4 minggu referensi + 4 minggu berturut-turut evaluasi; tiap minggu evaluasi massa pengelolaan unik ≥ baseline tetap, tidak turun; lihat §5 |
| GC09 | GSG keselamatan, Karma, BHI lokal, residu dan neraca terpenuhi sepanjang audit; tidak ada fraud terbuka |

Skala teknis kandidat seed: WtE rumah tangga input ≤5 kg/hari per modul, total WtE ≤10 kg/hari dan generator ≤2 kW; DRES rumah tangga ≤5 kW agregat (PV kWp DC dikonversi ke daya AC sesuai desain) dan storage ≤10 kWh. Nilai khusus kandidat, bukan pembatas seluruh katalog atau industri umum. Akses alat yang lebih besar bebas, tetapi tidak memenuhi jalur ini. Hindari penamaan "rumah tangga" sebagai standar legal/engineering. DRES non-kandidat tetap skala modul UMKM; batas agregat 100 kW/200 kWh file 07 hanya baseline review.

### Valuasi kekayaan
`net_worth = cash + inventory_fair_value + owned_asset_fair_value + recoverable_deposits + receivables - verified_liabilities`.
Harga wajar dari price book server, kondisi aset dan appraisal rule versioned; bukan harga listing yang dibuat pemain. Starter aset, lahan bila bernilai transaksi, investasi, aset bersama menurut beneficial share, uang/material dalam transit dihitung sekali. Hutang palsu, gift ke alt, jual murah ke akun terkait, memindahkan aset ke perusahaan yang dikendalikan, reset/reinkarnasi/pindah kota tidak menghapus history. Simpan peak per settlement dan revaluasi terjadwal; tidak memakai lifetime omzet sebagai kekayaan. Contoh: kas 200 juta + aset 600 juta + stok 150 juta − kewajiban sah 20 juta =930 juta. Jika sebelumnya 1,2 miliar kemudian turun ke 930 juta, tidak lulus kandidat (usulan penafsiran "tanpa mengumpulkan lebih dari"); tetap boleh God dan semua lencana lingkungan biasa. Aset sewa bukan aset milik; deposit dihitung; tidak menggunakan utang fiktif. Tidak menjadikan miskin sebagai skor atau memberikan ranking saldo terendah. Untuk sejarah prototipe yang tidak bisa dinilai, status kandidat pending sampai baseline baru disahkan; jangan mengarang high-water mark.

## 5. Konsistensi tonase tanpa menciptakan sampah
Satuan gram integer, tampil kg dan ton (1000 kg =1 ton). `completed_mass_week` = massa lot asal unik yang mencapai pemulihan/pengelolaan akhir terverifikasi; stok menunggu, transfer, rework dan output turunan tidak dihitung ulang. Untuk kandidat, baseline = median empat minggu referensi valid, minimal 20 kg/minggu [U], ditetapkan sebelum evaluasi; supply plan dan kapasitas dicatat. Setiap empat minggu evaluasi harus ≥ baseline dan ≥ minggu sebelumnya dalam window (tidak turun). Jangan menetapkan baseline baru setelah gagal untuk memoles hasil; ulang audit dengan aturan tetap setelah cooldown satu window bila memang perlu. Porsi listrik hanya dari waste-origin eligible; tidak semua tonase menjadi bahan bakar. Sampah yang dibeli atau diangkut dari wilayah lain sah hanya dari node resmi, tanpa double counting dan tanpa pembuangan untuk dipungut kembali. Lot biologis selesai setelah hasil dan residu aman.

Contoh baseline 20 kg/minggu =0,020 ton. Minggu 1–4: 20, 21, 21, 22 kg lulus; 20, 25, 24, 26 gagal tren walaupun total tinggi. Jika pasokan resmi menurun akibat pencegahan nyata, tidak menyuruh pemain membuat sampah; status kandidat `pending_supply` dengan bukti server, GSG umum tetap dapat dinilai dan lencana pencegahan tetap sah. Pemain boleh memakai sumber komunitas sah jika tersedia. Review pemilik apakah pengecualian pencegahan kelak boleh menjadi jalur kandidat alternatif; default belum mengurangi syarat tonase yang diminta. Tidak menggunakan jumlah sampah yang diproduksi pemain sebagai target positif. Sampah liar, daun, buah, kendaraan masuk ledger asal DWE sekali sebelum kredit resmi. K6 masih membutuhkan approval implementasi; fixture privat tidak menjadi kredit resmi multiplayer.

## 6. Jalur rumah tangga: contoh investasi bertahap
| Fase | Aset/akses | Harga seed GC |
|---|---|---:|
| Awal | Keranjang starter §1 | 700.000 |
| Tabungan | WTE-002 digester | 4.500.000 |
| Tabungan/sewa | WTE-015 genset biogas mikro | 18.000.000 |
| Energi tambahan | DRE-002 PLTS pico | 1.500.000 |
| Energi opsional | DRE-030 pico hydro 100 W | 3.000.000 |
| Storage opsional | DRE-075 LFP pico | 900.000 |
| Total modul ilustratif | jika semuanya dibeli | 28.600.000 |

Belum mencakup kontrol gas, metering, proteksi, sipil, instalasi, pengolahan digestat, pemeliharaan dan utilitas. Jangan tampilkan sebagai paket turnkey. WTE-015 memerlukan gas sesuai spesifikasi dan kontrol gas/safety, bukan disambung langsung; katalog industri WTE-013/014/020 bukan satu-satunya solusi untuk rumah tangga. Enam paket HME pada katalog v1.2 §10, total proksi 11 juta GC, melengkapi modul sebagai data usulan (total ilustratif 39,6 juta sebelum biaya lain), terkunci sampai mapping teknik/game disetujui. Hindari panduan fabrikasi/pembakaran. Insinerator rumahan WTE-001 tetap display_only dan tidak menghasilkan listrik. Baterai bukan pembangkit. Contoh ini menunjukkan CAPEX modul jauh di bawah 1 miliar, bukan bukti tercapainya God atau ROI.

## 7. Tambahan misi dan lencana (usulan, tanpa hadiah kas otomatis)
| ID | Nama | Kondisi server |
|---|---|---|
| GCH-M01 | The First Investment | beli 1 alat F1 dengan saldo valid |
| GCH-M02 | Living Within Means | 7 hari biaya operasi terbayar tanpa saldo negatif |
| GCH-M03 | The Little Spark | listrik neto waste-origin pertama dari alat rumah tangga |
| GCH-M04 | The Hybrid Home | listrik waste-origin dan non-waste masing-masing digunakan |
| GCH-M05 | Steady Hands | GC08 lulus |
| GCH-M06 | The Path of Enough | GC01–GC09 lulus |
| GCH-B01 | Small but Sustainable | GSG lulus tanpa pabrik F3–F5 |
| GCH-B02 | Unbroken Cycle | GC08 lulus |
| GCH-B03 | Home Energy Guardian | GC04–GC07 lulus |
| GCH-B04 | Gaia's Chosen Candidate | GC01–GC09 lulus, server audit |
| GCH-B05 | Chosen by Gaia | penghormatan naratif setelah mekanisme pemilihan/upacara disahkan |

Lencana pencapaian historis tidak dicabut; eligibility saat ini bisa berubah, tidak ada penghargaan ulang karena reset. Tidak ada penjualan lencana. Nama, hadiah naratif dan trigger dibandingkan file 03/06/07 sebelum seed untuk mencegah duplikasi. UI publik tidak perlu menampilkan kekayaan privat atau alasan detail kandidat lain. Pemain sendiri mendapat metrik dan sebab pending/fail; twist naratif baru terbuka di Archon, tetapi aturan tidak boleh manipulatif atau retroaktif.

## 8. Handoff dan migrasi
- Update GAME_SPEC §0.1 (katalog edukasi seluruh teknologi, operasi energi rumah tangga sebagai scope yang diprioritaskan setelah core loop), §7b/c/e/f/g (God umum vs kandidat, nontermal, upacara), §17.6, §33–36; DESIGN_SPEC §3/19–25, README dan dokumen 01–07. Jangan ubah versi histori. Pertahankan onboarding, navigasi, visual dan 8 lencana.
- Usulan pengujian lokal: backup gaia.sqlite3, simpan save prototipe sebagai histori read-only, gunakan database uji baru dengan starter 1 juta. Untuk akun yang sudah berjalan, jangan otomatis mengalikan saldo, menghapus aset, atau memberi top-up ulang. Rancang pilihan migrasi snapshot/season baru untuk approval; saldo lama tetap sampai keputusan. Price book versioned, quote lama invalidated, in-flight settlement diselesaikan di profil asal lalu ditutup. Tidak mencampur dua unit harga pada satu ledger.
- `economy_profile`, `price_book_version`, `starter_grant`, `asset_instance`, `beneficial_owner`, `valuation_snapshot`, `wealth_peak`, `origin_lot`, `completed_mass_ledger`, `energy_origin_ledger`, `gaia_audit_window`, `gaia_candidate_status`, `achievement_receipt` sebagai entitas usulan. ID unik, idempotency, transaksi atomik, time server Asia/Jakarta, nullable data kurang. Hanya satu settlement profile resmi setelah cutover.
- Operasional alat dibuka setelah resep, kapasitas, utilitas, biaya, slot, izin dan keselamatan tervalidasi; katalog text-first, lazy thumbnail, snapshot ≤20 KB. Tidak memuat 301 sprite. DRES tidak menggantikan WtE untuk God.

## 9. Acceptance / simulasi yang wajib dilakukan (belum dijalankan)
Uji 90 hari dengan seed yang sama, profil ekonomi realistis 100k vs 1M (untuk testing), jalur rumahan tanpa F3+, industri, komunitas, pencegahan, pemain gratis, pemain pasif dan kas habis. Ukur first sale, waktu beli/sewa alat, cashflow/margin, cash starvation, waktu Archon/God, eligibility kandidat, inflasi, pasokan/permintaan, energi neto, tonase, BHI. Uji juga 180 hari untuk window kandidat dan musim lintas batas bila dibutuhkan; jangan menjanjikan gelar dalam musim pertama jika window tidak cukup.

- 1M grant sekali; 100k test terpisah; saldo tak negatif; tidak membeli alat gratis lewat null/alias; dua tab dan retry tidak duplikat.
- God industri >1 miliar tetap lulus jika GSG lulus; kandidat tidak; jalur kecil <1 miliar gagal jika tidak ada WtE listrik atau energi tambahan; tepat batas lulus; peak >batas lalu transfer/hadiah/reset tidak lulus.
- Rumah tangga memenuhi GSG lewat window panjang tanpa pabrik; gagal bila emisi/ash/digestat tidak aman, hanya PV, gas dijual sekaligus dibakar, storage double counting, listrik dibeli dicatat waste-origin atau mitra industri diklaim operasi sendiri.
- Tonase 20/21/21/22 lulus; 20/25/24/26 gagal; recycle lot yang sama tidak dihitung; supply rendah dari pencegahan pending, bukan spawn tambahan.
- Archon tidak mustahil bagi jalur kecil; kalau simulasi gagal, revisi mastery dan akses sewa sebelum release, bukan menaikkan timbulan/XP buatan.
- Migrasi akun lama tidak hilang dan tidak memberi starter ganda; rollback mengembalikan backup konsisten tanpa mencampur price book.

**Batas:** Tidak ada kode, repo, DB atau aset yang diubah. Harga belum disurvei ulang; data teknis, recipe mapping, keamanan dan parameter kandidat belum tervalidasi. Dokumen ini menetapkan arah K5, bukan mengesahkan seluruh angka atau K1–K4/K6–K7. Keputusan pemilik diperlukan untuk nominal starter, definisi peak wealth, window/tonase, batas teknis kandidat dan mekanisme upacara sebelum aktivasi.
