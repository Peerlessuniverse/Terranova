# TERRA NOVA — Master Machinery & Energy Catalog v1.1

**Chapter I — The Calling of Gaia | Addendum 09 | 26 November 2026 | Seed katalog untuk review | GAME_SPEC v0.9 / DESIGN_SPEC v1.4**

## 1. Kontrak katalog
Gabungan utuh katalog file 05, 06 dan 07, bukan penawaran pemasok. Semua harga tabel master adalah harga referensi edukatif profil realistis (1 GC referensi merepresentasikan Rp1, tidak dapat ditukar uang), bukan harga aktif prototipe v0.9. Kapasitas, OPEX dan footprint adalah parameter game belum tervalidasi. Harga 0 berarti starter, referensi, mitra atau modifier sesuai konteks; bukan aset gratis untuk dijual. Katalog dapat dibaca setelah HUD tersedia (tanpa preload saat onboarding); tahap F adalah syarat akses operasi, bukan syarat melihat informasi. Seluruh aset berisiko tetap abstrak, tanpa panduan teknis dunia nyata. Jangan mengeksekusi resep, membebankan biaya atau menjanjikan kapasitas sebelum mapping dan QA selesai.

F1 Tukang Sampah; F2 Bank Sampah; F3 Industri Daur Ulang; F4 Eco Industrial Park; F5 Zero Waste Civilization. Skala industri besar WTE tetap terlihat; jalur kepemilikan/mitra sesuai validasi. DRES tetap modul rumah tangga–UMKM; batas agregat lama 100 kW/200 kWh dipertahankan sebagai default review, bukan batas visi ekspansi keseluruhan. Tidak menambah batas permanen baru tanpa keputusan eksplisit.

## 2. Tabel master untuk UI/seed
Satu baris per ID sumber; canonical_id menentukan inventaris, bukan ID kartu katalog. Angka harga integer GC. Kapasitas disimpan sebagai label sampai unit dinormalisasi. OPEX MCH/WTE adalah GC per unit basis sumber (input atau output/audit sesuai fungsi), DRES mengikuti profil §4. Area TBD berarti belum ditentukan. Mode `review akses` memerlukan aturan file 05; bukan izin beli otomatis. Harga alias ditampilkan dari canonical; nilai sumber tetap dicatat dalam lampiran konflik. Semua baris dapat dibaca, status awal operasi `locked_pending_validation`; `display_only` tidak bisa dioperasikan, `riset` tidak dianggap produksi komersial. 


### Pengumpulan, pemilahan dan penyimpanan

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-001 | MCH-001 | Tong sampah terpilah | 1 | 45000 | 30 kg/batch | 0 | 1 | review akses | sampah terpilah → stok |
| MCH-002 | MCH-002 | Gerobak dorong | 1 | 750000 | 25 kg/trip | 0 | 2 | review akses | sampah sumber → kargo |
| MCH-003 | MCH-003 | Timbangan gantung | 1 | 85000 | 50 kg/batch | 0 | 1 | review akses | lot → berat terukur |
| MCH-004 | MCH-004 | Timbangan digital meja | 2 | 450000 | 150 kg/batch | 5 | 1 | review akses | lot → berat terukur |
| MCH-005 | MCH-005 | Meja pilah manual starter | 1 | 0 | 20 kg/h | 50 | 4 | review akses | campuran → fraksi |
| MCH-006 | MCH-006 | Rak gudang | 1 | 350000 | 100 kg/batch | 0 | 3 | review akses | material → stok |
| MCH-007 | MCH-007 | Bak penampung tertutup | 1 | 250000 | 100 kg/batch | 0 | 2 | review akses | organik → stok |
| MCH-008 | MCH-008 | Stasiun cuci dan pilah | 2 | 2500000 | 100 kg/h | 400 | 8 | review akses | plastik terpilah → plastik bersih |
| MCH-009 | MCH-009 | Press manual kardus | 2 | 3500000 | 30 kg/h | 100 | 4 | review akses | kertas → bale |
| MCH-010 | MCH-010 | Baler hidrolik | 2 | 25000000 | 150 kg/h | 180 | 12 | review akses | kertas/plastik → bale |
| MCH-011 | MCH-011 | Conveyor pemilah | 3 | 75000000 | 500 kg/h | 100 | 35 | review akses | campuran → fraksi |
| MCH-012 | MCH-012 | Trommel screen | 3 | 150000000 | 1000 kg/h | 150 | 45 | review akses | campuran → fraksi ukuran |
| MCH-013 | MCH-013 | Magnetic separator | 3 | 45000000 | 500 kg/h | 80 | 10 | review akses | campuran → besi dan nonbesi |
| MCH-014 | MCH-014 | Eddy current separator | 4 | 450000000 | 1500 kg/h | 180 | 30 | review akses | campuran kering → nonferrous |
| MCH-015 | MCH-015 | Air classifier | 3 | 120000000 | 500 kg/h | 150 | 20 | review akses | campuran kering → fraksi ringan/berat |
| MCH-016 | MCH-016 | Ballistic separator | 4 | 500000000 | 2000 kg/h | 180 | 50 | review akses | campuran → fraksi 2D/3D |
| MCH-017 | MCH-017 | Optical NIR sorter | 4 | 1200000000 | 2000 kg/h | 250 | 50 | review akses | plastik → fraksi polimer |
| MCH-018 | MCH-018 | Robot pemilah AI | 5 | 2500000000 | 2500 kg/h | 300 | 60 | review akses | campuran → fraksi |
| MCH-019 | MCH-019 | Jembatan timbang | 4 | 350000000 | 30000 kg/batch | 500 | 100 | review akses | truk → berat terukur |
| MCH-020 | MCH-020 | Bunker penyimpanan | 4 | 150000000 | 20000 kg/batch | 0 | 100 | review akses | material → stok |

### Organik, kompos dan biokonversi

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-021 | MCH-021 | Tong komposter starter | 1 | 5000 | 2 kg/h | 120 | 1 | review akses | organik → kompos |
| MCH-022 | MCH-022 | Komposter ember bertingkat | 1 | 85000 | 10 kg/batch | 100 | 1 | review akses | organik → kompos dan cairan |
| MCH-023 | MCH-023 | Komposter takakura | 1 | 125000 | 5 kg/batch | 100 | 1 | review akses | organik → kompos |
| MCH-024 | MCH-024 | Komposter putar | 2 | 1500000 | 50 kg/batch | 150 | 3 | review akses | organik → kompos |
| MCH-025 | MCH-025 | Lubang biopori | 1 | 35000 | 2 kg/batch | 50 | 1 | review akses | organik sesuai → bahan terurai |
| MCH-026 | MCH-026 | Bak vermikompos | 2 | 750000 | 20 kg/batch | 180 | 3 | review akses | organik sesuai → vermikompos |
| MCH-027 | MCH-027 | Pencacah organik mini | 2 | 3500000 | 50 kg/h | 120 | 4 | review akses | organik → cacahan |
| MCH-028 | MCH-028 | Pencacah organik industri | 3 | 45000000 | 500 kg/h | 180 | 15 | review akses | organik → cacahan |
| MCH-029 | MCH-029 | Mixer kompos | 2 | 12000000 | 150 kg/h | 120 | 8 | review akses | organik dan bulking → campuran kompos |
| MCH-030 | MCH-030 | Pengayak kompos | 2 | 4500000 | 100 kg/h | 100 | 6 | review akses | kompos matang → kompos ayak |
| MCH-031 | MCH-031 | Windrow turner | 4 | 450000000 | 2000 kg/h | 180 | 100 | review akses | kompos → kompos teraerasi |
| MCH-032 | MCH-032 | Komposter in-vessel | 3 | 250000000 | 500 kg/batch | 350 | 35 | review akses | organik → kompos |
| MCH-033 | MCH-033 | Modul BSF | 2 | 5000000 | 10 kg/h | 250 | 10 | review akses | organik sesuai → maggot dan kasgot |
| MCH-034 | MCH-034 | Rak pembesaran BSF | 2 | 2500000 | 50 kg/batch | 150 | 8 | review akses | pakan BSF → maggot |
| MCH-035 | MCH-035 | Pemisah maggot kasgot | 3 | 18000000 | 100 kg/h | 200 | 8 | review akses | hasil BSF → maggot/kasgot |
| MCH-036 | MCH-036 | Pengering maggot | 3 | 35000000 | 20 kg/h | 800 | 10 | review akses | maggot → maggot kering |
| MCH-037 | MCH-037 | Penggiling tepung organik | 3 | 25000000 | 50 kg/h | 500 | 8 | review akses | bahan kering sesuai → tepung |
| MCH-038 | MCH-038 | Granulator pupuk | 3 | 55000000 | 100 kg/h | 350 | 15 | review akses | kompos → granul |
| MCH-039 | MCH-039 | Pengemas kompos | 2 | 8000000 | 100 kg/h | 300 | 6 | review akses | kompos dan kemasan → kompos kemasan |
| MCH-040 | MCH-040 | Digester anaerobik | 4 | 350000000 | 100 kg/h | 400 | 100 | review akses | organik sesuai → biogas dan digestat |
| MCH-041 | MCH-041 | Dewatering digestat | 4 | 120000000 | 300 kg/h | 250 | 30 | review akses | digestat → padatan dan cairan |
| MCH-042 | MCH-042 | Pemurni biogas | 4 | 180000000 | 30 m3/h | 500 | 25 | review akses | biogas → gas murni |
| MCH-043 | MCH-043 | Sistem penampung biogas | 4 | 85000000 | 50 m3/batch | 0 | 30 | review akses | biogas → stok gas |

