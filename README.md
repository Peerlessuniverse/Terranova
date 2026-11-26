# TERRA NOVA — Peradaban Bumi Baru
Chapter I · The Calling of Gaia · Paket Fase 0 (v0.8 · DWE + DLE + Kebun Gaia)

## Mainkan simulasi review lokal
Gunakan Python 3.9 atau lebih baru (seluruh dependensi memakai pustaka standar Python). Pada Windows jalankan:

    py -3 server.py

Pada macOS atau Linux jalankan:

    python3 server.py

Buka http://127.0.0.1:8765 di browser. Progres tersimpan atomik pada `gaia.sqlite3` dengan kunci permintaan UUID idempotent. Server terikat ke loopback untuk penggunaan lokal.

## Fitur pada prototipe review lokal (v0.8 / DESIGN_SPEC v1.3)
- **Landing page + akun (`web/landing.html`):** Membuka `/` tanpa sesi menampilkan landing page (desain `Asset/Terra Nova_ Gaia’s New Civilization.png`) dengan form **Daftar / Login**. Tombol Google tampil sebagai "segera hadir".
  - **Daftar** → opening cinematic *The Calling of Gaia* (`cinematic-web/runtime`, disajikan di `/intro/`) langsung diputar tanpa tombol awal. Di akhir video ada **Aku menerima panggilanmu** dan **Ulangi cinematic**. Menerima panggilan → langsung ke lahan (karakter dan kota bawaan, nama = nama pengguna).
  - **Login** pemain lama → langsung ke lahan, tanpa video. Akun yang sudah daftar tapi belum menerima panggilan akan melihat cinematic lagi.
  - Jika browser memblokir suara otomatis (umumnya Safari/iOS), cinematic menampilkan satu tombol *Putar* sebagai cadangan.
  - Server: tabel `akun`, `sesi`, `pemain_akun` (progres per akun). Kata sandi PBKDF2-SHA256 (240.000 iterasi, salt per akun), token sesi hanya disimpan sebagai SHA-256, cookie `HttpOnly; SameSite=Lax` (+`Secure` otomatis bila di belakang proxy HTTPS yang mengirim `X-Forwarded-Proto: https`), batas 8 percobaan login gagal per IP per 10 menit. Endpoint: `POST /daftar`, `POST /masuk`, `POST /keluar`, `GET /akun`; `/state` dan `/aksi` wajib login. Tombol ⎋ di HUD = keluar; ↺ = reset progres akun (opening diputar lagi).
- **Lahan Starter Isometrik (UI-09 & UI-19):** Ilustrasi isometrik `web/assets/img/yard_iso.webp` (1672×941) sebagai latar: Gudang/Kantor, Area Pilah, Tumpukan Sampah, Gerobak, Kebun Gaia, Gerbang ke Jalan Aspal, dan Sungai. Area klik, avatar, NPC/mobil DLE (mengikuti kemiringan jalan), penanda insiden `!`, progres kebun, dan gerobak di jalan digambar di atasnya dalam koordinat gambar. HUD dan menu bawah bergaya mockup `Yard UI Comparison.png`. Responsif desktop dan mobile.
- **Dynamic Waste Ecosystem (DWE · D15–D19):** Tiga node sumber MVP (Permukiman, Pasar, Sungai) dengan stok gram integer, pengiriman Gerobak (`in_transit → arrived → received`), pemilahan 6 fraksi (termasuk B3 khusus), dan Neraca Massa.
- **Dynamic Living Environment (DLE · D20–D21):** Pejalan kaki & mobil sayur melintas secara kosmetik di jalan (cap 4 NPC + 2 kendaraan, jeda otomatis saat tab tersembunyi, dukung `reduced motion`). Insiden sah server (`npc_litter_river` di tepi sungai & `vegetable_spill` di bahu jalan) muncul dengan penanda `!` serta daftar misi aksesibel, klaim atomik, cek kapasitas gudang, dan expiry 15 menit ke backlog.
- **Kebun Gaia (D14):** Satu petak di dalam lahan starter, tanam benih, pupuk kompos (-25% sisa waktu tanpa kredit ganda), panen, dan buka varietas langka acak.

