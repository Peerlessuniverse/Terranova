# TERRA NOVA — Waste Processing Machinery Database v1.0

**Chapter I — The Calling of Gaia | Addendum 05 DWE v1.0 | 26 November 2026 | Usulan review**

## 1. Kontrak desain
Katalog ini memperluas file 01–04 DWE v1.0, GAME_SPEC v0.8 dan DESIGN_SPEC v1.3. Tidak mengganti keputusan pemilik. Semua CAPEX, kapasitas dan OPEX adalah seed simulasi nominal Indonesia, bukan penawaran pemasok atau spesifikasi rekayasa yang terverifikasi. 1 GC merepresentasikan Rp1, tanpa nilai tukar nyata. Harga beragam menurut skala, merek, kondisi, instalasi dan lokasi. Starter komposter 5.000 GC sengaja bersifat subsidi game, bukan harga tong pasar. Angka WtE 1,5 miliar adalah placeholder akses modul game, bukan biaya PLTSa komersial lengkap.

F1 Tukang Sampah; F2 Bank Sampah; F3 Industri Daur Ulang; F4 Eco Industrial Park; F5 Zero Waste Civilization. Gate fisik mengikuti file 03; tier spiritual tidak otomatis membuka fasilitas atau memberi uang. Mesin tidak menghasilkan sampah dari ketiadaan. Semua operasi mengikuti mass ledger, QC, izin akses simulasi dan Lazy Tick Engine (maksimal offline 8 jam).

## 2. Katalog seed
ID permanen MCH-001 dst. CAPEX GC per unit; OPEX GC per unit **input** sesuai satuan kapasitas, kecuali listrik GC/kWh output dan audit GC/audit. kg/h = kapasitas alir; kg/batch = kapasitas muat, bukan laju; pcs/h dan L/h sesuai unit; m3 = meter kubik; area m² adalah footprint simulasi. Kapasitas listrik kWh/h adalah daya rata-rata kW; pembangkitan tunduk pada sumber energi. Kapasitas kontrol emisi kg/h adalah throughput lini yang dilayani, bukan massa gas. Nilai 0 untuk starter atau mitra bukan mesin gratis yang bisa dibeli. Peralatan penyimpanan dan pengukuran tidak memiliki yield produksi. Input/output di tabel adalah label konseptual, **bukan material ID atau resep eksekusi**. Default semua entri `locked_pending_recipe` kecuali yang sudah memiliki mapping dan telah lolos QA.

### Pengumpulan, pemilahan dan penyimpanan

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-001 | Tong sampah terpilah | 1 | 45000 | 30 | kg/batch | 0 | 1 | sampah terpilah | stok |
| MCH-002 | Gerobak dorong | 1 | 750000 | 25 | kg/trip | 0 | 2 | sampah sumber | kargo |
| MCH-003 | Timbangan gantung | 1 | 85000 | 50 | kg/batch | 0 | 1 | lot | berat terukur |
| MCH-004 | Timbangan digital meja | 2 | 450000 | 150 | kg/batch | 5 | 1 | lot | berat terukur |
| MCH-005 | Meja pilah manual starter | 1 | 0 | 20 | kg/h | 50 | 4 | campuran | fraksi |
| MCH-006 | Rak gudang | 1 | 350000 | 100 | kg/batch | 0 | 3 | material | stok |
| MCH-007 | Bak penampung tertutup | 1 | 250000 | 100 | kg/batch | 0 | 2 | organik | stok |
| MCH-008 | Stasiun cuci dan pilah | 2 | 2500000 | 100 | kg/h | 400 | 8 | plastik terpilah | plastik bersih |
| MCH-009 | Press manual kardus | 2 | 3500000 | 30 | kg/h | 100 | 4 | kertas | bale |
| MCH-010 | Baler hidrolik | 2 | 25000000 | 150 | kg/h | 180 | 12 | kertas/plastik | bale |
| MCH-011 | Conveyor pemilah | 3 | 75000000 | 500 | kg/h | 100 | 35 | campuran | fraksi |
| MCH-012 | Trommel screen | 3 | 150000000 | 1000 | kg/h | 150 | 45 | campuran | fraksi ukuran |
| MCH-013 | Magnetic separator | 3 | 45000000 | 500 | kg/h | 80 | 10 | campuran | besi dan nonbesi |
| MCH-014 | Eddy current separator | 4 | 450000000 | 1500 | kg/h | 180 | 30 | campuran kering | nonferrous |
| MCH-015 | Air classifier | 3 | 120000000 | 500 | kg/h | 150 | 20 | campuran kering | fraksi ringan/berat |
| MCH-016 | Ballistic separator | 4 | 500000000 | 2000 | kg/h | 180 | 50 | campuran | fraksi 2D/3D |
| MCH-017 | Optical NIR sorter | 4 | 1200000000 | 2000 | kg/h | 250 | 50 | plastik | fraksi polimer |
| MCH-018 | Robot pemilah AI | 5 | 2500000000 | 2500 | kg/h | 300 | 60 | campuran | fraksi |
| MCH-019 | Jembatan timbang | 4 | 350000000 | 30000 | kg/batch | 500 | 100 | truk | berat terukur |
| MCH-020 | Bunker penyimpanan | 4 | 150000000 | 20000 | kg/batch | 0 | 100 | material | stok |

