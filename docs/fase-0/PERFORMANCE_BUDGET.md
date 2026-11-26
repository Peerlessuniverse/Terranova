# Anggaran performa dan memori
Semua angka target [U], belum diukur pada aplikasi. Uji Android fisik RAM 2 GB dengan Chrome dan desktop browser umum. Catat model, OS/browser, DPR, suhu, mode baterai, cache dan jaringan. Profil jaringan pembanding [U] 4G terbatas 1,6 Mbps turun/0,75 Mbps naik, RTT 150 ms; ulangi pada Wi-Fi. Pisahkan cold/warm start dan unduhan pembuka dari pabrik.

| Komponen | Target | Cara mengukur dan tindakan bila melampaui |
|---|---|---|
| Shell JS awal | ≤250 KB terkompresi | Network/analisis bundle produksi cold load; pecah rute Kota dan Jurnal, hilangkan dependensi duplikat. |
| Pabrik awal | aset ≤1 MB; total awal game ≤3 MB | Catat transfer sebelum pabrik dapat dimainkan; gambar modular, lazy load fasilitas terkunci. |
| Opening terpisah | ilustrasi 800 KB, musik 400 KB, Opus 350 KB, JSON 10 KB, CSS 20 KB; total 1.580 KB | Fetch pertama hanya panel awal; prefetch satu panel. Tangguhkan audio hingga interaksi. Fallback teks dan audio opsional. |
| Heap JS | sasaran 50–100 MB saat bermain | Profil heap dan retained objects tiap 5 menit, catat heap sesudah GC di lab. Di bawah 50 MB juga lulus. Periksa memori proses, GPU dan gambar terdekode terpisah. |
| Frame | 30 FPS Eco/Standard, 60 Immersive bila mampu | Trace animasi 60 detik pada pabrik dan kota; anggaran frame sekitar 33/17 ms. Ukur dropped frames dan long tasks. |
| Web Vitals | LCP ≤2,5 detik, INP ≤200 ms | Ukur alur buka pabrik dan rangkaian interaksi berulang. Laporkan p75, ukuran sampel dan jaringan. Cocokkan dengan data lapangan saat tersedia. |
| API game dan snapshot | p95 ≤500 ms; snapshot user ≤20 KB terkompresi | Catat durasi ujung-ke-ujung, tunggu lock, waktu DB, ukuran wire. Uji cold start terpisah. |
| Soak | 30 menit, tanpa tren memori naik terus | Siklus pabrik–kota–visit–jurnal–pabrik, background/foreground. Bandingkan baseline pascapemanasan dengan akhir, jumlah listener dan tekstur. |

**Memori terdekode.** Ilustrasi RGBA 1.024×1.024 membutuhkan sekitar 4 MiB sebelum overhead. Dua panel ≈8 MiB; jika DPR dua menggandakan kedua dimensi, kebutuhan buffer dapat menjadi empat kali. Batasi DPR dan resolusi per perangkat, lepaskan tekstur, URL objek, audio dan listener saat unmount. Jangan memuat pabrik berat dan adegan akhir bersamaan. Gunakan grid 2D, culling area tampak, daftar riwayat paginasi. Object pooling atau Canvas/Pixi hanya setelah profiling. Cache PWA hanya aset publik ber-hash. Putus polling, audio dan animasi saat tab tersembunyi.

**Cadence.** Presence opsional 15–30 detik ketika Kota terbuka; BHI/ZWM 1–5 menit; pasar/ranking 5–15 menit. Snapshot cache ber-versi, jitter dan backoff. Batasi 20–50 marker tampak [U], NPC dekoratif lokal, tampilkan label. Visit read-only. Eco mengurangi efek dan NPC, semua mode memakai hasil server yang sama.

**Rencana beban.** Pada staging, ramp 1→20→100 pengguna simultan, 5 menit pemanasan dan 15 menit pengukuran per tingkat. Campuran awal [U] 50% baca snapshot, 25% settlement, 15% jual, 10% visit. Tambahkan gelombang login dan 20 penjual berebut satu SKU. Laporkan p50/p95/p99 per endpoint, error, koneksi, CPU, I/O, lock, antrean agregasi dan biaya per 1.000 aksi. Bandingkan penggunaan terhadap kuota paket aktual [V]. Simpan trace paling lambat. Budget yang gagal menahan pelebaran cohort. Hasil eksperimen ekonomi tidak memberi estimasi kapasitas infrastruktur.

## Penambahan Kebun Gaia

D14 memakai satu kartu petak dan ilustrasi ringan yang dimuat saat dibuka. Target JS, heap dan snapshot tetap tunduk pada anggaran di atas; ukur delta ukuran sebelum mengaktifkan fitur.

## Penambahan DWE, DLE & Visual (v0.8 / DESIGN_SPEC v1.3)
- **Atlas & memori GPU.** Maksimal dua atlas 1024×1024 RGBA (8 MiB decoded sebelum overhead) per scene aktif; target memori tekstur GPU awal ≤16 MiB [U] termasuk render targets. Satu atlas aktif per scene; jangan memuat atlas kota, katalog penuh, atau ilustrasi opening bersamaan dengan pabrik. Batasi DPR Eco maksimal 1 [U]; nearest-neighbor untuk pixel art.
- **DWE (node & peta).** Batasi 20–50 node kota pada fase beta dengan daftar terpaginasi dan snapshot cache ber-versi; jangan membuat satu baris per kantong atau timer per rumah. Update global dari agregat worker, bukan hot-row write per aksi.
- **DLE (jalan & sungai hidup).** Usulan cap visual simultan: maksimal 4 NPC pejalan kaki + 2 kendaraan + 3 insiden aktif. Gunakan object pooling, fixed waypoint, viewport culling, depth sorting berbasis anchor kaki, dan **satu scheduler renderer** (tanpa timer terpisah per sprite dan tanpa physics engine). Hentikan animasi, audio, dan polling saat `document.hidden` (tab tersembunyi). Mode `prefers-reduced-motion` menampilkan perubahan state tanpa animasi lempar/berjalan. Tidak ada traffic server per frame.
- **Aset referensi.** Gambar di `docs/fase-0/references/` hanya untuk dokumentasi pengembang dan dilarang masuk ke bundle publik/runtime. Seluruh angka cap di atas adalah target profiling [U] dan wajib diukur pada Android 2 GB + desktop sebelum rilis.
