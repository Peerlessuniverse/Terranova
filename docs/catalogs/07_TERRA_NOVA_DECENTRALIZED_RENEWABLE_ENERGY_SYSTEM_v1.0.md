# TERRA NOVA — Decentralized Renewable Energy System (DRES) v1.0

Addendum 07 | Chapter I — The Calling of Gaia | 26 November 2026 | Draft review

## 1. Ruang lingkup dan presedensi
[D] Pemilik meminta energi terbarukan selain PLTS, khususnya wind turbine dan mikrohidro, dengan skala rumah tangga sampai UMKM. [U] Batas teknis game: total daya nominal pembangkit DRES non-WtE per lahan ≤100 kW (PV dihitung kWp secara konservatif); penyimpanan ≤200 kWh; total ekspor DRES ≤100 kW dan kuota kontrak. Ini bukan definisi hukum UMKM. Batas berlaku agregat termasuk upgrade, sewa dan unit paralel; bukan per mesin. Tidak ada bendungan besar, ladang angin atau solar farm skala utilitas. WtE file 06 tetap memiliki batas sendiri; jangan diam-diam mengubahnya. Jika pemilik bermaksud membatasi seluruh pembangkit termasuk WtE, perlu amendemen terpisah.

Free energy berarti sumber alam tanpa biaya bahan bakar, bukan energi tak terbatas atau perpetual motion. TEG, generator pedal dan eksperimen memerlukan masukan energi. Seluruh harga, ukuran dan parameter adalah seed simulasi nominal GC≈Rp1, bukan kutipan harga pemasok, standar instalasi, atau jaminan produksi. GC tidak dapat dicairkan. CAPEX hanya modul sesuai deskripsi, biaya lokasi, instalasi, proteksi dan sambungan terpisah. Area angin adalah zona eksklusi simulasi, bukan pedoman keselamatan teknik. Semua entri pending validasi resep dan konfigurasi; display_only tidak executable; riset hanya setelah validasi, tidak boleh dipakai sebagai sumber daya tak terbatas.

## 2. Katalog seed
F1–F5 mengikuti file 03. Alias memakai ID lama dan inventaris bersama, tanpa duplikasi aset atau biaya. kWp = PV DC peak; kW = daya; kWh = kapasitas simpan; kWth = panas. Harga 0 pada mitra/display bukan aset gratis. Mode beli/sewa memerlukan kontrak sewa. Footprint simulasi harus muat pada peta dan survei lokasi harus lulus.

