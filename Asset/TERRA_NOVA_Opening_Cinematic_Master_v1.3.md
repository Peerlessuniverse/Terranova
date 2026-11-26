# TERRA NOVA — Opening Cinematic Script
**Peradaban Bumi Baru · Chapter I — The Calling of Gaia**  
**Versi 1.3 · 25 November 2026 · MASTER PRODUCTION SCRIPT · untuk review pemilik**

> Bumi tidak membutuhkan penghuni baru. Bumi membutuhkan peradaban baru.

Dokumen tunggal ini mengonsolidasikan v1.0 dan v1.1 serta mengembalikan desain Gaia orisinal (reference sheet pertama). Gunakan sebagai acuan produksi opening, menggantikan kedua draft cinematic sebelumnya; tidak menggantikan GAME_SPEC atau DESIGN_SPEC untuk mekanik permainan.

## 1. Brief produksi

- Judul prolog: **The Cry of Earth**; bab naratif berikutnya: **The Calling of Gaia**.
- Durasi video utama: 120 detik, tidak termasuk layar penerimaan interaktif.
- Format: fullscreen cinematic 16:9, 24 fps; fantasy realism dengan pembuka bergaya dokumenter ilustratif. Gameplay tetap pixel art isometrik 16-bit.
- Bahasa narasi: Indonesia; prompt generatif: Inggris. Subtitle ID dan EN terpisah.
- Kurva emosi: kekaguman → konsekuensi → perjuangan → krisis → wahyu → harapan → panggilan.
- Audiens: 13+; tanpa gore, sensualisasi, atau kilatan agresif.
- Tujuan: mengantar pemain dari masalah nyata menuju misi fiksi, tanpa membocorkan solusi/twist Neraca Massa.
- Acuan: GAME_SPEC v0.8 §17.1–17.8; DESIGN_SPEC v1.3 §1–2, §5, §8; OPENING_STORYBOARD.md dan PERFORMANCE_BUDGET.md dalam paket Fase 0; gambar landing yang disediakan pemilik.
- Status: rancangan produksi [R/U], bukan perubahan mekanik, approval gate Fase 1, ataupun pengesahan data publik. Delapan babak di bawah mempertajam enam babak baseline; The Awakening dan The Calling diperluas dengan Lament dan Title. Motion comic lama tetap fallback.

## 2. Character bible — Dewi Gaia

**Hierarki referensi visual (keputusan pemilik v1.3):**

1. `gaia_earth_goddess_character_reference.png` — reference sheet pertama, acuan utama wajah fiksi, rambut, kostum, turnaround, ekspresi, aksesori dan palet.
2. `Terra Nova_ Gaia’s New Civilization.png` — acuan pendukung atmosfer, pose tangan terulur dan branding.

![Gaia Character Reference Sheet — desain orisinal](./gaia_earth_goddess_character_reference.png)

Jika ada konflik, prioritaskan reference sheet pertama. Gunakan rambut panjang bergelombang cokelat dengan highlight hijau keemasan. Versi kedua dan foto wanita tidak digunakan sebagai referensi produksi. Jangan memasukkan form login, tulisan atau HUD ke footage. Tinjau lisensi aset sebelum publikasi.

| Atribut | Ketentuan kontinuitas |
|---|---|
| Identitas | Personifikasi Bumi; perempuan dewasa, anggun, bijaksana, beragensi, penuh harapan meski lelah |
| Wajah | Ikuti wajah fiksi pada reference sheet pertama: wajah lembut, mata hangat, alis natural, hidung dan bibir sesuai ilustrasi; pertahankan proporsi |
| Rambut | Rambut panjang bergelombang cokelat dengan highlight hijau keemasan, sesuai reference sheet pertama |
| Mahkota | Daun hijau, bunga putih, ornamen emas di dahi; bentuk tetap antar shot |
| Busana | Kain berlapis putih gading dan hijau zamrud dengan bordir emas serta ornamen daun; versi sinematik berpakaian lengkap dan tidak sugestif |
| Aksesori | Medali Bumi biru-hijau berbingkai emas di dada, anting emas-biru |
| Aura | Pita cahaya hijau-emas, partikel ringan; redup saat muncul, menguat saat memanggil |
| Gestur | Gerak halus, tatap kamera, tangan terbuka mengajak; bukan gestur memerintah |
| Suara | Perempuan dewasa, bahasa Indonesia natural, artikulasi jelas, tenang, hangat, sedikit melankolis, lalu tegas |
| State opening | Gaia masih terluka; peningkatan cahaya hanya simbol harapan, bukan pemulihan penuh atau kenaikan tier |

