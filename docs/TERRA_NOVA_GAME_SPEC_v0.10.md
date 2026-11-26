# GAME_SPEC v0.10 — TERRA NOVA: Peradaban Bumi Baru

**Chapter I — The Calling of Gaia**

Simulasi usaha pengelolaan sampah, idle factory tycoon, multiplayer asinkron berbasis kota, dan edukasi. Versi 0.9 (26 November 2026) — menyelaraskan spesifikasi dengan prototipe lokal yang sudah dimainkan: landing + akun, opening cinematic, lahan isometrik, Evaluasi 1 dan Evaluasi 2 (§30–§36). Basis sebelumnya: v0.8 (DWE + DLE). Referensi pengalaman: BosWarung.id; identitas, aset, kode dan cerita TERRA NOVA harus orisinal.

**Tagline merek [R]:** One Earth. One Destiny. A New Civilization. — Satu Bumi. Satu Takdir. Sebuah Peradaban Baru.

**Filosofi utama:** Bumi tidak membutuhkan penghuni baru. Bumi membutuhkan peradaban baru.

**Pesan kampanye opening:** Bumi tidak membutuhkan lebih banyak janji. Bumi membutuhkan tindakan.

**Status keputusan:** [D] keputusan pemilik/arah yang disetujui; [R] rekomendasi implementasi v0.5–v0.6, perlu review sebelum coding; [U] parameter usulan, wajib dikalibrasi; [V] perlu verifikasi eksternal. Ketentuan v0.4 tetap berlaku kecuali perubahan eksplisit di bagian 17–23 dan 30–36. [P] = sudah diimplementasikan di prototipe lokal (`server.py` + `web/`) atas arahan pemilik; belum berarti angka final atau gate Fase 1 terbuka. Jika bertentangan, rekomendasi v0.5–v0.6 tidak boleh diam-diam dianggap keputusan pemilik.
Tujuan file ini: dirujuk di setiap sesi AI baru agar konteks tidak diulang (hemat token).

**Amendemen pengendali v0.10:** §37–39 dan 00_FEATURE_FREEZE mengesampingkan aturan historis yang bertentangan. §30–36 adalah baseline implementasi v0.9, bukan klaim implementasi v0.10.

## 0. Identitas produk dan batas visi [D/R]

| Elemen | Identitas | Status |
|---|---|---|
| Nama game | TERRA NOVA | [D] menggantikan Bumi Bersih |
| Subjudul Indonesia | Peradaban Bumi Baru | [D] arah produk |
| Chapter I | The Calling of Gaia | [D] arah cerita |
| Genre | Multiplayer Idle Factory Tycoon | [D] arah gameplay |
| Platform | Web responsif / PWA | [R] implementasi |
| Referensi pengalaman | BosWarung.id | [D] kesederhanaan, bukan penyalinan |
| Filosofi | Waste Management Genesis | [D] arah edukasi |
| Tokoh utama | Dewi Gaia | [D] |
| Tujuan naratif | Zero Waste Civilization | [D] tujuan dalam simulasi |

TERRA NOVA berarti Bumi Baru. Yang dibangun bukan planet pengganti, melainkan peradaban yang mengubah hubungan manusia dengan materi dan lingkungan. Pengelolaan sampah adalah fondasi perjalanan pertama. Chapter I pada identitas produk adalah arc besar; chapter internal di §17.7 adalah bab cerita di dalam arc tersebut, bukan ekspansi terpisah.

### 0.1 Visi ekspansi jangka panjang [R — bukan scope MVP]
| Arc | Judul usulan | Tema |
|---|---|---|
| I | The Calling of Gaia | Pengelolaan sampah dan ekonomi sirkular |
| II | The Rise of Solaris | Energi terbarukan |
| III | The Awakening of Aqua | Pengelolaan air |
| IV | The Seeds of Life | Ketahanan pangan |
| V | The New Civilization | Peradaban berkelanjutan |

Hanya Arc I masuk scope roadmap saat ini. Jangan membangun sistem energi, air, pangan, atau engine ekspansi generik sebelum core loop stabil dan pemilik menyetujui fase baru. Judul dan urutan ekspansi adalah usulan, bukan komitmen rilis. Jangan menyamakan pencapaian game dengan dampak lingkungan nyata.

### 0.2 Aturan branding dan rilis [V]
Gunakan TERRA NOVA secara konsisten pada landing, opening, metadata, menu, UI, dokumentasi, dan materi promosi. Jangan mengganti identifier teknis, tabel database, domain, atau repo yang sudah ada tanpa audit migrasi. Nama dipilih pemilik tetapi belum lolos pemeriksaan merek dagang, konflik nama game, domain dan akun sosial. Lakukan pemeriksaan sebelum publikasi resmi; desain logo dan aset final belum ditetapkan.

## 1. Konsep dan visi
- **Tokoh:** Dewi Bumi "Gaia" — anggun, kharismatik, memikat. Ia terpuruk: tubuhnya terlilit sampah, wajah pucat, rambut kusam. Ia pulih bertahap lewat 5 state ilustrasi mengikuti tier pemain.
- **Rating & audiens:** 13+. **Arah visual (keputusan):** daya tarik lewat cahaya, warna, siluet, kain mengalir, dan aura; berpakaian lengkap; tanpa tampilan tubuh terbuka yang sugestif. Jika ingin visual lebih berani, itu produk berbeda: rating 18+, verifikasi usia, tinjauan hukum.
- **Permintaan Gaia:** "Hilangkan sampahku." Pemain mengira artinya musnahkan.
- **Twist edukatif tanpa kuis:** pemain mengalaminya sendiri lewat konsekuensi. Panel **Neraca Massa** selalu menunjukkan bahwa massa masuk = massa keluar (asap, abu, lindi, produk). Membakar/menimbun menaikkan **Karma**; jika tidak diperbaiki, pemain **bereinkarnasi** (§7d). Yang memahami bahwa sampah hanya bisa diubah, bukan dimusnahkan, membangun Konverter Asap dan lanjut ke God serta membuka hidden gem (§7f).
- **Struktur dunia (hybrid):**
  - *Semesta Pribadi* = lahan dan pabrik tiap pemain (aksi produksi, Karma, Neraca Massa).
  - *Kota Bersama* = hub usaha berbasis kota, terinspirasi kesederhanaan Bos Warung: pemain lain terlihat, bisa visit, trading, event (§8).
  - *Bumi Global (1 dunia logis, bukan satu proses fisik)* = ZWM dan BHI bersama; tujuan kolektif per Musim (§6, §7g, §7h).
- **Platform:** web, responsif mobile, tanpa instal.

## 2. Core loop (MVP solo dulu)

[R] Integrasi DWE §24–27 memperinci asal, reservasi, angkut dan penerimaan sampah; parameter lama tetap baseline hingga disahkan. Tidak ada penciptaan stok di pabrik tanpa sumber yang tercatat.
1. Sampah masuk ke kota tiap jam (per kelurahan).
2. Pemain memilih sampah mana yang "ditarik" ke pabriknya (kontrak angkut).
3. Pabrik memilah → mengolah → menghasilkan produk (plastik cacah, kompos, RDF/energi, residu).
4. Jual produk, bayar opex, upgrade unit.
5. Residu & emisi menurunkan Bumi Health Index (BHI) kota.
6. Eyang Gaia memberi misi harian/mingguan (edukasi + reward).

## 3. Jenis sampah (5 fraksi, cukup untuk MVP)
| Fraksi | Share awal | Jalur terbaik |
|---|---|---|
| Organik | 50% | Kompos / maggot BSF |
| Plastik | 18% | Daur ulang (butuh pemilahan bersih) |
| Kertas | 10% | Daur ulang |
| Logam/kaca | 7% | Daur ulang |
| Residu/B3 ringan | 15% | Olah termal / landfill terkendali / drop-off B3 |

*(Angka share = placeholder, validasi ke data SIPSN/KLHK sebelum rilis.)*

## 4. Unit pabrik
| Unit | Input | Output | Kapasitas dasar (kg/jam) | Opex/jam | Catatan |
|---|---|---|---|---|---|
| Pemilahan | campuran | fraksi terpisah | 200 | 50 | Menentukan kemurnian |
| Kompos/BSF | organik | kompos | 150 | 30 | Yield rendah, cepat |
| Daur ulang plastik | plastik | pelet | 100 | 80 | Butuh kemurnian ≥ 80% |
| Daur ulang kertas/logam | kertas, logam | bahan baku | 100 | 60 | |
| Insinerator bersih | residu | energi + abu | 120 | 120 | Emisi + abu; butuh filter |
| Filter/scrubber | (modifier) | −emisi | — | 40 | Wajib agar insinerator aman |

## 5. Rumus ekonomi (semua dihitung SERVER)
```
Kemurnian      = 1 - (kontaminan / throughput)           # dari kualitas pemilahan
Output         = Input × Yield_unit × Kemurnian_efek
Pendapatan     = Σ Output_i × Harga_i(t)
Harga_i(t)     = Harga_dasar_i × (1 + fluktuasi_t) × (1 - saturasi_i)
Saturasi_i     = min(0.5, total_dijual_kota_i / permintaan_kota_i)   # anti-banjir pasar
Laba/jam       = Pendapatan − Opex − Pajak_emisi − Biaya_residu
Pajak_emisi    = Emisi × (1 - efisiensi_filter) × tarif
Biaya_residu   = Residu_kg × tarif_tipping
```
**Sink uang (cegah inflasi):** pajak emisi, tipping fee residu, biaya perawatan (efisiensi turun 1%/hari tanpa maintenance), upgrade mahal bertingkat (×1.6 per level).

**Offline accrual:** produksi dihitung saat login, dibatasi maks 8 jam.

## 6. Indeks global Bumi (satu server)
```
ZWM  = 1 − sampah_belum_terkelola_global / sampah_total_musim      # 0–100%, tujuan kolektif
BHI  = 100 − 40×(sampah_tak_terkelola / total_sampah)
           − 30×(emisi_global_tak_terolah / ambang_emisi)
           − 30×(residu_landfill_global / kapasitas_landfill)
```
- ZWM = progres menuju kemenangan musim. BHI = kesehatan Bumi dan tampilan Gaia.
- BHI < 40 → event "Banjir sampah": penalti ke semua pemain, mendorong kerja sama.
### ZWM nyata vs ZWM game
- **ZWM game** = angka yang menentukan menang/kalah musim; target diskalakan dengan jumlah pemain aktif (§7h).
- **ZWM nyata** = panel edukatif yang menggambarkan skala sebenarnya: berapa timbulan sampah dunia/nasional dibanding kapasitas pengolahan. Tidak memengaruhi gameplay.
- **Faktor konversi** (1 kg game = k ton nyata) ditampilkan terbuka, dengan sumber data dan tahun. Data resmi (mis. SIPSN KLHK, World Bank "What a Waste") harus diverifikasi sebelum dipasang; jangan hard-code angka dari ingatan.
- Label wajib: "simulasi/ilustrasi", agar tidak menyesatkan seolah-olah kontribusi pemain setara dampak nyata.

## 7. Poin, tier, Karma, dan akhir cerita
### 7a. Sumber poin
```
Poin = Σ(kg_dialihkan_dari_landfill × bobot_fraksi)
     + Σ(kg_residu_dikonversi_jadi_material × 6)
     + misi_Gaia + 0.1 × kontribusi_BHI_global
     − penalti_emisi_tak_terolah − penalti_residu
bobot_fraksi: organik 1 | kertas 2 | plastik 3 | logam/kaca 4 | B3 benar 8
```
- Batas harian per sumber (diminishing returns) agar tidak bisa grinding semalaman.
- Kekayaan bukan poin; uang hanya alat.