| ID | Kategori | Nama | F | CAPEX GC | Kapasitas | m² | Mode | Fungsi |
|---|---|---|---:|---:|---|---:|---|---|
| DRE-001 | Surya | Solar kit DC | 1 | 450000 | 0.02 kWp | 1 | beli/sewa | Lampu DC; controller terintegrasi |
| DRE-002 | Surya | PLTS pico | 1 | 1500000 | 0.1 kWp | 1 | beli/sewa | PV + controller; baterai terpisah |
| DRE-003 | Surya | PLTS atap 500 Wp | 2 | 6000000 | 0.5 kWp | 3 | beli/sewa | PV dan mounting |
| DRE-004 | Surya | PLTS atap 1 kWp | 2 | 12000000 | 1 kWp | 6 | beli/sewa | PV dan mounting |
| DRE-005 | Surya | PLTS atap 3 kWp | 2 | 33000000 | 3 kWp | 18 | beli/sewa | PV dan mounting |
| DRE-006 | Surya | PLTS atap 5 kWp | 3 | 50000000 | 5 kWp | 30 | beli/sewa | PV dan mounting |
| DRE-007 | Surya | PLTS atap 10 kWp | 3 | 95000000 | 10 kWp | 60 | beli/sewa | PV dan mounting |
| DRE-008 | Surya | PLTS atap 20 kWp | 3 | 180000000 | 20 kWp | 120 | beli | PV dan mounting |
| DRE-009 | Surya | PLTS atap 50 kWp | 4 | 425000000 | 50 kWp | 300 | beli | PV dan mounting |
| DRE-010 | Surya | PLTS atap 100 kWp | 4 | 800000000 | 100 kWp | 600 | beli | PV dan mounting |
| DRE-011 | Surya | Panel fleksibel | 2 | 2500000 | 0.2 kWp | 2 | beli | PV untuk atap ringan |
| DRE-012 | Surya | Solar carport | 3 | 85000000 | 5 kWp | 35 | beli | PV dan struktur |
| DRE-013 | Surya | Solar tracker mini | 3 | 28000000 | 1 kWp | 12 | beli | PV tracker; motor konsumsi listrik |
| DRE-014 | Surya | PLTS terapung mini | 4 | 90000000 | 5 kWp | 45 | beli | Hanya kolam buatan yang layak; bukan sungai |
| DRE-015 | Surya | Solar dryer | 2 | 3500000 | 2 kWth | 6 | beli | Panas pengeringan; nol listrik |
| DRE-016 | Surya | Solar water heater | 2 | 7000000 | 2 kWth | 4 | beli | Panas air; nol listrik |
| DRE-017 | Angin | HAWT pico | 1 | 2500000 | 0.1 kW | 8 | beli/sewa | Turbin mini; lokasi terbuka |
| DRE-018 | Angin | HAWT 300 W | 2 | 6500000 | 0.3 kW | 16 | beli/sewa | Turbin dan tiang |
| DRE-019 | Angin | HAWT 1 kW | 2 | 22000000 | 1 kW | 40 | beli/sewa | Turbin dan tiang |
| DRE-020 | Angin | HAWT 3 kW | 3 | 65000000 | 3 kW | 100 | beli | Turbin dan tiang |
| DRE-021 | Angin | HAWT 5 kW | 3 | 110000000 | 5 kW | 180 | beli | Turbin dan tiang |
| DRE-022 | Angin | HAWT 10 kW | 4 | 250000000 | 10 kW | 350 | beli | Turbin dan tiang |
| DRE-023 | Angin | HAWT 20 kW | 4 | 550000000 | 20 kW | 600 | beli | Turbin dan tiang |
| DRE-024 | Angin | Savonius mini | 1 | 3000000 | 0.05 kW | 6 | beli | VAWT demonstrasi |
| DRE-025 | Angin | Savonius 300 W | 2 | 12000000 | 0.3 kW | 20 | beli | VAWT |
| DRE-026 | Angin | Darrieus 1 kW | 3 | 30000000 | 1 kW | 35 | beli | VAWT |
| DRE-027 | Angin | Helical VAWT 2 kW | 3 | 65000000 | 2 kW | 60 | beli | VAWT |
| DRE-028 | Angin | Helical VAWT 5 kW | 4 | 180000000 | 5 kW | 150 | beli | VAWT |
| DRE-029 | Angin | Anemometer | 1 | 650000 | 1 audit | 1 | beli | Survei angin; tidak menghasilkan listrik |
| DRE-030 | Hidro | Pico hydro 100 W | 1 | 3000000 | 0.1 kW | 3 | beli/sewa | Aliran layak; tanpa bendungan |
| DRE-031 | Hidro | Pico hydro 500 W | 2 | 12000000 | 0.5 kW | 6 | beli/sewa | Aliran layak |
| DRE-032 | Hidro | Pelton 1 kW | 2 | 28000000 | 1 kW | 10 | beli | Head tinggi; debit rendah |
| DRE-033 | Hidro | Turgo 2 kW | 3 | 50000000 | 2 kW | 15 | beli | Head menengah/tinggi |
| DRE-034 | Hidro | Crossflow 3 kW | 3 | 80000000 | 3 kW | 20 | beli | Debit dan head sesuai |
| DRE-035 | Hidro | Crossflow 5 kW | 3 | 125000000 | 5 kW | 25 | beli | Debit dan head sesuai |
| DRE-036 | Hidro | Crossflow 15 kW | 4 | 250000000 | 15 kW | 40 | alias MCH-125 | Aset mikrohidro saluran lama |
| DRE-037 | Hidro | Crossflow 25 kW | 4 | 550000000 | 25 kW | 65 | beli | Run-of-river |
| DRE-038 | Hidro | Francis mini 30 kW | 4 | 750000000 | 30 kW | 75 | beli | Head/debit sesuai |
| DRE-039 | Hidro | Kaplan mini 20 kW | 4 | 650000000 | 20 kW | 70 | beli | Head rendah |
| DRE-040 | Hidro | Propeller low-head 5 kW | 3 | 160000000 | 5 kW | 30 | beli | Head rendah |
| DRE-041 | Hidro | Archimedes screw 3 kW | 3 | 180000000 | 3 kW | 35 | beli | Head rendah |
| DRE-042 | Hidro | Archimedes screw 10 kW | 4 | 450000000 | 10 kW | 65 | beli | Head rendah |
| DRE-043 | Hidro | Kincir air 200 W | 2 | 7000000 | 0.2 kW | 10 | beli | Aliran dengan head sesuai |
| DRE-044 | Hidro | Kincir air 1 kW | 3 | 35000000 | 1 kW | 20 | beli | Aliran dengan head sesuai |
| DRE-045 | Hidro | Turbin hidrokinetik 500 W | 3 | 35000000 | 0.5 kW | 12 | beli | Arus tanpa head; model arus terpisah |
| DRE-046 | Hidro | Turbin hidrokinetik 2 kW | 4 | 100000000 | 2 kW | 25 | beli | Arus tanpa head; model arus terpisah |
| DRE-047 | Hidro | Saringan intake ramah fauna | 2 | 3000000 | 0.05 m3/s | 3 | beli | Kapasitas debit; bukan generator |
| DRE-048 | Hidro | Saluran bypass dan jalur fauna | 3 | 20000000 | 0.2 m3/s | 12 | beli | Aliran ekologis; bukan generator |
| DRE-049 | Hidro | Sensor debit dan muka air | 2 | 2500000 | 1 audit | 1 | beli | Survei hidrologi |
| DRE-050 | Hidro | Modul pico hidro pipa gravitasi | 3 | 15000000 | 0.5 kW | 4 | beli | Hanya tekanan surplus alami; bukan pompa sirkulasi |
| DRE-051 | Panas dan riset | TEG demonstrasi | 1 | 250000 | 0.005 kW | 1 | beli | Panas terukur; sensor |
| DRE-052 | Panas dan riset | TEG panas buang | 3 | 8000000 | 0.05 kW | 2 | beli | Panas buang teralokasi |
| DRE-053 | Panas dan riset | TEG modular | 4 | 45000000 | 0.25 kW | 6 | beli | Panas buang teralokasi |
| DRE-054 | Panas dan riset | Stirling demonstrasi | 2 | 3500000 | 0.01 kW | 2 | riset | Panas eksternal; tidak dijual |
| DRE-055 | Panas dan riset | Stirling solar termal | 4 | 75000000 | 0.5 kW | 20 | riset | Panas surya terukur |
| DRE-056 | Panas dan riset | ORC mikro | 4 | 400000000 | 5 kW | 30 | riset | Panas buang sesuai; bukan WTE-040 100 kW |
| DRE-057 | Panas dan riset | Plant microbial fuel cell | 2 | 750000 | 0.0001 kW | 2 | riset | Maks 0.1 W; sensor |
| DRE-058 | Panas dan riset | Microbial fuel cell air limbah | 3 | 5000000 | 0.001 kW | 4 | riset | Maks 1 W; tidak mengganti IPAL |
| DRE-059 | Panas dan riset | Piezoelectric tile kit | 2 | 2000000 | 0.001 kW | 2 | riset | Puncak 1 W saat tekanan |
| DRE-060 | Panas dan riset | Generator pedal | 1 | 1500000 | 0.1 kW | 2 | beli | Energi manusia; sesi terbatas |
| DRE-061 | Panas dan riset | Energy harvester getaran | 3 | 2500000 | 0.0005 kW | 1 | riset | Getaran eksternal; tidak menggandakan daya mesin |
| DRE-062 | Panas dan riset | Turbin pasang surut mini | 4 | 0 | 0 kW | 0 | display_only | Referensi lokasi pesisir; bukan aset aktif |
| DRE-063 | Panas dan riset | Geotermal mikro | 4 | 0 | 0 kW | 0 | display_only | Kajian; akses panas lokasi khusus |
| DRE-064 | Panas dan riset | Energi gelombang mini | 4 | 0 | 0 kW | 0 | display_only | Kajian; bukan aset aktif |
| DRE-065 | Penyimpanan dan distribusi | Controller PWM | 1 | 150000 | 0.1 kW | 1 | beli | PV DC |
| DRE-066 | Penyimpanan dan distribusi | MPPT 500 W | 2 | 750000 | 0.5 kW | 1 | beli | PV DC |
| DRE-067 | Penyimpanan dan distribusi | MPPT 3 kW | 2 | 3500000 | 3 kW | 1 | beli | PV DC |
| DRE-068 | Penyimpanan dan distribusi | Inverter off-grid 500 W | 2 | 2000000 | 0.5 kW | 1 | beli | DC ke AC |
| DRE-069 | Penyimpanan dan distribusi | Inverter hybrid 3 kW | 2 | 8500000 | 3 kW | 2 | beli | DC/AC dan storage |
| DRE-070 | Penyimpanan dan distribusi | Inverter hybrid 5 kW | 3 | 15000000 | 5 kW | 2 | beli | DC/AC dan storage |
| DRE-071 | Penyimpanan dan distribusi | Inverter hybrid 10 kW | 3 | 22000000 | 10 kW | 3 | beli | DC/AC dan storage |
| DRE-072 | Penyimpanan dan distribusi | Inverter 20 kW | 3 | 35000000 | 20 kW | 3 | alias WTE-065 | Aset dan proteksi lama |
| DRE-073 | Penyimpanan dan distribusi | Inverter 50 kW | 4 | 75000000 | 50 kW | 5 | beli | DC/AC |
| DRE-074 | Penyimpanan dan distribusi | Inverter 100 kW | 4 | 140000000 | 100 kW | 8 | beli | DC/AC |
| DRE-075 | Penyimpanan dan distribusi | Baterai LFP pico | 1 | 900000 | 0.25 kWh | 1 | beli | 0.1 kW charge/discharge |
| DRE-076 | Penyimpanan dan distribusi | Baterai LFP 1 kWh | 2 | 4500000 | 1 kWh | 1 | beli | 0.5 kW charge/discharge |
| DRE-077 | Penyimpanan dan distribusi | Baterai LFP 5 kWh | 2 | 20000000 | 5 kWh | 2 | beli | 2.5 kW charge/discharge |
| DRE-078 | Penyimpanan dan distribusi | Baterai LFP 10 kWh | 3 | 40000000 | 10 kWh | 3 | beli | 5 kW charge/discharge |
| DRE-079 | Penyimpanan dan distribusi | Baterai LFP 20 kWh | 3 | 80000000 | 20 kWh | 5 | alias WTE-066 | 10 kW charge/discharge; tipe usulan |
| DRE-080 | Penyimpanan dan distribusi | Baterai LFP 50 kWh | 4 | 180000000 | 50 kWh | 10 | beli | 25 kW charge/discharge |
| DRE-081 | Penyimpanan dan distribusi | Baterai LFP 100 kWh | 4 | 350000000 | 100 kWh | 18 | beli | 50 kW charge/discharge |
| DRE-082 | Penyimpanan dan distribusi | Smart meter | 1 | 350000 | 1 audit | 1 | alias WTE-064 | Meter sumber dan beban |
| DRE-083 | Penyimpanan dan distribusi | Meter energi dan air | 3 | 5000000 | 1 audit | 2 | alias MCH-135 | Meter utilitas |
| DRE-084 | Penyimpanan dan distribusi | EMS | 4 | 75000000 | 1 audit | 4 | alias WTE-068 | Optimasi dispatch |
| DRE-085 | Penyimpanan dan distribusi | Panel proteksi mikrogrid | 2 | 2500000 | 5 kW | 2 | beli | Proteksi dan isolasi |
| DRE-086 | Penyimpanan dan distribusi | Panel distribusi UMKM | 3 | 12000000 | 25 kW | 3 | beli | Proteksi dan isolasi |
| DRE-087 | Penyimpanan dan distribusi | Panel distribusi 100 kW | 4 | 45000000 | 100 kW | 6 | beli | Proteksi dan isolasi |
| DRE-088 | Penyimpanan dan distribusi | Stasiun pengisian gerobak listrik | 3 | 6000000 | 2 kW | 4 | beli | Beban listrik; bukan generator |
| DRE-089 | Penyimpanan dan distribusi | Kontrol turbin angin dan dump load | 2 | 2500000 | 1 kW | 2 | beli | Kontrol dan proteksi |
| DRE-090 | Penyimpanan dan distribusi | Kontrol hidro dan proteksi | 3 | 6000000 | 5 kW | 2 | beli | Kontrol dan proteksi |
| DRE-091 | Penyimpanan dan distribusi | Weather station mini | 3 | 7500000 | 1 audit | 2 | beli | Data cuaca kota |
| DRE-092 | Penyimpanan dan distribusi | Energy audit kit | 2 | 1500000 | 1 audit | 1 | beli/sewa | Pemetaan beban |
| DRE-093 | Penyimpanan dan distribusi | Kontrak mikrogrid komunitas | 2 | 0 | 10 kW | 0 | mitra | Kuota jasa, bukan pembangkit milik pemain |