### 2.1 Master character lock (tambahkan ke semua shot Gaia)

```text
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
```

### 2.2 Negative prompt global

```text
Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

Jika generator tidak mendukung negative prompt, masukkan larangan utama sebagai instruksi positif/negatif dalam prompt biasa. Buat terlebih dahulu reference still Gaia (front, three-quarter, profile, full-body, close-up, hand extended), review manual; pakai gambar referensi yang sama untuk semua shot Gaia. Seed tetap bila platform mendukung, tetapi bukan jaminan kontinuitas.

## 3. Skenario dan shot list (120 detik)

Timecode adalah target timeline final, bukan panjang klip yang wajib didukung tiap generator. Generate shot terpisah; trim dan sambung di editor. Audio dibangun terpisah agar suara narator dan Gaia konsisten. Shot A01–H01 berjumlah 23 klip, ditambah satu still H02.

| ID | Timecode | Durasi | Visual / aksi | Kamera / transisi | Audio / narasi cue |
|---|---|---:|---|---|---|
| A01 | 00:00–00:04 | 4s | Bumi biru-hijau dari orbit, matahari terbit | Slow push-in, fade in | N1 mulai, pad lembut |
| A02 | 00:04–00:08 | 4s | Hutan, gunung dan lembah diselimuti embun | Aerial glide, dissolve | N1, burung dan angin |
| A03 | 00:08–00:12 | 4s | Daun jatuh ke sungai jernih | Macro follow, match cut air | N1 selesai, riak air |
| B01 | 00:12–00:18 | 6s | Kota tumbuh, transportasi dan gedung | Timelapse terkontrol | N2, ritme mulai naik |
| B02 | 00:18–00:24 | 6s | Produksi, logistik, belanja, kemasan | Tracking montage | N2, bunyi kota |
| B03 | 00:24–00:30 | 6s | Kemasan di selokan, aliran menuju sungai tercemar; overlay 2,1 miliar ton/tahun (2023) | Follow debris lalu pull back | N2 selesai, musik turun |
| C01 | 00:30–00:36 | 6s | Relawan membersihkan tepi sungai | Medium tracking | N3, musik harapan |
| C02 | 00:36–00:42 | 6s | Bank sampah Indonesia, penimbangan dan pemilahan | Close-up tangan, cut ke warga | N3 |
| C03 | 00:42–00:48 | 6s | TPS3R, edukasi dan fasilitas daur ulang | Slow pan, dissolve | N3 selesai |
| D01 | 00:48–00:54 | 6s | TPA luas; overlay Indonesia >34,6 juta ton (2025; 327 kab/kota) | Aerial pull back | N4, bass rendah |
| D02 | 00:54–01:00 | 6s | Sungai tercemar; overlay 19–23 juta ton plastik/tahun masuk ekosistem perairan | Latar stabil untuk overlay | N4, pulse lembut |
| D03 | 01:00–01:05 | 5s | Bumi dari orbit, meredup; overlay proyeksi 3,8 miliar ton/tahun pada 2050 | Slow fade to black | N4 selesai; hening |
| E01 | 01:05–01:09 | 4s | Gelap, partikel hijau-emas; label kisah fiksi | Soft bloom | Choir masuk |
| E02 | 01:09–01:15 | 6s | Siluet Gaia di hutan rusak, kain bergerak | Reveal dari belakang/samping | G1 mulai |
| E03 | 01:15–01:21 | 6s | Gaia berdiri; medali bumi berdenyut redup | Dolly, medium shot | G1 |
| E04 | 01:21–01:27 | 6s | Wajah Gaia, tatapan lelah namun berwibawa | Close-up stabil | G1 selesai |
| F01 | 01:27–01:32 | 5s | Gaia membuka telapak tangan, bayangan sungai | Medium close-up | G2 mulai |
| F02 | 01:32–01:38 | 6s | Visi alam, kota, sampah, usaha manusia | Cutaway vision, dissolve | G2 |
| F03 | 01:38–01:43 | 5s | Gaia kembali menatap, aura menguat | Slow push-in | G2 selesai |
| G01 | 01:43–01:48 | 5s | Cahaya dari medali menyebar ke bumi dan kota | Orbit / aerial transition | G3 mulai, crescendo |
| G02 | 01:48–01:53 | 5s | Cahaya menuju sebuah lahan kecil, gerobak dan gudang | Match cut ke Gaia | G3 |
| G03 | 01:53–01:58 | 5s | Gaia mengulurkan tangan ke kamera seperti referensi | Eye-level, dolly sangat halus | G3 selesai |
| H01 | 01:58–02:00 | 2s | Fade ke hitam, logo TERRA NOVA emas | Fade, tanpa gerak kompleks | Resolusi musik |

**H02 — interactive hold (di luar durasi 120 detik):** gunakan still final Gaia, tangan terulur. UI HTML menampilkan filosofi, judul dan CTA; tidak dibatasi waktu. H02 dihitung sebagai satu aset still, bukan klip bergerak dalam 120 detik.

## 4. Naskah voice-over dan subtitle

Naskah berikut dikunci untuk draft ini. Pembagian cue menggunakan waktu adegan; sesuaikan timing subtitle berdasarkan rekaman suara aktual. Baca dengan jeda alami, jangan mempercepat suara secara berlebihan. Jika tes baca tidak muat, pendekkan kalimat sebelum final mixing (terutama G3). Narator hanya sampai 01:05; Gaia mulai sesudah label fiksi.

| Cue | Waktu | Pembicara | Dialog Indonesia | Subtitle English (draft) |
|---|---|---|---|---|
| N1 | 00:00–00:12 | Narator | Sejak awal, Bumi memiliki siklusnya sendiri. Setiap air yang mengalir, setiap daun yang gugur, memiliki tempat dalam perjalanan kehidupan. | Earth has its own cycles. Every flowing stream and every fallen leaf has a place in the journey of life. |
| N2 | 00:12–00:30 | Narator | Kota tumbuh. Industri berkembang. Konsumsi meningkat. Pada tahun 2023, dunia menghasilkan sekitar 2,1 miliar ton sampah perkotaan. | Cities grew, industries expanded, and consumption rose. In 2023, the world generated an estimated 2.1 billion tonnes of municipal solid waste. |
| N3 | 00:30–00:48 | Narator | Namun manusia tidak tinggal diam. Mereka memilah, membersihkan, mendaur ulang, dan mengedukasi. Perjuangan itu membawa perubahan. Tetapi tantangan yang kita hadapi masih begitu besar. | Yet humanity did not stand still. People sorted, cleaned, recycled and educated. Their efforts made a difference, but the challenge remains immense. |
| N4 | 00:48–01:05 | Narator | Di Indonesia, lebih dari 34 juta ton sampah tercatat pada 2025. Setiap tahun, sekitar 19 hingga 23 juta ton plastik memasuki perairan dunia. Masihkah ada harapan? | In Indonesia, more than 34 million tonnes of waste were recorded in 2025. Each year, an estimated 19 to 23 million tonnes of plastic waste enter aquatic ecosystems worldwide. Is there still hope? |
| G1 | 01:09–01:27 | Gaia | Aku adalah Gaia. Aku telah menyaksikan perjalanan peradabanmu. Aku merasakan setiap luka yang tertinggal di tanah, di sungai, dan di udara. | I am Gaia. I have witnessed the journey of your civilization. I feel every wound left upon the land, in the rivers and in the air. |
| G2 | 01:27–01:43 | Gaia | Manusia telah berusaha menyembuhkanku. Namun luka-lukaku terus bertambah. Aku tidak membutuhkan lebih banyak janji. Aku membutuhkan tindakan. | Humanity has tried to heal me. Yet my wounds keep growing. I do not need more promises. I need action. |
| G3 | 01:43–01:58 | Gaia | Bukan kekayaan, kekuatan, atau kedudukanmu yang membuatku memanggilmu. Aku masih percaya manusia dapat berubah. Maukah engkau membantuku? | I call you not for your wealth, power or status. I still believe humanity can change. Will you help me? |

**Setelah pemain menerima panggilan (bukan bagian video):**

Gaia: “Terima kasih, manusia terpilih. Perjalananmu kini dimulai. Pergilah ke kotamu. Aku akan selalu menyertaimu.”

**Saat tutorial pertama:** “Selamat datang. Dari tempat kecil inilah perjalananmu dimulai. Hilangkan sampahku.”

## 5. Prompt produksi video per shot

### Global visual prefix

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
```