### Organik, kompos dan biokonversi

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-021 | Tong komposter starter | 1 | 5000 | 2 | kg/h | 120 | 1 | organik | kompos |
| MCH-022 | Komposter ember bertingkat | 1 | 85000 | 10 | kg/batch | 100 | 1 | organik | kompos dan cairan |
| MCH-023 | Komposter takakura | 1 | 125000 | 5 | kg/batch | 100 | 1 | organik | kompos |
| MCH-024 | Komposter putar | 2 | 1500000 | 50 | kg/batch | 150 | 3 | organik | kompos |
| MCH-025 | Lubang biopori | 1 | 35000 | 2 | kg/batch | 50 | 1 | organik sesuai | bahan terurai |
| MCH-026 | Bak vermikompos | 2 | 750000 | 20 | kg/batch | 180 | 3 | organik sesuai | vermikompos |
| MCH-027 | Pencacah organik mini | 2 | 3500000 | 50 | kg/h | 120 | 4 | organik | cacahan |
| MCH-028 | Pencacah organik industri | 3 | 45000000 | 500 | kg/h | 180 | 15 | organik | cacahan |
| MCH-029 | Mixer kompos | 2 | 12000000 | 150 | kg/h | 120 | 8 | organik dan bulking | campuran kompos |
| MCH-030 | Pengayak kompos | 2 | 4500000 | 100 | kg/h | 100 | 6 | kompos matang | kompos ayak |
| MCH-031 | Windrow turner | 4 | 450000000 | 2000 | kg/h | 180 | 100 | kompos | kompos teraerasi |
| MCH-032 | Komposter in-vessel | 3 | 250000000 | 500 | kg/batch | 350 | 35 | organik | kompos |
| MCH-033 | Modul BSF | 2 | 5000000 | 10 | kg/h | 250 | 10 | organik sesuai | maggot dan kasgot |
| MCH-034 | Rak pembesaran BSF | 2 | 2500000 | 50 | kg/batch | 150 | 8 | pakan BSF | maggot |
| MCH-035 | Pemisah maggot kasgot | 3 | 18000000 | 100 | kg/h | 200 | 8 | hasil BSF | maggot/kasgot |
| MCH-036 | Pengering maggot | 3 | 35000000 | 20 | kg/h | 800 | 10 | maggot | maggot kering |
| MCH-037 | Penggiling tepung organik | 3 | 25000000 | 50 | kg/h | 500 | 8 | bahan kering sesuai | tepung |
| MCH-038 | Granulator pupuk | 3 | 55000000 | 100 | kg/h | 350 | 15 | kompos | granul |
| MCH-039 | Pengemas kompos | 2 | 8000000 | 100 | kg/h | 300 | 6 | kompos dan kemasan | kompos kemasan |
| MCH-040 | Digester anaerobik | 4 | 350000000 | 100 | kg/h | 400 | 100 | organik sesuai | biogas dan digestat |
| MCH-041 | Dewatering digestat | 4 | 120000000 | 300 | kg/h | 250 | 30 | digestat | padatan dan cairan |
| MCH-042 | Pemurni biogas | 4 | 180000000 | 30 | m3/h | 500 | 25 | biogas | gas murni |
| MCH-043 | Sistem penampung biogas | 4 | 85000000 | 50 | m3/batch | 0 | 30 | biogas | stok gas |