## 3. Parameter produksi dan biaya operasi [U]

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

## 4. Model energi deterministik
- PV: E_AC = min(P_kWp × irradiance_kWh_m2 / 1 kW_m2 × PR, P_AC_limit × jam). Cuaca malam nol. Shading dan degradasi sebagai faktor 0–1; jika sudah dalam PR jangan dihitung lagi.
- Wind: gunakan kurva daya tervalidasi; fallback P = rated × clamp((v³−v_cut_in³)/(v_rated³−v_cut_in³),0,1) pada cut-in hingga rated; rated hingga cut-out; nol di luar. E=P×jam. Jangan gunakan kecepatan rata-rata bulanan sebagai input kubik.
- Hydro: Q_use=min(Q_intake_max,max(0,Q_river−Q_ecological−Q_other_allocated)); P_kW=min(rated,9,81×Q_use_m3s×H_net_m×eta). E=P×jam. Jika head/debit tidak layak, banjir, intake tersumbat, atau fauna terancam, stop. Tidak ada pengeringan sungai atau head fiktif.
- Hydrokinetic: P_kW=min(rated,0,5×1000×A_m2×v_ms³×Cp_eta/1000). Tidak memakai rumus head sekaligus untuk lot energi yang sama. Batas ekstraksi aliran dan area sapuan bersama.
- TEG/ORC/Stirling: listrik ≤ min(rated×jam, panas masuk terukur×eta). Kurangi panas yang sama dari ledger panas; energi pemulihan panas WtE hanya dikreditkan melalui file 06 bila asal dan alokasi sah; default nol kredit God DRES. Panas buangan mesin listrik tidak boleh menghasilkan energi lebih dari masukan mesin.
- Eksperimen: E ≤ min(rated×jam aktif, energi masukan terukur×eta). Plant MFC cap 2,4 Wh/hari per unit; piezo cap 1 Wh/hari/unit fixture; pedal cap 50 Wh/sesi dan 2 sesi/hari. Tidak ada magnet-only, overunity, generator pengisian sendiri atau air yang dipompa naik untuk menghasilkan surplus.
- Storage: SOC_next=SOC+E_charge×eta_charge−E_discharge/eta_discharge; E_discharge dibatasi SOC_min, daya, dan permintaan. Tidak charge dan discharge serentak pada unit sama dalam interval. Kapasitas tidak dihitung sebagai produksi.
- Neraca AC per interval: generation_AC + grid_import + partner_delivered + storage_discharge = load_served + storage_charge + export + curtailment + AC_distribution_loss. Semua nonnegatif; rugi penyimpanan pada ledger DC terpisah. Unserved demand dicatat, bukan energi gratis.