Tambahkan prefix global ke setiap prompt. Untuk E02–E04, F01–F03, G01/G03 yang menampilkan Gaia, tambahkan character lock §2.1 dan reference still yang disetujui. Semua shot menggunakan negative prompt global.

| Shot | Prompt (English) |
|---|---|
| A01 | Earth slowly rotating in deep space, blue oceans, green continents, thin luminous atmosphere, sunrise cresting the horizon. Gentle forward camera drift, peaceful sacred wonder, realistic planetary scale. |
| A02 | Glide above a lush tropical forest toward mist-covered mountains and a river valley at dawn, warm sunlight filtering through clouds, tranquil ecosystem, smooth aerial movement. |
| A03 | Follow a single leaf drifting from a tree into a clear stream, delicate ripples and sunlit stones, macro-to-water-level camera, end on the moving water surface for a match cut. |
| B01 | A thriving modern city gradually expanding, towers, streets and moving transport, controlled time-lapse feeling, realistic urban progress without chaos, daylight turning slightly cooler. |
| B02 | Track along everyday production and distribution: neatly packaged goods, warehouse movement, shopping bags and plastic packaging, natural human activity, a single flowing camera move. |
| B03 | A discarded plastic wrapper floats along a roadside drain into a polluted river, camera follows the flow and gently pulls back to reveal accumulated litter, somber realism without graphic imagery. |
| C01 | Community volunteers in appropriate work clothing collect litter from a safe riverbank, cooperative movement, gloves and collection bags, warm natural light, respectful eye-level tracking. Fictional illustrative footage. |
| C02 | Indonesian-style neighborhood waste bank, residents bringing sorted bottles and paper to a weighing station, close detail of hands and material, respectful community atmosphere, no identifiable real organization. |
| C03 | Small community recycling and waste sorting facility, workers demonstrating separation of materials, orderly work area, gentle pan, hopeful but grounded mood. |
| D01 | Illustrative Indonesian municipal landfill seen from high above, layered waste piles and distant vehicles for scale, restrained gray palette, slow aerial pullback, reflective rather than sensational. |
| D02 | Illustrative polluted tropical river with floating plastic debris, slow stable water-level tracking, restrained dark teal palette, uncluttered upper or side area for editorial fact card, absolutely no generated numbers or text. |
| D03 | Earth from orbit in a gradually dimming symbolic light, thin atmosphere, darkness slowly envelops the frame, emotionally reflective, no claim of literal planetary transformation. |
| E01 | Near-black frame with delicate emerald and gold particles slowly gathering into a distant glow, quiet sacred atmosphere, no flashes, uncluttered center for separately added fiction label. |
| E02 | Reveal the silhouette of Gaia standing among damaged trees and scattered waste, flowing layered robes moving gently in the breeze, dim green-gold aura, slow side reveal, dignified posture. |
| E03 | Medium shot of Gaia standing upright, hands relaxed, blue-green Earth medallion pulsing softly, floral crown and emerald ivory gold robes identical to reference, controlled dolly, weary but powerful guardian. |
| E04 | Intimate eye-level close-up of Gaia's face, tender sorrow and quiet determination, natural blinking and subtle breathing, soft bokeh, stable face and lighting, clean performance plate for later lip-sync if used. |
| F01 | Gaia slowly opens her palm, a delicate luminous vision of a river appears above it, subtle restrained magic, hand anatomy correct, gentle medium close-up, her face remains compassionate. |
| F02 | A poetic magical vision of forests, city waterways, discarded materials and people restoring nature, contained within softly glowing green-gold light, seamless restrained dissolve, symbolic not factual footage. |
| F03 | Return to Gaia's face as she lifts her gaze toward the viewer, her aura grows slightly brighter but she remains visibly weary, subtle forward camera move, resolute expression. |
| G01 | Green-golden light flows from Gaia's Earth medallion and expands into a symbolic globe, luminous lines reach many cities, elegant transition, no precise map labels or generated text. |
| G02 | A humble fenced plot with a small warehouse, handcart and sorting area beside a permanent asphalt road and a river across the road, realistic cinematic interpretation of the starter map, no advanced machinery, a narrow shaft of hopeful light arrives. |
| G03 | Gaia extends one open hand toward the camera, matching the welcoming gesture of the landing reference and the face and hairstyle of the first original character sheet, direct compassionate eye contact, stable natural hand anatomy, flowing robes, soft golden-green light, camera gently settles into a clean final frame. |
| H01 | Pure elegant near-black background, restrained gold dust settling slowly, clean central space for the official title added in editing, no generated lettering. |
| H02 | Still image: Gaia at eye level reaching toward the viewer, same face, crown, robes and Earth medallion, gentle hopeful expression, clear negative space for interactive title and CTA, no embedded text or UI. |

