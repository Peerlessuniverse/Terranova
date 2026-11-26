# TERRA NOVA — The Final Awakening: Waste-to-Energy & God Gate v1.0

26 November 2026 | Chapter I — The Calling of Gaia | Addendum 06 | Draft integrasi untuk review

## 1. Keputusan dan presedensi

[D] Arahan pemilik: God bukan kekayaan atau XP maksimum, melainkan optimalisasi konversi sampah menjadi listrik dan keberlangsungan Bumi. [R] Implementasi yang diusulkan di bawah. File ini mengamendemen GAME_SPEC v0.8 §7b–c, file 01, 03, 04, 05 DWE v1.0 setelah review. Pertahankan delapan tier pertama dan lima tahap fasilitas. Hapus 400.000 XP sebagai hard gate God; Archon adalah tahap naratif sebelum evaluasi (ambang Archon lama tetap sementara, review agar tidak menjadi penghalang jalur energi). Tidak ada syarat saldo, laba, kepemilikan pembangkit, atau leaderboard XP. Hadiah God 2.500.000 GC lama tetap hibah sekali seumur akun sampai diputuskan lain. Reinkarnasi, upacara ZWM global, dan kosmetik lama tidak berubah. God personal tidak sama dengan kemenangan kolektif musim. 

Twist saat Archon: Gaia memperlihatkan neraca massa dan energi seluruh perjalanan. Dialog: “Kau telah mengubah sampah menjadi kekayaan. Kini tunjukkan bahwa kekayaan itu mampu menjaga kehidupan. Aku tidak meminta api yang lebih besar. Aku meminta energi yang tidak meninggalkan luka baru.” Misi akhir The Final Awakening membuka panel audit, bukan kuis. Tampilkan syarat operasional keselamatan sejak awal; jangan sembunyikan risiko demi twist.

## 2. Katalog mesin tambahan WTE

Semua angka [U] adalah seed simulasi, bukan harga pasar atau spesifikasi desain teknik yang terverifikasi. 1 GC ≈ Rp1 nominal edukasi, tidak dapat dicairkan. CAPEX modul, bukan total EPC; biaya lokasi, jaringan, izin, lahan, instalasi, pengendalian emisi terpisah. OPEX adalah biaya variabel per unit throughput (kg input, m³ gas, kWh output, atau audit sesuai tabel), belum termasuk energi eksternal, tenaga kerja tetap, dan depresiasi. Kapasitas kW adalah daya nominal, bukan energi otomatis. F = tahap fisik minimum. ID WTE baru tidak menimpa MCH-001–138. Alias MCH memakai aset lama, bukan pembelian ganda. `partner` = akses layanan, bukan kepemilikan. `display_only` = ensiklopedia, tidak dapat dibangun/dijalankan. Semua resep `locked_pending_recipe` sampai mapping ID, neraca energi, dan QA selesai. Tidak ada panduan pembuatan/pengoperasian pembakar rumahan; proses berisiko diabstraksikan.