### Fixture edukasi
PV 5 kWp ×4 PSH×0,8 =16 kWh/hari. Wind 1 kW dengan capacity factor ilustratif 20% =4,8 kWh/hari (bukan jaminan). Hidro Q=0,05 m³/s sesudah alokasi ekologis, head 3 m, eta 0,65: 0,956475 kW, 22,9554 kWh/24 jam bila stabil. Pada game hitung interval aktual, bukan membayar pendapatan 24 jam otomatis. Beban harian 20 kWh, PV 16 kWh dan 12 kWh bertepatan dengan beban: offset 18.000 GC; surplus 4 kWh diekspor hanya bila kontrak (4.000 GC), atau disimpan/dibatasi; grid 8 kWh sebelum storage. Jangan menghitung offset dari seluruh pembangkitan.

## 5. Gameplay, peta dan unlock
F1 kit solar pico, pedal dan survei; F2 PV hingga 3 kWp, turbin kecil, pico hidro; F3 hybrid dan lini UMKM; F4–F5 maksimal total 100 kW. F5 memperbaiki integrasi, bukan menaikkan batas skala. Tier spiritual tidak membuka aset langsung; gate fasilitas, lahan, kebutuhan energi dan survei berlaku. Aset DRES tidak mengikuti multiplier U1–U4 file 05: upgrade berupa controller, efisiensi yang tervalidasi, atau penggantian modul dengan penambahan daya terhitung. Tidak ada kenaikan daya gratis.

