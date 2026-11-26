# TERRA NOVA — G0 Audit, Conflict Matrix & Rollback Plan
**Tanggal:** 27 November 2026 · **Branch:** `dev/feature-freeze` · **Baseline Commit:** `main` (`12fa158`)  
**Backup Pre-Freeze:** `_backup/2026-11-27_pre_freeze/` (SQLite `PRAGMA integrity_check = ok`, 2 akun, 810 receipts)

---

## 1. Audit Repositori Baseline (v0.9 / Evaluasi 1–2)
- **Server (`server.py`, 1.106 baris):** Python 3 stdlib (`ThreadingHTTPServer` + SQLite), PBKDF2-SHA256 (240k iter), cookie `HttpOnly; SameSite=Lax`, rate-limit 8/10m, UUID idempotency receipt, Lazy Tick + DWE + DLE + Evaluasi 1 & 2.
- **Frontend (`web/landing.html`, `web/index.html`):** Painted isometric `yard_iso.webp` (1672×941), opening cinematic 120 dtk (`/intro/`), intro lahan sekali (`intro_selesai`), karakter pria & wanita, visibility-graph pathfinding, kendaraan 2 lajur, sampah pohon & kendaraan.
- **Pengujian Baseline:** 43/45 lulus pada uji awal; ditemukan 1 bug geometri (`TITIK_POHON` `(590, 258)` berada di dalam pagar & menabrak `OBST[1]` Area Pilah), plus 5 celah kode (`picking` nyangkut saat batal jalan, `terima_kargo` membuang komposisi fraksi node, Neraca Massa belum mencatat massa terjual/dipakai kebun, XSS kecil di `innerHTML`, `gender` hilang bila reload saat cinematic).

---

## 2. Conflict Matrix (v0.9 Aktual vs Feature Freeze v1.0)