| ID | Nama | F | CAPEX GC | Kapasitas nominal | OPEX GC/unit | Mode | Fungsi / output |
|---|---|---:|---:|---|---:|---|---|
| WTE-001 | Insinerator rumahan sederhana (edukasi risiko) | 1 | 0 | 0 kg/jam | 0 | display_only | Tidak menghasilkan listrik; risiko asap dan abu |
| WTE-002 | Digester biogas rumah tangga | 1 | 4500000 | 5 kg/hari | 100 | sewa/beli | Biogas, digestat; bukan listrik langsung |
| WTE-003 | Digester komunal kecil | 2 | 35000000 | 50 kg/hari | 180 | sewa/beli | Biogas, digestat |
| WTE-004 | Tangki penerima organik | 2 | 5000000 | 200 kg/batch | 20 | beli | Buffer bahan |
| WTE-005 | Depackager organik | 3 | 220000000 | 500 kg/jam | 250 | beli | Organik bersih, kemasan reject |
| WTE-006 | Pulping organik | 3 | 65000000 | 200 kg/jam | 180 | beli | Slurry organik |
| WTE-007 | Pompa slurry | 3 | 15000000 | 2 m3/jam | 150 | beli | Transfer, bukan konversi |
| WTE-008 | Digester anaerobik industri (MCH-040) | 4 | 350000000 | 100 kg/jam | 400 | alias | Biogas, digestat |
| WTE-009 | Digester industri besar | 4 | 8000000000 | 2000 kg/jam | 350 | beli/mitra | Biogas, digestat |
| WTE-010 | Digester limbah cair industri | 4 | 3500000000 | 10 m3/jam | 900 | beli/mitra | Biogas, efluen |
| WTE-011 | Gas holder (MCH-043) | 4 | 85000000 | 50 m3/batch | 0 | alias | Penyimpanan gas |
| WTE-012 | Pemurni biogas (MCH-042) | 4 | 180000000 | 30 m3/jam | 500 | alias | Gas terkondisi, reject |
| WTE-013 | Modul kontrol H2S | 3 | 25000000 | 10 m3/jam | 300 | beli | Gas terkondisi |
| WTE-014 | Pengering gas | 3 | 18000000 | 10 m3/jam | 200 | beli | Gas terkondisi, kondensat |
| WTE-015 | Genset biogas mikro | 2 | 18000000 | 1 kW | 500 | sewa/beli | Listrik, panas, emisi |
| WTE-016 | Genset biogas komunal | 2 | 65000000 | 5 kW | 400 | sewa/beli | Listrik, panas, emisi |
| WTE-017 | Genset biogas (MCH-123) | 4 | 150000000 | 50 kW | 250 | alias | Listrik, panas, emisi |
| WTE-018 | CHP biogas 250 kW | 4 | 4500000000 | 250 kW | 300 | beli/mitra | Listrik dan panas berguna |
| WTE-019 | CHP biogas 1 MW | 5 | 18000000000 | 1000 kW | 250 | mitra/beli | Listrik dan panas berguna |
| WTE-020 | Flare keselamatan | 3 | 45000000 | 30 m3/jam | 100 | beli | Pengamanan gas; nol kredit listrik |
| WTE-021 | Sensor kebocoran gas | 2 | 3500000 | 1 audit | 100 | beli | Interlock keselamatan |
| WTE-022 | Dewatering digestat (MCH-041) | 4 | 120000000 | 300 kg/jam | 250 | alias | Padat dan cair |
| WTE-023 | Pengolahan digestat lanjut | 4 | 350000000 | 300 kg/jam | 350 | beli | Produk QC dan reject |
| WTE-024 | RDF shredder (MCH-120) | 4 | 150000000 | 300 kg/jam | 200 | alias | Cacahan residu |
| WTE-025 | Lini RDF/SRF (MCH-121) | 4 | 300000000 | 150 kg/jam | 300 | alias | RDF/SRF; bukan listrik |
| WTE-026 | Pengering RDF industri | 4 | 650000000 | 500 kg/jam | 400 | beli | RDF kering, uap |
| WTE-027 | QC bahan bakar | 3 | 35000000 | 1 audit | 10000 | beli/mitra | LHV, kadar air, kelayakan |
| WTE-028 | Insinerator mikro institusi | 3 | 250000000 | 15 kg/jam | 1800 | display_only/mitra | Pengolahan termal terkontrol; tanpa listrik default |
| WTE-029 | Insinerator komunal terkontrol | 3 | 1500000000 | 50 kg/jam | 1500 | mitra | Panas; listrik hanya dengan modul tervalidasi |
| WTE-030 | Modul WtE mitra beta (MCH-126) | 4 | 1500000000 | 120 kg/jam | 900 | alias/mitra | Listrik dan residu |
| WTE-031 | Insinerator modular industri | 4 | 18000000000 | 500 kg/jam | 900 | mitra/beli | Panas, abu, gas |
| WTE-032 | Moving grate WtE | 4 | 150000000000 | 5000 kg/jam | 700 | mitra | Panas, abu, gas |
| WTE-033 | Moving grate PLTSa skala kota | 5 | 650000000000 | 25000 kg/jam | 650 | mitra | Panas, abu, gas |
| WTE-034 | Fluidized bed combustion | 5 | 120000000000 | 4000 kg/jam | 800 | mitra | Panas dari bahan bakar sesuai |
| WTE-035 | Rotary kiln industri khusus | 5 | 90000000000 | 1500 kg/jam | 1800 | mitra | Penanganan khusus; nol kredit God untuk B3 |
| WTE-036 | Waste heat boiler | 4 | 8000000000 | 1000 kW termal | 150 | beli/mitra | Uap dari panas tercatat |
| WTE-037 | Steam turbine mikro industri | 4 | 3500000000 | 100 kW | 350 | mitra/beli | Listrik dari uap |
| WTE-038 | Steam turbine 1 MW | 4 | 25000000000 | 1000 kW | 300 | mitra | Listrik dari uap |
| WTE-039 | Steam turbine 10 MW | 5 | 160000000000 | 10000 kW | 250 | mitra | Listrik dari uap |
| WTE-040 | Organic Rankine Cycle | 4 | 12000000000 | 100 kW | 400 | mitra | Listrik dari panas sesuai |
| WTE-041 | Condenser | 4 | 1500000000 | 1000 kW termal | 100 | beli/mitra | Kondensat, panas buang |
| WTE-042 | Cooling tower | 4 | 2500000000 | 1500 kW termal | 100 | beli/mitra | Pelepasan panas terkendali |
| WTE-043 | Water treatment boiler | 4 | 750000000 | 3 m3/jam | 1500 | beli/mitra | Air proses, reject |
| WTE-044 | Gasifier biomassa skala komunitas | 3 | 350000000 | 50 kg/jam | 800 | mitra | Syngas, char, reject |
| WTE-045 | Gasifier RDF industri | 5 | 25000000000 | 1000 kg/jam | 1000 | mitra | Syngas, char, reject |
| WTE-046 | Syngas cleaning train | 4 | 2500000000 | 200 m3/jam | 900 | mitra | Gas sesuai QC, reject |
| WTE-047 | Syngas engine generator | 4 | 3500000000 | 100 kW | 450 | mitra | Listrik, panas, emisi |
| WTE-048 | Pirolisis biomassa mitra | 4 | 1500000000 | 100 kg/jam | 1300 | mitra | Biochar, gas, cairan; listrik tidak otomatis |
| WTE-049 | Pirolisis residu industri | 5 | 35000000000 | 1000 kg/jam | 1500 | mitra | Produk antara dan residu; QC wajib |
| WTE-050 | Landfill gas collection | 4 | 8000000000 | 300 m3/jam | 300 | mitra | Gas dari landfill historis |
| WTE-051 | Landfill gas engine | 4 | 10000000000 | 500 kW | 350 | mitra | Listrik dari gas historis |
| WTE-052 | Fuel cell biogas tervalidasi | 5 | 15000000000 | 100 kW | 600 | mitra/riset | Listrik dari gas sangat terpurifikasi |
| WTE-053 | Microbial fuel cell demonstrasi | 5 | 150000000 | 0.01 kW | 1000 | riset | Edukasi; bukan rute God sendiri |
| WTE-054 | Baghouse (MCH-127) | 4 | 150000000 | 500 kg/jam throughput lini | 180 | alias | Debu tertangkap |
| WTE-055 | Scrubber (MCH-128) | 4 | 250000000 | 500 kg/jam throughput lini | 250 | alias | Gas terkendali, limbah sekunder |
| WTE-056 | Kontrol NOx | 4 | 2500000000 | 1000 kg/jam throughput lini | 300 | mitra/beli | Pengendalian NOx |
| WTE-057 | Adsorpsi karbon aktif | 4 | 750000000 | 1000 kg/jam throughput lini | 200 | mitra/beli | Pengendalian polutan, sorben bekas |
| WTE-058 | CEMS (MCH-133) | 4 | 450000000 | 1 audit | 1000 | alias | Data emisi, interlock |
| WTE-059 | Ash handling tertutup | 4 | 650000000 | 300 kg/jam | 250 | beli/mitra | Abu terpisah |
| WTE-060 | Pemulihan logam bottom ash | 4 | 1500000000 | 300 kg/jam | 400 | mitra/beli | Logam QC, mineral reject |
| WTE-061 | Stabilisasi fly ash mitra | 4 | 0 | 100 kg/jam | 3500 | mitra | Residu aman melalui layanan berizin simulasi |
| WTE-062 | IPAL (MCH-129) | 4 | 150000000 | 200 kg/jam | 250 | alias | Air olahan, lumpur |
| WTE-063 | Meter energi (MCH-135) | 3 | 5000000 | 1 audit | 0 | alias | Rekaman energi |
| WTE-064 | Smart meter mikro | 1 | 350000 | 1 audit | 0 | beli/mitra | Pengukuran energi |
| WTE-065 | Inverter dan proteksi jaringan | 3 | 35000000 | 20 kW | 50 | beli | Distribusi, bukan sumber listrik |
| WTE-066 | Baterai penyimpanan | 3 | 80000000 | 20 kWh/batch | 100 | beli | Penyimpanan, bukan sumber listrik |
| WTE-067 | Transformer dan interkoneksi | 4 | 350000000 | 250 kW | 50 | beli/mitra | Distribusi |
| WTE-068 | Energy management system | 4 | 75000000 | 1 audit | 1000 | beli | Optimasi utilitas |
| WTE-069 | Konverter Asap Gaia | 4 | 0 | 1 audit | 0 | virtual modifier | Alias logis bundle kontrol emisi; bukan alat ajaib |
| WTE-070 | Pusat audit energi dan lingkungan | 5 | 250000000 | 1 audit | 10000 | mitra/beli | Evaluasi God |