Pertahankan posisi jalan dan sungai dari DESIGN_SPEC. Lokasi mikrohidro hanya di segmen yang lolos survei; bypass menjaga aliran lingkungan; tidak semua lahan memiliki head layak. Pemain boleh menggunakan PV atau mitra jika angin/hidro tidak cocok. Sampah sungai dari DLE dapat menyumbat intake; cleanup memindahkan lot sampah existing dan memulihkan operasi, bukan membuat listrik tambahan dari sampah itu. Kincir tetap dekorasi bila tanpa generator atau sumber layak. Cuaca menentukan output, bukan animasi. Satu sungai shared memiliki anggaran debit kota; jangan mengalokasikan Q yang sama untuk beberapa pengambilan bersamaan. Untuk MVP gunakan fixture privat, jangan klaim dampak global ganda.

## 6. Dispatch dan God
Prioritas default: beban keselamatan (kontrol emisi, IPAL) → beban produksi/kebun → charge storage surplus → ekspor sesuai kontrak → curtail. Defisit ditutup grid/mitra atau pause mesin aman; jangan melewati interlock. Pemain dapat melihat produksi, penggunaan, SOC, impor, ekspor, curtailment, biaya dan porsi listrik terbarukan. Penghematan bukan pemasukan kas. Sumber energi diberi tag `solar`, `wind`, `hydro`, `ambient_heat`, `waste_origin`, `human`, `grid`, `research`; storage dan transfer mempertahankan proporsi provenance. Tidak boleh menyebut semua listrik sebagai waste-origin setelah masuk microgrid.