| ID | Topik | Kondisi Repo v0.9 | Kontrak Feature Freeze v1.0 | Resolusi Implementasi (G1–G7) |
|---|---|---|---|---|
| **C01** | Modal awal & skala ekonomi | 1.000 GC (`prototype_v09`), harga jual 5–24 GC, angkut 2–6 GC | `Realistic_v1` (1 GC ≈ Rp1 nominal simulasi): **1.000.000 GC** uji utama, **100.000 GC** stress test; akun lama **tidak** dimigrasi paksa | Akun baru / reset memakai `Realistic_v1` (default 1.000.000 GC, opsi skenario 100.000 GC di admin/simulasi); akun lama tetap kompatibel tanpa menimpa saldo historis. |
| **C02** | Katalog material & mesin | 6 fraksi dasar & 3 produk jadi hardcoded di `server.py` | 282 material/produk (`02`) + 307 baris mesin/energi (`09 v1.2`: 288 canonical + 19 alias); semua terlihat, hanya resep tervalidasi aktif | `data/catalog_seed.json` memuat 100% 282 material & 307 mesin (alias diselesaikan sebelum transaksi); 21 mesin/alat rumah tangga–UMKM aktif, sisanya `locked_pending_validation` / `display_only`. |
| **C03** | Progresi Tier & God | Berbasis XP poin (`TIERS`: 0–400.000 poin) | **GT01–GT09** berbasis aksi/bukti receipt + **GSG** untuk God (tanpa wajib pabrik F3 / tanpa top-up / tanpa 400k XP) | Jalur utama memakai GT01–GT09 + GSG; poin XP tetap tercatat sebagai statistik historis tanpa mengunci jalur rumahan; 8 lencana §34 dipertahankan (`Saudagar Hijau` berbasis laba operasi kumulatif ≥ 2.000 GC untuk akun baru). |
| **C04** | Kebun & Pangan | 1 jenis sayur (`Kangkung Gaia`) + 3 varietas langka acak, 40 detik | **15 tanaman (`CR01–CR15`)** (10 umum 30–180 dtk, 5 langka 300–900 dtk), **Vitalitas (0–100)** tanpa decay offline, 4 bahan pokok NPC (beras/tempe/telur/air), rare boost ber-cap | Implementasi penuh `CR01–CR15`, vitalitas aktif-only (efek manual 60–110%), cap demand harian & cap rare boost 5.000 GC/hari, stok benih langka maks 1/varietas/minggu. |
| **C05** | Angkut & Misi Berkala | Gerobak 5–50 kg, tarif 2–6 GC, ETA 6 dtk, 3 node | Starter `MCH-002` 25 kg/trip, 5 node (Permukiman, Pasar, Sungai, Sekolah/Kantor, Restoran), rumus biaya realistis + kompensasi jasa, **TR01–TR05** (Asia/Jakarta) + rotasi alternatif 3 jam | Implementasi kontrak angkut realistis (quote → reserve → in_transit → arrived → received), fraksi node asli dipertahankan saat pilah, plus TR01–TR05 & rotasi 3 jam. |
| **C06** | Spawn & Sungai | 9 dalam + 12 luar, liar 90s, pohon 60s, kendaraan 40s, DLE §28 | Pertahankan semua spawn §32 + tambah **sampah sungai mengalir** (slot 75s, 50%, maks 4, lintasan 90s, pindah ke backlog hilir bila lewat), semua debit ledger lingkungan | Tambah `jatuh_sungai` & visual objek terapung di polyline `RIVER`, perbaiki `(590, 258)` keluar pagar, catat ledger lingkungan, kompensasi pungut realistis + cap harian. |
| **C07** | Energi (WtE & DRES) | Belum ada | Jalur rumahan–UMKM: Digester biogas (`WTE-002`), genset mikro (`WTE-015` sewa/beli), PLTS (`DRE-001..005`), mikrohidro/angin (`DRE-030`), baterai LFP (`DRE-075..077`), audit energi & provenance kWh | Implementasi `Energy Center` (Wh integer, rugi baterai, provenance waste-origin vs renewable tanpa double-count, opsi akses mitra berbayar GC untuk jalur rumahan). |
| **C08** | Pasar NPC, Bekas & Recovery | 7 tombol jual flat di sheet Pasar | Pasar NPC multi-kategori (Rongsok, Organik, Tani, Benih, Mekanik, Energi, Sehat, dll.), search/filter/pagination 24, quote expiry, pasar mesin bekas/sewa, recovery anti-deadlock | Endpoint `/catalog`, `/market/quote`, jual/beli atomik, jual mesin bekas (terdepresiasi, anti-arbitrase), sewa alat/mitra. |
| **C09** | Fitur Pendukung, Sosial & Monetisasi | Belum ada (Kota/Bumi terkunci) | Gaia Radio, Selebrasi (queue + skip/mute), Jurnal, Knowledge Center, Replay Opening (tanpa grant), Dukung TERRA NOVA (`support_url=null` aman), Top-Up Sandbox & Leaderboard Fixture lokal, Export Kartu PNG (3 ukuran), Admin Config lokal, Feedback, Chosen **hanya evaluasi kandidat internal (tidak aktif)** | Seluruh modul tersedia di Menu Terpadu dengan label `SANDBOX / FIXTURE LOKAL` yang jelas; zero pembayaran nyata, zero pengiriman data eksternal, Chosen final tidak diaktifkan. |
| **C10** | Status Keputusan K1–K7 & D03–D21 | K1–K7 terbuka; D03–D21 di `GAME_SPEC_DECISIONS.md` | K1 Bandung default + ganti kota manual; K2 pria/wanita; K4 replay tanpa grant; K5 Realistic_v1; K6 ledger spawn; K7 optimasi aset dulu (zero belanja fal.ai) | Semua arah K1–K7 diterapkan sesuai freeze; K3 (usia/privasi/hukum) & seleksi final Gaia's Chosen tetap ditandai `BLOCKED / KEPUTUSAN PEMILIK` pada Public Beta Readiness Checklist. |

---

## 3. Rencana Rollback per Gate
1. **Rollback Kode:** `git checkout main` atau `git reset --hard <commit-gate-sebelumnya>` pada branch `dev/feature-freeze`.
2. **Rollback Database:** Hentikan `server.py`, salin kembali `_backup/2026-11-27_pre_freeze/gaia.sqlite3` ke `gaia.sqlite3`, jalankan `PRAGMA integrity_check`.
3. **Kompatibilitas Akun Lama:** `migrasi_state()` selalu non-destruktif (`setdefault`) dan tidak mengubah saldo/riwayat akun v0.9 yang sudah ada.