### 7b. Tier (placeholder, kalibrasi di Fase 0; target God ≈ 60–90 hari main aktif — asumsi)
| # | Tier | Poin minimum | Visual Gaia |
|---|---|---|---|
| 1 | Awaken | 0 | Terpuruk, tertimbun |
| 2 | Seeker | 500 | Lemah, mulai menatap |
| 3 | Sorter | 2.000 | Bangkit duduk |
| 4 | Recycler | 6.000 | Berdiri, warna kembali |
| 5 | Guardian | 15.000 | Tersenyum |
| 6 | Ascendant | 35.000 | Aura hijau |
| 7 | Titan | 80.000 | Bercahaya |
| 8 | Archon | 180.000 | Hampir pulih |
| 9 | **God** | 400.000 **+ gate** | Ilahi, pulih penuh |

### 7c. Gate untuk naik ke God (tanpa kuis)
1. Poin ≥ ambang God.
2. Karma ≤ 25%.
3. Emisi tak terolah = 0 (jika pemain memakai pengolahan termal, Konverter Asap §7e wajib aktif).
4. Pengalihan dari landfill ≥ 90%.

### 7d. Karma dan Reinkarnasi (pengalaman kesalahan sendiri)
- **Karma naik:** residu dibakar tanpa Konverter, landfill, emisi tak terolah. **Karma turun:** daur ulang, kompos, konversi residu, pengolahan emisi tuntas.
- **Umpan balik (bukan penalti tersembunyi):** langit kelabu, Gaia batuk, Neraca Massa menampilkan "massa tidak hilang: X kg → asap/abu/lindi". Peringatan jelas di Karma 50% dan 75%.
- **Karma 100% → Reinkarnasi:** tier reset ke Awaken. Dipertahankan: blueprint yang pernah dibuka, kosmetik, riwayat Neraca Massa, dan bonus kecil poin permanen (usulan: +10% per reinkarnasi, maks 3) agar ulangan terasa belajar, bukan hukuman buta.
- **Jalan keluar:** memasang Konverter Asap sebelum Karma 100% menghentikan penumpukan Karma dari emisi.

### 7e. Konverter Asap ("Penjernih Napas Gaia") — akurat secara ilmiah
Pembakaran menghasilkan CO₂, uap air, partikulat, gas asam, dan abu. Tidak ada alat yang mengubah "asap" langsung jadi oksigen murni. Versi game yang jujur:
| Unit | Fungsi | Sisa/produk (tetap tercatat di Neraca Massa) |
|---|---|---|
| Scrubber | Tangkap partikulat dan gas asam | Lumpur/abu terak |
| Fotobioreaktor alga | CO₂ → O₂ + biomassa | Biomassa alga |
| Penstabil abu | Abu → bahan paving/geopolimer | Material konstruksi |
Asap → oksigen hanya **clue** di antarmuka. Mekanik wajib berurutan, tidak bisa dilewati: Scrubber → Fotobioreaktor alga → Penstabil abu. Game boleh menyederhanakan angka, tetapi Neraca Massa tetap menampilkan seluruh sisa.

### 7f. Hidden gem (usulan nama: "Alkimia Gaia")
- **Syarat:** God + Karma ≤ 10% + 3 unit Konverter aktif ≥ 30 hari.
- **Isi:** lab yang mengubah biomassa dan abu menjadi material baru bernilai; kosmetik "Alkemis Bumi"; jalur cerita rahasia Gaia.

### 7g. Akhir cerita (Opsi A, final) — kolektif per Musim
- **Syarat upacara:** ZWM global = 100% sebelum Musim berakhir.
- **Penerima (berdasarkan tier akhir):**
| Peringkat akhir | Pria | Wanita |
|---|---|---|
| God | **Pendamping Gaia** (pernikahan naratif) | **Perwakilan Dewi Bumi** + "Kecantikan Abadi" (kosmetik permanen) |
| Awaken–Archon | Badge "Pengikut Gaia" sesuai tier | idem |
- **Syarat dan kondisi Perwakilan (usulan, bisa diubah):** God + Karma ≤ 10% + kontribusi ZWM ≥ median pemain God musim itu.
- **Pemain di bawah 18:** hadiah netral **"Penjaga Gaia"** (ritual suci penjaga bumi), tanpa konten romantik-seksual. Opsi A (Pendamping/Perwakilan) hanya untuk 18+.
- Semua hadiah hanya narasi dan kosmetik dalam game; tidak ada klaim dunia nyata.
- **Gender akun:** isian wajib saat daftar dengan dua pilihan (pria/wanita), sesuai keputusan pemilik. Data pribadi anak <18 kemungkinan butuh persetujuan orang tua (UU PDP) — verifikasi ke ahli hukum.

### 7h. Musim
- Panjang musim: 90 hari (placeholder). Target kapasitas pengolahan bersama diskalakan dengan pemain aktif 7 hari terakhir (sampah yang dihasilkan ∝ N aktif), supaya server sepi tidak mustahil menang dan server ramai tidak terlalu mudah.
- Jika ZWM < 100% di akhir musim: tanpa upacara, reward tier tetap diberikan, Gaia "menunggu musim berikutnya".
- Musim baru = Bumi baru; Hall of Eternity (daftar Pendamping/Perwakilan) permanen.
- Anti free-rider: kontribusi dicatat per pemain; God butuh kontribusi minimal pribadi.
- Anti-grief: tidak ada aksi yang langsung merugikan pemain lain; emisi tak terolah memengaruhi BHI bersama (tragedi milik bersama, sengaja) tetapi dibatasi lewat Karma per pemain.

## 8. Dunia multiplayer (fase 3)
- **Semesta Pribadi:** logika produksi per pemain, disimpan di baris sendiri.
- **Kota Bersama (model Bos Warung, versi hemat):**
  - Peta 2D/isometrik, bukan 3D bebas bergerak. Kerumunan "ramai" berupa **NPC animasi di sisi klien** (gratis); pemain asli ditampilkan sebagai penanda yang diperbarui tiap 10–30 detik.
  - Ruang gerak real-time penuh (websocket per avatar) adalah komponen termahal: tunda ke setelah beta.
  - Visit pabrik pemain lain (read-only), trading, event kota.
- **Komunikasi:** TANPA chat teks bebas (audiens 13+ bercampur dewasa). Gunakan emote/pesan preset. Chat bebas hanya jika ada moderasi aktif.
- **Bumi Global:** satu server live untuk ZWM/BHI. Agregasi lewat cron tiap 1 menit; klien menerima via Realtime tiap 10–60 detik. Jangan biarkan banyak pemain menulis ke satu baris yang sama.
- Misi kolektif musim (target ton per fraksi per minggu). Moderasi: filter nama, tombol laporan.

## 9. Monetisasi via Saweria
- **Model:** donasi sukarela → hadiah kosmetik/dukungan (skin pabrik, nama di "Tugu Donatur", title di ranking). **Tanpa keunggulan ekonomi.**
- **Dilarang dijual:** jalan pintas ke tier/God, poin, atau "kesempatan menikahi Gaia". Menjual akses romansa dengan karakter bertema sensual berisiko dinilai eksploitatif dan merusak makna edukasi.
- **Asumsi yang HARUS diverifikasi:** apakah Saweria menyediakan webhook/API otomatis. Jika tidak, alurnya manual: donatur menulis username game di pesan donasi → admin/skrip memverifikasi → reward diberikan.
- Cadangan: tautan donasi + kode redeem manual (paling aman di MVP).
- **ASN:** proyek ini tidak dikaitkan dengan pekerjaan ASN (keputusan pemilik). Jaga pemisahan akun, brand, dan penerima donasi; identitas publik sebagai penulis tetap bisa menautkan, jadi periksa konsistensi.

## 10. Tech stack (hemat, AI-friendly)
- Frontend: Next.js + React + Tailwind (UI-driven; visual SVG/CSS; tanpa game engine di MVP).
- Backend/DB/Auth/Realtime: Supabase (Postgres + RLS + Edge Functions).
- Tick ekonomi: Supabase cron / Edge Function per jam, fungsi murni yang bisa diuji.
- Hosting: Vercel. Aset: SVG buatan AI + maskot orisinal.
- Aturan emas: **klien tidak pernah mengirim uang/hasil produksi; hanya mengirim niat (aksi).**

## 11. Roadmap build (1 modul = 1 sesi AI)
| Fase | Isi | Selesai bila |
|---|---|---|
| 0 | Simulasi ekonomi di spreadsheet/script, uji keseimbangan | Tidak ada strategi dominan jelas |
| 1 | Solo loop: 3 unit, 5 fraksi, UI dasar, simpan progres | 1 pemain bisa main 7 hari simulasi |
| 2 | Auth, DB, tick server, BHI, misi Gaia | Progres tersimpan, anti-cheat dasar |
| 3 | Kota bersama, ranking, visit, pasar bersama | 20 pemain uji bersamaan |
| 4 | Saweria, kosmetik, analitik, konten edukasi | Beta tertutup 50 orang |

## 12. Metrik uji (validasi asumsi)
- Retensi D1 ≥ 30%, D7 ≥ 10% (beta tertutup).
- Median sesi 5–10 menit.
- Pemahaman tanpa kuis: ≥ 60% pemain yang punya emisi memasang Konverter sebelum Karma 100%; tingkat Reinkarnasi (pantau, target awal < 25% pemain yang mencapai Archon).
- Rasio pemain yang berdonasi (realistis < 2%): jangan jadikan sumber pendapatan utama.

## 13. Risiko & mitigasi
| Risiko | Mitigasi |
|---|---|
| Ekonomi rusak/exploit | Server-authoritative, sink uang, simulasi fase 0 |
| Pesan edukasi keliru ("musnahkan selamanya") | Twist di §1, review konten oleh Anda sebagai pakar |
| Biaya server membengkak | Hitung batch saat login, cap offline 8 jam |
| Donasi rendah | Anggap hobi/portofolio dulu, bukan bisnis |
| Tautan ke pekerjaan ASN lewat identitas publik | Pisahkan akun/brand/penerima donasi; keputusan pemilik: tidak dikaitkan |
| Spam/nama kasar | Filter nama, batas kreasi |

## 14. Protokol sesi AI (hemat token)
1. Mulai sesi baru dengan: "Baca GAME_SPEC.md, kerjakan Fase X modul Y saja."
2. Satu sesi = satu modul; commit sebelum lanjut.
3. Perubahan desain → update file ini dulu, baru kode.
4. Berhenti & reset sesi setelah: modul selesai diuji, atau konteks mulai berulang/melenceng.