## 6. Audio direction and editing

- 00:00–00:12: piano, warm strings, gentle nature ambience.
- 00:12–00:30: light rhythmic pulse, urban textures; gradual tension.
- 00:30–00:48: human warmth, restrained hopeful strings; no triumphant exaggeration.
- 00:48–01:05: darker low drone, sparse percussion, brief silence before fiction transition.
- 01:05–01:27: soft wordless choir, harp, ethereal ambience.
- 01:27–01:43: intimate strings, leave room for Gaia's speech.
- 01:43–02:00: hopeful orchestral crescendo then warm resolution.

**Music generation prompt:** `Original two-minute cinematic environmental fantasy score, instrumental with subtle wordless choir. Begin serene and sacred, develop restrained industrial tension, return to human warmth, sink into reflective silence, reveal a mystical green-gold goddess motif, then resolve in a hopeful orchestral climax. No lyrics, no imitation of existing copyrighted themes, dialogue-friendly arrangement, soft ending.`

**Voice prompt — narrator:** `Adult Indonesian narrator, warm documentary tone, clear natural Bahasa Indonesia, reflective and factual, calm pacing, no exaggerated announcer delivery.`

**Voice prompt — Gaia:** `Adult female voice speaking natural Bahasa Indonesia, gentle and dignified, compassionate and wise, subtle sorrow becoming quiet resolve, intimate direct address, clear articulation, natural pauses, consistent voice throughout, no whispery sensual delivery.`

