# TERRA NOVA — Final Validation, Economy Simulation & Public Beta Readiness Report
**Tanggal:** 27 November 2026 · **Versi:** Feature Freeze v1.0 (`Realistic_v1`) · **Branch:** `dev/feature-freeze`  
**Backup Pre-Freeze:** `_backup/2026-11-27_pre_freeze/`

---

## 1. Ringkasan Eksekutif Deliverables
- **Playable Local Prototype:** Berjalan lokal via `py -3 server.py` di `http://127.0.0.1:8765` (Python 3 stdlib + SQLite WAL, zero external paid dependencies).
- **Katalog Canonical Utuh:** `data/catalog_seed.json` memuat **282 material/produk**, **307 mesin & energi (288 canonical + 19 alias)**, **15 tanaman (`CR01–CR15`)**, dan **4 bahan pangan pokok NPC**. Seluruh katalog dapat dicari/dipelajari (paginated 24/halaman); hanya 22 mesin rumah tangga–UMKM tervalidasi yang aktif, sisanya berstatus `locked_pending_validation` atau `display_only` (termasuk `WTE-001` insinerator edukasi risiko dan `HME-001..006`).
- **Dokumen Tersinkronisasi:** `TERRA_NOVA_GAME_SPEC_v0.10.md`, `DESIGN_SPEC_v1.5.md`, `00_FEATURE_FREEZE.md`, seluruh katalog `docs/catalogs/*`, serta 7 dokumen `docs/fase-0/*.md` telah digabung dengan kontrak `*_SYNC_v1.0.md` tanpa menimpa histori versi lama (`v0.6–v0.9`, `v1.2–v1.4`).
- **Audit & Conflict Matrix:** `docs/G0_AUDIT_AND_CONFLICT_MATRIX.md`.

---

## 2. Laporan Simulasi Ekonomi 90 & 180 Hari
> **Diperbarui 27 November 2026 (pasca Evaluasi 2–3).** Hasil versi sebelumnya (God hari 142) tidak berlaku lagi:
> sejak perbaikan B5 audit neraca wajib dijalankan sebagai aksi, sedangkan simulator lama tidak pernah menjalankannya
> sehingga semua skenario macet di Seeker. `tools/simulate_economy_180d.py` kini menjalankan audit setelah batch baru,
> dan CSV di bawah dibuat ulang dengan engine terbaru (termasuk panel surya waktu nyata WIB).

Data mentah lengkap tersimpan di:
- `docs/reports/sim_180d_daily.csv` (1.080 baris harian, 6 skenario)
- `docs/reports/sim_180d_summary.csv`

| Skenario | Modal Awal | Hari 90 (Tier / Saldo) | Hari 180 (Tier / Saldo) | Hari Capai God (GSG) | Deadlock | Self-Made | Chosen Final |
|---|---:|---|---|---:|---:|---|---|
| `modest_1M_nopay` (Rumahan, gratis) | 1.000.000 GC | Ascendant / 1.790.050 GC | **God** / 6.638.250 GC | **Hari 179** | 0 | Ya | Nonaktif (provisional) |
| `modest_100k_stress` (Stress test 100k) | 100.000 GC | Ascendant / 890.050 GC | **God** / 5.738.250 GC | **Hari 179** | 0 | Ya | Nonaktif (provisional) |
| `industrial_1M_nopay` (Ekspansi lahan) | 1.000.000 GC | Ascendant / 840.050 GC | **God** / 5.688.250 GC | **Hari 179** | 0 | Ya | Nonaktif (provisional) |
| `paid_sandbox_1M_plus_5M` (+5M Sandbox) | 1.000.000 GC (+5M) | Ascendant / 6.790.050 GC | **God** / 11.638.250 GC | **Hari 179** | 0 | Tidak (Sandbox) | Nonaktif (provisional) |
| `low_activity_1M` (2 aksi/hari, tanpa biogas) | 1.000.000 GC | Recycler / 1.495.750 GC | Guardian / 1.968.750 GC | *Tidak tercapai* | 0 | Ya | Nonaktif |
| `cash_exhaustion_recovery` (Saldo dipaksa 0 GC) | 1.000.000 → 0 GC | Ascendant / 1.047.550 GC | **God** / 5.895.750 GC | **Hari 179** | 0 | Ya | Nonaktif (provisional) |