## 15. Risiko tambahan v0.2
| Risiko | Mitigasi |
|---|---|
| Rating 13+ dengan tokoh perempuan memikat + hadiah pernikahan untuk pemain pria; UU Pornografi/UU ITE, kebijakan rating game Indonesia (IGRS) — verifikasi kategori | Visual tidak sugestif (§1), tinjau ilustrasi sebelum rilis, tombol laporan, upacara non-romantik untuk <18 |
| Opsi A + isian gender dua pilihan: sebagian calon pemain mungkin enggan mendaftar | Keputusan pemilik; pantau drop-off di pendaftaran saat beta |
| Chat bebas antar pemain (13+ bercampur dewasa) | Hanya emote/preset; moderasi aktif jika chat dibuka |
| Kota GTA real-time memicu biaya server | NPC sisi klien, penanda pemain tiap 10–30 detik (§8) |
| Skala ZWM nyata dianggap menyesatkan | Label simulasi + sumber data + faktor konversi terbuka (§6) |
| Gaia "terpuruk" dibaca sebagai glorifikasi penderitaan perempuan | Bingkai sebagai kelelahan alam akibat sampah, bukan kekerasan; Gaia punya agensi (ia memandu, bukan sekadar korban) |
| Scope creep (9 tier + 4 gate + Bumi pribadi + kota bersama) | MVP: 5 tier (Awaken, Sorter, Recycler, Guardian, God), 1 Bumi Pribadi sederhana, kota bersama menyusul |
| Ilustrasi Gaia konsisten di 5 state butuh banyak gambar AI | Mulai dengan gaya flat/siluet, satu set referensi karakter, generate per state |
| Tujuan kolektif bisa mustahil/terlalu mudah tergantung jumlah pemain; free-rider | Target diskalakan pemain aktif, kontribusi pribadi minimum (§7h) |
| Reinkarnasi (reset tier) memicu churn | Peringatan 50%/75%, bonus poin permanen, jalan keluar lewat Konverter (§7d) |
| "Asap jadi oksigen" menyesatkan secara ilmiah | Konverter 3 unit dengan Neraca Massa (§7e) |

## 16. Prompt serah-terima sesi baru (baseline v0.5)
Tempel di awal sesi:
"Baca GAME_SPEC v0.6.md secara lengkap, termasuk bagian 17–23. Kerjakan Fase 0 saja: (1) simulasi ekonomi dan keseimbangan unit pabrik di script, (2) kalibrasi tier, Karma, dan Reinkarnasi, (3) uji apakah ada strategi dominan. Beri hasil dalam tabel dan tandai asumsi. Jangan ubah desain tanpa memperbarui spec terlebih dahulu. Laporkan konflik, asumsi, dan keputusan yang memerlukan persetujuan; jangan membangun aplikasi sebelum review Fase 0."
Revisi konsep: update spec dulu, baru lanjut ke kode.


---

## 17. Lore, opening cinematic & player onboarding [D]

### 17.1 Premis naratif — Reality to Fantasy
TERRA NOVA dimulai dari realitas krisis sampah, bukan dari layar pabrik. Pemain melihat sejarah konsumsi, timbulan sampah, upaya manusia, serta kesenjangan antara hasil upaya tersebut dan skala masalah yang masih berlangsung. Setelah presentasi faktual berakhir, cerita beralih secara jelas ke fiksi: Dewi Gaia, personifikasi Bumi, memanggil manusia dari berbagai kota untuk membantu memulihkannya. Setiap pemain adalah salah satu manusia yang dipanggil; tidak ada klaim bahwa panggilan tersebut terjadi di dunia nyata. Misi dimulai dari kota pilihan pemain, kemudian berkembang dari pabrik pribadi ke kolaborasi kota dan Bumi Global.

Pesan: tindakan kolektif yang sudah berjalan penting, tetapi belum cukup mengimbangi krisis. Jangan mengklaim organisasi atau aktivis tidak menghasilkan dampak sama sekali tanpa bukti. Jangan menyalahkan satu kelompok atau organisasi. Gaia memiliki agensi: ia memandu dan memberi misi, bukan sekadar korban.

### 17.2 Storyboard opening (120 detik, usulan)
| Waktu | Babak | Visual dan narasi |
|---|---|---|
| 00–10 | The Beautiful Earth | Bumi, hutan, sungai, laut. “Alam memiliki siklusnya sendiri. Setiap materi memiliki tempat dalam perjalanan kehidupan.” |
| 10–30 | The Human Footprint | Kota, industri, konsumsi, TPA, sungai tercemar. “Seiring berkembangnya peradaban, manusia menciptakan sesuatu yang mereka sebut sampah.” |
| 30–50 | Humanity’s Efforts | Relawan, bank sampah, TPS3R, gerakan global, kebijakan produsen. “Jutaan manusia telah bergerak. Namun, perjuangan itu belum cukup mengimbangi sampah yang terus dihasilkan.” |
| 50–65 | The Crisis | Kartu data dunia, Indonesia, dan keterbatasan pelaporan. “Apakah masih ada harapan?” |
| 65–90 | The Awakening of Gaia | Transisi bertanda ‘kisah fiksi’; Gaia lemah, berpakaian lengkap, cahaya redup. “Aku adalah Gaia. Aku telah menyaksikan perjalanan peradabanmu. Kini, aku membutuhkan pertolonganmu.” |
| 90–120 | The Calling | Cahaya menjangkau berbagai kota. “Aku memanggilmu bukan tanpa alasan. Mulailah dari tempatmu berada. Pulihkan kotamu. Pulihkan tubuhku.” |

### 17.3 Data nyata dan gerakan lingkungan [V]
Sumber kandidat (bukan feed data terverifikasi): UNEP Global Waste Management Outlook 2024, World Bank What a Waste, SIPSN kementerian yang berwenang, publikasi pemda, laporan resmi organisasi. Kandidat narasi: International Day of Zero Waste, World Cleanup Day (global dan Indonesia), bank sampah, TPS3R, gerakan masyarakat setempat, serta kebijakan Extended Producer Responsibility. Bedakan organisasi, kampanye, fasilitas, dan kebijakan. Gunakan data hasil kegiatan bila tersedia; jangan menyamakan jumlah relawan dengan massa sampah yang berhasil diproses.

Setiap fakta memiliki `source_url`, `publisher`, `publication_date`, `reference_year`, `geography`, `metric`, `value`, `unit`, `coverage`, `methodology_note`, `verified_at`, `review_status`. Angka nasional harus menjelaskan jumlah daerah pelapor; proyeksi wajib diberi label. Jangan tampilkan angka yang belum diverifikasi. Bila data kota tidak tersedia, tampilkan “data belum tersedia” dan gunakan konfigurasi simulasi yang diberi label terpisah. Sumber, tahun, dan keterangan dapat dibuka dari setiap kartu. Admin menerbitkan snapshot data versioned; tidak ada panggilan API eksternal setiap login. Foto dokumenter perlu izin penggunaan; ilustrasi AI harus dilabeli sebagai ilustrasi, bukan dokumentasi faktual.

### 17.4 Dialog pertama dan penerimaan panggilan
Gaia: “Aku telah menunggu begitu lama. Manusia telah berusaha menyembuhkanku. Namun, luka-lukaku terus bertambah. Aku tidak memanggilmu karena kekayaanmu, kekuatanmu, ataupun kedudukanmu. Aku memanggilmu karena aku masih percaya bahwa manusia dapat berubah. Maukah engkau membantuku?”

CTA: **Aku menerima panggilanmu**. Setelah diterima: “Terima kasih, manusia terpilih. Perjalananmu kini dimulai. Pergilah ke kotamu. Aku akan selalu menyertaimu.” Tier Awaken terbuka setelah akun dan inisialisasi state berhasil. Pemain boleh melewati cinematic tanpa kehilangan akses permainan.

### 17.5 Alur onboarding
**[D/P] v0.9 — alur yang berlaku (keputusan pemilik 26 Nov 2026):** Landing (domain, mis. teranova.id) → **Daftar** (nama pengguna, email, kata sandi, pilih karakter pria/wanita) → opening cinematic *The Calling of Gaia* langsung diputar tanpa tombol awal → di akhir: **Aku menerima panggilanmu** atau **Ulangi cinematic** → langsung ke lahan (tanpa layar pilih kota/buat profil) → intro lahan sekali (§31) → Cara Bermain → permainan reguler. Pemain lama yang **Login** langsung ke lahan tanpa video; akun yang belum menerima panggilan melihat cinematic lagi. Rincian §30.

*Alur v0.8 (historis, digantikan):* Landing → Prologue (fakta nyata → fiksi) → terima panggilan → daftar/login dan pemeriksaan usia yang sesuai → pilih negara dan kota/kabupaten secara manual → buat nama karakter → inisialisasi lahan → tutorial interaktif → operasi pertama → permainan reguler.

**Belum ada di prototipe (terbuka, lihat §36):** pemeriksaan usia 13+, pilihan kota manual (sementara otomatis Bandung), kustomisasi kosmetik, replay opening dari menu cerita/Jurnal.

- Tidak meminta GPS, alamat rumah, atau lokasi presisi. Kota adalah pilihan karakter, bukan verifikasi tempat tinggal. Tampilkan hanya nama karakter dan kota pilihan pada profil publik; jangan tampilkan usia atau data kontak.
- Mulai Indonesia; daftar kota berasal dari master data administratif yang tervalidasi. Kota yang belum punya data lingkungan memakai profil simulasi generik. Satu kota logis dapat berisi banyak distrik, tanpa instance server per kota.
- Pilihan kota dapat disimpan setelah onboarding; perpindahan kota dan konsekuensi ekonomi perlu keputusan Fase 0. Kota awal tidak boleh memberikan keuntungan ekonomi permanen yang tidak adil.
- Simpan `onboarding_version`, `onboarding_step`, `intro_seen_at`, `city_id`, `tutorial_completed_at`. Inisialisasi akun dan starter pack idempotent; refresh tidak menggandakan hadiah. Opening dapat diulang lewat menu cerita. Akun lama tidak dipaksa mengulang opening versi baru.
- Ketentuan gender dan hadiah naratif §7g tetap keputusan v0.4, tetapi pemeriksaan legal/privasi anak dan mekanisme pengumpulan data minimal merupakan blocker sebelum rilis 13+.

### 17.6 The Genesis — tutorial bermain, bukan ujian
| Starter pack [U] | Nilai awal |
|---|---|
| Gaia Coin | ~~10.000~~ → **1.000 [D/P v0.9, Evaluasi 1]** (mata uang virtual, tanpa nilai tunai); koin berikutnya dari memungut, mengolah dan menjual sampah |
| Lahan | 100 m² |
| Gerobak | 1 |
| Gudang | 1 (kapasitas 500 kg; dapat diperluas, §33) |
| Tempat pemilahan | 1 |
| Benih Kebun Gaia | 3 [P] |
| Lahan awal | Berantakan: 9 sampah di dalam pagar + 12 di luar [P, §32] |
| Tier | Awaken |
| Karma | 0% |

Gaia hanya memberi misi: **“Hilangkan sampahku.”** Jangan membocorkan twist hukum kekekalan massa pada opening. Tutorial mengarahkan melalui highlight dan satu tindakan per langkah: pilih kontrak → ambil sampah → pilah → olah/jual → lihat perubahan saldo dan lingkungan. Neraca Massa tersedia sejak awal, penjelasan mendalam muncul kontekstual setelah pemain melihat akibat tindakannya. Pilihan pengolahan berisiko hanya berupa simulasi abstrak, bukan petunjuk pembakaran atau penanganan B3 dunia nyata. Jangan membuka mesin termal sebelum tutorial keselamatan/konsekuensi yang sesuai. Tidak ada forced wait panjang untuk tindakan pertama. [U] Target tindakan bermakna pertama ≤ 3 menit setelah onboarding (di luar durasi cinematic).

### 17.7 Struktur chapter [U]
| Chapter | Judul | Fungsi / pemicu usulan |
|---|---|---|
| Prologue | The Cry of Earth | Presentasi fakta dunia nyata |
| 1 | The Calling of Gaia | Menerima panggilan, memilih kota |
| 2 | The Genesis | Operasi pengolahan pertama |
| 3 | The Illusion of Waste | Mengamati residu dan emisi |
| 4 | The Cycle of Matter | Menutup neraca massa dan meningkatkan daur ulang |
| 5 | The Rise of Guardians | Berkontribusi pada misi kota |
| 6 | The Alchemy of Gaia | Penelitian lanjutan, hidden gem sesuai §7f |
| Final | The Rebirth of Earth | Upacara kolektif bila syarat §7g terpenuhi |