### Plastik

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-044 | MCH-044 | Pencacah plastik mini | 2 | 7500000 | 25 kg/h | 600 | 6 | review akses | plastik terpilah → cacahan kotor |
| MCH-045 | MCH-045 | Granulator plastik | 3 | 35000000 | 100 kg/h | 450 | 12 | review akses | plastik → cacahan kotor |
| MCH-046 | MCH-046 | Pemisah label botol | 3 | 45000000 | 200 kg/h | 200 | 12 | review akses | PET botol → PET dan label |
| MCH-047 | MCH-047 | Bak float-sink | 3 | 35000000 | 150 kg/h | 300 | 15 | review akses | cacahan → fraksi densitas |
| MCH-048 | MCH-048 | Friction washer | 3 | 45000000 | 150 kg/h | 400 | 15 | review akses | cacahan → cacahan basah |
| MCH-049 | MCH-049 | Hot wash line | 3 | 120000000 | 200 kg/h | 800 | 30 | review akses | PET cacah → cacahan basah bersih |
| MCH-050 | MCH-050 | Centrifugal dryer | 3 | 45000000 | 150 kg/h | 350 | 12 | review akses | cacahan basah → flakes kering |
| MCH-051 | MCH-051 | Lini cacah-cuci plastik | 3 | 85000000 | 100 kg/h | 1200 | 45 | review akses | plastik terpilah → flakes |
| MCH-052 | MCH-052 | Agglomerator film | 3 | 55000000 | 80 kg/h | 600 | 12 | review akses | film bersih → aglomerat |
| MCH-053 | MCH-053 | Densifier EPS | 3 | 65000000 | 50 kg/h | 500 | 12 | review akses | EPS bersih → EPS padat |
| MCH-054 | MCH-054 | Extruder pellet line | 3 | 250000000 | 100 kg/h | 1800 | 40 | review akses | flakes sesuai → pellet |
| MCH-055 | MCH-055 | Filter lelehan polimer | 3 | 35000000 | 100 kg/h | 200 | 6 | review akses | lelehan → lelehan tersaring |
| MCH-056 | MCH-056 | Injection molding | 3 | 180000000 | 50 kg/h | 1500 | 25 | review akses | pellet sesuai → produk cetak |
| MCH-057 | MCH-057 | Compression molding | 3 | 85000000 | 40 kg/h | 1000 | 20 | review akses | polimer sesuai → produk cetak |
| MCH-058 | MCH-058 | Extruder profil plastik | 4 | 450000000 | 150 kg/h | 1800 | 45 | review akses | pellet sesuai → profil |
| MCH-059 | MCH-059 | Mesin lembaran plastik | 3 | 120000000 | 80 kg/h | 1200 | 25 | review akses | pellet sesuai → lembaran |
| MCH-060 | MCH-060 | Lini serat polyester | 4 | 3500000000 | 500 kg/h | 2500 | 200 | review akses | rPET sesuai → serat |
| MCH-061 | MCH-061 | Lini rPET food-grade bersertifikasi | 5 | 15000000000 | 1000 kg/h | 3500 | 500 | review akses | PET memenuhi syarat → rPET khusus |

### Kertas dan karton

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-062 | MCH-062 | Pemotong kertas manual | 2 | 750000 | 20 kg/h | 50 | 3 | review akses | kertas → potongan |
| MCH-063 | MCH-063 | Paper shredder | 2 | 3500000 | 25 kg/h | 150 | 4 | review akses | kertas → cacahan |
| MCH-064 | MCH-064 | Hydrapulper | 3 | 150000000 | 150 kg/h | 700 | 35 | review akses | kertas dan air → pulp basah |
| MCH-065 | MCH-065 | Screening pulp | 3 | 85000000 | 150 kg/h | 300 | 20 | review akses | pulp → pulp tersaring |
| MCH-066 | MCH-066 | Deinking line | 4 | 650000000 | 300 kg/h | 1600 | 100 | review akses | pulp cetak → pulp deinked |
| MCH-067 | MCH-067 | Lini pulp terpadu | 3 | 350000000 | 150 kg/h | 1500 | 100 | review akses | kertas → pulp |
| MCH-068 | MCH-068 | Cetak pulp kemasan | 3 | 120000000 | 50 kg/h | 1000 | 30 | review akses | pulp → kemasan |
| MCH-069 | MCH-069 | Mesin tray telur | 3 | 250000000 | 100 kg/h | 1200 | 60 | review akses | pulp → tray |
| MCH-070 | MCH-070 | Paper machine | 4 | 5000000000 | 1000 kg/h | 2000 | 500 | review akses | pulp → kertas daur ulang |

### Logam, kaca dan konstruksi

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-071 | MCH-071 | Pemotong kabel manual | 2 | 1500000 | 10 kg/h | 200 | 4 | review akses | kabel aman → logam dan isolasi |
| MCH-072 | MCH-072 | Cable granulator | 3 | 125000000 | 100 kg/h | 1200 | 25 | review akses | kabel aman → granul tembaga dan plastik |
| MCH-073 | MCH-073 | Lini pemisahan logam | 3 | 95000000 | 150 kg/h | 500 | 35 | review akses | logam campur → logam terpilah |
| MCH-074 | MCH-074 | Metal shear | 3 | 180000000 | 300 kg/h | 500 | 30 | review akses | besi → scrap ukuran |
| MCH-075 | MCH-075 | Metal baler | 3 | 350000000 | 500 kg/h | 350 | 50 | review akses | logam → bale logam |
| MCH-076 | MCH-076 | Metal shredder | 4 | 2500000000 | 2000 kg/h | 1000 | 150 | review akses | logam aman → shredded scrap |
| MCH-077 | MCH-077 | Smelter aluminium mitra | 4 | 0 | 300 kg/h | 3500 | 0 | review akses | aluminium sesuai → ingot |
| MCH-078 | MCH-078 | Smelter baja mitra | 4 | 0 | 500 kg/h | 3000 | 0 | review akses | besi sesuai → baja sekunder |
| MCH-079 | MCH-079 | Pemurnian tembaga mitra | 4 | 0 | 100 kg/h | 5000 | 0 | review akses | tembaga sesuai → tembaga sekunder |
| MCH-080 | MCH-080 | Refinery logam mulia mitra | 4 | 0 | 5 kg/h | 50000 | 0 | review akses | lot teruji → logam pulih |
| MCH-081 | MCH-081 | Glass crusher | 3 | 65000000 | 120 kg/h | 250 | 20 | review akses | kaca → cullet |
| MCH-082 | MCH-082 | Glass optical sorter | 4 | 750000000 | 1000 kg/h | 300 | 50 | review akses | cullet → cullet grade |
| MCH-083 | MCH-083 | Pencuci botol guna ulang | 3 | 85000000 | 200 pcs/h | 300 | 25 | review akses | botol utuh → botol QC |
| MCH-084 | MCH-084 | Glass furnace mitra | 4 | 0 | 500 kg/h | 2500 | 0 | review akses | cullet sesuai → kaca sekunder |
| MCH-085 | MCH-085 | Jaw crusher konstruksi | 3 | 250000000 | 1000 kg/h | 350 | 75 | review akses | beton bersih → agregat |
| MCH-086 | MCH-086 | Vibrating screen agregat | 3 | 85000000 | 1000 kg/h | 120 | 40 | review akses | agregat → agregat tergrade |
| MCH-087 | MCH-087 | Lini blok agregat | 3 | 120000000 | 300 kg/h | 450 | 50 | review akses | agregat dan binder → blok QC |