### Plastik

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-044 | Pencacah plastik mini | 2 | 7500000 | 25 | kg/h | 600 | 6 | plastik terpilah | cacahan kotor |
| MCH-045 | Granulator plastik | 3 | 35000000 | 100 | kg/h | 450 | 12 | plastik | cacahan kotor |
| MCH-046 | Pemisah label botol | 3 | 45000000 | 200 | kg/h | 200 | 12 | PET botol | PET dan label |
| MCH-047 | Bak float-sink | 3 | 35000000 | 150 | kg/h | 300 | 15 | cacahan | fraksi densitas |
| MCH-048 | Friction washer | 3 | 45000000 | 150 | kg/h | 400 | 15 | cacahan | cacahan basah |
| MCH-049 | Hot wash line | 3 | 120000000 | 200 | kg/h | 800 | 30 | PET cacah | cacahan basah bersih |
| MCH-050 | Centrifugal dryer | 3 | 45000000 | 150 | kg/h | 350 | 12 | cacahan basah | flakes kering |
| MCH-051 | Lini cacah-cuci plastik | 3 | 85000000 | 100 | kg/h | 1200 | 45 | plastik terpilah | flakes |
| MCH-052 | Agglomerator film | 3 | 55000000 | 80 | kg/h | 600 | 12 | film bersih | aglomerat |
| MCH-053 | Densifier EPS | 3 | 65000000 | 50 | kg/h | 500 | 12 | EPS bersih | EPS padat |
| MCH-054 | Extruder pellet line | 3 | 250000000 | 100 | kg/h | 1800 | 40 | flakes sesuai | pellet |
| MCH-055 | Filter lelehan polimer | 3 | 35000000 | 100 | kg/h | 200 | 6 | lelehan | lelehan tersaring |
| MCH-056 | Injection molding | 3 | 180000000 | 50 | kg/h | 1500 | 25 | pellet sesuai | produk cetak |
| MCH-057 | Compression molding | 3 | 85000000 | 40 | kg/h | 1000 | 20 | polimer sesuai | produk cetak |
| MCH-058 | Extruder profil plastik | 4 | 450000000 | 150 | kg/h | 1800 | 45 | pellet sesuai | profil |
| MCH-059 | Mesin lembaran plastik | 3 | 120000000 | 80 | kg/h | 1200 | 25 | pellet sesuai | lembaran |
| MCH-060 | Lini serat polyester | 4 | 3500000000 | 500 | kg/h | 2500 | 200 | rPET sesuai | serat |
| MCH-061 | Lini rPET food-grade bersertifikasi | 5 | 15000000000 | 1000 | kg/h | 3500 | 500 | PET memenuhi syarat | rPET khusus |