Chapter bersifat naratif, tidak mengganti sembilan tier §7b. Story unlock dan pencapaian permanen disimpan terpisah dari reward musim. Dialog berbasis aturan dan template, tanpa LLM saat gameplay.

### 17.8 Motion Comic Cinematic [R]
**[P] v0.9:** opening sudah dibuat sebagai web player (`cinematic-web/runtime`, disajikan di `/intro/`), 120 detik, ilustrasi + gerak kamera + subtitle ID/EN + narasi ElevenLabs (narator **Eric Dipoetra**, `eleven_multilingual_v2`, bahasa Indonesia; Gaia suara Serena `eleven_v3` dengan gema) + musik. Ukuran runtime ±4,0 MB (melebihi anggaran usulan 1,6 MB di bawah; perlu optimasi, §36). Autoplay pada daftar; bila browser memblokir suara, tampil satu tombol *Putar cinematic* sebagai cadangan. Label kecil 'ilustrasi' di pojok video dihapus atas permintaan pemilik — keterangan bahwa gambar adalah ilustrasi perlu ditempatkan di tempat lain (mis. kredit akhir atau halaman Tentang) agar tetap memenuhi §17.3.

*Teks v0.8:* Ilustrasi WebP/AVIF orisinal + gerak kamera CSS + subtitle + narasi opsional + musik. Target aset terkompresi seluruh opening: ilustrasi 800 KB, musik 400 KB, suara Opus 350 KB, JSON 10 KB, CSS 20 KB (sekitar 1,6 MB; anggaran, bukan hasil ukur). Muat adegan pertama dahulu; prefetch satu adegan berikutnya; lepaskan tekstur/audio setelah selesai. Audio hanya setelah interaksi pengguna, ada mute, volume, subtitle dan mode reduced motion. Jika aset gagal dimuat, teks dan tombol lanjut tetap tersedia. Tidak perlu video 3D, autoplay berat, maupun streaming per pemain. Uji kompatibilitas audio; sediakan fallback jika perlu.

## 18. Gameplay model Bos Warung [D: arah pengalaman; R: rincian]

Referensi pengalaman bermain: usaha kecil yang berkembang, tindakan singkat, ekonomi mudah dipahami, kota bersama, kunjungan tetangga. Bukan penyalinan merek, source code, aset, atau UI BosWarung.id; teknologi internal situs referensi belum diaudit.

| Pola simulasi usaha | Adaptasi TERRA NOVA |
|---|---|
| Kulakan | Kontrak angkut sampah |
| Stok barang | Inventaris bahan, produk, residu |
| Penjualan | Pesanan pasar material |
| Dekorasi warung | Tata letak dan kosmetik pabrik |
| Tetangga | Pabrik pemain lain, visit read-only |
| Kompetisi | Kontribusi lingkungan, bukan kekayaan saja |

### 18.1 Layar utama mobile-first
- Header: Gaia Coin, tier, Karma, indikator status operasi.
- Peta pabrik top-down/isometrik 2D, mesin dapat diketuk; panel aksi menampilkan kapasitas, stok, biaya, hasil, residu.
- Kartu pesan Gaia kontekstual; indikator BHI dan akses Neraca Massa.
- Navigasi utama: Pabrik, Angkut, Pasar, Kota, Bumi. **[P v0.9]:** Pabrik, Kebun, Angkut, Pasar, Menu; Kota/Bumi masuk Menu sebagai terkunci (§34). Pengaturan, jurnal, riset dan profil melalui menu sekunder.
- Aksi penting dapat dilakukan dengan tombol/daftar tanpa drag-and-drop. Teks terbaca, tidak mengandalkan warna saja. Mode terang/gelap opsional setelah MVP.

### 18.2 Perkembangan fisik pabrik (berbeda dari tier spiritual) [U]
| Tahap | Fasilitas |
|---|---|
| 1 Tukang Sampah | Gerobak, gudang, pilah manual |
| 2 Bank Sampah | Timbangan, pegawai, angkut |
| 3 Industri Daur Ulang | Mesin otomatis, produk industri |
| 4 Eco Industrial Park | Pengolahan terpadu, energi dan simbiosis industri |
| 5 Zero Waste Civilization | Riset sirkular, teknologi lanjutan, Alkimia Gaia bila memenuhi syarat |

Tahap fisik berdasarkan fasilitas yang dibangun, bukan pengganti tier Awaken–God. Gunakan aset modular yang dapat dipakai ulang. Lima state ilustrasi Gaia dipetakan sementara: Awaken–Seeker, Sorter–Recycler, Guardian–Ascendant, Titan–Archon, God; sembilan tier tetap tersedia secara logika. Rincian visual tiap tier pada §7b adalah arah narasi, bukan kewajiban sembilan aset terpisah.

### 18.3 Kota dan komunitas
Pemain memilih kontrak sampah dari kelurahan/zona simulasi. Kota memiliki pasar, pabrik tetangga, pusat riset dan misi kolektif. Kota berkompetisi melalui leaderboard yang dinormalisasi terhadap target/kapasitas agar kota kecil tidak selalu kalah. Kota bukan replika geografis presisi. Untuk beta awal, gabungkan komunitas melalui misi lintas kota dan daftar kunjungan sehingga kota dengan sedikit pemain tetap hidup. NPC dekoratif harus dibedakan dari pemain asli. Tidak ada chat bebas atau jual beli uang nyata.

## 19. Arsitektur ringan dan server-authoritative [R]

### 19.1 Stack dan batas scope
Next.js + TypeScript + React + Tailwind; Supabase Auth/Postgres/RLS/RPC, Cron untuk snapshot global; Vercel/CDN; Zustand opsional untuk state UI; PWA setelah core loop stabil. SVG/CSS untuk pabrik sederhana; Canvas 2D/PixiJS dimuat dinamis hanya bila profiling menunjukkan kebutuhan banyak sprite. Hindari Unity, Unreal, Redis, microservices, Kubernetes, dedicated WebSocket server dan LLM dalam gameplay MVP. Satu dunia logis dapat memakai beberapa proses stateless dan satu database transaksi. Jangan mengklaim kapasitas tertentu sebelum load test.

### 19.2 Lazy Tick Engine — menggantikan tick ekonomi per pemain setiap jam setelah disetujui
Server menghitung produksi ketika membuka game atau tindakan ekonomi relevan, maksimal 8 jam offline sesuai §5. Waktu server adalah acuan. Cron tidak menjalankan produksi semua pemain, hanya agregasi, snapshot pasar/musim dan pekerjaan terbatas yang memang perlu dijadwalkan.

Algoritma:
1. Autentikasi, validasi payload niat aksi, rate limit, cek idempotency key yang terikat user dan isi permintaan.
2. Mulai transaksi DB; lock state pemain dan inventory terkait dengan urutan konsisten. Baca waktu server dan versi aturan/resep yang berlaku.
3. Hitung interval yang belum diselesaikan, cap 8 jam untuk offline; buang interval offline yang melebihi cap secara eksplisit agar tidak dapat diklaim pada request berikutnya. Segmentasikan bila perubahan musim/aturan relevan terjadi dalam interval yang sah.
4. Batasi input oleh stok, kapasitas mesin, kapasitas gudang output, uang untuk opex, kemurnian dan waktu. Gunakan aritmetika fixed-point/integer (gram dan unit koin terkecil). Cegah pembagian nol, nilai negatif dan overflow.
5. Terapkan resep dan neraca massa; catat output, residu, emisi, perubahan saldo, poin, Karma, kontribusi, dan versi aturan. Tidak menjual otomatis kecuali fitur itu disetujui.
6. Selesaikan produksi lama sebelum upgrade/perubahan resep/penjualan; validasi dan lakukan aksi baru dalam transaksi yang sama. Penjualan lintas pemain membutuhkan lock konsisten dan ledger debit-kredit atomik.
7. Simpan state, `last_settled_at`, hasil idempotensi dan event agregasi (outbox atau ledger incremental) dalam transaksi atomik. Commit; retry memakai key yang sama mengembalikan hasil yang sama, bukan produksi kedua.
8. Klien menerima snapshot resmi dan menampilkan interpolasi visual; tidak ada penulisan saldo/hasil produksi langsung dari browser. Saat offline jaringan, prediksi UI bukan progres resmi.

Jangan menggandakan settlement melalui login, refresh, banyak tab, cron, request retry atau race condition. Simpan timestamp server UTC. Definisikan aktif/offline secara konsisten di Fase 0, agar refresh tidak menciptakan waktu produksi tambahan. Untuk leaderboard musim, gunakan cutoff yang konsisten: finalisasi kontribusi yang belum diselesaikan melalui batch terukur atau aturan cutoff yang diumumkan; jangan memindahkan kontribusi musim lama ke musim baru. Agregasi harus idempotent dengan watermark/deduplikasi dan dapat direkonsiliasi dari ledger.

### 19.3 Data model awal
`profiles`, `cities`, `districts`, `player_state`, `player_machines`, `inventory`, `machine_catalog`, `material_catalog`, `production_recipes`, `market_prices`, `game_transactions`, `action_receipts`, `missions`, `player_missions`, `seasons`, `player_contributions`, `global_snapshots`, `achievements`, `game_config`, `story_progress`, `education_sources`.

Ini daftar konseptual, bukan migrasi siap pakai. Simpan state terkini dan transaksi batch; bukan satu row per kilogram, frame, atau NPC. Gunakan indeks pada user_id, city_id, season_id, waktu dan kunci idempotensi sesuai query nyata. RLS deny-by-default; RPC mutasi dengan hak minimum, pemeriksaan auth eksplisit; service key tidak pernah masuk bundle browser. Pisahkan profil publik dari data privat. Batasi riwayat dan pagination; kebijakan retensi/backup disepakati sebelum rilis.

### 19.4 Multiplayer dan update cadence
| Data | Interval/teknik usulan |
|---|---|
| Animasi NPC, truk, mesin | Lokal; tidak dikirim ke server |
| State ekonomi | Settlement saat aksi yang relevan |
| Presence distrik (opsional) | 15–30 detik, hanya saat halaman kota aktif |
| BHI/ZWM | Snapshot 1–5 menit |
| Pasar dan leaderboard | 5–15 menit |
| Visit | Snapshot read-only, paginasi/cache |
| Trading | Transaksi langsung, setelah beta stabil |

Awali polling snapshot dengan cache, backoff/jitter dan penghentian ketika tab tersembunyi. Realtime Broadcast hanya jika kebutuhan UX terbukti; hindari subscription semua tabel atau satu kanal global berisi setiap aksi. Distrik usulan 20–50 avatar yang terlihat, bukan batas kapasitas teruji. Satu pemain tidak boleh menjadi hot writer pada satu row global; agregasi incremental per kota/musim. Batasi dampak griefing dan sediakan laporan/moderasi.

## 20. Penyelarasan aturan ekonomi dan sains — agenda Fase 0 [R]
Bagian ini adalah usulan penyelesaian konflik v0.4, bukan perubahan diam-diam terhadap keputusan pemilik. Sebelum coding, tetapkan satu aturan final dan perbarui bagian asalnya.