### Tekstil, kayu, karet dan upcycling

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-088 | MCH-088 | Mesin jahit | 2 | 2500000 | 4 pcs/h | 1000 | 4 | review akses | kain dan aksesori → produk jahit |
| MCH-089 | MCH-089 | Mesin obras | 2 | 3500000 | 4 pcs/h | 800 | 4 | review akses | kain → produk jahit |
| MCH-090 | MCH-090 | Pemotong kain | 2 | 2000000 | 20 kg/h | 150 | 4 | review akses | tekstil → potongan |
| MCH-091 | MCH-091 | Textile fiber opener | 3 | 120000000 | 80 kg/h | 800 | 30 | review akses | tekstil → serat |
| MCH-092 | MCH-092 | Lini nonwoven | 4 | 1800000000 | 300 kg/h | 1500 | 120 | review akses | serat → lembaran nonwoven |
| MCH-093 | MCH-093 | Lini benang daur ulang | 4 | 2500000000 | 250 kg/h | 2000 | 150 | review akses | serat → benang |
| MCH-094 | MCH-094 | Meja kerajinan starter | 1 | 0 | 2 pcs/h | 500 | 4 | review akses | material bersih → kerajinan |
| MCH-095 | MCH-095 | Bengkel upcycling | 2 | 5000000 | 4 pcs/h | 1000 | 15 | review akses | material dan hardware → produk BOM |
| MCH-096 | MCH-096 | Gergaji bengkel | 2 | 2500000 | 20 kg/h | 300 | 5 | review akses | kayu aman → potongan |
| MCH-097 | MCH-097 | Wood chipper | 3 | 45000000 | 120 kg/h | 300 | 20 | review akses | kayu → chip |
| MCH-098 | MCH-098 | Hammer mill kayu | 3 | 55000000 | 150 kg/h | 400 | 20 | review akses | chip → serbuk |
| MCH-099 | MCH-099 | Pengering biomassa | 3 | 75000000 | 150 kg/h | 500 | 30 | review akses | biomassa → biomassa kering |
| MCH-100 | MCH-100 | Lini pellet biomassa | 3 | 120000000 | 100 kg/h | 600 | 45 | review akses | chip → pellet |
| MCH-101 | MCH-101 | Press briket | 3 | 45000000 | 80 kg/h | 500 | 20 | review akses | biomassa sesuai → briket |
| MCH-102 | MCH-102 | Coco fiber separator | 3 | 65000000 | 100 kg/h | 400 | 25 | review akses | sabut → cocofiber/cocopeat |
| MCH-103 | MCH-103 | Tire debeader | 3 | 45000000 | 100 kg/h | 300 | 15 | review akses | ban → karet dan kawat |
| MCH-104 | MCH-104 | Tire shredder | 3 | 180000000 | 150 kg/h | 900 | 35 | review akses | ban → cacahan |
| MCH-105 | MCH-105 | Rubber crumb line | 3 | 180000000 | 80 kg/h | 1500 | 40 | review akses | karet → crumb |
| MCH-106 | MCH-106 | Rubber powder mill | 4 | 350000000 | 100 kg/h | 1800 | 40 | review akses | crumb → bubuk karet |
| MCH-107 | MCH-107 | Reclaimed rubber mitra | 4 | 0 | 100 kg/h | 2000 | 0 | review akses | karet sesuai → reclaimed rubber |

### Jelantah, elektronik dan limbah khusus

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-108 | MCH-108 | Jeriken jelantah tertutup | 1 | 35000 | 20 L/batch | 0 | 1 | review akses | jelantah → stok |
| MCH-109 | MCH-109 | Filter jelantah sederhana | 2 | 1500000 | 20 L/h | 200 | 4 | review akses | UCO → UCO tersaring |
| MCH-110 | MCH-110 | Lini pemurnian UCO | 3 | 45000000 | 80 kg/h | 700 | 20 | review akses | UCO → UCOF |
| MCH-111 | MCH-111 | Biodiesel mitra | 4 | 0 | 100 L/h | 1500 | 0 | review akses | UCO sesuai → biodiesel |
| MCH-112 | MCH-112 | Drop box elektronik | 2 | 750000 | 30 kg/batch | 0 | 3 | review akses | elektronik → stok aman |
| MCH-113 | MCH-113 | Penyimpanan baterai khusus | 3 | 10000000 | 100 kg/batch | 0 | 10 | review akses | baterai → stok aman |
| MCH-114 | MCH-114 | Stasiun inspeksi elektronik | 3 | 15000000 | 20 kg/h | 500 | 10 | review akses | elektronik → lot teridentifikasi |
| MCH-115 | MCH-115 | Recovery elektronik mitra | 3 | 0 | 30 kg/h | 6000 | 0 | review akses | EW → material pulih |
| MCH-116 | MCH-116 | Recovery baterai mitra | 4 | 0 | 50 kg/h | 8000 | 0 | review akses | baterai → material pulih |
| MCH-117 | MCH-117 | Recovery panel surya mitra | 4 | 0 | 100 kg/h | 3500 | 0 | review akses | panel → material pulih |
| MCH-118 | MCH-118 | Recovery refrigeran mitra | 3 | 0 | 10 pcs/h | 50000 | 0 | review akses | alat pendingin → komponen dan refrigeran aman |
| MCH-119 | MCH-119 | Pengolahan limbah B3 mitra | 3 | 0 | 100 kg/h | 10000 | 0 | review akses | limbah khusus → disposition aman |

### Energi dan pengendalian lingkungan

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| MCH-120 | MCH-120 | RDF shredder | 4 | 150000000 | 300 kg/h | 200 | 40 | review akses | residu eligible → cacahan RDF |
| MCH-121 | MCH-121 | Lini RDF/SRF | 4 | 300000000 | 150 kg/h | 300 | 70 | review akses | residu eligible → RDF/SRF |
| MCH-122 | MCH-122 | Biochar mitra | 4 | 0 | 50 kg/h | 1300 | 0 | review akses | biomassa sesuai → biochar |
| MCH-123 | MCH-123 | Genset biogas | 4 | 150000000 | 50 kWh/h | 250 | 30 | review akses | biogas → listrik |
| MCH-124 | MCH-124 | PLTS atap | 3 | 150000000 | 10 kWh/h | 0 | 60 | review akses | matahari → listrik |
| MCH-125 | MCH-125 | Mikrohidro saluran | 4 | 250000000 | 15 kWh/h | 0 | 40 | review akses | aliran air sesuai → listrik |
| MCH-126 | MCH-126 | Waste-to-energy mitra beta | 4 | 1500000000 | 120 kg/h | 900 | 200 | review akses | RDF eligible → listrik dan residu |
| MCH-127 | MCH-127 | Baghouse filter | 4 | 150000000 | 500 kg/h | 180 | 30 | review akses | aliran proses terkait → debu tertangkap |
| MCH-128 | MCH-128 | Scrubber gas | 4 | 250000000 | 500 kg/h | 250 | 40 | review akses | aliran proses terkait → aliran terkendali |
| MCH-129 | MCH-129 | IPAL terpadu | 4 | 150000000 | 200 kg/h | 250 | 60 | review akses | air limbah → air olahan dan lumpur |
| MCH-130 | MCH-130 | Bak pengendap | 3 | 15000000 | 200 kg/h | 100 | 15 | review akses | air limbah → air dan lumpur |
| MCH-131 | MCH-131 | Filter press lumpur | 4 | 120000000 | 100 kg/h | 300 | 25 | review akses | lumpur → cake dan filtrat |
| MCH-132 | MCH-132 | Sistem kontrol bau | 3 | 35000000 | 200 kg/h | 120 | 15 | review akses | aliran proses terkait → bau terkendali |
| MCH-133 | MCH-133 | Monitoring emisi CEMS | 4 | 450000000 | 1 audit/h | 1000 | 8 | review akses | data emisi → rekaman |
| MCH-134 | MCH-134 | Laboratorium QC material | 3 | 75000000 | 10 audit/h | 2500 | 20 | review akses | sampel → hasil QC |
| MCH-135 | MCH-135 | Meter energi dan air | 3 | 5000000 | 1 audit/h | 0 | 2 | review akses | data utilitas → rekaman |
| MCH-136 | MCH-136 | Sistem monitoring neraca massa | 4 | 25000000 | 1 audit/h | 0 | 5 | review akses | ledger → audit |
| MCH-137 | MCH-137 | Water reuse system | 5 | 350000000 | 500 kg/h | 300 | 50 | review akses | air olahan → air proses |
| MCH-138 | MCH-138 | Pusat riset Gaia | 5 | 1000000000 | 1 audit/h | 10000 | 100 | review akses | data riset → blueprint terkunci |