Mix dialogue above music; duck music during speech. Keep ambience subtle; avoid clipping. Proposed web master around -16 LUFS integrated and true peak ≤ -1 dBTP, subject to listening tests. Record voice first, then lock timeline; use off-camera/vision shots for longer speech and optional lip-sync on selected close-ups only. Do not rely on video model to generate coherent dialogue or text.

## 7. Editorial overlay & provenance

- 00:00–01:05: mark AI-generated real-world imagery `Ilustrasi` unobtrusively; never describe generated scenes as actual documentary evidence.
- 00:24–00:30, 00:48–01:05: fact cards as editorial overlays, not generated text. Keep captions separate; detailed sources accessible from Jurnal / pause overlay.
- 01:05–01:09: `Kisah fiksi • The Calling of Gaia` clearly visible.
- 01:58–02:00: add official TERRA NOVA title as separate graphic; longer text belongs on the interactive hold, not a two-second card.

### Statistik produksi — diwarisi dari register v1.1 bertanggal 25 November 2026

| Shot | Teks overlay | Sumber / cakupan |
|---|---|---|
| B03 | 2,1 MILIAR TON / sampah perkotaan dunia, 2023 | UNEP, Global Waste Management Outlook 2024, estimasi global |
| D01 | LEBIH DARI 34,6 JUTA TON / Indonesia, 2025 | SIPSN KLH, 34.674.702,79 ton; 327 kabupaten/kota pelapor, bukan total seluruh Indonesia |
| D02 | 19–23 JUTA TON / sampah plastik memasuki ekosistem perairan setiap tahun | UNEP, Plastic Pollution & Marine Litter, estimasi global; bukan hanya laut |
| D03 | 3,8 MILIAR TON/TAHUN / proyeksi sampah perkotaan dunia 2050 | UNEP GWMO 2024; skenario tanpa perubahan memadai, bukan fakta aktual |

Sumber langsung:
- https://www.unep.org/en/publications/report/global-waste-management-outlook-2024
- https://sampahnasional.kemenlh.go.id/portal-indikatif/
- https://www.unep.org/en/what-we-do/ocean-seas-and-coasts/ecosystem-degradation-pollution/plastic-pollution-marine-litter

Status menurut register v1.1: angka berasal dari halaman sumber yang diperiksa pada revisi sebelumnya; tidak diverifikasi ulang dalam konsolidasi v1.2, menunggu persetujuan editorial pemilik dan arsip snapshot sebelum publikasi. Jangan menyamakan timbulan dengan sampah tidak terkelola atau pencemaran. Gunakan tahun, cakupan dan label estimasi/proyeksi. SIPSN dinamis; jangan mengubah angka dalam video tanpa versioning. Angka 2050 ditampilkan visual saja agar narasi tidak terlalu padat. Uji durasi pembacaan N4; bila perlu pindahkan sebagian narasi ke overlay, bukan mempercepat suara. Tambahkan semua sumber ke Jurnal dan fallback. Data cards harus terbaca di mobile serta tersedia di transkrip. D02: gunakan footage ilustratif sungai tercemar dengan ruang kosong untuk overlay; D03: sisakan ruang teks sebelum fade. Dilarang membuat angka dengan model video. Lisensi aset tetap wajib.

## 8. Interactive ending and game handoff

At video end or Skip, show H02 (static still, no auto-replaying video), official logo and the following HTML text:

> Bumi tidak membutuhkan penghuni baru.  
> Bumi membutuhkan peradaban baru.  
> **TERRA NOVA — Peradaban Bumi Baru**  
> Chapter I — The Calling of Gaia  
> *One Earth. One Destiny. A New Civilization.*

Primary CTA: **Aku menerima panggilanmu**. Secondary: Ulangi cinematic; access to login remains available. Show acceptance dialogue after CTA; no required audio delay.