| Konflik / risiko | Usulan penyelesaian |
|---|---|
| Residu dan B3 digabung (§3) | Enam fraksi: organik, plastik, kertas, logam/kaca, residu biasa, B3 rumah tangga. B3 masuk jalur penanganan khusus, bukan insinerator biasa. Pembagian 15% lama tidak langsung dibagi tanpa data/kalibrasi. |
| Neraca massa (§1,4,5,7e) | Massa input sampah + air + oksigen + bahan tambahan = produk + residu + emisi + perubahan stok. Energi dalam kWh, bukan kg. Yield/kemurnian tidak boleh menghapus massa. Uji konservasi per resep. |
| Konverter (§7e) | Scrubber menghasilkan residu; alga memerlukan cahaya, air, nutrien dan hanya menangkap sebagian CO₂; abu memiliki jalur paralel yang diuji sebelum digunakan. Urutan unlock naratif boleh tetap tiga tahap, tetapi aliran material tidak dipaksakan menjadi rangkaian fisik yang keliru. Tidak ada klaim emisi nol atau keamanan nyata karena filter saja. |
| Gate God (§7c) | Definisikan ‘emisi tak terolah’ sebagai metrik simulasi emisi yang tidak melalui jalur kendali yang disyaratkan; bukan nol emisi fisik. Pertahankan Karma ≤25% dan pengalihan landfill ≥90% sebagai target kalibrasi. |
| Hidden gem (§7f) | Usulkan jalur nontermal setara yang memenuhi tujuan sirkular dan durasi/kontribusi sebanding, agar pemain tidak dipaksa membakar sampah. Gate asli tetap sampai disetujui. |
| Bonus reinkarnasi (§7d) | Uji eksploit reset sukarela; usulkan bantuan belajar satu kali/nonkompetitif sebagai alternatif pengganda poin 10%. Tentukan secara eksplisit nasib uang, stok, mesin, poin, kontribusi musim dan timestamp saat reset. |
| Pasar (§5) | Tetapkan demand per periode dan kuantitas pembelian maksimum; stok tidak laku tetap tercatat. Harga server versioned; hindari arbitrase dan harga negatif. Simulasikan biaya angkut, gudang dan risiko bangkrut; jalur pemulihan tanpa pay-to-win. |
| Poin (§7a) | Material unik/lot lineage atau akuntansi kontribusi bersih mencegah poin ganda karena jual-beli, pemrosesan berulang atau pemindahan antarpemain. Pisahkan pengalihan landfill dari pengelolaan aman. |
| BHI (§6) | Clamp 0–100; definisikan denominator nol, ambang emisi, jendela waktu, unit dan bobot. Batasi penalti bersama agar satu pemain tidak menghancurkan seluruh musim. |
| ZWM (§6,7h) | Target/timbulan kumulatif tidak turun saat pemain keluar; skalakan penambahan timbulan berdasarkan aktivitas terverifikasi dengan batas anti-bot. ZWM 100% harus berarti seluruh target pengelolaan yang didefinisikan tercapai, bukan sekadar mengirim ke landfill. Definisikan batas residu dan emisi serta pencegahan double count. |
| God 60–90 hari vs musim 90 hari | Usulkan progres pribadi lintas musim (kecuali reinkarnasi), kontribusi/ranking musim terpisah. Pendatang baru tetap dapat mengikuti misi dan reward tier. Tetapkan matriks reset/carry-over sebelum implementasi. |
| Lima vs sembilan tier | Usulan sembilan tier logis, lima ilustrasi Gaia; tidak memangkas tier tanpa persetujuan. |

Simulasi 90 hari menggunakan beberapa strategi: organik, plastik, campuran, termal terkendali, landfill, pemain aktif ringan/berat, pemain baru pertengahan musim, pemain berhenti, bot/retry, pasar jenuh. Uji 0/1/banyak pemain, tidak ada stok/uang, permintaan nol, cap offline dan pergantian musim. Laporkan distribusi waktu naik tier, saldo, inflasi, Karma, residu, kontribusi dan kemungkinan dominasi strategi. Semua parameter berada pada konfigurasi berversi; hasil simulasi bukan bukti performa server.

## 21. Performance budget dan kualitas perangkat [R/U]
| Metrik | Target awal |
|---|---|
| Perangkat minimum uji | Android RAM 2 GB dan desktop browser umum |
| JS awal terkompresi | ≤250 KB sebagai target shell; ukur bundle aktual |
| Aset awal pabrik | ≤1 MB; total unduhan awal permainan ≤3 MB, opening dihitung terpisah |
| Opening | ~1,6 MB total aset; streaming bertahap |
| JS heap | 50–100 MB target; bukan total RAM browser/GPU |
| FPS | 30 Eco/Standard, 60 Immersive bila perangkat mendukung |
| LCP / INP | ≤2,5 detik / ≤200 ms pada profil perangkat dan jaringan yang ditetapkan |
| API game p95 | ≤500 ms dalam skenario load test yang ditetapkan |
| Snapshot pemain | ≤20 KB terkompresi sebagai target |
| Soak test | 30 menit tanpa pertumbuhan memori yang terus menerus; uji perpindahan layar berulang |

Teknik: sprite atlas kecil sesuai perangkat, tilemap, culling, object pooling bila profiling membuktikan manfaat, lazy loading kota/ilustrasi, lepaskan tekstur dan listener, hentikan animasi ketika tab tidak terlihat, batasi device pixel ratio, gunakan cache aset ber-hash, jangan simpan seluruh ledger di state React. Hindari memuat opening dan pabrik berat sekaligus. Mode Eco mengurangi partikel dan NPC dekoratif; hasil ekonomi semua mode sama. PWA cache aset publik saja; jangan cache respons privat secara tidak aman. Ukur heap, decoded textures/GPU dan penggunaan memori browser bila alat/perangkat mendukung; heap saja tidak cukup. Monitor biaya, koneksi DB, CPU, latency, error rate, quota, dan volume penyimpanan. Tidak ada estimasi kapasitas produksi terjamin sebelum benchmark.

## 22. Roadmap peluncuran revisi [R]
Menggantikan urutan §11 setelah persetujuan teknis; §11 tetap referensi historis scope awal.
| Fase | Modul | Gate |
|---|---|---|
| 0 | Audit aturan, simulasi 90 hari, TDD, schema, aset dan storyboard | Konflik §20 diselesaikan dan hasil simulasi direview |
| 1 | Prototype pabrik solo, 3 unit awal, tutorial dan prologue motion comic | Loop 7 hari simulasi berjalan; dapat dipahami tanpa admin |
| 2 | Private alpha: Auth, DB, Lazy Tick, misi, tier, Karma, neraca massa | 10–20 tester usulan; race/retry dan pemulihan progres lulus |
| 3 | Closed beta: kota pilihan, Bumi Global, leaderboard, pasar sistem, visit sederhana | 50–100 tester usulan; 20 concurrent awal; data edukasi diverifikasi |
| 4 | Open beta: kota 2D, PWA, kosmetik, monitoring, donasi opsional | Target 500 akun terdaftar; load test 100 concurrent sebagai gate usulan, bukan kapasitas maksimum |
| 5 | Official launch: Season 1, Hall of Eternity, trading bila siap | Semua gate rilis terpenuhi; rollback dan dukungan operasional siap |

Tidak menjadikan trading langsung, chat, avatar real-time, atau integrasi Saweria sebagai blocker untuk alpha. Donasi baru aktif setelah aturan penyedia, privasi, dan rekonsiliasi terverifikasi. Deployment dev/staging/prod terpisah; feature flag untuk opening, kota, pasar, dan musim. Migrasi DB kompatibel mundur, backup dan uji restore; rollback aplikasi tidak otomatis membalik migrasi data. Luncurkan terbatas terlebih dahulu; perluas setelah error, latensi, retensi dan biaya stabil.

### 22.1 Acceptance criteria rilis
- Neraca massa setiap resep seimbang; tidak ada output/saldo negatif; unit dan sumber fakta jelas.
- Settlement idempotent, uji multi-tab dan concurrent action, stok tidak ganda, timestamp server, akses silang akun ditolak.
- Ekonomi dan musim diuji 90 hari, termasuk pemain baru, churn, batas offline, reinkarnasi dan rollover; tidak ada eksploit dominan yang diketahui.
- Opening dapat dilewati, diulang, subtitle/mute/reduced motion bekerja; fallback data dan aset gagal bekerja.
- Pemilihan kota tidak meminta lokasi presisi; kota kosong tetap playable; kota/Bumi snapshot konsisten dan tidak menggandakan kontribusi.
- Performance budget terukur pada perangkat target; load test, soak test, restore dan rollback diuji; dashboard monitoring dan prosedur insiden siap.
- Review sains, lisensi aset, klasifikasi usia, privasi anak, keamanan, ketentuan donasi dan pemisahan aktivitas ASN selesai. Tidak ada klaim legal compliance sebelum ditinjau.
- Metrik §12 dipertahankan sebagai hipotesis beta; tambahkan completion onboarding, skip rate, time-to-first-action, tutorial abandonment, first sale, error settlement, retention per kota. Tidak mengumpulkan data pribadi yang tidak perlu. Telemetri event kecil, tanpa log isi data sensitif.

## 23. Changelog, status dan handoff AI
**Changelog v0.6 (24 November 2026):** nama TERRA NOVA dipilih pemilik; identitas Peradaban Bumi Baru, arc The Calling of Gaia, filosofi, tagline usulan, batas ekspansi dan pemeriksaan merek ditambahkan pada §0. Seluruh mekanik dan status keputusan v0.5 dipertahankan; tidak ada perubahan angka, scope MVP, atau arsitektur yang disetujui diam-diam.

**Disetujui secara konseptual:** referensi kesederhanaan Bos Warung, opening dari fakta nyata menuju fiksi Gaia, paparan gerakan lingkungan yang belum cukup mengatasi krisis, panggilan Gaia kepada pemain di kota masing-masing, dan pengayaan alur cerita/onboarding.

**Dipertahankan dari v0.4:** Gaia, sembilan tier, Karma, Reinkarnasi, Neraca Massa, Konverter, Alkimia Gaia, hadiah akhir cerita Opsi A, musim, satu Bumi Global, donasi kosmetik tanpa pay-to-win, target audiens 13+ yang masih memerlukan tinjauan.

**Perlu keputusan pemilik/Fase 0:** modal starter, durasi dan chapter, aturan perpindahan kota, pemetaan ilustrasi, enam fraksi dan proporsinya, Lazy Tick sebagai mekanisme tunggal, aturan poin/reinkarnasi, gate nontermal, definisi ZWM/BHI, carry-over musim, pasar, jadwal dan target pengujian. Jangan menafsirkan usulan sebagai persetujuan final atas angka atau mekanik.

**Perlu verifikasi:** konflik merek/nama TERRA NOVA, domain, akun sosial, statistik dunia/Indonesia/kota terbaru dan sumber gerakan, kebenaran resep teknis, legal/usia/privasi, lisensi aset, kemampuan integrasi Saweria, batas paket hosting/Supabase dan benchmark perangkat. Tidak ada data statistik aktual yang dikunci dalam versi ini. Tidak ada source code Bos Warung yang diaudit. Tidak ada kode atau database yang diubah.

### Prompt awal untuk AI coding agent
> Baca `GAME_SPEC v0.6.md` lengkap. Gunakan §0 dan §17–23 untuk memahami identitas, batas scope dan arah produk dan rekomendasi baru; pertahankan keputusan v0.4 yang belum diganti. Kerjakan Fase 0 saja. Buat matriks aturan final vs usulan, daftar konflik dan pertanyaan keputusan, model ekonomi 90 hari yang reproducible, desain Lazy Tick/transaksi, schema dan RLS, data provenance untuk opening, storyboard dan alur onboarding, performance budget, test plan, roadmap dan release gate. Pisahkan fakta eksternal dari simulasi. Jangan membuat aplikasi atau migrasi sebelum hasil review dan persetujuan. Gunakan bahasa Indonesia. Satu modul per sesi, commit dan catat status sebelum pindah modul.