### Waste-to-Energy

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| WTE-001 | WTE-001 | Insinerator rumahan sederhana (edukasi risiko) | 1 | 0 | 0 kg/jam | 0 | TBD | display_only | Tidak menghasilkan listrik; risiko asap dan abu |
| WTE-002 | WTE-002 | Digester biogas rumah tangga | 1 | 4500000 | 5 kg/hari | 100 | TBD | sewa/beli | Biogas, digestat; bukan listrik langsung |
| WTE-003 | WTE-003 | Digester komunal kecil | 2 | 35000000 | 50 kg/hari | 180 | TBD | sewa/beli | Biogas, digestat |
| WTE-004 | WTE-004 | Tangki penerima organik | 2 | 5000000 | 200 kg/batch | 20 | TBD | beli | Buffer bahan |
| WTE-005 | WTE-005 | Depackager organik | 3 | 220000000 | 500 kg/jam | 250 | TBD | beli | Organik bersih, kemasan reject |
| WTE-006 | WTE-006 | Pulping organik | 3 | 65000000 | 200 kg/jam | 180 | TBD | beli | Slurry organik |
| WTE-007 | WTE-007 | Pompa slurry | 3 | 15000000 | 2 m3/jam | 150 | TBD | beli | Transfer, bukan konversi |
| WTE-008 | MCH-040 | Digester anaerobik industri (MCH-040) | 4 | 350000000 | 100 kg/jam | 400 | TBD | alias | Biogas, digestat |
| WTE-009 | WTE-009 | Digester industri besar | 4 | 8000000000 | 2000 kg/jam | 350 | TBD | beli/mitra | Biogas, digestat |
| WTE-010 | WTE-010 | Digester limbah cair industri | 4 | 3500000000 | 10 m3/jam | 900 | TBD | beli/mitra | Biogas, efluen |
| WTE-011 | MCH-043 | Gas holder (MCH-043) | 4 | 85000000 | 50 m3/batch | 0 | TBD | alias | Penyimpanan gas |
| WTE-012 | MCH-042 | Pemurni biogas (MCH-042) | 4 | 180000000 | 30 m3/jam | 500 | TBD | alias | Gas terkondisi, reject |
| WTE-013 | WTE-013 | Modul kontrol H2S | 3 | 25000000 | 10 m3/jam | 300 | TBD | beli | Gas terkondisi |
| WTE-014 | WTE-014 | Pengering gas | 3 | 18000000 | 10 m3/jam | 200 | TBD | beli | Gas terkondisi, kondensat |
| WTE-015 | WTE-015 | Genset biogas mikro | 2 | 18000000 | 1 kW | 500 | TBD | sewa/beli | Listrik, panas, emisi |
| WTE-016 | WTE-016 | Genset biogas komunal | 2 | 65000000 | 5 kW | 400 | TBD | sewa/beli | Listrik, panas, emisi |
| WTE-017 | MCH-123 | Genset biogas (MCH-123) | 4 | 150000000 | 50 kW | 250 | TBD | alias | Listrik, panas, emisi |
| WTE-018 | WTE-018 | CHP biogas 250 kW | 4 | 4500000000 | 250 kW | 300 | TBD | beli/mitra | Listrik dan panas berguna |
| WTE-019 | WTE-019 | CHP biogas 1 MW | 5 | 18000000000 | 1000 kW | 250 | TBD | mitra/beli | Listrik dan panas berguna |
| WTE-020 | WTE-020 | Flare keselamatan | 3 | 45000000 | 30 m3/jam | 100 | TBD | beli | Pengamanan gas; nol kredit listrik |
| WTE-021 | WTE-021 | Sensor kebocoran gas | 2 | 3500000 | 1 audit | 100 | TBD | beli | Interlock keselamatan |
| WTE-022 | MCH-041 | Dewatering digestat (MCH-041) | 4 | 120000000 | 300 kg/jam | 250 | TBD | alias | Padat dan cair |
| WTE-023 | WTE-023 | Pengolahan digestat lanjut | 4 | 350000000 | 300 kg/jam | 350 | TBD | beli | Produk QC dan reject |
| WTE-024 | MCH-120 | RDF shredder (MCH-120) | 4 | 150000000 | 300 kg/jam | 200 | TBD | alias | Cacahan residu |
| WTE-025 | MCH-121 | Lini RDF/SRF (MCH-121) | 4 | 300000000 | 150 kg/jam | 300 | TBD | alias | RDF/SRF; bukan listrik |
| WTE-026 | WTE-026 | Pengering RDF industri | 4 | 650000000 | 500 kg/jam | 400 | TBD | beli | RDF kering, uap |
| WTE-027 | WTE-027 | QC bahan bakar | 3 | 35000000 | 1 audit | 10000 | TBD | beli/mitra | LHV, kadar air, kelayakan |
| WTE-028 | WTE-028 | Insinerator mikro institusi | 3 | 250000000 | 15 kg/jam | 1800 | TBD | display_only/mitra | Pengolahan termal terkontrol; tanpa listrik default |
| WTE-029 | WTE-029 | Insinerator komunal terkontrol | 3 | 1500000000 | 50 kg/jam | 1500 | TBD | mitra | Panas; listrik hanya dengan modul tervalidasi |
| WTE-030 | MCH-126 | Modul WtE mitra beta (MCH-126) | 4 | 1500000000 | 120 kg/jam | 900 | TBD | alias/mitra | Listrik dan residu |
| WTE-031 | WTE-031 | Insinerator modular industri | 4 | 18000000000 | 500 kg/jam | 900 | TBD | mitra/beli | Panas, abu, gas |
| WTE-032 | WTE-032 | Moving grate WtE | 4 | 150000000000 | 5000 kg/jam | 700 | TBD | mitra | Panas, abu, gas |
| WTE-033 | WTE-033 | Moving grate PLTSa skala kota | 5 | 650000000000 | 25000 kg/jam | 650 | TBD | mitra | Panas, abu, gas |
| WTE-034 | WTE-034 | Fluidized bed combustion | 5 | 120000000000 | 4000 kg/jam | 800 | TBD | mitra | Panas dari bahan bakar sesuai |
| WTE-035 | WTE-035 | Rotary kiln industri khusus | 5 | 90000000000 | 1500 kg/jam | 1800 | TBD | mitra | Penanganan khusus; nol kredit God untuk B3 |
| WTE-036 | WTE-036 | Waste heat boiler | 4 | 8000000000 | 1000 kW termal | 150 | TBD | beli/mitra | Uap dari panas tercatat |
| WTE-037 | WTE-037 | Steam turbine mikro industri | 4 | 3500000000 | 100 kW | 350 | TBD | mitra/beli | Listrik dari uap |
| WTE-038 | WTE-038 | Steam turbine 1 MW | 4 | 25000000000 | 1000 kW | 300 | TBD | mitra | Listrik dari uap |
| WTE-039 | WTE-039 | Steam turbine 10 MW | 5 | 160000000000 | 10000 kW | 250 | TBD | mitra | Listrik dari uap |
| WTE-040 | WTE-040 | Organic Rankine Cycle | 4 | 12000000000 | 100 kW | 400 | TBD | mitra | Listrik dari panas sesuai |
| WTE-041 | WTE-041 | Condenser | 4 | 1500000000 | 1000 kW termal | 100 | TBD | beli/mitra | Kondensat, panas buang |
| WTE-042 | WTE-042 | Cooling tower | 4 | 2500000000 | 1500 kW termal | 100 | TBD | beli/mitra | Pelepasan panas terkendali |
| WTE-043 | WTE-043 | Water treatment boiler | 4 | 750000000 | 3 m3/jam | 1500 | TBD | beli/mitra | Air proses, reject |
| WTE-044 | WTE-044 | Gasifier biomassa skala komunitas | 3 | 350000000 | 50 kg/jam | 800 | TBD | mitra | Syngas, char, reject |
| WTE-045 | WTE-045 | Gasifier RDF industri | 5 | 25000000000 | 1000 kg/jam | 1000 | TBD | mitra | Syngas, char, reject |
| WTE-046 | WTE-046 | Syngas cleaning train | 4 | 2500000000 | 200 m3/jam | 900 | TBD | mitra | Gas sesuai QC, reject |
| WTE-047 | WTE-047 | Syngas engine generator | 4 | 3500000000 | 100 kW | 450 | TBD | mitra | Listrik, panas, emisi |
| WTE-048 | WTE-048 | Pirolisis biomassa mitra | 4 | 1500000000 | 100 kg/jam | 1300 | TBD | mitra | Biochar, gas, cairan; listrik tidak otomatis |
| WTE-049 | WTE-049 | Pirolisis residu industri | 5 | 35000000000 | 1000 kg/jam | 1500 | TBD | mitra | Produk antara dan residu; QC wajib |
| WTE-050 | WTE-050 | Landfill gas collection | 4 | 8000000000 | 300 m3/jam | 300 | TBD | mitra | Gas dari landfill historis |
| WTE-051 | WTE-051 | Landfill gas engine | 4 | 10000000000 | 500 kW | 350 | TBD | mitra | Listrik dari gas historis |
| WTE-052 | WTE-052 | Fuel cell biogas tervalidasi | 5 | 15000000000 | 100 kW | 600 | TBD | mitra/riset | Listrik dari gas sangat terpurifikasi |
| WTE-053 | WTE-053 | Microbial fuel cell demonstrasi | 5 | 150000000 | 0.01 kW | 1000 | TBD | riset | Edukasi; bukan rute God sendiri |
| WTE-054 | MCH-127 | Baghouse (MCH-127) | 4 | 150000000 | 500 kg/jam throughput lini | 180 | TBD | alias | Debu tertangkap |
| WTE-055 | MCH-128 | Scrubber (MCH-128) | 4 | 250000000 | 500 kg/jam throughput lini | 250 | TBD | alias | Gas terkendali, limbah sekunder |
| WTE-056 | WTE-056 | Kontrol NOx | 4 | 2500000000 | 1000 kg/jam throughput lini | 300 | TBD | mitra/beli | Pengendalian NOx |
| WTE-057 | WTE-057 | Adsorpsi karbon aktif | 4 | 750000000 | 1000 kg/jam throughput lini | 200 | TBD | mitra/beli | Pengendalian polutan, sorben bekas |
| WTE-058 | MCH-133 | CEMS (MCH-133) | 4 | 450000000 | 1 audit | 1000 | TBD | alias | Data emisi, interlock |
| WTE-059 | WTE-059 | Ash handling tertutup | 4 | 650000000 | 300 kg/jam | 250 | TBD | beli/mitra | Abu terpisah |
| WTE-060 | WTE-060 | Pemulihan logam bottom ash | 4 | 1500000000 | 300 kg/jam | 400 | TBD | mitra/beli | Logam QC, mineral reject |
| WTE-061 | WTE-061 | Stabilisasi fly ash mitra | 4 | 0 | 100 kg/jam | 3500 | TBD | mitra | Residu aman melalui layanan berizin simulasi |
| WTE-062 | MCH-129 | IPAL (MCH-129) | 4 | 150000000 | 200 kg/jam | 250 | TBD | alias | Air olahan, lumpur |
| WTE-063 | MCH-135 | Meter energi (MCH-135) | 3 | 5000000 | 1 audit | 0 | TBD | alias | Rekaman energi |
| WTE-064 | WTE-064 | Smart meter mikro | 1 | 350000 | 1 audit | 0 | TBD | beli/mitra | Pengukuran energi |
| WTE-065 | WTE-065 | Inverter dan proteksi jaringan | 3 | 35000000 | 20 kW | 50 | TBD | beli | Distribusi, bukan sumber listrik |
| WTE-066 | WTE-066 | Baterai penyimpanan | 3 | 80000000 | 20 kWh/batch | 100 | TBD | beli | Penyimpanan, bukan sumber listrik |
| WTE-067 | WTE-067 | Transformer dan interkoneksi | 4 | 350000000 | 250 kW | 50 | TBD | beli/mitra | Distribusi |
| WTE-068 | WTE-068 | Energy management system | 4 | 75000000 | 1 audit | 1000 | TBD | beli | Optimasi utilitas |
| WTE-069 | WTE-069 | Konverter Asap Gaia | 4 | 0 | 1 audit | 0 | TBD | virtual modifier | Alias logis bundle kontrol emisi; bukan alat ajaib |
| WTE-070 | WTE-070 | Pusat audit energi dan lingkungan | 5 | 250000000 | 1 audit | 10000 | TBD | mitra/beli | Evaluasi God |

