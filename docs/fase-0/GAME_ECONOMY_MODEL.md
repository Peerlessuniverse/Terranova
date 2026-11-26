# Ekonomi Chapter I · eksperimen 90 hari
**Status: keseimbangan belum lulus.** Pada pasar bersama dengan dua kunjungan per hari, hanya agen termal mencapai God. Kandidat misi membuka jalur organik, tetapi belum memperbaiki jalur campuran dan kebuntuan modal. Keputusan produk yang paling berdampak ialah apa yang dihitung sebagai pengelolaan berhasil.

## Reproduksi dan pembacaan
Dari direktori ini, jalankan berurutan dengan Python 3 tanpa dependensi tambahan:

    python3 simulasi.py
    python3 uji_batas.py

konfigurasi.json memuat parameter utama versi uji-0.6.1. Aturan skenario tetap di skrip versi paket ini. Lima benih mengubah fluktuasi harga dan urutan kedatangan. Untuk setiap benih: kota kosong, lima kota tunggal (satu per strategi), atau kota bersama 20 agen (empat per strategi). 90 simulasi kota, 1.225 lintasan pemain. Hasil CSV berisi setiap pemain, ringkasan strategi, musim, distribusi waktu tier dan sensitivitas reset. Dua eksekusi skrip utama menghasilkan CSV identik. Semua kuantitas permainan ilustratif.

Kontrak adalah batch konsentrat berbeda menurut strategi, bukan komposisi statistik sampah kota. Input campuran 50/18/10/7/14/1%. Semua lini tersedia sejak awal eksperimen agar rute akhir dapat dibandingkan dengan modal sama. Ini cenderung menguntungkan termal karena tidak membebankan investasi awal tiga unit. Model menggunakan lot 100 kg, output kg bulat dan saldo koin bulat. Rancangan DB final memakai gram/subkoin. Validasi realisme starter memerlukan lintasan dari gerobak sampai mesin terbuka.

## Aturan eksperimen
Jumlah batch dibatasi stok kontrak, minimum kapasitas lini per fraksi, gudang 4.000 kg dan reservasi 4 koin/kg. Nilai reservasi konservatif bisa mengunci pemain sebelum kas nol. Pemain secara eksplisit menjual produk setelah pengolahan lalu membeli upgrade bila kas menyisakan modal awal. Permintaan kota per hari dibagi semua agen; harga dasar × variasi harian ±8% × (1 − min(0,5, penjualan/permintaan)). Pembelian dibatasi kuota sisa. Hitung integral harga marginal atas kuantitas terjual. Permintaan nol memberi penjualan nol. Sisa produk mengisi gudang.

Input + pembantu = produk + aliran terkendali + residu + perubahan stok untuk batas sistem yang dipilih. Pada benchmark ekonomi, input pembantu dinolkan, keluaran dipisah menjadi produk, aliran terlacak, landfill. Fraksi B3 ditransfer utuh. Resep uji gram dengan input pembantu terdapat di uji_batas.py. Massa gas/air aktual perlu review terpisah. Asumsi mutu tetap memenuhi ambang plastik ≥80%; koefisien produk efektif sudah mengandung rugi mutu. Tipping, angkut, opex, pajak simulasi termal, perawatan dan upgrade ×1,6 dihitung sebagai sink. Pemain membayar perawatan harian ketika beroperasi pada sesi pertama; skenario penundaan perawatan/penurunan 1% per hari perlu diuji saat alpha.

Poin pengalihan berbobot 1/3/2/4, B3 aman ×8, produk residu ×6. Kurangi landfill dan batasi 6.100 poin/hari. Premi BHI dan misi awal dinolkan untuk mengisolasi rute. Karma bertambah 0,013 per kg landfill dan pulih 0,002 per kg terkendali. Semua agen termal memakai kendali lengkap; tidak ada emisi bypass pada benchmark. Karma dijepit 0–100, pada 100 reset Karma dan poin, aset tetap. Pengalihan God diukur kumulatif; minimal kontribusi 6.000 kg [U]. Tier CSV berisi hari pertama mencapai, termasuk bila kemudian reset.

## Kota bersama, dua sesi per hari
Median per strategi, n=20 lintasan masing-masing (4 pemain × 5 benih, pasar bersama membuat hasil saling bergantung).

