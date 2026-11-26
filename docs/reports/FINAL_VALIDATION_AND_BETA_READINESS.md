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
Data mentah lengkap tersimpan di:
- `docs/reports/sim_180d_daily.csv` (1.080 baris harian across 6 skenario)
- `docs/reports/sim_180d_summary.csv`

| Skenario | Modal Awal | Hari 90 (Tier / Saldo) | Hari 180 (Tier / Saldo) | Hari Capai God (GSG) | Deadlock | Self-Made | Chosen Final |
|---|---:|---|---|---:|---:|---|---|
| `modest_1M_nopay` (Rumahan, gratis) | 1.000.000 GC | Ascendant / 2.726.650 GC | **God** / 7.627.200 GC | **Hari 142** | 0 | Ya | Nonaktif (provisional) |
| `modest_100k_stress` (Stress test 100k) | 100.000 GC | Ascendant / 1.826.650 GC | **God** / 6.727.200 GC | **Hari 142** | 0 | Ya | Nonaktif (provisional) |
| `industrial_1M_nopay` (Ekspansi lahan) | 1.000.000 GC | Titan / 2.859.750 GC | **God** / 7.350.950 GC | **Hari 156** | 0 | Ya | Nonaktif (provisional) |
| `paid_sandbox_1M_plus_5M` (+5M Sandbox) | 1.000.000 GC (+5M) | Ascendant / 7.726.650 GC | **God** / 12.627.200 GC | **Hari 142** | 0 | Tidak (Sandbox) | Nonaktif (provisional) |
| `low_activity_1M` (2 aksi/hari, tanpa biogas) | 1.000.000 GC | Guardian / 2.037.850 GC | Guardian / 2.037.850 GC | *Tidak tercapai* | 0 | Ya | Nonaktif |
| `cash_exhaustion_recovery` (Saldo dipaksa 0 GC) | 1.000.000 → 0 GC | Ascendant / 1.983.150 GC | **God** / 6.883.700 GC | **Hari 142** | 0 | Ya | Nonaktif (provisional) |

**Temuan Utama Simulasi:**
1. **Kesetaraan Jalur Rumahan & Industri Terbukti:** Pemain sederhana tanpa pabrik besar (`F3+`) dan tanpa top-up mencapai God (`GSG`) pada Hari ke-142, baik pada modal 1.000.000 GC maupun stress test 100.000 GC.
2. **Pay to Build, Play to Achieve Terbukti:** Tambahan modal sandbox +5.000.000 GC meningkatkan likuiditas ekonomi (+5M GC), tetapi **tidak** mempercepat pencapaian God (tetap Hari 142) dan otomatis menandai `self_made_provisional = False`.
3. **Anti-Deadlock Kas Terbukti:** Pada skenario `cash_exhaustion_recovery` (saldo dipaksa 0 GC di Hari 1), pemain berhasil pulih lewat jual mesin bekas terdepresiasi + pungut sampah gratis dan tetap mencapai God tanpa buntu.
4. **Skenario Gagal Tercatat Jujur:** `low_activity_1M` berhenti di `Guardian` karena tidak menjalankan siklus energi waste-origin (biogas) untuk GSG.

---

## 3. Laporan Regression, Security & Performance Testing
Skrip uji: `tools/test_feature_freeze.py` · Hasil JSON mentah: `docs/reports/regression_results.json`.
- **Total Regression & FF01–FF24:** **39/39 PASS (0 FAIL)**.
- **Keamanan:**
  - Path traversal (`/assets/../../server.py`) → diblokir `404`.
  - Unauthenticated `/state`, `/aksi`, `/admin/config`, `/feedback` → diblokir `401`.
  - Password PBKDF2-SHA256 (240k iter) + token sesi SHA-256 + `HttpOnly; SameSite=Lax` + rate-limit login (8 gagal/10m).
  - UUID idempotency receipt menolak replay dengan payload berbeda (`400`).
  - HTML escaping (`esc()`) diterapkan pada nama pemain, kota, katalog, leaderboard, dan feedback.
  - Material B3/berbahaya (`HZ01`) diblokir dari perdagangan bebas NPC; mesin edukasi risiko (`WTE-001`) dan terkunci (`HME-001`) diblokir dari pembelian.
  - Tidak ada email/usia/data pembayaran di endpoint `/leaderboard` atau ekspor Kartu PNG.