### Kertas dan karton

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-062 | Pemotong kertas manual | 2 | 750000 | 20 | kg/h | 50 | 3 | kertas | potongan |
| MCH-063 | Paper shredder | 2 | 3500000 | 25 | kg/h | 150 | 4 | kertas | cacahan |
| MCH-064 | Hydrapulper | 3 | 150000000 | 150 | kg/h | 700 | 35 | kertas dan air | pulp basah |
| MCH-065 | Screening pulp | 3 | 85000000 | 150 | kg/h | 300 | 20 | pulp | pulp tersaring |
| MCH-066 | Deinking line | 4 | 650000000 | 300 | kg/h | 1600 | 100 | pulp cetak | pulp deinked |
| MCH-067 | Lini pulp terpadu | 3 | 350000000 | 150 | kg/h | 1500 | 100 | kertas | pulp |
| MCH-068 | Cetak pulp kemasan | 3 | 120000000 | 50 | kg/h | 1000 | 30 | pulp | kemasan |
| MCH-069 | Mesin tray telur | 3 | 250000000 | 100 | kg/h | 1200 | 60 | pulp | tray |
| MCH-070 | Paper machine | 4 | 5000000000 | 1000 | kg/h | 2000 | 500 | pulp | kertas daur ulang |

### Logam, kaca dan konstruksi

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-071 | Pemotong kabel manual | 2 | 1500000 | 10 | kg/h | 200 | 4 | kabel aman | logam dan isolasi |
| MCH-072 | Cable granulator | 3 | 125000000 | 100 | kg/h | 1200 | 25 | kabel aman | granul tembaga dan plastik |
| MCH-073 | Lini pemisahan logam | 3 | 95000000 | 150 | kg/h | 500 | 35 | logam campur | logam terpilah |
| MCH-074 | Metal shear | 3 | 180000000 | 300 | kg/h | 500 | 30 | besi | scrap ukuran |
| MCH-075 | Metal baler | 3 | 350000000 | 500 | kg/h | 350 | 50 | logam | bale logam |
| MCH-076 | Metal shredder | 4 | 2500000000 | 2000 | kg/h | 1000 | 150 | logam aman | shredded scrap |
| MCH-077 | Smelter aluminium mitra | 4 | 0 | 300 | kg/h | 3500 | 0 | aluminium sesuai | ingot |
| MCH-078 | Smelter baja mitra | 4 | 0 | 500 | kg/h | 3000 | 0 | besi sesuai | baja sekunder |
| MCH-079 | Pemurnian tembaga mitra | 4 | 0 | 100 | kg/h | 5000 | 0 | tembaga sesuai | tembaga sekunder |
| MCH-080 | Refinery logam mulia mitra | 4 | 0 | 5 | kg/h | 50000 | 0 | lot teruji | logam pulih |
| MCH-081 | Glass crusher | 3 | 65000000 | 120 | kg/h | 250 | 20 | kaca | cullet |
| MCH-082 | Glass optical sorter | 4 | 750000000 | 1000 | kg/h | 300 | 50 | cullet | cullet grade |
| MCH-083 | Pencuci botol guna ulang | 3 | 85000000 | 200 | pcs/h | 300 | 25 | botol utuh | botol QC |
| MCH-084 | Glass furnace mitra | 4 | 0 | 500 | kg/h | 2500 | 0 | cullet sesuai | kaca sekunder |
| MCH-085 | Jaw crusher konstruksi | 3 | 250000000 | 1000 | kg/h | 350 | 75 | beton bersih | agregat |
| MCH-086 | Vibrating screen agregat | 3 | 85000000 | 1000 | kg/h | 120 | 40 | agregat | agregat tergrade |
| MCH-087 | Lini blok agregat | 3 | 120000000 | 300 | kg/h | 450 | 50 | agregat dan binder | blok QC |