Flow: Landing → explicit start → video or fallback → acceptance → registration/login and age checks → character/city/profile setup → initialization → The Genesis tutorial. GAME_SPEC §17.5 and DESIGN_SPEC §2 differ in ordering city and character setup; preserve existing approved implementation order or resolve separately. No GPS. Intro skip/replay never grants coins, tier or inventory. Returning users resume existing onboarding/game state; replay available in Jurnal. Tier Awaken only after successful initialization. Preserve starter and DWE/DLE rules; do not initialize twice on refresh.

Use existing fields `onboarding_version`, `onboarding_step`, `intro_seen_at`, `city_id`, `tutorial_completed_at`; draft distinction between seen/skipped may be local until schema approved. Do not change database in Fase 0.

## 9. Web delivery specification (proposal)

| Item | Target / behavior |
|---|---|
| Master | 1920×1080, 24 fps, separate audio stems and clean master |
| Standard web | H.264 MP4 + AAC, 1080p, 20–35 MB target |
| Eco web | H.264 MP4 + AAC, 854×480, 5–9 MB target |
| Optional | WebM after codec/size testing; no need to ship both formats initially |
| Playback | HTML5 video, playsinline, progressive download / faststart, CDN with byte-range support |
| Loading | Poster first; preload none/metadata depending on test; video fetched after explicit start; default Eco on constrained connection where detectable or via manual setting |
| Fullscreen | Full viewport CSS by default; native fullscreen only on supported user gesture; safe-area controls |
| Mobile framing | Preserve whole 16:9 frame by default with tasteful dark background; avoid cropping face, hands or captions; separate portrait edit optional |
| Accessibility | Subtitle on by default, mute, volume, play/pause, skip, replay, keyboard focus, transcript, reduced-motion static option |
| Failure | Network/codec error or stall exposes retry, Eco, static fallback and skip; never traps player |
| Lifecycle | Pause on hidden tab; release video source/listeners on exit; do not load gameplay renderer concurrently |
| Budget | Opening separate from ≤3 MB initial gameplay, ≤250 KB compressed shell JS; previous 1.58 MB motion comic budget applies to fallback target, not video |

All file sizes and performance values are targets, not measured results. At the existing 1.6 Mbps test network, downloading 5–9 MB in full would take roughly 25–45 seconds before overhead; progressive playback and skip/fallback are essential. Do not cache full video automatically in PWA. CDN delivery creates bandwidth costs, to be measured on staging.

### Proposed asset tree

```text
cinematic/
  reference/gaia-character-reference.png  # production-only
  masters/                                # production-only, not public
  runtime/
    manifest.json
    poster.webp
    opening-1080p.mp4
    opening-480p.mp4
    ending-gaia.webp
    subtitle-id.vtt
    subtitle-en.vtt
    transcript-id.md
    fallback/                             # motion comic or static panels
```

Only runtime assets deployed to CDN. Version/hash URLs and editorial snapshot; do not commit large masters to the game repo. Manifest should identify version, duration, variants, poster, ending still, captions and fallback; exact schema deferred until implementation review.

## 10. Production workflow and acceptance

- [ ] Approve Gaia reference stills and visual continuity before video generation.
- [ ] Record scratch narration and verify all 120-second time slots; refine cuts and speech before final renders.
- [ ] Generate shot plates separately; inspect face, costume, hands, lighting, camera and material continuity.
- [ ] Edit in timeline, add approved titles and source/fiction labels, mix music and dialogue, create timed captions from final audio.
- [ ] Review fact register, asset rights, 13+ visual suitability, and absence of twist spoilers.
- [ ] Encode both variants and test actual size and quality; check seek/range support.
- [ ] Test desktop 1366×768 and mobile 360×800 / 390×844; Android physical 2 GB RAM; Wi-Fi and 1.6 Mbps constrained 4G; cold and warm cache.
- [ ] Check explicit start with audio, mute, captions, keyboard, reduced motion, full viewport, rotation, background/resume, skip at start/middle/end, network failure, fallback and replay.
- [ ] Verify no duplicated initialization or rewards on refresh/replay/two tabs; existing gameplay budgets remain intact; release video memory before renderer mount.
- [ ] Review GAME_SPEC v0.9 and DESIGN_SPEC v1.4 proposed amendments, update performance budget/technical design/test plan/roadmap/decisions only after approval; keep gate Fase 0 intact.

## 11. Master prompt (creative brief for multi-shot tools)