### Surya

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| DRE-001 | DRE-001 | Solar kit DC | 1 | 450000 | 0.02 kWp | profil DRES | 1 | beli/sewa | Lampu DC; controller terintegrasi |
| DRE-002 | DRE-002 | PLTS pico | 1 | 1500000 | 0.1 kWp | profil DRES | 1 | beli/sewa | PV + controller; baterai terpisah |
| DRE-003 | DRE-003 | PLTS atap 500 Wp | 2 | 6000000 | 0.5 kWp | profil DRES | 3 | beli/sewa | PV dan mounting |
| DRE-004 | DRE-004 | PLTS atap 1 kWp | 2 | 12000000 | 1 kWp | profil DRES | 6 | beli/sewa | PV dan mounting |
| DRE-005 | DRE-005 | PLTS atap 3 kWp | 2 | 33000000 | 3 kWp | profil DRES | 18 | beli/sewa | PV dan mounting |
| DRE-006 | DRE-006 | PLTS atap 5 kWp | 3 | 50000000 | 5 kWp | profil DRES | 30 | beli/sewa | PV dan mounting |
| DRE-007 | DRE-007 | PLTS atap 10 kWp | 3 | 95000000 | 10 kWp | profil DRES | 60 | beli/sewa | PV dan mounting |
| DRE-008 | DRE-008 | PLTS atap 20 kWp | 3 | 180000000 | 20 kWp | profil DRES | 120 | beli | PV dan mounting |
| DRE-009 | DRE-009 | PLTS atap 50 kWp | 4 | 425000000 | 50 kWp | profil DRES | 300 | beli | PV dan mounting |
| DRE-010 | DRE-010 | PLTS atap 100 kWp | 4 | 800000000 | 100 kWp | profil DRES | 600 | beli | PV dan mounting |
| DRE-011 | DRE-011 | Panel fleksibel | 2 | 2500000 | 0.2 kWp | profil DRES | 2 | beli | PV untuk atap ringan |
| DRE-012 | DRE-012 | Solar carport | 3 | 85000000 | 5 kWp | profil DRES | 35 | beli | PV dan struktur |
| DRE-013 | DRE-013 | Solar tracker mini | 3 | 28000000 | 1 kWp | profil DRES | 12 | beli | PV tracker; motor konsumsi listrik |
| DRE-014 | DRE-014 | PLTS terapung mini | 4 | 90000000 | 5 kWp | profil DRES | 45 | beli | Hanya kolam buatan yang layak; bukan sungai |
| DRE-015 | DRE-015 | Solar dryer | 2 | 3500000 | 2 kWth | profil DRES | 6 | beli | Panas pengeringan; nol listrik |
| DRE-016 | DRE-016 | Solar water heater | 2 | 7000000 | 2 kWth | profil DRES | 4 | beli | Panas air; nol listrik |

### Angin

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| DRE-017 | DRE-017 | HAWT pico | 1 | 2500000 | 0.1 kW | profil DRES | 8 | beli/sewa | Turbin mini; lokasi terbuka |
| DRE-018 | DRE-018 | HAWT 300 W | 2 | 6500000 | 0.3 kW | profil DRES | 16 | beli/sewa | Turbin dan tiang |
| DRE-019 | DRE-019 | HAWT 1 kW | 2 | 22000000 | 1 kW | profil DRES | 40 | beli/sewa | Turbin dan tiang |
| DRE-020 | DRE-020 | HAWT 3 kW | 3 | 65000000 | 3 kW | profil DRES | 100 | beli | Turbin dan tiang |
| DRE-021 | DRE-021 | HAWT 5 kW | 3 | 110000000 | 5 kW | profil DRES | 180 | beli | Turbin dan tiang |
| DRE-022 | DRE-022 | HAWT 10 kW | 4 | 250000000 | 10 kW | profil DRES | 350 | beli | Turbin dan tiang |
| DRE-023 | DRE-023 | HAWT 20 kW | 4 | 550000000 | 20 kW | profil DRES | 600 | beli | Turbin dan tiang |
| DRE-024 | DRE-024 | Savonius mini | 1 | 3000000 | 0.05 kW | profil DRES | 6 | beli | VAWT demonstrasi |
| DRE-025 | DRE-025 | Savonius 300 W | 2 | 12000000 | 0.3 kW | profil DRES | 20 | beli | VAWT |
| DRE-026 | DRE-026 | Darrieus 1 kW | 3 | 30000000 | 1 kW | profil DRES | 35 | beli | VAWT |
| DRE-027 | DRE-027 | Helical VAWT 2 kW | 3 | 65000000 | 2 kW | profil DRES | 60 | beli | VAWT |
| DRE-028 | DRE-028 | Helical VAWT 5 kW | 4 | 180000000 | 5 kW | profil DRES | 150 | beli | VAWT |
| DRE-029 | DRE-029 | Anemometer | 1 | 650000 | 1 audit | profil DRES | 1 | beli | Survei angin; tidak menghasilkan listrik |

### Hidro

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| DRE-030 | DRE-030 | Pico hydro 100 W | 1 | 3000000 | 0.1 kW | profil DRES | 3 | beli/sewa | Aliran layak; tanpa bendungan |
| DRE-031 | DRE-031 | Pico hydro 500 W | 2 | 12000000 | 0.5 kW | profil DRES | 6 | beli/sewa | Aliran layak |
| DRE-032 | DRE-032 | Pelton 1 kW | 2 | 28000000 | 1 kW | profil DRES | 10 | beli | Head tinggi; debit rendah |
| DRE-033 | DRE-033 | Turgo 2 kW | 3 | 50000000 | 2 kW | profil DRES | 15 | beli | Head menengah/tinggi |
| DRE-034 | DRE-034 | Crossflow 3 kW | 3 | 80000000 | 3 kW | profil DRES | 20 | beli | Debit dan head sesuai |
| DRE-035 | DRE-035 | Crossflow 5 kW | 3 | 125000000 | 5 kW | profil DRES | 25 | beli | Debit dan head sesuai |
| DRE-036 | MCH-125 | Crossflow 15 kW | 4 | 250000000 | 15 kW | profil DRES | 40 | alias MCH-125 | Aset mikrohidro saluran lama |
| DRE-037 | DRE-037 | Crossflow 25 kW | 4 | 550000000 | 25 kW | profil DRES | 65 | beli | Run-of-river |
| DRE-038 | DRE-038 | Francis mini 30 kW | 4 | 750000000 | 30 kW | profil DRES | 75 | beli | Head/debit sesuai |
| DRE-039 | DRE-039 | Kaplan mini 20 kW | 4 | 650000000 | 20 kW | profil DRES | 70 | beli | Head rendah |
| DRE-040 | DRE-040 | Propeller low-head 5 kW | 3 | 160000000 | 5 kW | profil DRES | 30 | beli | Head rendah |
| DRE-041 | DRE-041 | Archimedes screw 3 kW | 3 | 180000000 | 3 kW | profil DRES | 35 | beli | Head rendah |
| DRE-042 | DRE-042 | Archimedes screw 10 kW | 4 | 450000000 | 10 kW | profil DRES | 65 | beli | Head rendah |
| DRE-043 | DRE-043 | Kincir air 200 W | 2 | 7000000 | 0.2 kW | profil DRES | 10 | beli | Aliran dengan head sesuai |
| DRE-044 | DRE-044 | Kincir air 1 kW | 3 | 35000000 | 1 kW | profil DRES | 20 | beli | Aliran dengan head sesuai |
| DRE-045 | DRE-045 | Turbin hidrokinetik 500 W | 3 | 35000000 | 0.5 kW | profil DRES | 12 | beli | Arus tanpa head; model arus terpisah |
| DRE-046 | DRE-046 | Turbin hidrokinetik 2 kW | 4 | 100000000 | 2 kW | profil DRES | 25 | beli | Arus tanpa head; model arus terpisah |
| DRE-047 | DRE-047 | Saringan intake ramah fauna | 2 | 3000000 | 0.05 m3/s | profil DRES | 3 | beli | Kapasitas debit; bukan generator |
| DRE-048 | DRE-048 | Saluran bypass dan jalur fauna | 3 | 20000000 | 0.2 m3/s | profil DRES | 12 | beli | Aliran ekologis; bukan generator |
| DRE-049 | DRE-049 | Sensor debit dan muka air | 2 | 2500000 | 1 audit | profil DRES | 1 | beli | Survei hidrologi |
| DRE-050 | DRE-050 | Modul pico hidro pipa gravitasi | 3 | 15000000 | 0.5 kW | profil DRES | 4 | beli | Hanya tekanan surplus alami; bukan pompa sirkulasi |