God Gate G02–G11 file 06 tetap. DRES memperkuat BHI lewat indikator dampak yang terukur dan mengurangi impor, tetapi tidak menggantikan minimal listrik net dari sampah atau syarat pengelolaan residu. Usulan badge tambahan untuk kemandirian energi bukan syarat wajib God; pemain lokasi tanpa angin atau hidro tetap dapat lulus. Jangan memberi poin berdasarkan produksi bruto, pembelian aset atau listrik yang dibuang. Listrik solar/hidro tidak menghapus emisi aktual. Biogas dan WtE tetap katalog 06 (tidak dibuat ulang). Jejak karbon hanya ditampilkan jika faktor emisi sumber dan baseline tervalidasi; tanpa itu tampilkan kWh impor dihindari, bukan klaim CO2.

## 7. Misi dan lencana tambahan [U]

Semua hadiah sekali per akun, GC dari hibah terbatas; badge tidak membayar hadiah tambahan untuk kondisi yang sama. Koin bukan XP God. Kondisi berbasis ledger settled, bukan klik. Nama dan ID tidak menggantikan misi lama.

| Misi ID | Nama | F | Kondisi | GC | Badge ID / nama |
|---|---|---:|---|---:|---|
| DRQ-01 | Kenali Matahari | 1 | Survei PV valid satu kali | 1000 | DRB-01 Solar Scout |
| DRQ-02 | Cahaya Pertama | 1 | 0,1 kWh PV dipakai | 1500 | DRB-02 Sun Spark |
| DRQ-03 | Membaca Angin | 1 | 7 snapshot angin berbeda hari | 2000 | DRB-03 Wind Scout |
| DRQ-04 | Angin Bekerja | 2 | 1 kWh angin dipakai | 5000 | DRB-04 Wind Keeper |
| DRQ-05 | Sungai Hidup | 2 | Survei head/debit valid; bypass disetujui | 5000 | DRB-05 River Surveyor |
| DRQ-06 | Air Menjadi Listrik | 2 | 1 kWh hidro dipakai tanpa pelanggaran debit | 5000 | DRB-06 Water Power |
| DRQ-07 | Intake Bersih | 2 | 5 cleanup DLE lot unik yang memulihkan intake | 3000 | DRB-07 Flow Guardian |
| DRQ-08 | Simpan Surya | 2 | 1 kWh PV keluar storage ke beban | 4000 | DRB-08 Energy Saver |
| DRQ-09 | Pabrik Hemat | 2 | 10 kWh impor dihindari berdasarkan beban served | 8000 | DRB-09 Efficient Workshop |
| DRQ-10 | Hybrid Harmony | 3 | 2 sumber terbarukan berbeda, masing-masing 5 kWh dipakai | 10000 | DRB-10 Hybrid Builder |
| DRQ-11 | Panas Kedua | 3 | 0,05 kWh TEG dari panas tercatat dipakai | 3000 | DRB-11 Heat Recovery |
| DRQ-12 | Sains Kecil | 2 | 3 eksperimen tervalidasi dengan neraca energi | 2000 | DRB-12 Gaia Scientist |
| DRQ-13 | Microgrid Aman | 3 | 7 hari aktif tanpa overload atau interlock bypass | 10000 | DRB-13 Safe Grid |
| DRQ-14 | Energi Tetangga | 2 | 10 kWh mitra terbarukan diterima dan dipakai | 7000 | DRB-14 Community Energy |
| DRQ-15 | Mandiri Energi | 3 | 14 hari, ≥10 aktif, ≥50 kWh beban served, ≥80% terbarukan dan ≥95% demand served | 25000 | DRB-15 Energy Independent |
| DRQ-16 | Sungai Tetap Hidup | 3 | 14 hari, ≥10 aktif, ≥5 kWh hidro dipakai; aliran ekologis terpenuhi seluruh interval | 15000 | DRB-16 Living River |
| DRQ-17 | Zero Waste Microgrid | 4 | God gate lulus dan ≥80% listrik terbarukan pada window yang sama; ≥95% demand served | 50000 | DRB-17 Gaia Microgrid |