F1 pemain dapat menyetor organik ke digester mitra dan menerima alokasi listrik. Insinerator rumahan bukan generator dan tidak menjadi mesin operasional. Tidak ada jalur pembakaran terbuka. Modul skala kecil yang tidak dapat memenuhi kontrol emisi tidak boleh beroperasi; jangan membuat UI petunjuk teknis. Pembangkit mitra memerlukan bukti penyelesaian dan alokasi energi unik. Mesin berkapasitas besar bukan otomatis lebih baik.

## 3. Jalur energi dan parameter seed

| Route ID | Jalur | Bahan eligible | Energi bruto referensi | Rasio net/bruto seed | Efisiensi net referensi | Status |
|---|---|---|---|---:|---:|---|
| ER01 | AD + genset mikro | organik basah sesuai | 0.12 kWh/kg | 0.80 | 0.24 terhadap energi gas | MVP mitra |
| ER02 | AD + CHP industri | organik basah sesuai | 0.20 kWh/kg | 0.85 | 0.32 terhadap energi gas | review |
| ER03 | RDF + WtE mitra | residu kering non-recyclable | 0.65 kWh/kg | 0.80 | 0.19 | MVP mitra |
| ER04 | Moving grate | residu eligible | 0.50 kWh/kg | 0.80 | 0.20 | review |
| ER05 | Fluidized bed | RDF sesuai | 0.75 kWh/kg | 0.80 | 0.22 | review |
| ER06 | Gasifikasi + engine | biomassa residu sesuai | 0.65 kWh/kg | 0.75 | 0.20 | research/partner |
| ER07 | Pirolisis + energi gas | residu sesuai | 0.35 kWh/kg | 0.70 | 0.12 | research only |
| ER08 | Landfill gas | gas historis terukur | 1.8 kWh/m3 gas | 0.85 | 0.26 | partner; terpisah dari God core |
| ER09 | ORC / waste heat | panas buang eligible | 0.10 kWh/kWh panas | 0.90 | 0.09 | tambahan, tanpa hitung ganda |
| ER10 | Fuel cell | gas QC | 2.2 kWh/m3 gas | 0.85 | 0.35 | research |