### Panas dan riset

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| DRE-051 | DRE-051 | TEG demonstrasi | 1 | 250000 | 0.005 kW | profil DRES | 1 | beli | Panas terukur; sensor |
| DRE-052 | DRE-052 | TEG panas buang | 3 | 8000000 | 0.05 kW | profil DRES | 2 | beli | Panas buang teralokasi |
| DRE-053 | DRE-053 | TEG modular | 4 | 45000000 | 0.25 kW | profil DRES | 6 | beli | Panas buang teralokasi |
| DRE-054 | DRE-054 | Stirling demonstrasi | 2 | 3500000 | 0.01 kW | profil DRES | 2 | riset | Panas eksternal; tidak dijual |
| DRE-055 | DRE-055 | Stirling solar termal | 4 | 75000000 | 0.5 kW | profil DRES | 20 | riset | Panas surya terukur |
| DRE-056 | DRE-056 | ORC mikro | 4 | 400000000 | 5 kW | profil DRES | 30 | riset | Panas buang sesuai; bukan WTE-040 100 kW |
| DRE-057 | DRE-057 | Plant microbial fuel cell | 2 | 750000 | 0.0001 kW | profil DRES | 2 | riset | Maks 0.1 W; sensor |
| DRE-058 | DRE-058 | Microbial fuel cell air limbah | 3 | 5000000 | 0.001 kW | profil DRES | 4 | riset | Maks 1 W; tidak mengganti IPAL |
| DRE-059 | DRE-059 | Piezoelectric tile kit | 2 | 2000000 | 0.001 kW | profil DRES | 2 | riset | Puncak 1 W saat tekanan |
| DRE-060 | DRE-060 | Generator pedal | 1 | 1500000 | 0.1 kW | profil DRES | 2 | beli | Energi manusia; sesi terbatas |
| DRE-061 | DRE-061 | Energy harvester getaran | 3 | 2500000 | 0.0005 kW | profil DRES | 1 | riset | Getaran eksternal; tidak menggandakan daya mesin |
| DRE-062 | DRE-062 | Turbin pasang surut mini | 4 | 0 | 0 kW | profil DRES | 0 | display_only | Referensi lokasi pesisir; bukan aset aktif |
| DRE-063 | DRE-063 | Geotermal mikro | 4 | 0 | 0 kW | profil DRES | 0 | display_only | Kajian; akses panas lokasi khusus |
| DRE-064 | DRE-064 | Energi gelombang mini | 4 | 0 | 0 kW | profil DRES | 0 | display_only | Kajian; bukan aset aktif |

### Penyimpanan dan distribusi

| ID | Canonical ID | Nama | F | Harga GC | Kapasitas sumber | OPEX sumber | m² | Mode sumber | Fungsi |
|---|---|---|---:|---:|---|---|---:|---|---|
| DRE-065 | DRE-065 | Controller PWM | 1 | 150000 | 0.1 kW | profil DRES | 1 | beli | PV DC |
| DRE-066 | DRE-066 | MPPT 500 W | 2 | 750000 | 0.5 kW | profil DRES | 1 | beli | PV DC |
| DRE-067 | DRE-067 | MPPT 3 kW | 2 | 3500000 | 3 kW | profil DRES | 1 | beli | PV DC |
| DRE-068 | DRE-068 | Inverter off-grid 500 W | 2 | 2000000 | 0.5 kW | profil DRES | 1 | beli | DC ke AC |
| DRE-069 | DRE-069 | Inverter hybrid 3 kW | 2 | 8500000 | 3 kW | profil DRES | 2 | beli | DC/AC dan storage |
| DRE-070 | DRE-070 | Inverter hybrid 5 kW | 3 | 15000000 | 5 kW | profil DRES | 2 | beli | DC/AC dan storage |
| DRE-071 | DRE-071 | Inverter hybrid 10 kW | 3 | 22000000 | 10 kW | profil DRES | 3 | beli | DC/AC dan storage |
| DRE-072 | WTE-065 | Inverter 20 kW | 3 | 35000000 | 20 kW | profil DRES | 3 | alias WTE-065 | Aset dan proteksi lama |
| DRE-073 | DRE-073 | Inverter 50 kW | 4 | 75000000 | 50 kW | profil DRES | 5 | beli | DC/AC |
| DRE-074 | DRE-074 | Inverter 100 kW | 4 | 140000000 | 100 kW | profil DRES | 8 | beli | DC/AC |
| DRE-075 | DRE-075 | Baterai LFP pico | 1 | 900000 | 0.25 kWh | profil DRES | 1 | beli | 0.1 kW charge/discharge |
| DRE-076 | DRE-076 | Baterai LFP 1 kWh | 2 | 4500000 | 1 kWh | profil DRES | 1 | beli | 0.5 kW charge/discharge |
| DRE-077 | DRE-077 | Baterai LFP 5 kWh | 2 | 20000000 | 5 kWh | profil DRES | 2 | beli | 2.5 kW charge/discharge |
| DRE-078 | DRE-078 | Baterai LFP 10 kWh | 3 | 40000000 | 10 kWh | profil DRES | 3 | beli | 5 kW charge/discharge |
| DRE-079 | WTE-066 | Baterai LFP 20 kWh | 3 | 80000000 | 20 kWh | profil DRES | 5 | alias WTE-066 | 10 kW charge/discharge; tipe usulan |
| DRE-080 | DRE-080 | Baterai LFP 50 kWh | 4 | 180000000 | 50 kWh | profil DRES | 10 | beli | 25 kW charge/discharge |
| DRE-081 | DRE-081 | Baterai LFP 100 kWh | 4 | 350000000 | 100 kWh | profil DRES | 18 | beli | 50 kW charge/discharge |
| DRE-082 | WTE-064 | Smart meter | 1 | 350000 | 1 audit | profil DRES | 1 | alias WTE-064 | Meter sumber dan beban |
| DRE-083 | MCH-135 | Meter energi dan air | 3 | 5000000 | 1 audit | profil DRES | 2 | alias MCH-135 | Meter utilitas |
| DRE-084 | WTE-068 | EMS | 4 | 75000000 | 1 audit | profil DRES | 4 | alias WTE-068 | Optimasi dispatch |
| DRE-085 | DRE-085 | Panel proteksi mikrogrid | 2 | 2500000 | 5 kW | profil DRES | 2 | beli | Proteksi dan isolasi |
| DRE-086 | DRE-086 | Panel distribusi UMKM | 3 | 12000000 | 25 kW | profil DRES | 3 | beli | Proteksi dan isolasi |
| DRE-087 | DRE-087 | Panel distribusi 100 kW | 4 | 45000000 | 100 kW | profil DRES | 6 | beli | Proteksi dan isolasi |
| DRE-088 | DRE-088 | Stasiun pengisian gerobak listrik | 3 | 6000000 | 2 kW | profil DRES | 4 | beli | Beban listrik; bukan generator |
| DRE-089 | DRE-089 | Kontrol turbin angin dan dump load | 2 | 2500000 | 1 kW | profil DRES | 2 | beli | Kontrol dan proteksi |
| DRE-090 | DRE-090 | Kontrol hidro dan proteksi | 3 | 6000000 | 5 kW | profil DRES | 2 | beli | Kontrol dan proteksi |
| DRE-091 | DRE-091 | Weather station mini | 3 | 7500000 | 1 audit | profil DRES | 2 | beli | Data cuaca kota |
| DRE-092 | DRE-092 | Energy audit kit | 2 | 1500000 | 1 audit | profil DRES | 1 | beli/sewa | Pemetaan beban |
| DRE-093 | DRE-093 | Kontrak mikrogrid komunitas | 2 | 0 | 10 kW | profil DRES | 0 | mitra | Kuota jasa, bukan pembangkit milik pemain |

## 3. Rekonsiliasi alias dan varian

Total 301 kartu sumber, 19 alias eksplisit, 282 ID kanonik (termasuk referensi, layanan dan modifier; bukan jumlah mesin fisik unik).