Alternatif DRQ-10 dan DRQ-15 dapat memakai alokasi mitra berprovenance; tidak harus membeli pembangkit. Untuk DRQ-09, baseline adalah impor yang benar-benar akan memenuhi beban tersebut dengan grid tersedia, bukan permintaan fiktif. Misi energi tidak menambah sampah atau XP lingkungan otomatis. Lokasi tanpa hidro tidak dipaksa menyelesaikan semua badge.

## 8. Implementasi dan QA
Reuse `machine_catalog`, `energy_batches`, `energy_meter_events`, `energy_allocations` file 05–06. Tambah `renewable_site_profiles(city_id, plot_id, resource, version, valid_from, head_net_mm, flow_ml_s, ecological_flow_ml_s, wind_profile_id, shading_bp)`, `weather_hourly_fixture`, `dres_asset_specs`, `storage_state`, `grid_contracts`, `energy_dispatch_receipts`. Gunakan integer Wh, W, GC dan basis points; carry remainder untuk output kecil, bukan pembulatan ke atas setiap aksi. Unique receipt per interval/aset/versi; transaction lock pada SOC, saldo, meter, alokasi debit dan kuota ekspor. Ledger provenance tidak boleh negatif. Snapshot tidak perlu menyimpan semua jam historis di klien. RLS/ownership sesuai file 04. Lazy Tick maksimal offline 8 jam; cuaca per jam deterministik dari seed kota dan tanggal server; segmentasi interval saat kondisi berubah. Tidak perlu simulasi fluida, aerodinamika atau LLM realtime.