Parameter bukan jaminan hasil; kalibrasi menggunakan data teknis. Untuk konsistensi, `gross = min(seed_per_unit*input, energy_in_kWh*eta_gross, rated_kW*active_hours)`. Untuk AD, energi masuk generator berasal dari volume gas yang benar-benar tercatat, bukan nilai kalor organik mentah; gas tidak boleh dijual dan dipakai sekaligus. Untuk termal, `energy_in_kWh = eligible_kg * LHV_MJ_kg / 3.6` dengan LHV aktual simulasi yang tervalidasi. LHV basis as-received. `net = max(0,gross - parasitic_kWh - allocated_external_process_kWh)`; jika konsumsi melebihi produksi, catat defisit; jangan hilangkan biaya. Pengeringan, pemilahan, pompa, kontrol emisi termasuk beban. Seed rasio net hanya fallback beta, jangan dikurangkan lagi bila beban aktual sudah dihitung. Listrik tidak menutup neraca massa. Gas, digestat, abu, air, emisi dan residu tercatat terpisah. Panas tidak dihitung sebagai listrik. Tidak ada perkalian produksi saat transfer atau storage.

Harga listrik seed: offset konsumsi sendiri 1500 GC/kWh, ekspor kontrak 1000 GC/kWh; hanya ekspor menciptakan kas, offset mengurangi tagihan yang benar-benar ada. Tidak ada klaim tarif PLN/PPA aktual. Meter ekspor, konsumsi, rugi penyimpanan dan inventaris harus seimbang. Pasokan/pasar terbatas. PV dan mikrohidro boleh mendukung BHI dan menekan biaya tetapi bukan listrik dari sampah. Gas landfill lama memberi kredit remediasi terpisah; jangan memberi insentif membuat landfill baru.