| Alias | Canonical ID | Harga sumber GC | Harga canonical GC | Kapasitas alias | Kapasitas canonical | OPEX alias | OPEX canonical |
|---|---|---:|---:|---|---|---|---|
| WTE-008 | MCH-040 | 350000000 | 350000000 | 100 kg/jam | 100 kg/h | 400 | 400 |
| WTE-011 | MCH-043 | 85000000 | 85000000 | 50 m3/batch | 50 m3/batch | 0 | 0 |
| WTE-012 | MCH-042 | 180000000 | 180000000 | 30 m3/jam | 30 m3/h | 500 | 500 |
| WTE-017 | MCH-123 | 150000000 | 150000000 | 50 kW | 50 kWh/h | 250 | 250 |
| WTE-022 | MCH-041 | 120000000 | 120000000 | 300 kg/jam | 300 kg/h | 250 | 250 |
| WTE-024 | MCH-120 | 150000000 | 150000000 | 300 kg/jam | 300 kg/h | 200 | 200 |
| WTE-025 | MCH-121 | 300000000 | 300000000 | 150 kg/jam | 150 kg/h | 300 | 300 |
| WTE-030 | MCH-126 | 1500000000 | 1500000000 | 120 kg/jam | 120 kg/h | 900 | 900 |
| WTE-054 | MCH-127 | 150000000 | 150000000 | 500 kg/jam throughput lini | 500 kg/h | 180 | 180 |
| WTE-055 | MCH-128 | 250000000 | 250000000 | 500 kg/jam throughput lini | 500 kg/h | 250 | 250 |
| WTE-058 | MCH-133 | 450000000 | 450000000 | 1 audit | 1 audit/h | 1000 | 1000 |
| WTE-062 | MCH-129 | 150000000 | 150000000 | 200 kg/jam | 200 kg/h | 250 | 250 |
| WTE-063 | MCH-135 | 5000000 | 5000000 | 1 audit | 1 audit/h | 0 | 0 |
| DRE-036 | MCH-125 | 250000000 | 250000000 | 15 kW | 15 kWh/h | profil DRES | 0 |
| DRE-072 | WTE-065 | 35000000 | 35000000 | 20 kW | 20 kW | profil DRES | 50 |
| DRE-079 | WTE-066 | 80000000 | 80000000 | 20 kWh | 20 kWh/batch | profil DRES | 100 |
| DRE-082 | WTE-064 | 350000 | 350000 | 1 audit | 1 audit | profil DRES | 0 |
| DRE-083 | MCH-135 | 5000000 | 5000000 | 1 audit | 1 audit/h | profil DRES | 0 |
| DRE-084 | WTE-068 | 75000000 | 75000000 | 1 audit | 1 audit | profil DRES | 1000 |

Alias tidak boleh membuat aset atau tagihan kedua. Perbedaan unit, stage, luas, OPEX dan fungsi harus direkonsiliasi sebelum aktivasi; normalisasi kg/h=kg/jam, kWh/h=kW rata-rata, jangan samakan audit/h dan audit tanpa aturan. MCH-124 dan DRE-007 sama-sama 10 kWp dengan harga berbeda (150 juta vs 95 juta GC): pertahankan sebagai varian calon paket berbeda sampai pemilik mengonfirmasi; jangan mengklaim perbedaan spesifikasi yang belum ada. WTE-069 adalah modifier virtual, bukan aset fisik.

## 4. Aturan harga dan simulasi biaya
- Harga pembelian pada profil realistis setelah disahkan = harga canonical + instalasi yang berlaku + fasilitas pendukung terpisah. MCH F3–F5 +10%, F1–F2 0%; DRES +15% kecuali kit terintegrasi; sipil hidro +30% sebagai seed tambahan. WTE biaya EPC belum ditentukan; tampilkan estimasi modul, bukan total pembangunan.
- MCH upgrade U1–U4: kapasitas ×1/1,5/2/3; biaya incremental 0/40/75/120% CAPEX; OPEX per unit ×1/0,98/0,95/0,90. Tidak berlaku otomatis untuk WTE, DRES, storage, audit atau layanan; review utilitas dan bottleneck. Maintenance MCH 0,1% CAPEX/hari aktif; DRES sesuai profil tahunan. Satu kebijakan per aset.
- Sewa DRES 0,1% CAPEX/hari aktif + OPEX; MCH mitra 1,25× biaya variabel + pengiriman; WTE mitra wajib kuota dan tarif tervalidasi. Tidak mendebit CAPEX mitra.
- Grid import 1.500 GC/kWh; ekspor 1.000 GC/kWh bila kontrak aktif; offset dan ekspor tidak dapat dihitung ganda. Semua tarif simulasi.
- Contoh MCH lini cacah-cuci 85 juta GC: instalasi 8,5 juta; total 93,5 juta sebelum utilitas. Contoh DRE-006 PV 5 kWp: 50 juta + 7,5 juta instalasi =57,5 juta; 4 PSH ×0,8 ×5 =16 kWh/hari; penghematan maksimum 24.000 GC/hari jika seluruh listrik menggantikan impor. Bukan proyeksi ROI pasti.
- Jangan mengarang harga untuk biaya yang belum diketahui; UI beri status estimasi atau TBD, bukan nol.

| Jalur | Seed profil | OPEX variabel GC/kWh AC | Maintenance tahunan CAPEX | Ketentuan |
|---|---|---:|---:|---|
| PV | 3–5 peak sun hours/hari, PR 0,75–0,85 | 20 | 1% | PR termasuk rugi konversi; jangan kurangi inverter dua kali |
| HAWT | kurva daya, cut-in 3 m/s, rated 12, cut-out 25 (fixture) | 80 | 3% | Model spesifik mesin wajib mengganti fixture |
| VAWT | kurva daya, cut-in 3, rated 11, cut-out 20 (fixture) | 100 | 3% | Tidak menjanjikan daya pada angin lemah |
| Hidro head | efisiensi total 0,55–0,75 | 60 | 3% | Debit ekologis dan head net wajib |
| Hidrokinetik | Cp×efisiensi 0,20–0,35 | 80 | 4% | luas sapuan dan arus terukur |
| TEG | 1–4% panas masuk | 100 | 2% | panas buang tercatat |
| Stirling/ORC | 5–12% panas masuk, hanya fixture riset | 200 | 4% | suhu dan kualitas panas divalidasi |
| Eksperimen/pedal | energi dari aktivitas aktual; tidak ada pendapatan default | 0 | 2% | batas sesi dan daya, bukan generator pabrik |
| Storage | efisiensi charge 95%, discharge 95%, SOC 10–90% | 100 per kWh keluar | 2% | degradasi dan penggantian terpisah |
| Meter/proteksi/kontrol | bukan pembangkit | 0 | 2% | konsumsi standby tercatat jika aktif |

Maintenance DRES ini menggantikan aturan generik file 05 untuk aset DRES setelah persetujuan; alias lintas WTE/MCH pakai satu kebijakan saja. Biaya tahunan diprorata per hari kalender, dibukukan sekali. Sewa seed 0,1% CAPEX/hari aktif + OPEX, tidak sekaligus dengan maintenance pemilik; akses mitra 1.200 GC/kWh delivered, kuota kontrak. Harga beli grid/offset 1.500 GC/kWh; ekspor 1.000 GC/kWh sesuai file 06, hanya jika kontrak aktif. Bukan tarif resmi. Instalasi seed +15% modul (kecuali kit terintegrasi), survei lokasi 5.000–50.000 GC menurut tier; biaya sipil hidro khusus +30% modul sebagai placeholder, tidak menggantikan kajian lokasi. OPEX tidak termasuk konsumsi eksternal atau investasi. Tidak ada uang dari energi yang tidak digunakan atau tidak diekspor.


## 5. UI katalog dan integrasi
Tab: Semua / Pemilahan / Organik / Plastik / Kertas / Logam dan kaca / Upcycling / Limbah khusus / Waste-to-Energy / Surya / Angin / Hidro / Panas & riset / Penyimpanan. Filter F1–F5, harga, mode akses, input/output, status riset, dan daya. Kartu menampilkan nama, gambar aset berlisensi (placeholder bila belum tersedia), harga modul, kapasitas beserta unit, biaya operasi, fungsi, persyaratan, keterbatasan, alasan terkunci. Tombol lihat teknologi selalu tersedia; beli/sewa/mitra hanya jika tervalidasi. Jangan gunakan label “gratis” untuk nol harga atau sumber energi alam. 

Schema minimal: catalog_id PK, canonical_id FK, source_file, category, name, min_stage, capex_gc bigint, capacity_label, capacity_value decimal nullable, capacity_unit nullable, opex_basis nullable, opex_gc nullable, footprint_m2 nullable, access_modes, educational_description, input_material_ids, output_material_ids, recipe_ids, energy_profile_id, dependency_ids, asset_ref nullable, validation_state, version. Gunakan bigint untuk harga hingga miliaran GC; serialisasi string bila melebihi safe integer. Data tampilan tidak menjadi otoritas settlement. Server memvalidasi harga, kapasitas, kontrak, lokasi, neraca massa dan energi; pagination dan cache versi katalog, Lazy Tick tanpa satu timer per mesin.

## 6. Sumber internal dan QA
File 05, 06, 07 v1.0 tetap referensi aturan teknis lengkap; master ini menggantikan tabel tampilan yang terpisah, bukan seluruh isi spesifikasi. File 01–04 merupakan referensi usulan; baseline prototipe mengikuti v0.9 §30–35, dan amendemen God mengikuti arah Constitution 08 v1.1 setelah review. Periksa mapping alias, perbedaan unit, tarif mitra, kapasitas kontrol emisi, resep, kebutuhan listrik/air, simulasi 90 hari, dan akses pemain kecil sebelum rilis. Harga tidak diverifikasi ulang ke pasar. Tidak ada perubahan repo/DB. Pemeriksaan otomatis hanya jumlah baris, ID unik, dan target alias tersedia.


## 7. Overlay prototipe v0.9 (tidak menimpa 301 baris master)
Sumber: GAME_SPEC §17.6, §32–35; DESIGN_SPEC §20–23. Semua angka [P/U] merupakan dokumentasi perilaku prototipe, bukan harga pasar. Overlay ini adalah rancangan data integrasi, belum seed yang diaktifkan. ID `PROTO-*` baru adalah usulan namespace aksi/fasilitas, bukan ID mesin atau endpoint yang diklaim telah tersedia.