### Tekstil, kayu, karet dan upcycling

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-088 | Mesin jahit | 2 | 2500000 | 4 | pcs/h | 1000 | 4 | kain dan aksesori | produk jahit |
| MCH-089 | Mesin obras | 2 | 3500000 | 4 | pcs/h | 800 | 4 | kain | produk jahit |
| MCH-090 | Pemotong kain | 2 | 2000000 | 20 | kg/h | 150 | 4 | tekstil | potongan |
| MCH-091 | Textile fiber opener | 3 | 120000000 | 80 | kg/h | 800 | 30 | tekstil | serat |
| MCH-092 | Lini nonwoven | 4 | 1800000000 | 300 | kg/h | 1500 | 120 | serat | lembaran nonwoven |
| MCH-093 | Lini benang daur ulang | 4 | 2500000000 | 250 | kg/h | 2000 | 150 | serat | benang |
| MCH-094 | Meja kerajinan starter | 1 | 0 | 2 | pcs/h | 500 | 4 | material bersih | kerajinan |
| MCH-095 | Bengkel upcycling | 2 | 5000000 | 4 | pcs/h | 1000 | 15 | material dan hardware | produk BOM |
| MCH-096 | Gergaji bengkel | 2 | 2500000 | 20 | kg/h | 300 | 5 | kayu aman | potongan |
| MCH-097 | Wood chipper | 3 | 45000000 | 120 | kg/h | 300 | 20 | kayu | chip |
| MCH-098 | Hammer mill kayu | 3 | 55000000 | 150 | kg/h | 400 | 20 | chip | serbuk |
| MCH-099 | Pengering biomassa | 3 | 75000000 | 150 | kg/h | 500 | 30 | biomassa | biomassa kering |
| MCH-100 | Lini pellet biomassa | 3 | 120000000 | 100 | kg/h | 600 | 45 | chip | pellet |
| MCH-101 | Press briket | 3 | 45000000 | 80 | kg/h | 500 | 20 | biomassa sesuai | briket |
| MCH-102 | Coco fiber separator | 3 | 65000000 | 100 | kg/h | 400 | 25 | sabut | cocofiber/cocopeat |
| MCH-103 | Tire debeader | 3 | 45000000 | 100 | kg/h | 300 | 15 | ban | karet dan kawat |
| MCH-104 | Tire shredder | 3 | 180000000 | 150 | kg/h | 900 | 35 | ban | cacahan |
| MCH-105 | Rubber crumb line | 3 | 180000000 | 80 | kg/h | 1500 | 40 | karet | crumb |
| MCH-106 | Rubber powder mill | 4 | 350000000 | 100 | kg/h | 1800 | 40 | crumb | bubuk karet |
| MCH-107 | Reclaimed rubber mitra | 4 | 0 | 100 | kg/h | 2000 | 0 | karet sesuai | reclaimed rubber |

### Jelantah, elektronik dan limbah khusus

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-108 | Jeriken jelantah tertutup | 1 | 35000 | 20 | L/batch | 0 | 1 | jelantah | stok |
| MCH-109 | Filter jelantah sederhana | 2 | 1500000 | 20 | L/h | 200 | 4 | UCO | UCO tersaring |
| MCH-110 | Lini pemurnian UCO | 3 | 45000000 | 80 | kg/h | 700 | 20 | UCO | UCOF |
| MCH-111 | Biodiesel mitra | 4 | 0 | 100 | L/h | 1500 | 0 | UCO sesuai | biodiesel |
| MCH-112 | Drop box elektronik | 2 | 750000 | 30 | kg/batch | 0 | 3 | elektronik | stok aman |
| MCH-113 | Penyimpanan baterai khusus | 3 | 10000000 | 100 | kg/batch | 0 | 10 | baterai | stok aman |
| MCH-114 | Stasiun inspeksi elektronik | 3 | 15000000 | 20 | kg/h | 500 | 10 | elektronik | lot teridentifikasi |
| MCH-115 | Recovery elektronik mitra | 3 | 0 | 30 | kg/h | 6000 | 0 | EW | material pulih |
| MCH-116 | Recovery baterai mitra | 4 | 0 | 50 | kg/h | 8000 | 0 | baterai | material pulih |
| MCH-117 | Recovery panel surya mitra | 4 | 0 | 100 | kg/h | 3500 | 0 | panel | material pulih |
| MCH-118 | Recovery refrigeran mitra | 3 | 0 | 10 | pcs/h | 50000 | 0 | alat pendingin | komponen dan refrigeran aman |
| MCH-119 | Pengolahan limbah B3 mitra | 3 | 0 | 100 | kg/h | 10000 | 0 | limbah khusus | disposition aman |