## Berkas Fase 0 (induk: GAME_SPEC v0.9 & DESIGN_SPEC v1.4; dokumen turunan masih v0.8)
- **Spesifikasi induk:** [TERRA_NOVA_GAME_SPEC_v0.9.md](docs/TERRA_NOVA_GAME_SPEC_v0.9.md) — §30–§36 memuat landing/akun, intro lahan, Evaluasi 1–2, ekonomi prototipe, celah & keputusan terbuka (histori: [v0.8](docs/TERRA_NOVA_GAME_SPEC_v0.8.md), [v0.7](docs/TERRA_NOVA_GAME_SPEC_v0.7.md), [v0.6](docs/GAME_SPEC_v0.6.md))
- **Desain visual:** [DESIGN_SPEC_v1.4.md](docs/fase-0/DESIGN_SPEC_v1.4.md) ([DESIGN_SPEC.md](docs/fase-0/DESIGN_SPEC.md), histori [v1.3](docs/fase-0/DESIGN_SPEC_v1.3.md), [v1.2](docs/fase-0/DESIGN_SPEC_v1.2.md)) & referensi pengembang di `docs/fase-0/references/`
- **Keputusan & review:** [UPDATE_README.md](docs/fase-0/UPDATE_README.md), [REVIEW_FASE_0.md](docs/fase-0/REVIEW_FASE_0.md), [GAME_SPEC_DECISIONS.md](docs/fase-0/GAME_SPEC_DECISIONS.md) (D01–D21), [KEBUN_GAIA.md](docs/fase-0/KEBUN_GAIA.md)
- **Teknis & QA:** [TECHNICAL_DESIGN.md](docs/fase-0/TECHNICAL_DESIGN.md), [DATABASE_SCHEMA.md](docs/fase-0/DATABASE_SCHEMA.md), [OPENING_STORYBOARD.md](docs/fase-0/OPENING_STORYBOARD.md), [PERFORMANCE_BUDGET.md](docs/fase-0/PERFORMANCE_BUDGET.md), [TEST_PLAN.md](docs/fase-0/TEST_PLAN.md) (Q01–Q28), [IMPLEMENTATION_ROADMAP.md](docs/fase-0/IMPLEMENTATION_ROADMAP.md)
- **Model ekonomi & simulasi:** [GAME_ECONOMY_MODEL.md](docs/fase-0/GAME_ECONOMY_MODEL.md), skrip `simulasi.py`, `uji_batas.py`, `simulasi_kebun.py`, `simulasi_dwe_dle.py`, dan hasil CSV di `docs/fase-0/hasil/`

## Evaluasi 1 (pengayaan gameplay)
- **Sprite isometrik** (`web/assets/sprites/`, dibuat dengan `tools/gen_assets_fal.py` memakai fal.ai nano-banana + birefnet, gaya mengikuti ilustrasi lahan): pemain (duduk, menoleh, berdiri, berjalan depan/belakang), 3 pejalan kaki, 3 kendaraan (pikap sayur, truk boks, motor sampah roda tiga untuk gerobak), 8 jenis sampah, 4 tahap petak tanam, 8 lencana. Biaya pembuatan tercatat di `Asset/generated/cost_ledger.json`.
- **Intro di lahan** (sekali, `intro_selesai`): lahan berantakan → sinar cahaya → karakter muncul duduk kebingungan, menoleh kiri-kanan, berdiri → pesan Gaia → *Cara Bermain* → HUD muncul.
- **Bergerak keluar pagar:** karakter berjalan lewat gerbang dan mengitari pagar (graf visibilitas), tidak bisa menembus pagar/bangunan/sungai atau keluar dari batas gambar.
- **Modal awal 1.000 koin** untuk akun baru (akun lama tetap). Koin dari memungut sampah (+2), mengolah, dan menjual.
- **Sampah liar:** 9 titik di dalam pagar + 24 titik di luar (rumput, depan pagar, tepi sungai), 8 jenis dengan fraksi masing-masing (kantong campur → Area Pilah, baterai → B3). Sampah baru muncul di luar pagar tiap 90 detik (maks 16).
- **Pengembangan lahan:** 3 petak tanam tambahan (250/500/750 koin) di sisi kanan lahan, perluasan gudang +250 kg (400/800 koin).
- **Pencapaian:** 8 lencana dihitung server (`meta.pencapaian`), pratinjau di Profil (ketuk avatar di HUD) dan halaman Pencapaian.
- **Menu terpadu** (tombol Menu di HUD dan menu bawah): Misi, Pencapaian, Profil, Pabrik, Kebun, Kembangkan Lahan, Angkut, Pasar, Gudang & Neraca, Cara Bermain, Kota/Bumi (terkunci), musik, suara, mulai ulang, keluar.

