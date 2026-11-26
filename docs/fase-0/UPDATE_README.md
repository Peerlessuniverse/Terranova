# TERRA NOVA — DWE + DLE update

Baca `../TERRA_NOVA_GAME_SPEC_v0.8.md` dan `DESIGN_SPEC_v1.3.md`. `DESIGN_SPEC.md` adalah alias identik v1.3. Versi lama (`GAME_SPEC_v0.6.md`, `TERRA_NOVA_GAME_SPEC_v0.7.md`, `DESIGN_SPEC_v1.2.md`) dipertahankan sebagai histori.

**Status sinkronisasi Fase 0 (selesai):**
- D20 arah fitur diminta pemilik; D21 parameter review.
- Register keputusan (`GAME_SPEC_DECISIONS.md`), `TECHNICAL_DESIGN.md`, `DATABASE_SCHEMA.md`, `GAME_ECONOMY_MODEL.md`, `TEST_PLAN.md` (Q01–Q28), `PERFORMANCE_BUDGET.md`, `OPENING_STORYBOARD.md`, dan `IMPLEMENTATION_ROADMAP.md` telah disinkronkan terhadap v0.8 + DESIGN_SPEC v1.3 termasuk D15–D21.
- Simulasi terintegrasi `simulasi_dwe_dle.py` telah dibuat dan dijalankan ulang bersama `simulasi.py`, `uji_batas.py`, dan `simulasi_kebun.py`; seluruh CSV pada `hasil/` terverifikasi reproducible dengan konservasi massa 0 gram.
- Review D03–D08, D14–D19, dan D21 tetap menjadi bahan keputusan pemilik sebelum gate Fase 1 produksi. Gambar referensi di `references/` hanya untuk dokumentasi pengembang, bukan aset runtime.