- **Performa Terukur:**
  - **API `/state` p95 latency (60 sampel):** **35,8 ms** (target ≤ 500 ms → **PASS**).
  - **Shell JS + HTML (gzip):** **34,4 KB** (target ≤ 250 KB → **PASS**).
  - **Snapshot `/state` JSON:** **15,5 KB** (target ≤ 20 KB → **PASS**).
  - **Catatan Aset Statis (Belum Dikompresi Lanjut):** Sprite PNG saat ini masih ~3,5 MB dan opening runtime ~4,0 MB (melebihi target budget 1 MB / 1,6 MB — dicatat sebagai item optimasi aset sebelum public beta tanpa biaya fal.ai tambahan).

---

## 4. Daftar Blocker & Keputusan Pemilik yang Masih Diperlukan
1. **[BLOCKER BETA] K3 — Kebijakan Usia 13+, Privasi, Consent Orang Tua, Lupa Sandi, Verifikasi Email & Hapus Akun:** Wajib review hukum & implementasi sebelum rilis publik.
2. **[KEPUTUSAN PEMILIK] Seleksi Akhir Gaia's Chosen:** Sengaja **tidak diaktifkan** (`final_selection_active: false`). Definisi peak wealth, periode musim, dan mekanisme upacara/penghormatan akhir menunggu keputusan pemilik.
3. **[KEPUTUSAN PEMILIK] Tautan Resmi Dukungan & Audio:** `support_url`, `sponsor_contact_url`, dan `soundtrack_url` (serta file lagu karya pemilik untuk Gaia Radio) masih `null` / WebAudio fallback sampai pemilik memberikan tautan & berkas resmi.
4. **[OPTIMASI PRA-BETA] Kompresi Aset & Uji Perangkat Nyata:** Konversi sprite PNG → WebP atlas untuk menekan ukuran dari ~3,5 MB ke ≤ 1 MB serta uji fisik di perangkat Android RAM 2 GB dan iOS Safari.
5. **[INFRASTRUKTUR BETA] Migrasi ke Server Produksi:** `ThreadingHTTPServer` + SQLite hanya untuk review lokal; rilis publik memerlukan Postgres/Supabase + RLS, HTTPS domain (`teranova.id`), payment gateway terverifikasi (bila top-up diaktifkan), dan load test.

---

## 5. Public Beta Readiness Checklist
- [x] Playable local prototype berjalan mulus (`http://127.0.0.1:8765`)
- [x] Backup pra-migrasi & rollback plan terverifikasi (`_backup/2026-11-27_pre_freeze/` + git branch `dev/feature-freeze`)
- [x] Katalog 282 material & 307 mesin (288 canonical + 19 alias) tervalidasi
- [x] 39/39 automated regression, security & performance checks PASS
- [x] Simulasi ekonomi 90 & 180 hari (6 skenario) selesai & CSV mentah tersimpan
- [x] Gaia's Chosen final selection tidak aktif; Sandbox Top-Up & Leaderboard dilabeli lokal
- [ ] Kompresi aset sprite PNG → WebP ≤ 1 MB & uji perangkat Android 2 GB / iOS
- [ ] Review hukum/privasi (K3), Google OAuth, dan infrastruktur produksi (Postgres/RLS/HTTPS)
- [ ] Penetapan tautan resmi donasi/sponsor/soundtrack & keputusan final Gaia's Chosen oleh pemilik