**Temuan Utama Simulasi:**
1. **Jalur rumahan & industri tetap setara:** semua skenario aktif mencapai God (GSG) di hari yang sama tanpa pabrik besar (`F3+`) dan tanpa top-up, termasuk modal 100.000 GC.
2. **Pay to Build, Play to Achieve tetap berlaku:** +5.000.000 GC sandbox menambah saldo tetapi **tidak** mempercepat God, dan menandai `self_made_provisional = False`.
3. **Anti-deadlock kas tetap terbukti:** saldo dipaksa 0 GC pulih lewat jual mesin bekas + pungut sampah gratis.
4. **Keputusan pemilik (Evaluasi 4): God tidak dibatasi waktu.** Pada pola simulasi God tercapai di hari 179; ini bukan batas, God tercapai seiring pemain menambah pencapaian. Syarat paling lambat adalah 200 kg pulih, lalu 10 kWh listrik dari sampah. Energi terbarukan ±41 kWh/180 hari karena panel surya mengikuti waktu nyata. Efek produksi alat dasar (Evaluasi 4) tidak mengubah jalur simulasi karena alat starter memberi kapasitas yang sama dengan sebelumnya.
5. **Skenario gagal dicatat jujur:** `low_activity_1M` berhenti di Guardian karena tidak menjalankan siklus biogas.

---

## 3. Laporan Regression, Security & Performance Testing
Skrip uji: `tools/test_feature_freeze.py` · Hasil JSON mentah: `docs/reports/regression_results.json`.
- **Total Regression & FF01–FF26:** **85/85 PASS (0 FAIL)**, termasuk tata lahan seret-dan-jatuhkan (E3), progress misi, filter katalog, format angka Indonesia, dan anggaran snapshot yang kini benar-benar diperiksa (sebelumnya tidak dicek).
- **Keamanan:**
  - Path traversal (`/assets/../../server.py`) → diblokir `404`.
  - Unauthenticated `/state`, `/aksi`, `/admin/config`, `/feedback` → diblokir `401`.
  - Password PBKDF2-SHA256 (240k iter) + token sesi SHA-256 + `HttpOnly; SameSite=Lax` + rate-limit login (8 gagal/10m).
  - UUID idempotency receipt menolak replay dengan payload berbeda (`400`).
  - HTML escaping (`esc()`) diterapkan pada nama pemain, kota, katalog, leaderboard, dan feedback.
  - Posisi alat divalidasi server (lahan, bangunan, pohon, pagar, jalan, tumpang tindih); klien hanya pratinjau.
  - Material B3/berbahaya (`HZ01`) diblokir dari perdagangan bebas NPC; mesin edukasi risiko (`WTE-001`) dan terkunci (`HME-001`) diblokir dari pembelian.
  - Tidak ada email/usia/data pembayaran di endpoint `/leaderboard`, `/meta-statis`, atau ekspor Kartu PNG.
- **Performa Terukur:**
  - **API `/state` p95 latency (60 sampel):** **35,4 ms** (target ≤ 500 ms → **PASS**).
  - **Shell JS + HTML (gzip, termasuk `tn_mesin.js`):** **52,2 KB** (target ≤ 250 KB → **PASS**).
  - **Snapshot `/state` JSON:** **15,6 KB** (target ≤ 20 KB → **PASS**). Sempat 21,4 KB setelah fitur Evaluasi 3; teks misi, geometri lahan, dan paket statis kini dikirim sekali lewat `GET /meta-statis`.
  - **Aset statis:** sprite PNG dikonversi ke WebP (2,7 MB → ±0,68 MB untuk semua sprite terpakai; pemain hanya memuat sprite gendernya); latar `yard_iso.webp` 321 KB; transfer awal gameplay ±0,94 MB (target ≤ 3 MB). Opening: transfer awal ±1,2 MB (gambar adegan pertama + audio Opus 692 KB), sisa adegan di-stream setelah film mulai (target ≤ 1,6 MB awal). Kualitas gambar opening belum diturunkan; perlu perbandingan visual dahulu.