| Strategi | Saldo akhir | Poin akhir | Karma | Reset | Landfill kg | Kontribusi model kg | Mencapai God |
|---|---:|---:|---:|---:|---:|---:|---:|
| Organik | 411.282 | 321.644 | 0 | 0 | 24.979 | 253.772 | 0/20 |
| Plastik | 631.061 | 275.192 | 10,82 | 0 | 19.326 | 120.275 | 0/20 |
| Campuran | 624.712 | 47.688 | 27,91 | 2 | 48.729 | 215.171 | 0/20 |
| Termal terkendali | 375.672 | 506.705 | 0 | 0 | 12.498 | 361.552 | 20/20 |
| Landfill | 319 | 0 | 98,95 | 0 | 7.623 | 77 | 0/20 |

Untuk 100 pemain acuan, jumlah yang pertama mencapai tier 1–9 adalah 100, 80, 80, 80, 80, 80, 80, 59, 20. Di antara yang mencapai God, P10/median/P90 hari 68,2/72/78,8. Target 60–90 hari tercapai hanya oleh jalur termal pada kondisi ini. Jalur plastik memberi median saldo tertinggi. Uang beredar bersih bertambah median 621.061 koin per agen plastik dari modal 10.000. Ini indikator penciptaan uang; harga ditentukan sistem sehingga angka tersebut belum mengukur inflasi harga antarpemain. Pantau indeks keranjang harga saat trading tersedia.

## Uji tekanan dan kalibrasi
- Satu pemain: nol God pada kelima strategi dan lima benih; kuota pasar kecil menghambat penjualan. Kota tanpa pemain tidak membagi dengan nol, tidak mengadakan upacara.
- Ringan (1 sesi/hari) tidak menghasilkan God termal; berat (3 sesi/hari) 18/20 termal, median 76,5 hari. Lebih sering masuk bisa menguras permintaan lebih awal. Model memakai satu order rapat per sesi, tak mewakili semua kebiasaan manusia.
- Masuk hari 46: nol God hingga akhir. Separuh berhenti sesudah hari 30: hanya 10/20 termal pernah God; target kumulatif yang sudah terbit tetap. Pemain baru masih dapat mengejar reward tier. Jalur lintas musim perlu dipertahankan.
- Pasar jenuh 20% permintaan: median hari macet plastik 68, organik 54. Tanpa permintaan barang tetap tersimpan. Tanpa modal atau stok produksi nol selama 90 hari. Pemulihan gratis layak diuji dengan batas hibah yang hanya membayar satu batch kecil; larang klaim poin dari hibah.
- Dua request identik berurutan setiap sesi menghasilkan state identik untuk semua 100 pasangan acuan. Ini uji perilaku simulator; race database dan bot dengan key berbeda tetap harus diuji.
- Pengganda reset membuat median poin akhir campuran 53.202 versus 47.688. Uji analitik pemain adaptif pada 5.800 poin/hari: God hari 69 tanpa reset, hari 67 bila satu reset hanya memakan satu hari dengan bonus 10% dan cap 6.100. Biaya reset satu hari adalah skenario sensitivitas, belum dibuktikan pada progres starter. Usul bantuan belajar tanpa pengganda ranking.
- Kandidat misi: +2.200 poin satu kali sehari jika batch pertama menangani ≥500 kg dan landfill ≤10%. Organik mencapai God 17/20, median hari 81; termal 20/20, median 66,5. Ini menunjukkan dua jalur dapat hidup pada skenario bersama. Ambang batch tunggal masih menguntungkan mesin besar; uji alternatif kontribusi kumulatif harian dan akses pasar kota kecil.
- Di lima kota bersama acuan, meter mentah mencapai 100% tetapi upacara gagal karena residu melebihi batas. Counterexample ini disengaja disimpan di musim.csv. Simulator mengukur kapasitas olah terhadap target virtual; belum membatasi penerbitan tiap lot ke target kota. Aliran terkendali dan B3 dihitung dalam kontribusi proksi. Jangan memakai rumus proksi di rilis. TDD mendefinisikan meter tunggal berdasarkan gram asal tersertifikasi.
- Uji batas menutup sembilan contoh resep termasuk gas yang tersisa, serta interval 26 jam dengan cutoff jam 24 (6 jam musim lama, 2 jam baru). Ini verifikasi aritmetika, belum simulasi penuh dua musim.

