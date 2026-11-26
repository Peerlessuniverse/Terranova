# Rencana QA dan bukti kelulusan
Status **M** = sudah dijalankan pada model lokal, **M/P** = contoh model lulus tetapi implementasi wajib diuji, **P** = pengujian terencana, **F** = ditemukan hasil yang menahan gate. Catat versi aturan, skenario, benih, perangkat, build, waktu server, hasil aktual dan artefak. Simpan data tester tersamarkan.

| ID/status | Persiapan dan aksi | Oracle / bukti penerimaan |
|---|---|---|
| Q01 M/P | Jalankan seluruh benih dua kali, cek per batch dan per wallet. | CSV identik, massa masuk=semua aliran keluar, kas awal+sumber−sink=kas akhir, stok/uang nonnegatif. Di DB ulangi pada gram/subkoin hingga batas angka. |
| Q02 M/P | Sembilan resep dan rantai termal dengan udara, air, nutrien, aditif, lumpur dan gas sisa. Ulang dengan kemurnian 79,99/80%, throughput nol. | Contoh numerik menutup hingga gram; input kualitas rendah tetap tersimpan/dialihkan. Pisahkan kWh. Penelaah sains menandatangani resep final. |
| Q03 M/P | 26 jam offline dengan batas musim di jam 24, retry pada jam sama, >8 jam lagi, jam klien berubah. | Model segmen [18,24), [24,26); refresh = nol; server menjadi acuan. Uji pembulatan saat interval dibagi dan versi resep berubah. |
| Q04 M/P | Duplikasi seluruh aksi model. Di staging buka dua tab, balapan upgrade/jual lalu putus jaringan sesudah commit. | Model 100 pasangan setara. Di DB satu receipt, satu mutasi dan saldo sama; key dengan payload berbeda ditolak, key baru tak menggandakan starter/misi. |
| Q05 P | Kosongkan satu input, penuhkan gudang salah satu output, uang cukup untuk sebagian batch, mesin berbagi bahan, upgrade di tengah durasi. | Throughput minimum benar, semua keluaran punya ruang, batch lama memakai versi lama; produksi yang tertahan tidak dapat diklaim belakangan. |
| Q06 M/F | Lima strategi, satu/20 pemain, ringan/berat, pasar 20% dan kuota nol, modal/stok nol. | CSV ringkasan; nihil saldo negatif. Dominasi God termal dan kebuntuan gratis belum lulus. Uji ulang dua rute serta pemulihan tanpa pembayaran. |
| Q07 M/P | Karma tepat di bawah/tepat 50/75/100; uji pengganda dan pemain adaptif. | Peringatan sekali per lintasan naik, reset/retensi aset persis matriks. Model sensitivitas menunjukkan insentif reset. UI menjelaskan konsekuensi sebelum reset. |
| Q08 P | Termal terkendali/bypass, nontermal, God pada batas Karma 25%, pengalihan 90%, poin 400.000; Alkimia hari ke-29/30, Karma 10%. | Semua gate AND berlaku, gas fisik tetap tercatat. Hari aktif dihitung sekali hanya dengan operasi sah. Kunci hadiah dideduplikasi. |
| Q09 M/F | Kota kosong, baru hari 46, pemain churn, cap, event banjir, musim sukses/gagal. | Target kumulatif monoton, T=0 aman. Hasil uji menunjukkan proksi ZWM=100 dan upacara gagal; wajib selaraskan satu fungsi kelayakan. |
| Q10 P | Finalizer dan pemain berlomba di 23:59:59/00:00 UTC; worker mati setelah tulis subtotal; replay ledger lama terlambat commit. | Satu alokasi per event, tidak ada gap/waktu ganda, snapshot cocok rekonsiliasi. Hadiah, Hall dan carry-over sekali. |
| Q11 P | Lot dipilah, dijual, ditransfer, diproses ulang. Dua pembeli memesan stok terakhir. | Massa dan kredit maksimum dibagi pada turunan; poin ekonomi tidak kembali dari transfer. Satu transaksi pembelian memenuhi stok, sisanya gagal/parsial sesuai konfirmasi. |
| Q12 P | Uji matriks tamu/A/B/worker/editor, termasuk akses langsung tabel dan kolom privat, log, bundle dan cache. | Akses lintas akun ditolak server, kunci istimewa/atribut umur tak terekspos, moderasi tidak membuka akses wallet. Data citra/nama publik tersanitasi. |
| Q13 P | Lewati, ulangi, putus di tiap langkah, nama bentrok, kota tanpa data, akun legacy, audio/ilustrasi gagal. | Bisa lanjut dan bermain tanpa admin, starter sekali. Subtitle/mute/volume/reduced motion, fokus keyboard, daftar aksi tanpa drag. Tidak ada GPS. Aksi pertama ≤3 menit setelah setup. |
| Q14 P | Uji kelas umur sebelum signup dan hadiah saat cutoff, musim menang/gagal, kondisi Perwakilan belum terpenuhi. | Reward netral sesuai §7g bagi pemain di bawah 18; tidak ada konten dewasa untuk anak. Tahan rilis hingga kebijakan kelayakan hadiah disahkan. |
| Q15 P | Bandingkan akun identik berkosmetik dan biasa, pembelian ulang/redeem ganda. | State ekonomi, akses tier dan probabilitas hadiah identik. Grant kosmetik tepat sekali. |
| Q16 P | Jalankan matriks perangkat/beban dan soak sesuai PERFORMANCE_BUDGET.md. | Lampirkan trace, ukuran aset, latensi dan konsumsi memori perangkat nyata. Perbaiki regresi sebelum tambah cohort. |
| Q17 P | Pulihkan backup staging, putar ulang ledger, jalankan aplikasi versi sebelumnya, matikan flag pasar/season. | Login dan inventaris konsisten, settlement/receipt tidak hilang; catat durasi aktual dan selisih data. Tetapkan RPO/RTO sebelum rilis. |
| Q18 P | Editor mencoba merilis fakta tanpa tahun/cakupan/izin; data kota tidak tersedia. | Publikasi ditolak, fallback berjalan, fakta dan simulasi terpisah, sumber dapat dibuka, statistik proyeksi berlabel. |