## 4. God Gate: audit 14 hari aktif dalam musim

Seluruh ambang berikut [U] untuk balancing, bukan standar lingkungan resmi. Window rolling 14 hari kalender server Asia/Jakarta; minimal 10 hari aktif dengan settlement valid. Tidak dapat menghapus riwayat dengan pindah kota atau reset. Evaluasi server atomik; gagal satu gate => Archon / God eligibility pending. Tidak ada rata-rata skor yang dapat menutupi pelanggaran keselamatan.

| Gate | Kondisi usulan |
|---|---|
| G01 | Archon narrative reached; tidak ada tambahan XP God |
| G02 | ≥100 kg sampah eligible asal unik ditangani selama window; ≥20 kWh listrik net waste-origin terselesaikan |
| G03 | ≥90% pengalihan landfill sesuai definisi DWE 01; stok belum selesai tetap denominator |
| G04 | ≥85% material recoverable yang diterima benar-benar digunakan ulang/didaur ulang/biokonversi material; tidak ada pengalihan material recyclable ke termal |
| G05 | ≥80% potensi listrik net layak dari residu eligible yang tersedia dan dipilih melalui rencana alokasi yang ditetapkan sebelum produksi; denominator mencakup lot eligible belum diproses, bukan hanya lot sukses; kuota dibatasi kapasitas kontrak dan kebutuhan listrik yang dibuktikan |
| G06 | ≥80% efisiensi relatif referensi per jalur, berbobot energi input; 100% bukan efisiensi fisik absolut |
| G07 | ≥85% listrik net digunakan atau diekspor secara terukur; tidak ada produksi sia-sia untuk grinding |
| G08 | Karma ≤25%; nol kejadian emisi tak terolah, semua kontrol wajib aktif dan catatan emisi valid; nol pelanggaran belum diselesaikan |
| G09 | 100% B3, fly ash, digestat reject, efluen dan residu lain memiliki disposition aman atau penyimpanan valid dalam batas waktu/kapasitas; tidak ada pembuangan liar |
| G10 | Neraca massa dan energi 100% lolos; tidak ada kredit ganda atau transaksi fraud |
| G11 | BHI lokal rata-rata ≥80/100 dan tidak turun selama window; gunakan BHI asli setelah normalisasi yang disetujui; jangan diam-diam ubah formula |