## Syarat lulus pengujian ekonomi berikutnya
Pemilik menetapkan kebijakan kredit dan gate. Ulangi 90 hari dari starter dengan harga unlock/biaya tiga unit, pasokan kota terbatas per fraksi, penanganan B3 tersendiri, jalur nontermal, emisi bypass, reinkarnasi dan dua musim berurutan. Bandingkan beberapa strategi adaptif pada pasokan identik. Target usulan: ≥2 jalur layak God pada 60–90 hari dalam kota kecil dan bersama; tidak ada jalur unggul sekaligus dalam uang, progres dan dampak pada seluruh keadaan pasar; pemulihan tanpa pembayaran dalam satu sesi; nol upacara/meter yang bertentangan. Kalibrasi dengan target D1/D7 dan perilaku tester setelah alpha.

### Pemeriksaan kandidat penyelesaian
hasil/rollover.csv menguji formula tersertifikasi pada dua musim sintetik 90 hari. Musim pertama menerbitkan 90.000 g, 81.000 g material dan 9.000 g residu terkendali dalam anggaran, sehingga 100% dan upacara sama-sama benar. Pada musim kedua aktivitas turun di pertengahan musim, target 67.500 g tidak menyusut, hanya 64.125 g layak, meter 95%, tanpa upacara. Poin dan kas lanjut, denominator dan kredit musim kembali nol. Ini fixture keputusan D08 dengan kelayakan landfill terbatas, terpisah dari pasar dan kohort 20 pemain. Untuk pemulihan, uji voucher biaya batch 400 pada saldo 0/319/399/400/10.000: penggunaan mengisi tepat kekurangan dan tidak meninggalkan voucher cair. Di pasar permintaan nol, voucher saja tetap bisa menghasilkan gudang buntu; kontrak kerja harus menyediakan pembeli/imbalan jasa atas keluaran aktual.

## Penambahan Kebun Gaia

Eksperimen tambahan per petak, 90 hari dan 24 skenario: lihat KEBUN_GAIA.md, simulasi_kebun.py dan hasil/kebun.csv. Model kota di atas menjadi pembanding sebelum integrasi.

## Penambahan Simulasi Terintegrasi DWE + DLE + Kebun Gaia (v0.8 / D15–D21)
Jalankan `python3 simulasi_dwe_dle.py` dari direktori ini (deterministik terhadap 5 benih `konfigurasi.json`, hasil pada `hasil/dwe_dle_ringkasan.csv`, `hasil/dwe_dle_harian.csv`, dan `hasil/dwe_dle_uji_batas.csv`). Model menguji tiga node MVP (Permukiman, Pasar, Sungai) dalam satuan gram integer, overflow konservatif ke backlog TPA, WCS gerobak→pickup, Kebun Gaia tanpa kredit ganda, serta DLE (slot UTC 3 menit, cap 6 insiden/hari, maks 3 aktif, cap 12 kg/hari, expiry 15 menit ke backlog).

| Skenario (90 hari, 5 benih) | Median saldo akhir | Median poin akhir | Kontrak masuk (kg) | Bonus DLE (kg) | Porsi DLE | Selisih massa (g) |
|---|---:|---:|---:|---:|---:|---:|
| Tanpa DLE (`tanpa_dle`) | 20.415 | 16.873 | 9.000,0 | 0,0 | 0,00% | 0 |
| Dengan DLE normal (`dengan_dle`, 20%/slot) | 20.521 | 17.414 | 9.000,0 | 412,6 | 4,38% | 0 |
| Pencegahan tinggi (`pencegahan_tinggi`, 8%/slot) | 20.463 | 17.090 | 9.000,0 | 177,5 | 1,93% | 0 |

**Temuan utama Q26–Q28:**
- Seluruh 15 lintasan (3 skenario × 5 benih) menutup neraca massa tepat hingga **0 gram** dan lulus 6 uji batas (`dle_deterministik_reload`, `dle_dua_tab_klaim_sekali`, `dle_gudang_penuh_tolak`, `dle_b3_ditolak`, `wcs_reservasi_expiry_dan_kargo`, `dle_tidak_mengalahkan_kontrak`).
- Porsi material bonus DLE hanya **4,38%** dari total pasokan sehingga tidak mengalahkan kontrak WCS utama; saat pencegahan meningkat, insiden turun ke **1,93%** tanpa mematikan ekonomi pemain.
- Hasil ini melengkapi model kota v0.6; penutupan C1–C4 (dominasi God termal di kota bersama 20 agen dan satu definisi upacara D08) tetap menunggu penetapan pemilik sebelum gate Fase 1.