---

## 4. Daftar Blocker & Keputusan Pemilik yang Masih Diperlukan
1. **[BLOCKER BETA] K3 — Kebijakan Usia 13+, Privasi, Consent Orang Tua, Lupa Sandi, Verifikasi Email & Hapus Akun:** Wajib review hukum & implementasi sebelum rilis publik.
2. **[KEPUTUSAN PEMILIK] Seleksi Akhir Gaia's Chosen:** Sengaja **tidak diaktifkan** (`final_selection_active: false`). Definisi peak wealth, periode musim, dan mekanisme upacara/penghormatan akhir menunggu keputusan pemilik.
3. **[KEPUTUSAN PEMILIK] Tautan Resmi Dukungan & Audio:** `support_url`, `sponsor_contact_url`, dan `soundtrack_url` (serta file lagu karya pemilik untuk Gaia Radio) masih `null` / WebAudio fallback sampai pemilik memberikan tautan & berkas resmi.
4. **[OPTIMASI PRA-BETA] Uji Perangkat Nyata:** kompresi aset sudah selesai (lihat §3); uji fisik di Android RAM 2 GB dan iOS Safari belum dilakukan.
6. **[DIPUTUSKAN] Kalibrasi:** God tanpa batas waktu; alat dasar kini punya efek produksi nyata (meja pilah, komposter, tong terpilah, timbangan, rak, bak, pencacah); harga alat tetap ("start small") dengan petunjuk menambah koin lewat kerja angkut.
7. **[SCOPE BELUM LENGKAP] Pasar NPC material:** beli/jual material per kios kategori (Rongsok, Organik, Tani, …) dengan bid/ask dan kuota belum ada; pasar baru menjual 5 produk olahan + hasil panen. Juga belum ada: putar ulang selebrasi dari Jurnal, pengingat waktu bermain sehat, dan alat sebagai penghalang jalan karakter.
5. **[INFRASTRUKTUR BETA] Migrasi ke Server Produksi:** `ThreadingHTTPServer` + SQLite hanya untuk review lokal; rilis publik memerlukan Postgres/Supabase + RLS, HTTPS domain (`teranova.id`), payment gateway terverifikasi (bila top-up diaktifkan), dan load test.

---

## 5. Public Beta Readiness Checklist
- [x] Playable local prototype berjalan mulus (`http://127.0.0.1:8765`)
- [x] Backup pra-migrasi & rollback plan terverifikasi (`_backup/2026-11-27_pre_freeze/` + git branch `dev/feature-freeze`)
- [x] Katalog 282 material & 307 mesin (288 canonical + 19 alias) tervalidasi
- [x] 85/85 automated regression, security & performance checks PASS
- [x] Simulasi ekonomi 90 & 180 hari (6 skenario) dibuat ulang dengan engine terbaru & CSV mentah tersimpan (God hari 179 pada pola simulasi; tanpa batas waktu sesuai keputusan pemilik)
- [x] Gaia's Chosen final selection tidak aktif; Sandbox Top-Up & Leaderboard dilabeli lokal
- [x] Kompresi aset sprite PNG → WebP (transfer awal gameplay ±0,94 MB)
- [ ] Uji perangkat fisik Android 2 GB / iOS
- [x] Map Pasar dengan 7 kios NPC (tampilan prosedural; ilustrasi & sprite pedagang fal.ai menunggu izin eksekusi)
- [ ] Jual-beli material mentah per kios (bid/ask, kuota)
- [ ] Review hukum/privasi (K3), Google OAuth, dan infrastruktur produksi (Postgres/RLS/HTTPS)
- [ ] Penetapan tautan resmi donasi/sponsor/soundtrack & keputusan final Gaia's Chosen oleh pemilik