Deliverables Fase 0: `GAME_SPEC_DECISIONS.md`, `TECHNICAL_DESIGN.md`, `DATABASE_SCHEMA.md`, `GAME_ECONOMY_MODEL.md` beserta script dan hasil, `OPENING_STORYBOARD.md`, `PERFORMANCE_BUDGET.md`, `TEST_PLAN.md`, `IMPLEMENTATION_ROADMAP.md`. File ini adalah sumber desain induk; bila keputusan berubah, revisi file induk terlebih dahulu.


## 24. Dynamic Waste Ecosystem (DWE) [R/U]
Arah pemilik: sampah adalah objek utama dan amunisi peradaban. DWE memasok WCS (angkut), WPS (olah), CES (ekonomi sirkular), GES (ekosistem Gaia), BHI dan ZWM. Keputusan rinci D15–D19 di bawah adalah usulan; tidak membatalkan D03–D14 atau membuka gate Fase 1.

### 24.1 Asal sampah
| Sumber | Material khas | Akses awal |
|---|---|---|
| Permukiman | Organik, plastik, kertas | Manual/drop-off/kontrak kecil |
| Pasar | Organik, kemasan | Kontrak gerobak |
| Komersial | Kardus, PET, kaleng, jelantah | Kontrak/pembelian |
| Industri | Logam, palet, residu | Kontrak lanjutan |
| Sungai/lingkungan | Material tercecer dan tercampur | Misi bersih lingkungan |
| TPA | Timbunan historis | Waste mining lanjutan |

Stok terdiri dari legacy waste (saldo awal terbatas), timbulan baru eksternal, dan material kembali pascapakai. Sungai/TPA menerima transfer dari sumber, bukan menciptakan ulang massa yang sudah dihitung. Produk kembali melalui kohort umur pakai pada fase lanjutan; tidak dihitung sekaligus sebagai timbulan baru. Data nyata kota hanya konteks edukatif bersumber dan bertahun; volume game dikalibrasi terpisah. MVP solo: permukiman, pasar, sungai sebagai tiga node awal usulan; katalog memuat tipe lain tanpa mengaktifkannya. Setelah multiplayer, node bersama per kota, bukan duplikasi per akun.

### 24.2 Aturan stok
Gunakan gram integer, timestamp server UTC, katalog versi dan komposisi berjumlah 100%. Tiap node memiliki stok per fraksi, kapasitas, laju timbulan, kontaminasi, asal massa, timestamp settlement.
```text
stok_akhir = stok_awal + timbulan_eksternal + transfer_masuk + pengembalian_produk - muat - transfer_keluar
tersedia = stok_fisik - reservasi_aktif
```
Kelebihan kapasitas dipindahkan ke node limpasan lingkungan/TPA dengan ledger, tidak hilang. Timbulan kota tetap berjalan tanpa login; cap 8 jam hanya berlaku produksi offline pribadi, bukan timbulan publik. Hitung interval secara batch, pecah pada batas perubahan laju/event/musim. Komposisi dan pembulatan harus mempertahankan gram. Node tidak mengalokasikan stok negatif. Pisahkan residu biasa dan B3 dalam katalog; B3 tidak dapat masuk pengolahan umum; penanganan khusus atau pengolah berizin dalam simulasi, mengikuti keputusan D02/D03 yang relevan.

### 24.3 Waste Collection System (WCS)
Manual collection, drop-off warga, pembelian material, kontrak kawasan, kontrak kota dan waste mining adalah jalur pasokan. MVP: pilih sumber, kendaraan gerobak, jumlah dan kontrak; drop-off opsional setelah loop stabil. Pada level lanjut motor roda tiga, pickup, truk dan otomatisasi kontrak. Kendaraan memiliki kapasitas, biaya, waktu perjalanan, kompatibilitas, status. Tidak ada perjalanan real-time wajib.

Status job: offered → reserved → in_transit → arrived → received; cancelled/expired sebelum muat mengembalikan reservasi. Saat muat, stok berpindah node→kargo, bukan langsung ke gudang. Setelah muat pembatalan tidak menghapus massa; kargo harus diterima atau dikembalikan melalui aksi tercatat. Gudang penuh membuat kargo menunggu, tidak hilang. Satu kendaraan tidak boleh memiliki dua perjalanan aktif. Server memvalidasi kapasitas, dana, sumber, izin, jam siap dan kepemilikan. Biaya dan imbalan dicatat satu kali; imbalan jasa dapat positif, nol, atau pembelian berbayar. Imbalan jasa dibayar saat penerimaan sah (usulan), tidak otomatis memberi kredit pengalihan.

Reserve/dispatch/receive masing-masing idempotent; row lock node, kendaraan, job, saldo, inventory dengan urutan global yang terdokumentasi. Reservasi kedaluwarsa yang belum dimuat dapat dilepas; job in_transit tidak dihapus saat TTL. Waktu tiba dihitung server; settle saat aksi relevan, tanpa ticker per kendaraan. Animasi lokal tidak menentukan hasil.

Contoh fixture [U]: pasar 500 kg, gerobak 50 kg, jarak 4 km, tarif dan biaya belum disahkan. UI menunjukkan estimasi biaya/imbalan, waktu PP, jumlah dan kapasitas gudang sebelum konfirmasi. Jangan memakai angka mockup sebagai harga resmi.

## 25. Siklus sirkular, lingkungan dan perkembangan [R/U]
Peradaban → konsumsi → timbulan → pengangkutan → pemilahan/pengolahan → produk → penggunaan → pengembalian pascapakai. Produk reuse/upcycle, kompos, material daur ulang, energi dan residu memiliki resep berversi. Energi kWh terpisah dari neraca massa; air, oksigen, bahan tambahan, gas, abu, lindi dan perubahan stok tetap tercatat. Poin/Karma/BHI/ZWM mengikuti aturan induk yang disahkan; transfer dan jual beli tidak otomatis memberi kredit pengolahan. Ledger gram asal dan siklus material mencegah kredit berulang akibat transfer atau jual-beli; material kembali tidak otomatis menambah target/kredit musim yang sama. Kebijakan kredit siklus lintas musim harus disahkan bersama D08.

Kebun Gaia: usulan D14 tetap berlaku; satu petak di lahan awal, benih dari Gaia, kompos matang dari pabrik, panen dan penjualan; residu tanaman dapat kembali ke organik setelah resep massa disahkan. Tidak ada sistem pertanian penuh pada Chapter I. Sungai: sumber misi, stok pencemaran dan indikator lokal; level tinggi dapat membuka penangkap sampah dan mikrohidro jika debit serta head memenuhi kelayakan simulasi. Posisi alur utama sungai dan jalan depan tetap; intake/return melalui saluran terpisah di bawah jalan, tidak membuang air ke jalan atau mencampur air proses kotor dengan sungai. Mikrohidro bukan waste-to-energy termal. WtE memakai residu yang layak setelah pemilahan, dengan kendali emisi dan sisa; tidak wajib bagi jalur God nontermal yang sedang dievaluasi.

### 25.1 Tahap fisik dan pasokan
| Tahap | Pasokan / kemampuan |
|---|---|
| Tukang Sampah | Manual, gerobak, kontrak kecil |
| Bank Sampah | Drop-off, pembelian, rute lokal |
| Industri Daur Ulang | Kontrak komersial, kendaraan lebih besar |
| Eco Industrial Park | Kontrak kota, pemulihan material dan energi |
| Zero Waste Civilization | Waste mining, pencegahan timbulan, jasa sirkular |

Tahap fisik bukan tier spiritual. Tidak ada fasilitas otomatis hanya karena tier naik. Pencegahan timbulan harus dihargai melalui jasa pemulihan, repair/reuse, efisiensi dan misi; jangan memberi insentif menghasilkan sampah baru. Usulan reward pencegahan perlu baseline/cap terverifikasi dan terpisah dari kredit massa.

### 25.2 Event [R]
Festival meningkatkan kemasan; panen raya organik; renovasi konstruksi; banjir memindahkan stok ke lingkungan; kampanye pemilahan menurunkan kontaminasi; pencegahan plastik menurunkan laju timbulan. Event data-driven, berversi, dengan interval, cap dan fraksi; jangan hitung massa banjir sebagai baru jika transfer. Tidak perlu peta baru.

## 26. Data, performa dan QA DWE [R]
Usulan entitas: waste_source_templates, waste_source_state (city/node/fraksi/gram/cursor/version), waste_origin_ledger, collection_jobs, vehicles, source_events, returned_material_cohorts (lanjutan). Reuse inventory, receipts, missions, transactions dan snapshots. Fase 1 fixture privat deterministik; fase auth server-authoritative; fase kota migrasi ke stok bersama tanpa menambahkan fixture privat ke kontribusi global. Jangan membuat satu row per kantong atau satu timer per rumah. Node kota usulan 20–50 pada beta, daftar/pagination/cache; update global dari agregat, bukan write hot-row setiap aksi. Snapshot pemain ≤20 KB dan performance budget §21 tetap.

QA tambahan: gram konservatif pada overflow dan return; kontaminasi/komposisi valid; dua pemain berebut stok terakhir; dua tab reserve/receive; expiry sebelum muat; kargo terlambat/gudang penuh; biaya dan reward tepat sekali; idle kota >8 jam; event/cutoff; permintaan nol; B3 ditolak; tidak ada kredit ganda pada transfer/olah ulang; kota kecil vs besar; jalur termal/nontermal dan pencegahan tetap layak. Ulang simulasi 90 hari dengan node terbatas, biaya kendaraan, permintaan, Kebun Gaia dan strategi pasokan; ukur kas buntu, dominasi, inflasi, stok tak terkelola, ZWM/upacara dan tier. Hasil CSV lama tidak dianggap validasi DWE.

## 27. Keputusan dan handoff v0.7
| ID baru | Usulan keputusan | Status |
|---|---|---|
| D15 | DWE, tiga node MVP, stok kota bersama lanjutan | Review |
| D16 | Reservasi, kargo, receipt, biaya/imbalan angkut | Review |
| D17 | Returned materials, ledger kredit dan pencegahan | Review bersama D08 |
| D18 | Sungai, saluran mikrohidro, WtE opsional | Review |
| D19 | Event timbulan, kurva pasokan, balancing | Review |

Gunakan DESIGN_SPEC v1.2 untuk visual. Audit D03–D19; sinkronkan TECHNICAL_DESIGN, DATABASE_SCHEMA, GAME_ECONOMY_MODEL, TEST_PLAN, PERFORMANCE_BUDGET dan roadmap setelah persetujuan. Tidak ada perubahan kode, DB, angka ekonomi atau status gate dari dokumen ini. Jika konflik dengan prompt historis §16/23, gunakan baseline v0.6 dan amendemen v0.7 sebagai usulan review terkini.


## 28. DLE — Dynamic Living Environment [D/R/U]
[D] Pemilik meminta NPC berjalan melintasi jalan depan gerbang; sesekali NPC membuang sampah ke sungai. Mobil pengangkut sayur terkadang menjatuhkan sayuran di jalan. Pemain mendapat tugas membersihkan dan bonus berupa material yang dapat diolah. Fitur tersedia sejak lahan awal, tetap hadir saat upgrade. DLE adalah subsistem DWE, bukan sumber massa independen atau simulasi lalu lintas real-time.