### Energi dan pengendalian lingkungan

| ID | Mesin | F | CAPEX GC | Kapasitas | Unit | OPEX GC/unit | m² | Input | Output/fungsi |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| MCH-120 | RDF shredder | 4 | 150000000 | 300 | kg/h | 200 | 40 | residu eligible | cacahan RDF |
| MCH-121 | Lini RDF/SRF | 4 | 300000000 | 150 | kg/h | 300 | 70 | residu eligible | RDF/SRF |
| MCH-122 | Biochar mitra | 4 | 0 | 50 | kg/h | 1300 | 0 | biomassa sesuai | biochar |
| MCH-123 | Genset biogas | 4 | 150000000 | 50 | kWh/h | 250 | 30 | biogas | listrik |
| MCH-124 | PLTS atap | 3 | 150000000 | 10 | kWh/h | 0 | 60 | matahari | listrik |
| MCH-125 | Mikrohidro saluran | 4 | 250000000 | 15 | kWh/h | 0 | 40 | aliran air sesuai | listrik |
| MCH-126 | Waste-to-energy mitra beta | 4 | 1500000000 | 120 | kg/h | 900 | 200 | RDF eligible | listrik dan residu |
| MCH-127 | Baghouse filter | 4 | 150000000 | 500 | kg/h | 180 | 30 | aliran proses terkait | debu tertangkap |
| MCH-128 | Scrubber gas | 4 | 250000000 | 500 | kg/h | 250 | 40 | aliran proses terkait | aliran terkendali |
| MCH-129 | IPAL terpadu | 4 | 150000000 | 200 | kg/h | 250 | 60 | air limbah | air olahan dan lumpur |
| MCH-130 | Bak pengendap | 3 | 15000000 | 200 | kg/h | 100 | 15 | air limbah | air dan lumpur |
| MCH-131 | Filter press lumpur | 4 | 120000000 | 100 | kg/h | 300 | 25 | lumpur | cake dan filtrat |
| MCH-132 | Sistem kontrol bau | 3 | 35000000 | 200 | kg/h | 120 | 15 | aliran proses terkait | bau terkendali |
| MCH-133 | Monitoring emisi CEMS | 4 | 450000000 | 1 | audit/h | 1000 | 8 | data emisi | rekaman |
| MCH-134 | Laboratorium QC material | 3 | 75000000 | 10 | audit/h | 2500 | 20 | sampel | hasil QC |
| MCH-135 | Meter energi dan air | 3 | 5000000 | 1 | audit/h | 0 | 2 | data utilitas | rekaman |
| MCH-136 | Sistem monitoring neraca massa | 4 | 25000000 | 1 | audit/h | 0 | 5 | ledger | audit |
| MCH-137 | Water reuse system | 5 | 350000000 | 500 | kg/h | 300 | 50 | air olahan | air proses |
| MCH-138 | Pusat riset Gaia | 5 | 1000000000 | 1 | audit/h | 10000 | 100 | data riset | blueprint terkunci |

## 3. Aturan operasi, upgrade dan pembelian