| Overlay ID | Item/aksi | Harga aktif GC | Efek/capacity | Mapping |
|---|---|---:|---|---|
| PROTO-START | Modal awal | 0 | grant 1000 sekali akun baru | bukan aset |
| PROTO-CART | Gerobak starter | 0 | 5–50 kg/trip pada kontrak prototipe | MCH-002 referensi 25 kg/trip; jangan menimpa |
| PROTO-SORT | Area pilah starter | 0 | maks 10 kg/aksi | MCH-005 referensi 20 kg/h; tidak sama |
| PROTO-WH | Gudang starter | 0 | 500 kg | fasilitas, bukan MCH-006 rak 100 kg |
| PROTO-PLOT1 | Petak awal | 0 | petak kebun awal, 3 benih starter terpisah | fasilitas |
| PROTO-PLOT2 | Petak kedua | 250 | +1 petak | fasilitas |
| PROTO-PLOT3 | Petak ketiga | 500 | +1 petak | fasilitas |
| PROTO-PLOT4 | Petak keempat | 750 | +1 petak | fasilitas |
| PROTO-WH1 | Gudang I | 400 | 500→750 kg | upgrade fasilitas |
| PROTO-WH2 | Gudang II | 800 | 750→1000 kg | upgrade fasilitas |
| PROTO-COMPOST | Aksi kompos | TBD | 2 kg→1 kg kompos + 0,9 kg air/gas + 0,1 kg residu; +40 poin | MCH-021 referensi; kepemilikan tidak tersirat |
| PROTO-PLASTIC | Aksi plastik | TBD | 1 kg→0,85 kg pelet/pot; +60 poin | resep prototipe; 0,15 kg harus tercatat sebagai sisa sebelum rilis |
| PROTO-B3 | Serah B3 | TBD | ≥100 g, poin kecil, tanpa koin | jasa, bukan penjualan |
| PROTO-SEED | Benih | 2 | tumbuh 40 detik uji | pupuk 1 kg kompos −25% sisa waktu |

TBD = biaya aksi tidak disebut dalam §35, jangan diasumsikan nol. Starter entitlement gratis tidak berarti harga pengganti gratis. Tidak membuat asset_instance dari aksi kompos/plastik yang berjalan tanpa bukti kepemilikan mesin. Gudang/petak di slot tetap, tidak mengubah latar atau poligon tanpa desain baru.

### Harga dan reward aktif yang harus dipertahankan sampai K5
| Aksi | Nilai prototipe |
|---|---|
| Pungut liar | +2 GC / +3 poin |
| Angkut Permukiman/Pasar/Sungai | biaya 4/6/2 GC, 5–50 kg, ETA 6 detik uji |
| Pilah | 50% organik, 18% plastik, 10% kertas, 7% logam/kaca, 14% residu, 1% B3 |
| Jual sayur | 24 GC (satuan transaksi tidak dijelaskan di §35) |
| Jual kompos | 5 GC/kg |
| Jual pelet / pot | 12 / 14 GC per 850 g |
| Jual kertas / logam-kaca | 9 / 12 GC/kg |
| DLE | +15 poin misi, material masuk gudang |

### Profil harga dan kutipan transaksi [R]
- `prototype_v09`: gunakan harga di server.py yang dikonfirmasi melalui audit; overlay hanya untuk dokumentasi dan UI. Tidak menjalankan harga master untuk pembelian baru. `realistic_v1`: seluruh 301 kartu mempertahankan harga referensi; aktif hanya di sandbox simulasi tersendiri setelah mapping. Jangan memakai pengali tunggal (GC 5/kg kompos vs referensi 500–1500/kg, sementara struktur biaya lain berbeda). Saldo lama tidak dikonversi otomatis.
- Tambah `reference_price_gc`, `active_price_gc` nullable, `economy_profile_id`, `price_version`, `price_status`, `operation_status`, `canonical_id`, `asset_status`. Harga aktif null berarti tidak tersedia untuk transaksi, bukan gratis. `owned_starter` berasal dari entitlement, bukan harga katalog nol.
- Contoh kartu MCH-002: gerobak starter dimiliki, referensi 750.000 GC, pembelian pengganti belum tersedia, kapasitas prototipe 5–50 kg/trip. MCH-021: referensi 5.000 GC, aksi kompos prototipe tersedia tetapi pembelian mesin belum aktif. DRE-006: 50 juta GC referensi, 5 kWp, belum tersedia untuk dibeli. Ini mencegah pemain mengira modal 1.000 GC harus membeli gerobak.
- Settlement wajib mengikat profile_id, price_version, canonical_id, quantity, expiry, akun; server menghitung ulang, stale quote ditolak/konfirmasi ulang. Alias tidak menjadi inventaris baru. Simulasi profil terpisah tidak memengaruhi ledger live.
- K5 uji tiga konfigurasi: A baseline §35; B reward/harga jual dan sewa disesuaikan secara eksplisit; C realistis penuh termasuk biaya dan waktu. Uji 90 hari jalur sederhana, komunitas, industri dan tanpa pembayaran. Ukur median waktu transaksi pertama, kebuntuan kas, waktu unlock, margin, inflasi, GSG, distribusi tier; pilih setelah review, bukan mengaktifkan C langsung. Pertahankan harga realistis edukatif pada semua konfigurasi.

## 8. Integrasi UI dan anggaran aset v1.4 [R]
- Menu → Ensiklopedia Teknologi Gaia; Pasar → Peralatan; Pabrik → detail aset yang dimiliki. Tidak menambah tab navigasi bawah. Semua kartu terbaca setelah HUD, termasuk WTE makro dan DRES UMKM; operasi mengikuti flag fase, safety dan mapping. Kota/Bumi terkunci Fase 3.
- `display_only`, `research`, `partner_pending`, `locked_pending_validation`, `available`, `owned_starter` dibedakan; akses mitra bukan kepemilikan. Katalog semua fase terlihat, bukan semua fase dibangun sekarang (§0.1 GAME_SPEC). God tidak mensyaratkan koleksi teknologi, kekayaan atau pabrik besar. GSG file 06 masih usulan balancing; BHI/ZWM global tidak boleh menerima kredit fixture privat.
- Tampilan isometrik lukis, koordinat gambar 1672×941, anchor kaki, poligon FENCE/OBST/RIVER, gerbang dan jalan §20. Footprint m² tetap data teknik, bukan konversi piksel otomatis. Slot tetap untuk gudang/petak; alat tanpa slot sah hanya tampil katalog. Jangan mengubah sungai atau jalan; hidro menunggu lokasi dan debit ekologis tervalidasi.
- Katalog text-first, ikon reusable, pagination (usulan 24 kartu), thumbnail WebP/AVIF lazy load saat terlihat, detail aset terpisah; jangan memuat 301 gambar saat masuk lahan. Tidak menggunakan renderer tambahan. Manifest asset_ref, ukuran, hash, lisensi, anchor, status. G7: sprite 3,5 MB + latar 321 KB; cinematic 4 MB. Target aset pabrik ≤1 MB, opening ≤1,6 MB, gameplay awal ≤3 MB. Belum dikompres atau diuji dalam revisi dokumen ini. Pertahankan anggaran snapshot ≤20 KB dan heap ≤100 MB; katalog endpoint/cache terpisah dari snapshot.

## 9. QA dan handoff v1.1
| ID | Acceptance (belum dieksekusi) |
|---|---|
| MC01 | 301 baris sumber, 282 canonical, 19 alias; ID/price/kapasitas tabel asli identik |
| MC02 | Akun baru 1000 GC, 500 kg, 3 benih; akun lama tetap; replay tidak grant ulang |
| MC03 | Petak/gudang biaya §33; harga referensi tidak mendebit saldo |
| MC04 | Semua harga §35 tetap dalam prototype_v09; null harga aktif tidak berarti gratis |
| MC05 | Alias, retry, dua tab, saldo dan stok tidak ganda; stale quote ditolak |
| MC06 | Katalog dapat dibuka tanpa beli; mesin makro/riset terlihat tetapi tidak otomatis aktif |
| MC07 | 8 lencana §34 tetap tanpa reward tambahan; tidak ada kredit karena membuka kartu |
| MC08 | Sampah liar privat tidak mengubah BHI/ZWM global; setelah K6 setiap gram punya asal dan expiry backlog |
| MC09 | Fallback ikon, lazy load, Q20/Q24/Q26–Q32 pada perangkat nyata dan budget aset |
| MC10 | GSG terpisah dari kekayaan dan pembelian; jalur kecil/mitra setara setelah uji 90 hari |
| MC11 | Kebutuhan energi/air, recipe ID, dependensi, alias OPEX/unit divalidasi sebelum operasi |
| MC12 | Penanganan B3, residu/emisi dan keselamatan tidak bisa dilewati lewat UI/mitra |

Changelog: v1.1 mempertahankan semua 301 baris dan menambah overlay prototipe, profil harga, aturan UI, QA. File 05–07 tetap referensi teknis; konflik PLTS 10 kWp dan alias masih terbuka. Tidak menetapkan K1–K7, tidak mengubah kode/DB/asset, belum audit harga pasar atau simulasi 90 hari. Sinkronkan dokumen induk dan turunannya setelah review pemilik; jangan mengubah histori.