G05: `potential = Σ eligible_lot_allocated_input * validated_net_yield`; ukur realisasi `min(1, net/potential)`. Alokasi ex-ante berdasarkan sumber, kapasitas dan kebutuhan; dilarang memilih hanya hasil sukses setelah kejadian. G06: `ratio = Σ min(actual_net,reference_net_for_actual_input) / Σ reference_net_for_actual_input`. Denominator nol/kurang data = pending, bukan lulus. G04 denominator seluruh fraksi recoverable masuk termasuk stok. AD memakai organik yang sesuai, digestat harus ditangani; tidak perlu memaksa termal untuk lulus. Target 20 kWh dapat dicapai via komunitas, bukan pembelian mesin. Jika pencegahan sukses sehingga pasokan rendah, kontribusi proyek bersama yang sudah ada dapat dialokasikan; jangan menambah sampah buatan. Uji wilayah rendah pasokan sebelum rilis. BHI kolektif tidak dijadikan hard gate personal agar pemain lain tidak dapat menyabotase; ZWM tetap syarat upacara global.

## 5. Misi dan lencana baru

Reward GC hibah sekali per ID lifetime, tunduk ledger file 03. Poin lingkungan bonus 0 agar tidak menyamarkan twist; poin biasa tetap berasal dari aksi valid. Tidak ada hadiah per kg dibakar.

| ID | Misi | Trigger server | GC | Badge |
|---|---|---|---:|---|
| WE01 | First Spark | ≥1 kWh net waste-origin dimanfaatkan | 1000 | BE01 Percikan Gaia |
| WE02 | Organic Power | ≥5 kWh AD net digunakan, digestat aman | 5000 | BE02 Biogas Pioneer |
| WE03 | Residue Only | 20 kg residu eligible diolah, nol recyclable termal | 5000 | BE03 Recycle First |
| WE04 | Energy Literacy | audit energi pertama valid | 2000 | BE04 Energy Accountant |
| WE05 | Community Grid | alokasi listrik mitra ≥10 kWh digunakan | 10000 | BE05 Community Power |
| WE06 | Clean Air | 7 hari aktif operasi tanpa emisi tak terolah | 15000 | BE06 Breath of Earth |
| WE07 | Ash Responsibility | 10 lot abu ditangani aman | 10000 | BE07 Ash Guardian |
| WE08 | Water Guardian | 10 lot efluen diolah dan tercatat | 10000 | BE08 Water Steward |
| WE09 | No Methane Leak | 10 audit AD valid tanpa kebocoran belum ditangani | 10000 | BE09 Methane Keeper |
| WE10 | Efficient Power | G06 dan G07 lolos satu window | 25000 | BE10 Energy Optimizer |
| WE11 | Circular Balance | G03 dan G04 lolos satu window | 25000 | BE11 Circular Master |
| WE12 | Final Awakening | G01–G11 lulus atomik | 0 (hibah tier terpisah) | BE12 The Final Awakening |
| WE13 | Gaia Sustained | God gate dipertahankan 30 hari, evaluasi rolling | 50000 | BE13 Eternal Steward |
| WE14 | Earth Reborn | upacara kolektif sesuai §7g | 0 | badge existing, jangan duplikasi |

BE01–04 bronze, BE05–09 silver, BE10–11 gold, BE12–13 legendary. Lencana historis permanen; status operasi God dapat pending jika gate dilanggar. Jangan mengharuskan misi khusus abu atau biogas untuk semua jalur; hanya relevan sesuai teknologi. Badge BE12 berbeda dari BT09 sebagai bukti audit, bukan pengganda reward.

## 6. Schema dan integrasi