**Indikator beta.** D1 ≥30%, D7 ≥10% dari cohort signup yang layak dengan jendela kembali didefinisikan sebelum beta; median sesi aktif 5–10 menit. Di antara pemain yang menghasilkan emisi, ≥60% memasang Konverter sebelum reset; di antara yang pernah mencapai Archon, <25% mengalami reinkarnasi [U]. Ukur completion onboarding, skip, waktu setup→aksi bermakna, langkah abandonment, first sale, error settlement dan retensi per kota dengan minimum sampel agar identitas tidak terungkap. Rasio donasi <2% adalah perkiraan, bukan syarat kelulusan. Event analitik cukup nama event, pseudonim, versi, cohort dan timestamp; tanpa email, GPS atau isi laporan.

**Keputusan QA.** Hanya artefak offline telah diuji. Prioritas penutupan: C1 ketimpangan rute God, C2 meter musim dan upacara, C3 pemulihan modal gratis, C4 harga/akses mesin dari starter. Security, beban, UX anak dan recovery operasional harus memiliki bukti terpisah di fase yang sesuai.

## Penambahan Kebun Gaia

Q19 [P] • Jalankan kasus kebun, gudang, ledger, unlock langka dan akses silang yang dirinci di KEBUN_GAIA.md. hasil/kebun.csv hanya bukti pengujian ekonomi lokal.

## Penambahan Visual, DWE & DLE (v0.8 / DESIGN_SPEC v1.3)

| ID/status | Persiapan dan aksi | Oracle / bukti penerimaan |
|---|---|---|
| Q20 P | Screenshot desktop 1366×768 dan mobile 360×800/390×844 pada scene pabrik + onboarding. | Lahan yang sama tampil, gerbang/jalan/sungai tidak terpotong tanpa cara pan, HUD terbaca, target sentuh ≥44 CSS px, tanpa scroll horizontal. |
| Q21 P | Hit-test tiap objek pada berbagai zoom/pan, collision pagar/sungai, depth sorting, daftar aksi fallback, sentuhan ganda. | Tap/klik akurat, avatar tidak menembus pagar/sungai, tidak ada aksi ganda akibat double tap, seluruh aksi dapat dijalankan lewat menu daftar/keyboard. |
| Q22 P | Seluruh slot avatar, dua karakter pria/wanita, payload kombinasi invalid, resume profil, hak kosmetik. | Kombinasi invalid ditolak server, profil kembali utuh saat refresh, tidak membocorkan data privat, kemampuan & ekonomi identik. |
| Q23 P | Tutorial skip/resume/replay, putus jaringan saat aksi, modal pending, retry receipt, cek dialog Gaia. | Starter tidak ganda, tidak ada perubahan saldo spekulatif, receipt konsisten, dialog awal tidak membocorkan twist Neraca Massa. |
| Q24 P | Ukur budget tekstur GPU (≤16 MiB), 30 menit soak pindah scene, pause saat tab hidden, fallback renderer. | Tidak ada kebocoran listener/tekstur, ticker/audio berhenti saat tab tersembunyi, FPS & memory trace perangkat nyata tercatat. |
| Q25 P | Kebun Gaia flag off/on, sprite tanah/tunas/matang sesuai server, timer matang, gudang penuh, klaim langka retry. | Flag off menampilkan tanah non-interaktif; gudang penuh menahan panen; klaim langka idempotent; tanpa kredit lingkungan ganda (terhubung Q19). |
| Q26 M/P | DWE: overflow stok node ke lingkungan/TPA, komposisi 100%, dua pemain/tab berebut stok terakhir, expiry reservasi sebelum muat, kargo tiba saat gudang penuh, B3 ditolak dari olah umum. | Konservasi gram terpenuhi (`simulasi_dwe_dle.py` lulus model); hanya satu klaim stok berhasil; kargo `in_transit` tidak hilang; tidak ada kredit ganda saat transfer/olah ulang. |
| Q27 M/P | DLE: reload & dua tab pada slot sama, klaim ganda dua tab, sumber kosong, cap harian 6 insiden / 12 kg UTC, expiry 15 menit ke backlog, offline >8 jam, gudang penuh, reduced motion. | RNG deterministik tidak meroll ulang saat reload; pickup hanya sukses sekali; expiry memindahkan massa ke backlog tanpa menghapus gram; gudang penuh menolak pickup tanpa mengubah sprite/stok. |
| Q28 M/P | Simulasi 90 hari terintegrasi DWE + DLE (dengan vs tanpa bonus DLE) + Kebun Gaia pada 5 benih (`simulasi_dwe_dle.py`). | CSV `dwe_dle_ringkasan.csv`, `dwe_dle_harian.csv`, `dwe_dle_uji_batas.csv` reproducible; bonus DLE tidak mengalahkan kontrak utama; pencegahan menurunkan insiden tanpa mematikan ekonomi. |