- Starter: gerobak, meja pilah, gudang dan lahan mengikuti starter pack file 01; jangan mendebit pembelian aset yang sudah diberikan. Meja kerajinan starter merupakan usulan aset akses, bukan tambahan hadiah jual kembali.
- F1 komposter baseline 2 kg/h adalah throughput pengisian abstrak; usulan kapasitas aktif 10 kg dan maturasi 24 jam game. Komposter batch lain: 24 jam; vermikompos 48 jam; BSF 48 jam; digester 48 jam. Angka waktu dipercepat, bukan durasi nyata. Batch tidak dapat menerima input baru sampai slot bebas.
- Harga pembelian + instalasi usulan 10% untuk mesin F3–F5, 0% F1–F2; area harus tersedia. Biaya instalasi bukan pengganti CAPEX fasilitas pendukung. Sewa mitra menggunakan 1,25× biaya variabel + pengiriman sesuai file 01; tidak memungut biaya kepemilikan lagi. Mitra khusus memakai tarif yang ditampilkan, bukan markup sewa kedua.
- Satu pekerjaan hanya memilih **lini terpadu ATAU rangkaian komponen**; tidak menghitung dua kali OPEX, massa, poin, kapasitas ataupun output. Lini terpadu memerlukan QC dan kontrol lingkungan yang sesuai. Mesin pendukung tidak otomatis menciptakan barang jual.
- Usulan upgrade U1–U4: kapasitas ×1/1,5/2/3; biaya upgrade masing-masing 0/40%/75%/120% CAPEX dasar (incremental); OPEX per unit ×1/0,98/0,95/0,90. Area dan utilitas ditinjau ulang; tidak boleh melebihi kemampuan lini terendah. Tidak menaikkan yield otomatis. Mitra, storage, meter, audit dan fasilitas khusus dikecualikan dari rumus upgrade generik.
- Maintenance aktif 0,1% CAPEX dasar per hari (file 01); usulan wear +1 poin per 8 jam kerja; pada 80 poin peringatan, 100 poin stop menerima job baru. Servis mengurangi 50 poin dengan biaya 0,5% CAPEX (minimum 100 GC); tidak merusak stok. Parameter balancing, bukan reliabilitas engineering.
- Tidak ada pendapatan dari mesin idle. Uang dan input direserve saat job dimulai; penggunaan listrik/air/bahan tambahan dicatat. Penjualan aset maksimal 50% CAPEX yang benar-benar dibayar, setelah 24 jam; aset subsidi/starter/mitra tidak bisa dijual. Batalkan job dengan pengembalian stok yang belum dikonsumsi dan biaya sesuai tahap, tepat sekali.

## 4. Rantai produksi dan mapping integrasi

| Jalur | Urutan | Gate dan syarat |
|---|---|---|
| Kompos | pilah → cacah opsional → komposter → ayak → kemas | F1; pengemasan F2; COMP/COMPP sesuai file 02 |
| BSF | pilah organik layak → modul BSF → pisah → pengering opsional | F2; R-BSF, R-MAGD; feed QC |
| PET | pilah → baler opsional → cacah/cuci → flakes → pellet | F3; PETF/PETP, R-PETP |
| HDPE/PP/PE/PVC/ABS/HIPS/PC/PS | lini terpisah sesuai polimer → flakes → pellet | F3; gunakan recipe ID file 01; jangan mencampur polimer tanpa resep tervalidasi |
| Kertas | pilah → baler → pulp → screening → produk | F2–F4; R-PULP/R-DIP; air dan reject wajib tercatat |
| Logam | pilah → separator → shear/baler → mitra smelter | F3–F4; logam khusus via assay/mitra |
| Kaca | pilah warna → crusher → cullet | F3; cermin/keramik tidak otomatis diterima |
| Karet | pisah logam → shred → crumb | F3; hindari hitung ulang kredit ban |
| Kayu | chip → kering → pellet/briket | F3; R-BIOPEL; kayu terkontaminasi ditolak |
| Sabut | separator → cocopeat/cocofiber | F3; R-COCO |
| Jelantah | tampung → filter → pemurnian | F3; R-UCO; density 0,92 kg/L dari file 01 |
| Elektronik/B3 | inspeksi → penyimpanan aman → mitra | F2–F4; biaya dan disposition terverifikasi; abstraksi tanpa petunjuk kimia |
| RDF/WtE | pilah residu eligible → RDF → mitra energi → disposition abu/gas | F4; R-WTE; recycle-first, kontrol emisi wajib, PVC/B3/wet reject |
| Konstruksi | seleksi bersih → crusher → screen | F3; R-AGG; produk struktural terkunci sampai QC |
| Upcycling | bahan bersih → bengkel/mesin → produk BOM | F2; gunakan BOM file 01, bukan output gratis |
| Biogas | digester → gas cleanup → genset atau offtake | F4; resep baru wajib tervalidasi; jangan mengkredit gas dan listrik dari input gas yang sama |
| IPAL | air limbah → pengolahan → air reuse/lumpur | F3–F5; disposition lumpur tercatat, tidak menghapus massa |