Tambahkan `energy_route_catalog`, `machine_energy_specs`, `energy_batches`, `energy_meter_events`, `energy_allocations`, `environmental_audits`, `god_gate_snapshots`. Gunakan integer Wh, gram, mL, GC; energi termal dipisah dari listrik; `origin_lot_id`, `route_id`, `process_batch_id`, `meter_event_id`, `recipient_id`, `ruleset_version`, `window_start/end`, `city_id`, `quality_status`, `evidence_id`, `idempotency_key`. Alokasi energi partner total ≤ meter net aktual; atribusi hanya ke origin waste yang diterima, tidak mengklaim listrik grid. Ledger konsumsi/ekspor sekali; ownership dan RLS. Lazy Tick tetap maksimal offline 8 jam; audit agregat saat settlement, daily snapshot dan final gate; tidak ada loop per detik. Aturan God versi baru berlaku untuk musim berikutnya atau beta sebelum season dimulai; tidak merampas badge historis.

Mapping: file 01 aturan terminal diversion dan pasar listrik; file 02 tambah harga listrik seed terpisah serta material gas/abu jika belum tersedia dengan ID existing; file 03 baris God dan gate, misi WE/BE; file 04 tambah test; file 05 §261 cabut klaim God tanpa listrik, pertahankan tanpa termal melalui AD. Alias WTE-008/011/012/017/022/024/025/030/054/055/058/062/063 merujuk MCH yang disebut, bukan aset baru. Seluruh 70 record termasuk alias, display dan audit. Field luas, kebutuhan air, pemetaan recipe, dan ukuran kontrol emisi belum ditetapkan untuk aset tambahan: wajib sebelum executable. `partner` harus memiliki harga jasa dan bukti kapasitas sebelum aktivasi. Nilai CAPEX 0 bukan pembelian bebas.

## 7. Acceptance tests

1. Pemain terkaya tanpa listrik gagal; XP 1 juta tanpa G02 gagal. 2. Pemain Archon dengan saldo rendah dan AD mitra dapat lulus. 3. Pembakaran PET bersih ditolak. 4. B3 dan PVC tidak masuk jalur residu eligible. 5. Insinerator rumah tidak executable. 6. Mesin termal tanpa kontrol emisi, monitoring atau kapasitas pendukung gagal start. 7. Genset tanpa gas menghasilkan nol. 8. Daya dikali waktu tidak melampaui energi bahan. 9. Konsumsi parasitik melebihi bruto menghasilkan defisit. 10. Penyimpanan tidak menduplikasi Wh. 11. Ekspor dan offset tidak ganda. 12. Dua pemain tidak mengklaim alokasi sama. 13. Abu landfill mengurangi diversion sesuai definisi lama. 14. Emisi tertangkap tetap punya residu. 15. BHI turun atau data hilang gagal. 16. Window dengan denominator nol gagal/pending. 17. Retry audit tidak membayar hibah ulang. 18. Season reset tidak menghapus audit historis. 19. Jalur termal dan nontermal sama-sama feasible. 20. PV-only gagal G02. 21. Heat-only gagal G02. 22. Landfill baru tidak memberi kredit. 23. Reinkarnasi tidak mengulang hadiah. 24. Pasokan rendah dapat memakai mitra tanpa membuat sampah baru. 25. Simulasi 90 hari mengukur proporsi lulus, kas buntu, dominasi rute, energi net, emisi, residu, inflasi dan kontribusi bersama.

Belum menjalankan simulasi, belum mengaudit harga pemasok, belum membuat migration/kode. Referensi teknis untuk verifikasi lanjutan: World Bank What a Waste, UNEP Global Waste Management Outlook, IEA Bioenergy, IPCC waste sector guidance, standar teknis dan ketentuan emisi Indonesia yang berlaku. Dokumen ini bukan manual rekayasa atau bukti kepatuhan hukum. Review pemilik diperlukan atas ambang G01–G11 dan jadwal penerapan sebelum coding.
