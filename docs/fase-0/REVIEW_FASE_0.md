# Review tambahan — 25 November 2026
Status: gate Fase 1 tetap ditahan. Paket asli dipertahankan; tambahan bukan persetujuan mekanik.

- SHA-256 baseline v0.6 cocok dengan GAME_SPEC_DECISIONS.md; salinan identik disertakan.
- Jalankan ulang `python3 simulasi.py`, `python3 uji_batas.py`, `python3 simulasi_kebun.py`: semua selesai tanpa error, tujuh CSV identik byte-for-byte terhadap ZIP asli. Ini bukti reproduksibilitas model, bukan validasi aplikasi.
- C1: God termal 20/20, empat strategi lain 0/20 pada skenario bersama; kandidat misi organik 17/20 masih perlu uji starter dan kota kecil.
- C2: meter proksi 100% dan upacara gagal; pilih definisi kredit D08, termasuk apakah landfill terkendali layak, lalu gunakan satu fungsi.
- C3: modal/stok nol buntu; kontrak pemulihan perlu pembeli/jasa nyata dalam simulasi, bukan voucher saja.
- C4: harga/unlock mesin dari starter, jalur alternatif, insentif reset dan cutoff dua musim belum ditutup. Q03 fixture membagi cap lintas cutoff; TDD menawarkan jeda cutoff, harus pilih satu lalu sesuaikan tes.
- D14: kebun 24 skenario standalone, harga tetap dan stok cukup; belum terintegrasi model kota, dosis terlambat belum disimulasikan. Integrasikan kas, kuota, gudang, kredit, cutoff dan biaya peluang. Tidak menambah poin dari kompos yang sudah dikreditkan.
- Visual: DESIGN_SPEC.md menutup gap onboarding, sprite, layout awal, responsif, kebun dan QA. Gambar mockup bukan angka atau aset produksi. Skema avatar/placement usulan saja.
- Roadmap menyebut delapan dokumen sebelum penambahan kebun; gunakan README ini sebagai indeks aktual, bukan jumlah lama.

Prioritas sebelum izin build: keputusan D03–D08 dan D14, simulasi ulang terintegrasi, perbarui induk setelah persetujuan, baru implementasi bertahap. Tidak ada kode aplikasi, DDL, pengujian browser/device atau audit keamanan produksi di paket ini.

## Urutan baca
TERRA_NOVA_GAME_SPEC_v0.6.md → GAME_SPEC_DECISIONS.md → REVIEW_FASE_0.md → DESIGN_SPEC.md → GAME_ECONOMY_MODEL.md → KEBUN_GAIA.md → TECHNICAL_DESIGN.md → DATABASE_SCHEMA.md → OPENING_STORYBOARD.md → PERFORMANCE_BUDGET.md → TEST_PLAN.md → IMPLEMENTATION_ROADMAP.md.

## Instruksi Antigravity
Baca seluruh paket dan references/gameplay-road-river.png serta gameplay-responsive.png. Pertahankan desain satu lahan 2D pixel art dengan jalan dan sungai. Jangan mengubah angka berdasarkan gambar. Kerjakan penutupan gate ekonomi Fase 0 dan proposal desain teknis visual dahulu; jangan mengubah database atau memulai Fase 1 tanpa izin pemilik. Laporkan konflik, keputusan yang diperlukan, hasil uji ulang, dan rencana spike renderer. Setelah izin diberikan, implementasikan satu scene playable dengan aset modular dan anggaran performa. Gunakan bahasa Indonesia.

## Status Sinkronisasi DWE + DLE (v0.8 / DESIGN_SPEC v1.3)
- Seluruh dokumen Fase 0 (`GAME_SPEC_DECISIONS.md`, `TECHNICAL_DESIGN.md`, `DATABASE_SCHEMA.md`, `GAME_ECONOMY_MODEL.md`, `TEST_PLAN.md`, `PERFORMANCE_BUDGET.md`, `OPENING_STORYBOARD.md`, `IMPLEMENTATION_ROADMAP.md`) telah disinkronkan terhadap `TERRA_NOVA_GAME_SPEC_v0.8.md` (D15–D21) dan `DESIGN_SPEC_v1.3.md` (UI-01 hingga UI-19).
- Seluruh skrip (`simulasi.py`, `uji_batas.py`, `simulasi_kebun.py`, `simulasi_dwe_dle.py`) telah dijalankan ulang dan reproducible (nol error, selisih massa 0 gram, 6 uji batas DWE+DLE lulus).
- Prototipe review lokal (`server.py` + `web/index.html`) telah diselaraskan dengan layout starter UI-09/UI-19 (satu lahan 2D pixel art isometrik + gerbang + jalan aspal + sungai), alur onboarding §2, DWE 3 node MVP, dan DLE jalan & sungai hidup untuk keperluan review pemilik. Gate Fase 1 produksi tetap menunggu penetapan akhir pemilik atas D03–D08, D14–D19, dan D21.