```text
Create a 120-second cinematic opening for TERRA NOVA: Peradaban Bumi Baru, Chapter I — The Calling of Gaia. Start with Earth's natural beauty (0–12s), human civilization and its waste footprint (12–30s), sincere community recycling and environmental action (30–48s), and the scale of environmental challenges (48–65s). Clearly transition from illustrative reality into fiction at 65s. Reveal Gaia, the Earth Goddess, using the first original fictional Gaia character reference sheet as the strict visual identity reference (65–87s). She is an adult, dignified, fully clothed guardian with long flowing wavy brown hair with subtle green-gold highlights, white flower and leaf crown, emerald and ivory layered robes with gold botanical details, blue-gold earrings and a glowing Earth medallion. Show her sorrow and determination (87–103s), then her personal invitation to the viewer as green-gold light reaches cities and a humble starter waste-management plot (103–118s). End on her extended hand, fade to an elegant dark title background (118–120s). Deliver a separate final still of Gaia reaching toward the viewer for the interactive screen. Preserve identity and costume across shots. Mood: wonder, consequence, struggle, crisis, revelation, hope, calling. Cinematic fantasy realism, 16:9, controlled camera, 24 fps delivery, restrained green-gold-blue palette. No gore, sensualization, flicker, random text, invented statistics or website UI. Do not reveal the game's mass-balance twist. Leave text, factual overlays, dialogue, music and interactive controls for post-production. Insert the four source-attributed fact cards (subject to editorial approval) listed in section 7 at their specified timecodes; never generate statistics within footage. Use the individual shot prompts and Indonesian voice script as the authoritative edit plan; do not assume a model can generate the full film in one pass.
```

## 12. Change log and unresolved items

- Retained 120-second target, expanded storyboard to eight babak and separated interactive hold from video duration. Dialogue shortened to fit proposed slots; actual recording not yet timed.
- Earlier draft explicitly explained that waste moves/burns/leaves residue; revised N4 avoids revealing the mass-balance twist per GAME_SPEC §17.6.
- Added character lock, mobile framing, data labeling, audio production, fallback, and QA. Character reference sheet has been generated in the preceding conversation; individual shot stills, video and audio have not been produced or tested.
- Source figures updated in v1.1 from UNEP and SIPSN pages; editorial approval, archived snapshots and playback/read-aloud testing remain pending. No changes made to ZIP, original specs, repo, database or implementation gates.
- Generator platform, final asset licenses, voice selection, CDN provider, editorial approval and exact final onboarding ordering are unresolved. Platform-neutral prompts are provided; adjust clip length and settings to the selected tool.

- v1.2: consolidated prior scripts, updated face reference hierarchy, hairstyle and all relevant prompts, and aligned D02 footage with the statistical storyboard. No new external data verification in this consolidation.

## 13. Prompt siap pakai untuk produksi individual

Setiap blok di bawah menggabungkan visual prefix, character lock bila relevan, prompt shot dan negative prompt sehingga tidak perlu merakit instruksi manual. Audio dan kartu statistik tetap ditambahkan saat editing. Gunakan reference image/crop yang sesuai untuk shot Gaia.