## Evaluasi 2
- **Karakter wanita** (`playerf_*.png`, pose sama dengan pria). Dipilih saat daftar (landing) dan bisa diganti di Profil (`ganti_karakter`).
- **Kendaraan tampak samping** (`veh_*_1.png`, `vehicles2_3/4`): pikap sayur, truk boks, motor, sepeda, becak, delman, motor sampah (gerobak saat angkut). Semua jenis berjalan di kedua lajur (`RL`), dicerminkan sesuai arah, dan dimiringkan mengikuti jalan.
- **Sampah jatuh dari kendaraan:** server menjadwalkan secara acak (slot 40 detik, peluang 45%, maks 5 di jalan) dengan jenis kendaraan, arah, dan isi. Klien menampilkan kendaraan itu melintas dan sampah muncul tepat saat dijatuhkan.
- **Sampah organik dari pohon:** daun kering, ranting, dahan patah, buah busuk (`pohon_*.png`) jatuh di dekat 10 pohon sekitar lahan (slot 60 detik, maks 6), dengan animasi daun berguguran; daun tunggal juga berguguran sesekali sebagai suasana.

## Final Feature Freeze v1.0 (27 November 2026 · branch `dev/feature-freeze`)
- **Ekonomi Realistis (`Realistic_v1`):** Modal uji utama 1.000.000 GC (dan opsi stress test 100.000 GC), 500 kg gudang, 3 benih starter (`CR01` ×2, `CR02` ×1), akun v0.9 lama dipertahankan tanpa menimpa saldo historis.
- **Katalog Canonical Utuh (`data/catalog_seed.json`):** 282 material/produk, 307 mesin & energi (288 canonical + 19 alias), 15 tanaman (`CR01–CR15`), 4 pangan pokok NPC. Semua dapat dicari & dipelajari (paginated 24/halaman); mesin tanpa resep tervalidasi dan `WTE-001` (edukasi risiko) terkunci aman.
- **Gameplay Lengkap:** Misi Tier `GT01–GT09` + `GSG` (God tanpa wajib pabrik besar / top-up), misi tambahan `PR01–PR10`, angkut realistis 5 node + misi berkala `TR01–TR05` (WIB + rotasi 3 jam), sampah sungai mengalir (`pungut_sungai` + backlog hilir), 15 tanaman + Vitalitas (0–100, tidak turun offline), Energy Center rumahan (`WTE-002`, `WTE-015`, `DRE-001..005`, `DRE-030`, `DRE-075..077`), penempatan mesin modular 6 slot, pasar mesin bekas & sewa, Gaia Radio, Selebrasi, Jurnal & Export Kartu PNG (3 ukuran), Knowledge Center, Replay Opening (tanpa hadiah), Admin Config Lokal + Audit + Rollback, Feedback lokal, Sandbox Top-Up & Fixture Leaderboard 14 papan. Seleksi akhir *Gaia's Chosen* sengaja tidak diaktifkan.
- **Pengujian & Simulasi:** Jalankan `py -3 tools/test_feature_freeze.py` (39/39 PASS) dan `py -3 tools/simulate_economy_180d.py` (simulasi 90 & 180 hari, 6 skenario). Laporan lengkap di `docs/reports/FINAL_VALIDATION_AND_BETA_READINESS.md`.

## Menaruh di domain (mis. teranova.id)
Server ini terikat ke `127.0.0.1:8765`. Untuk domain publik, jalankan di VPS dan pasang reverse proxy HTTPS (Caddy atau Nginx) yang meneruskan ke `127.0.0.1:8765` serta mengirim header `X-Forwarded-Proto` dan `X-Forwarded-For`. Tanpa HTTPS, cookie sesi tidak diberi flag `Secure`. `ThreadingHTTPServer` + SQLite cukup untuk uji coba tertutup; untuk peluncuran publik tetap mengikuti rencana infrastruktur produksi di bawah.

## Batas prototipe & gate Fase 1
Prototipe ini memakai satu pemain lokal, waktu perjalanan/tumbuh dipercepat untuk review, serta tab **Kota** dan **Bumi** berlabel terkunci (Fase 3). Infrastruktur produksi (Next.js/Supabase/RLS), akun terpisah, pasar antarpemain, musim, dan upacara menunggu penetapan akhir pemilik atas gate Fase 0 (D03–D08, D14–D19, D21).