Acceptance tests:
1. PV malam nol; awan menurunkan output. 2. Wind di bawah cut-in dan di atas cut-out nol. 3. VAWT tidak selalu unggul. 4. Debit ekologis tidak dilanggar. 5. Head nol menghasilkan nol pada rute head. 6. Hidrokinetik menggunakan model arus terpisah. 7. Dua pemain tidak memakai debit yang sama. 8. Intake tersumbat pause. 9. Tidak ada energi gratis dari pompa loop. 10. TEG mengambil panas tercatat sekali. 11. Storage tidak menghasilkan Wh. 12. Charge/discharge bersamaan ditolak. 13. Ekspor dan offset tidak ganda. 14. Grid import bukan energi renewable. 15. PV-only gagal God G02. 16. Waste-origin tetap terpisah setelah storage. 17. Batas agregat 100 kW berlaku untuk upgrade dan sewa. 18. Alias tidak menduplikasi aset. 19. Display-only tidak dapat dijalankan. 20. Safety load tetap diprioritaskan. 21. Dua tab settlement tidak menggandakan saldo. 22. Offline >8 jam tidak mencetak pendapatan ekstra. 23. Misi dan badge hanya sekali. 24. Tidak ada pendapatan tanpa kontrak ekspor. 25. Simulasi 90 hari untuk kota cerah, berangin, tanpa hidro, banjir, musim kering, dan pemain modal kecil; ukur ROI, kas buntu, porsi energi, BHI, distribusi tier, serta dominasi teknologi.

## 9. Handoff
File 07 memperluas file 01–06 dan GAME_SPEC v0.8; tidak mengubah repository. Sebelum aktivasi: mapping alias, aturan beban mesin, kurva daya, footprint, kebutuhan jaringan, biaya dan data cuaca/hidro. Parameter belum diverifikasi pemasok, belum diuji 90 hari, dan tidak boleh dipakai sebagai panduan desain instalasi nyata. Validasi katalog ID dan jumlah baris adalah pemeriksaan struktural saja. Sumber rujukan teknis untuk tahap verifikasi: [Global Solar Atlas](https://globalsolaratlas.info/), [Global Wind Atlas](https://globalwindatlas.info/), [US DOE small wind guidebook](https://windexchange.energy.gov/small-wind-guidebook), [US DOE microhydropower](https://www.energy.gov/energysaver/microhydropower-systems). Tautan adalah referensi lanjutan, bukan bukti verifikasi harga.