### 28.1 Jenis aktivitas dan event
| Event | Lokasi | Material | Jalur setelah diambil | Status |
|---|---|---|---|---|
| npc_litter_river | Tepi sungai/titik jangkau aman | PET, kaleng, plastik campuran | Pilah, jual, olah | D |
| vegetable_spill | Bahu jalan depan gerbang | Sayur/buah rusak | Kompos, BSF atau biogas bila tersedia dan layak | D |
| npc_litter_road | Bahu jalan | Kemasan makanan/kertas | Pilah | R |
| cargo_cardboard_spill | Bahu jalan | Kardus | Pilah/daur ulang | R |
| wind_debris / upstream_debris / fallen_leaves | Tepi lahan/sungai | Material campuran/daun | Pilah/kompos sesuai kualitas | R, lanjutan |
NPC/ kendaraan biasa tidak selalu menghasilkan sampah. NPC tidak dapat diprovokasi, ditabrak, atau dipaksa membuang sampah. Pemain tidak mengejar kendaraan. Buah/sayur jatuh dianggap tidak layak konsumsi langsung; bahan organik terkontaminasi dipisahkan dan tidak otomatis cocok untuk BSF/kompos. B3 ditolak dari pickup biasa.

### 28.2 Loop tugas dan hadiah
NPC atau mobil lewat → insiden muncul → ikon misi/pesan Gaia → pemain klik/tap sampah atau tugas alternatif → avatar menuju titik aman (opsional visual) → server memvalidasi → material masuk inventaris belum dipilah → pemain mengolahnya. Contoh pesan: “Ada sayuran tercecer di depan gerbangmu. Bersihkan jalan dan manfaatkan bahan organiknya.” Material adalah bonus utama; poin misi kecil opsional, terpisah dari kredit pengolahan; tidak ada uang premium, stamina atau hadiah berulang otomatis. Kredit pengalihan/Karma/BHI/ZWM mengikuti aturan induk, tidak diberikan dua kali saat pickup dan pengolahan. Kesehatan lokal dapat membaik saat sampah dipindah dari lingkungan ke penampungan yang benar, tanpa menyatakan materi hilang. Tidak menghukum pemain karena offline atau melewatkan insiden.

### 28.3 Parameter awal [U] — fixture, bukan balancing final
| Parameter | Nilai uji |
|---|---|
| Lalu lintas kosmetik | 1 NPC atau kendaraan setiap 20–60 detik saat scene terlihat |
| Slot evaluasi insiden | 3 menit waktu server; probabilitas 20% per slot |
| Batas insiden | 6 per hari UTC per pemain pada prototipe privat; maksimal 3 aktif |
| Sampah sungai | 0,2–1 kg per insiden |
| Sayuran jatuh | 1–3 kg per insiden |
| Batas material bonus | 12 kg per hari UTC; gram integer |
| Masa tampil/tugas | 15 menit sejak insiden dialokasikan; tidak menghapus massa |
Semua nilai konfigurabel dan wajib disimulasikan. Tidak ada akumulasi hadiah pickup pribadi selama offline; timbulan publik DWE tetap berlangsung. Jika pemain kembali, hanya insiden yang masih sah tampil. Frekuensi turun ketika pencegahan timbulan/edukasi warga meningkat (usulan), bukan naik karena pemain membeli mesin. Misi tutorial pertama boleh dijamin satu insiden, termasuk dalam kuota dan hanya sekali per akun.

### 28.4 Asal massa dan konsistensi server
NPC membuang dari alokasi stok permukiman/komersial; mobil sayur menjatuhkan dari alokasi pasar/organik atau kargo sumber yang sudah dicatat. Insiden memindahkan gram dari node sumber ke node bahu jalan/sungai; pickup memindahkan gram yang sama ke inventory. Tidak menambah timbulan eksternal kedua kali. Bila stok sumber tidak cukup, kecilkan insiden atau batalkan. Fixture privat memakai ledger terpisah dan tidak dihitung global; saat multiplayer gunakan alokasi node bersama, bukan menyalin sampah yang sama ke semua akun. NPC visual hanya merepresentasikan insiden sah, tidak dapat membuat massa.
Status: available → collected atau expired; expiry memindahkan alokasi ke backlog node lingkungan/TPA yang sesuai, tidak menghapus massa. Kapasitas gudang penuh: pickup ditolak tanpa mengubah stok. Server settle slot berdasarkan UTC dan cursor berversi; RNG deterministik/seed server, unik per scope+slot; refresh atau dua tab tidak membuat event baru. Batasi catch-up, catat slot terlewat tanpa membuat tumpukan tugas pribadi; stok publik dihitung oleh DWE terpisah. Klaim atomik dengan row lock, idempotency key, validasi pemilik/izin, status, expiry, kapasitas dan ledger; satu event hanya bisa diklaim sekali. Jangan mempercayai posisi avatar dari browser untuk menentukan hadiah; gunakan titik interaksi yang telah disahkan dan opsi daftar aksesibel.

### 28.5 Data, performa dan QA [R]
Usulan environmental_event_templates (jenis, bobot, fraksi, gram, ttl, versi), environmental_events (id, scope, source_node, target_node, slot, mass_g per fraksi, anchor, expires_at, status), environmental_event_cursor (scope, slot terakhir, kuota), reuse ledger dan receipts. Integrasi transaksi mengikuti urutan lock global DWE. Tidak perlu WebSocket, server physics, NPC pathfinding global atau cron per NPC. Animasi berjalan/mobil/lempar/jatuh lokal; status diambil pada aksi atau refresh batch terbatas. Scene hanya memuat aset yang diperlukan; detail di DESIGN_SPEC v1.3 §17–18.
QA: reload tidak meroll ulang; dua tab klaim sekali; sumber kosong; cap harian, pergantian UTC/musim, expiry, offline >8 jam, gudang penuh; gram source→environment→inventory→processing seimbang; tidak ada kredit ganda; pemain tak bisa memicu litter sendiri; bonus tidak mengalahkan kontrak; pencegahan menurunkan insiden tanpa mematikan ekonomi. Ulang simulasi 90 hari dengan/ tanpa bonus DLE dan ukur inflasi, waktu tier, kas buntu serta distribusi strategi. Target RAM/FPS tetap; belum dibuktikan.

## 29. Handoff v0.8 (historis — lihat §36 untuk handoff v0.9)
D20 [D]: NPC melintas, litter sungai, mobil sayur menjatuhkan muatan, tugas pembersihan dan bonus material. D21 [R/U]: probabilitas, kuota, reward tambahan, expiry, event opsional dan kebijakan multiplayer perlu review. D03–D19 tetap pada status sebelumnya. Gunakan DESIGN_SPEC v1.3 sebagai acuan visual terkini; §28–29 menambah §24–27 tanpa mengesahkan parameter lama. Perbarui register/TDD/schema/simulator/test plan/budget/roadmap setelah review; gate Fase 0 tetap berlaku.

## 30. Landing, akun dan opening [D/P — v0.9]
[D] Pemilik: domain (mis. teranova.id) langsung menampilkan landing sesuai desain `Asset/Terra Nova_ Gaia's New Civilization.png` dengan form Daftar/Login. Setelah daftar, cinematic langsung diputar tanpa tombol apa pun di awal; tombol hanya muncul di akhir video. Menerima panggilan → langsung ke lahan.

### 30.1 Landing (`web/landing.html`)
- Hero ilustrasi (potongan dari desain), kartu **Daftar / Login**, tombol **Lanjutkan dengan Google** berlabel "segera hadir" (nonaktif).
- Bagian bawah: kartu fitur, pratinjau lencana, Tentang, Cerita, Cara Bermain.
- Form daftar: nama pengguna, email, kata sandi, **pilih karakter pria/wanita**.
- Iframe cinematic `/intro/?embed=1&autostart=1` dibuka di dalam klik daftar (agar autoplay suara diizinkan browser). Mode embed menyembunyikan tautan login di dalam player; tombol Ulangi tetap tampil.
- Akhir video: event `terranova:intro-accepted` → kirim aksi `terima` (nama = nama pengguna, gender pilihan, kota Bandung) → fade ke hitam → `/` (lahan). Event `terranova:intro-done` dikirim saat audio penerimaan selesai (cadangan 12 detik, 3,5 detik bila bisu).

### 30.2 Akun (server)
| Komponen | Ketentuan prototipe |
|---|---|
| Tabel | `akun`, `sesi`, `pemain_akun` (state permainan per akun, JSON) |
| Nama pengguna | `^[A-Za-z0-9_.]{3,24}$`, unik |
| Kata sandi | 8–128 karakter; PBKDF2-SHA256 240.000 iterasi, salt per akun |
| Sesi | token acak; disimpan hanya SHA-256; cookie `tn_sesi` HttpOnly, SameSite=Lax, `Secure` otomatis bila `X-Forwarded-Proto: https`; umur 30 hari |
| Pembatasan | 8 login gagal per IP per 10 menit |
| Endpoint | `POST /daftar`, `POST /masuk`, `POST /keluar`, `GET /akun`; `/state` & `/aksi` wajib login (401) |
| Idempotensi | receipt aksi di-scope `akun_id:kunci` |
| Reset | tombol ↺ di Menu = reset progres akun; opening diputar lagi |

**Belum:** login Google (OAuth), verifikasi email, lupa kata sandi, pemeriksaan usia, kebijakan privasi & syarat layanan, penghapusan akun. Semua wajib sebelum rilis publik (§36).

### 30.3 Opening
Lihat §17.8. Panjang 120 detik, mengikuti storyboard §17.2. Penerimaan memutar dialog §17.4.

## 31. Intro di lahan (sekali per akun) [D/P — Evaluasi 1]
Urutan (`intro_selesai`, disimpan server; akun lama yang sudah menerima panggilan otomatis dianggap selesai):
1. HUD disembunyikan; kamera menampilkan lahan yang **berantakan** (§32).
2. Sinar cahaya Gaia turun ke tengah lahan; karakter muncul (teleport) dalam pose duduk.
3. Karakter menoleh kiri–kanan kebingungan, lalu berdiri.
4. Pesan Gaia (bertahap, dapat dilewati dengan tombol *Lewati*).
5. Kartu **Cara Bermain** (dapat dibuka lagi dari Menu).
6. HUD dan menu bawah muncul; aksi `intro_selesai` dikirim.

## 32. Sampah liar dan sumber sampah gratis [D/P — Evaluasi 1 & 2]
Sampah liar adalah material yang tergeletak di sekitar lahan dan dapat **dipungut** langsung (klik → avatar berjalan → aksi `pungut`). Setiap pungutan: material masuk gudang (kantong campur → Area Pilah; baterai → B3), **+2 koin, +3 poin**; ditolak bila gudang penuh.

| Jenis | Fraksi tujuan | Berat (g) |
|---|---|---|
| Botol plastik | plastik | 300–700 |
| Kaleng | logam/kaca | 200–500 |
| Kardus & kertas | kertas | 400–1.000 |
| Sisa organik | organik | 600–1.500 |
| Botol kaca | logam/kaca | 400–900 |
| Kantong sampah campur | campuran (perlu dipilah) | 1.500–3.000 |
| Baterai bekas | B3 | 80–200 |
| Sterofoam | residu | 150–400 |
| Daun kering / ranting / dahan / buah busuk (dari pohon) | organik | 150–400 / 250–700 / 600–1.200 / 300–700 |