F5 teknologi lanjutan adalah roadmap, bukan kewajiban mencapai God. Alkimia Gaia tetap mengikuti gate spesifikasi asli, tidak membuka proses industri nyata yang belum tervalidasi.

## 5. Schema dan state machine

```yaml
machine_template:
  id: MCH-xxx
  version: 1
  stage_min: F1
  category: string
  purchase_gc: integer
  capacity_value: decimal
  capacity_unit: enum
  variable_gc_per_unit: integer
  footprint_m2: decimal
  access_mode: owned_or_rental_or_partner_or_starter
  recipe_ids: [] # explicit existing ID, never infer from display text
  dependency_ids: []
  batch_duration_s: null
  storage_capacity_g: null
  energy_wh_per_input_unit: null
  water_g_per_input_unit: null
  status: locked_pending_recipe
  price_basis: simulation_assumption
machine_instance:
  player_id: uuid
  template_id: string
  upgrade_level: integer
  wear_bp: integer
  status: idle_or_reserved_or_running_or_paused_or_maintenance
  last_settled_at: timestamp
  version: integer
```

Use integer grams, milliliters, Wh, GC and basis points internally; fractional capacity values normalized on seed import. Audit/service units use integer count. Job state: quote → reserve → run → settle → QC → inventory/disposition. Lock machine slot and lot atomically; no client timestamps; unique settlement key. Capacity for continuous line = minimum compatible stage throughput; batch line = batch capacity and duration, no automatic conversion to kg/h. Storage capacity is not processing rate. For PCS require SKU mass/BOM. Unknown energy/water/dependencies are null and block activation where required; do not silently assume zero. For bundled variable cost, utility charges must be allocated inside bundle or charged separately after replacing bundle, never both.

## 6. Pendidikan dan balancing

UI kartu mesin: nama, gambar, fungsi nyata, harga, syarat F, kapasitas, OPEX, estimasi pendapatan bersih berdasarkan order, limbah sekunder, energi/air bila tersedia, status sewa, waktu game dan catatan durasi nyata jika bersumber. Tampilkan alasan lock. Jangan menunjukkan klaim bahwa filter menghapus semua emisi atau WtE tidak menghasilkan abu. Daur ulang, pencegahan, guna ulang dan kompos tetap dapat mencapai God tanpa termal. Harga mesin tidak dipengaruhi indeks harian komoditas secara otomatis.

QA sebelum enable: unique IDs; mapping recipe existing; unit kompatibel; semua output/ancillary mass tercatat; no negative stock/cash; rental dan ownership tidak bertumpuk; batch tidak overwrite; slot offline tidak melampaui 8 jam settlement; simultaneous jobs; failed QC; electricity limit; wastewater disposition; maintenance pause; sale/refund idempotent; no double credits; beginner solvent with starter 10.000 GC; 90-day economy rerun; compare manual and automated paths; verify CAPEX with local RFQ if using real market labels. No actual 90-day simulation, industrial procurement validation or code changes performed by this document.

## 7. Handoff
Import sebagai seed terpisah, bukan mengganti file 01. Buat mapping ID, dependency, utilitas, recipe dan akses untuk tiap mesin; audit konflik biaya dan kapasitas terhadap file 01–04. Prioritas F1/F2 untuk MVP, F3 setelah QC, F4/F5 feature flags. Mesin tanpa resep, data utilitas atau gate yang diperlukan tetap locked. Minta persetujuan pemilik sebelum migration produksi. Seluruh konfigurasi baru adalah usulan review.