### A01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Earth slowly rotating in deep space, blue oceans, green continents, thin luminous atmosphere, sunrise cresting the horizon. Gentle forward camera drift, peaceful sacred wonder, realistic planetary scale.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### A02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Glide above a lush tropical forest toward mist-covered mountains and a river valley at dawn, warm sunlight filtering through clouds, tranquil ecosystem, smooth aerial movement.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### A03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Follow a single leaf drifting from a tree into a clear stream, delicate ripples and sunlit stones, macro-to-water-level camera, end on the moving water surface for a match cut.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### B01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
A thriving modern city gradually expanding, towers, streets and moving transport, controlled time-lapse feeling, realistic urban progress without chaos, daylight turning slightly cooler.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### B02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Track along everyday production and distribution: neatly packaged goods, warehouse movement, shopping bags and plastic packaging, natural human activity, a single flowing camera move.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### B03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
A discarded plastic wrapper floats along a roadside drain into a polluted river, camera follows the flow and gently pulls back to reveal accumulated litter, somber realism without graphic imagery.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### C01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Community volunteers in appropriate work clothing collect litter from a safe riverbank, cooperative movement, gloves and collection bags, warm natural light, respectful eye-level tracking. Fictional illustrative footage.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### C02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Indonesian-style neighborhood waste bank, residents bringing sorted bottles and paper to a weighing station, close detail of hands and material, respectful community atmosphere, no identifiable real organization.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### C03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Small community recycling and waste sorting facility, workers demonstrating separation of materials, orderly work area, gentle pan, hopeful but grounded mood.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### D01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Illustrative Indonesian municipal landfill seen from high above, layered waste piles and distant vehicles for scale, restrained gray palette, slow aerial pullback, reflective rather than sensational.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### D02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Illustrative polluted tropical river with floating plastic debris, slow stable water-level tracking, restrained dark teal palette, uncluttered upper or side area for editorial fact card, absolutely no generated numbers or text.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### D03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Earth from orbit in a gradually dimming symbolic light, thin atmosphere, darkness slowly envelops the frame, emotionally reflective, no claim of literal planetary transformation.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### E01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Near-black frame with delicate emerald and gold particles slowly gathering into a distant glow, quiet sacred atmosphere, no flashes, uncluttered center for separately added fiction label.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### E02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Reveal the silhouette of Gaia standing among damaged trees and scattered waste, flowing layered robes moving gently in the breeze, dim green-gold aura, slow side reveal, dignified posture.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### E03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Medium shot of Gaia standing upright, hands relaxed, blue-green Earth medallion pulsing softly, floral crown and emerald ivory gold robes identical to reference, controlled dolly, weary but powerful guardian.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### E04

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Intimate eye-level close-up of Gaia's face, tender sorrow and quiet determination, natural blinking and subtle breathing, soft bokeh, stable face and lighting, clean performance plate for later lip-sync if used.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### F01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Gaia slowly opens her palm, a delicate luminous vision of a river appears above it, subtle restrained magic, hand anatomy correct, gentle medium close-up, her face remains compassionate.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### F02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
A poetic magical vision of forests, city waterways, discarded materials and people restoring nature, contained within softly glowing green-gold light, seamless restrained dissolve, symbolic not factual footage.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### F03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Return to Gaia's face as she lifts her gaze toward the viewer, her aura grows slightly brighter but she remains visibly weary, subtle forward camera move, resolute expression.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### G01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Green-golden light flows from Gaia's Earth medallion and expands into a symbolic globe, luminous lines reach many cities, elegant transition, no precise map labels or generated text.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### G02

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
A humble fenced plot with a small warehouse, handcart and sorting area beside a permanent asphalt road and a river across the road, realistic cinematic interpretation of the starter map, no advanced machinery, a narrow shaft of hopeful light arrives.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### G03

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Gaia extends one open hand toward the camera, matching the welcoming gesture of the landing reference and the face and hairstyle of the first original character sheet, direct compassionate eye contact, stable natural hand anatomy, flowing robes, soft golden-green light, camera gently settles into a clean final frame.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### H01

```text
16:9 cinematic film shot, 24 fps delivery, polished environmental fantasy realism, natural motion, coherent spatial continuity, subtle filmic lighting, restrained color grading, one clear subject and one controlled camera move. Compose essential action within the central safe area for mobile adaptation. No embedded titles, captions, logos or interface. Generate clean visual footage for separate narration, music and editorial overlays.
Pure elegant near-black background, restrained gold dust settling slowly, clean central space for the official title added in editing, no generated lettering.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```

### H02

```text
16:9 cinematic still image, polished environmental fantasy realism, clean composition, no embedded text or interface.
Use the first original fictional Gaia character reference sheet as the strict visual identity reference. Use the original TERRA NOVA landing artwork as a supporting reference for atmosphere and welcoming pose. Preserve the referenced adult facial proportions, almond-shaped eyes, natural brows, nose and lips, long flowing wavy brown hair with subtle green-gold highlights, white flower and green leaf crown, delicate gold forehead ornament, blue-gold earrings, emerald and ivory layered flowing robes with botanical gold embroidery, and the blue-green Earth medallion. Adapt the outfit to full modest coverage suitable for a 13+ audience. Her expression is compassionate, dignified and weary but resolute. Maintain identical face, costume design, proportions and accessories across every shot. Soft green-gold magical aura, restrained particles, polished cinematic fantasy realism. No website UI, no logo, no generated text. Natural anatomy and physically coherent cloth motion.
Still image: Gaia at eye level reaching toward the viewer, same face, crown, robes and Earth medallion, gentle hopeful expression, clear negative space for interactive title and CTA, no embedded text or UI.
Avoid: Identity drift, face swap, age regression, changing crown or jewelry, inconsistent hair or costume, revealing clothing, sexualized pose, exaggerated anatomy, extra fingers, malformed hands, duplicated limbs, warped face, uncanny lip motion, flickering textures, unstable background, rapid camera shake, strobe, gore, horror, oversaturated neon, random text, watermark, login form, game HUD, fake documentary labels.
```


- v1.3: keputusan pemilik mengembalikan reference sheet pertama; semua character lock dan prompt terkait diselaraskan. Statistik, storyboard, durasi dan arsitektur tetap; tidak ada verifikasi data baru.