| Sumber | Lokasi | Aturan [U] |
|---|---|---|
| Lahan awal | 9 titik di dalam pagar + 12 dari 24 titik luar | Sekali saat `terima` |
| Pertumbuhan liar | 24 titik luar (rumput atas/kiri/kanan, depan pagar, tepi sungai) | 1 per slot 90 detik, maks 16 di luar pagar |
| Pohon (Evaluasi 2) | 10 pohon sekitar lahan | Slot 60 detik, peluang 60%, maks 6; bobot daun 5, ranting 3, dahan 1, buah 2 |
| Kendaraan lewat (Evaluasi 2) | Bahu jalan atas (lajur ke kanan) / trotoar bawah (lajur ke kiri) | Slot 40 detik, peluang 45%, maks 5 di jalan; jarak minimum antar sampah |
| DLE v0.8 (§28) | Tepi sungai / bahu jalan | Tetap seperti §28.3, berjalan berdampingan |

Isi muatan per kendaraan: pikap sayur (organik, kardus), truk boks (kardus, kantong, sterofoam), motor (botol, kaleng, kantong), sepeda (botol, kardus), becak (kardus, organik, sterofoam), delman (organik, daun). Semua slot memakai RNG deterministik ber-seed slot, catch-up maksimal 3 slot, tanpa penumpukan offline.

**Catatan konsistensi massa [R, terbuka]:** sampah liar Evaluasi 1/2 saat ini adalah fixture privat yang **belum** diambil dari stok node DWE (§24, §28.4) sehingga berpotensi menjadi "massa baru". Sebelum multiplayer: sambungkan ke node permukiman/pasar/lingkungan atau beri label fixture terpisah yang tidak dihitung kontribusi global. Server juga **belum memvalidasi jarak** avatar saat memungut (posisi tetap bukan otorisasi, sesuai §28.4, tetapi titik interaksi perlu disahkan).

## 33. Pengembangan lahan [D/P — Evaluasi 1]
| Item | Harga (Gaia Coin) [U] | Efek |
|---|---|---|
| Petak tanam tambahan ke-2 / 3 / 4 | 250 / 500 / 750 | Petak di sisi kanan lahan, perilaku sama dengan Kebun Gaia (tanam, pupuk −25%, panen) |
| Perluasan gudang I / II | 400 / 800 | +250 kg per tahap (500 → 750 → 1.000 kg) |
Pembangunan bebas (posisi dipilih pemain) belum ada; posisi petak tetap. Tidak ada keunggulan berbayar uang nyata.

## 34. Pencapaian, misi dan menu terpadu [D/P — Evaluasi 1]
### 34.1 Delapan lencana (dihitung server, `meta.pencapaian`)
| Lencana | Syarat |
|---|---|
| Tangan Pertama | Pungut 1 sampah |
| Pemilah Andal | Pilah 10 kg bahan campuran |
| Penyubur Tanah | Buat kompos pertama |
| Panen Perdana | Panen sayur pertama |
| Saudagar Hijau | Memiliki 2.000 Gaia Coin |
| Penjaga Sungai | Bersihkan 5 sampah tepi sungai |
| Petani Kota | Memiliki petak tanam tambahan |
| Lahan Bersih | Semua sampah di dalam pagar dibersihkan |
Lencana bersifat kosmetik/naratif, tanpa hadiah koin. Pratinjau di Profil (ketuk avatar HUD) dan halaman Pencapaian.

### 34.2 Menu terpadu
Tombol Menu (HUD dan menu bawah) membuka: Misi (panduan langkah berikutnya), Pencapaian, Profil (ganti karakter pria/wanita), Pabrik, Kebun, Kembangkan Lahan, Angkut, Pasar, Gudang & Neraca, Cara Bermain, Kota/Bumi (terkunci, Fase 3), musik, suara, mulai ulang, keluar.

## 35. Ekonomi prototipe saat ini [P/U — wajib kalibrasi]
Angka yang berjalan di `server.py` (bukan balancing final):

| Aksi | Biaya / hasil |
|---|---|
| Pungut sampah liar | +2 koin, +3 poin |
| Angkut gerobak (Permukiman / Pasar / Sungai) | −4 / −6 / −2 koin; 5–50 kg; tiba 6 detik uji |
| Pilah | maks 10 kg campuran → 50% organik, 18% plastik, 10% kertas, 7% logam/kaca, 14% residu, 1% B3 |
| Kompos | 2 kg organik → 1 kg kompos + 900 g air/gas terkendali + 100 g residu; +40 poin |
| Daur plastik (pelet / pot) | 1 kg plastik → 850 g produk; +60 poin |
| Serah B3 | ≥100 g; poin kecil, tanpa koin |
| Benih | −2 koin; tumbuh 40 detik uji; pupuk 1 kg kompos −25% sisa waktu |
| Jual | sayur 24, kompos 1 kg 5, pelet 850 g 12, pot 850 g 14, kertas 1 kg 9, logam/kaca 1 kg 12 |
| DLE (§28) | +15 poin misi, material masuk gudang |

Pengamatan uji: satu siklus angkut 10 kg → pilah → olah → jual menghasilkan ±40 koin; petak ke-2 (250) butuh ±6 siklus. **Keputusan pemilik diperlukan:** apakah tingkat kesulitan ini disengaja (§36 K5). `simulasi.py` dan model 90 hari belum diperbarui dengan modal 1.000, sampah liar dan harga Evaluasi 1.

## 36. Handoff v0.9, celah dan keputusan terbuka
### 36.1 Status implementasi prototipe
Sudah dimainkan dan diuji di Chrome (akun penguji lokal): daftar → autoplay → ulangi → terima → intro lahan → pungut dalam/luar pagar → pilah/olah/jual → kebun & petak → gudang → angkut → DLE → keluar/masuk → sampah pohon & kendaraan → karakter wanita → arah kendaraan di kedua lajur. Tanpa error konsol.

### 36.2 Celah yang diketahui
| # | Celah | Dampak | Usulan |
|---|---|---|---|
| G1 | Animasi jalan memakai pose depan/belakang dicerminkan, bukan siklus langkah 4 arah | Gerak terasa kaku | Sheet jalan 4 arah × 3–4 frame (pria & wanita) |
| G2 | Login Google "segera hadir" | Tidak ada SSO | OAuth Google setelah domain & HTTPS siap |
| G3 | Tanpa pemeriksaan usia, kebijakan privasi, lupa sandi, verifikasi email, hapus akun | Blocker rilis publik 13+ | Wajib sebelum peluncuran |
| G4 | Kota otomatis Bandung; tidak ada layar pilih kota/profil | Bertentangan dengan §17.5 lama | Keputusan K1 |
| G5 | Tidak ada replay cinematic dari Menu/Jurnal | §17.5 meminta replay | Tambah "Tonton ulang opening" di Menu |
| G6 | Sampah liar belum terhubung ke stok DWE; jarak pungut tidak divalidasi | Massa baru / klik jarak jauh | §32 catatan |
| G7 | Aset: sprite 3,5 MB + latar 321 KB + cinematic 4,0 MB | Melebihi PERFORMANCE_BUDGET (aset pabrik ≤1 MB, opening 1,6 MB) | Kompres sprite ke WebP/atlas, turunkan resolusi, audio Opus |
| G8 | Mobile responsif tetapi belum diuji di perangkat Android 2 GB/iOS | Risiko performa & sentuhan | Uji Q20/Q24 |
| G9 | Telemetri onboarding (skip rate, time-to-first-action) belum ada | Metrik §22 tidak terukur | Event ringan tanpa data pribadi |
| G10 | Server `ThreadingHTTPServer` + SQLite | Cukup untuk uji tertutup saja | Infrastruktur produksi §19 |
| G11 | Label "ilustrasi" di video dihapus | §17.3 meminta ilustrasi AI dilabeli | Keterangan di kredit/Tentang |
| G12 | Tab Kota & Bumi terkunci | Sesuai rencana Fase 3 | — |

### 36.3 Keputusan yang diminta dari pemilik
- **K1** Pilihan kota: tetap otomatis, atau kembalikan layar pilih kota (sebelum/sesudah cinematic)?
- **K2** Kustomisasi karakter (rambut, baju, topi, aksesori) — perlu di Chapter I atau ditunda?
- **K3** Pemeriksaan usia & persetujuan orang tua untuk 13+ — bentuk dan posisinya di alur daftar.
- **K4** Replay cinematic dari Menu — ya/tidak.
- **K5** Kurva ekonomi (§35): pertahankan ketat atau naikkan harga jual/hadiah pungut.
- **K6** Sampah liar sebagai bagian neraca DWE resmi atau fixture privat.
- **K7** Prioritas siklus jalan karakter (G1) dan anggaran aset tambahan (fal.ai; terpakai US$0,56 dari batas US$1,50 yang disetujui).

### 36.4 Aturan untuk sesi AI berikutnya
Gunakan GAME_SPEC v0.9 + DESIGN_SPEC v1.4 sebagai acuan terkini. §30–§35 mendeskripsikan perilaku prototipe yang disetujui pemilik melalui evaluasi; angka bertanda [U] tetap usulan. D03–D21 tetap pada status sebelumnya. Evaluasi pemilik berikutnya dicatat di folder `Evaluasi/` lalu dirujuk ke nomor bagian dokumen ini. Dokumen turunan (TECHNICAL_DESIGN, DATABASE_SCHEMA, GAME_ECONOMY_MODEL, TEST_PLAN, PERFORMANCE_BUDGET, OPENING_STORYBOARD, roadmap) **belum** disinkronkan dengan v0.9.

**Changelog v0.9 (26 November 2026):** §17.5 alur onboarding baru; §17.6 modal 1.000; §17.8 status cinematic; §18.1 navigasi; §30 landing/akun; §31 intro lahan; §32 sampah liar, pohon, kendaraan; §33 pengembangan lahan; §34 pencapaian & menu; §35 ekonomi prototipe; §36 celah & keputusan.

## 37. Target gameplay feature freeze [D/R/U]
Realistic Economy, starter 1M GC uji utama; 100k pembanding; §35 histori. Semua harga katalog 02/09, quotes server dan resep tervalidasi; 11 §2–8 mengatur GT01–09, spawn, angkut, 15 tanaman, vitality, pasar, build, audio. §7b/c lama diganti oleh GT/GSG (06/10/11), tanpa 400k XP; §1/7e konverter hanya bagi proses relevan. §0.1 larangan sistem energi/pangan lama diganti scope lokal terbatas ini. 8 badge aktif tetap; merge IDs semantik dan grant satu kali. Stage fisik bukan tier. Sampah dari lingkungan, kargo, pohon dan sungai debit asal resmi, expiry backlog. Spawn tidak meningkat semata karena tier. Pangan 30–180 detik, langka 300–900 detik; label akselerasi. Vitalitas tidak turun offline. Jalan dan sungai tetap.
## 38. Sistem baru dan beta
Pay to Build menggantikan larangan top-up lama §9; payment nyata hanya beta setelah gate. GME/GBN, GGL/GPP, GIS/GAS/GCG/GAV mengikuti dokumen khusus. Global leaderboard multidimensi dan Self-Made; data lokal tidak masuk ranking. Chosen hanya kandidat dan konsep penghormatan; seleksi final ditunda. Prolog tidak diubah, replay tanpa grant, cinematic lanjut tidak membocorkan twist. Event, pasar bekas, recovery cash, knowledge center, feedback, admin config dan audit termasuk scope.
## 39. Release contract
Gunakan 00_FEATURE_FREEZE, TECHNICAL_DESIGN, DATABASE_SCHEMA, GAME_ECONOMY_MODEL, TEST_PLAN, PERFORMANCE_BUDGET, IMPLEMENTATION_ROADMAP dalam paket sebagai rancangan sinkronisasi; review terhadap repo sebelum merge. K1–K7 arah sesuai freeze; parameter dan hukum belum final. Tidak ada deploy publik, pengeluaran atau migrasi irreversible.
