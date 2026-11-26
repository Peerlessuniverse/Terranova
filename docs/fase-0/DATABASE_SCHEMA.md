# Skema logis dan hak akses
[R] Kamus desain Postgres untuk review. UUID untuk akun, ID kecil stabil untuk katalog, timestamptz UTC, bigint untuk gram/subkoin/poin, basis poin 0–10.000 untuk Karma. Semua FK menunjuk baris induk; transaksi lama mempertahankan versi katalog. CHECK nilai nonnegatif pada saldo/stok, kuantitas positif pada niat dan batas overflow pada perkalian. Tidak ada DDL dalam paket.

| Entitas | Kunci, relasi dan data minimum | Jalur akses / indeks |
|---|---|---|
| profiles | PK user_id → auth; nama karakter dinormalisasi unik, kelompok usia, gender privat, status persetujuan bila diperlukan | Profil privat milik sendiri. Proyeksi publik hanya nama karakter/kota. Kontak di Auth. |
| cities, districts | Kode wilayah berversi, PK kota, distrik FK kota, unik (kota,kode) | Master tervalidasi terbit dapat dibaca. Distrik logis tanpa lokasi presisi. |
| player_state | PK user; FK kota/musim, koin, tier, poin, Karma, cursor, versi, jumlah reinkarnasi, kapasitas gudang | Lock baris PK. Indeks (musim,cursor) untuk finalisasi terbatas pada operasi terbuka. |
| player_machines | PK mesin, FK user/katalog/resep, level, kondisi, aktif, sisa produksi pecahan | Indeks (user,id); status blueprint persisten pada achievements. |
| material_catalog, machine_catalog, production_recipes | (kode,versi); daftar input/output, jumlah gram dan kWh terpisah, kemurnian minimum, kapasitas, opex, waktu efektif | Hanya versi terbit dibaca. Publikasi memvalidasi seluruh koefisien dan neraca. |
| inventory, lots | (user,lot,material), gram tersedia/terpesan; lot memiliki asal kontrak, musim, hak kredit tersisa, rujukan batch | Indeks (user,material,lot). Ringkas lot kompatibel tanpa menghidupkan kembali kredit. |
| contracts | PK kontrak, FK musim/kota/distrik, profil dan kuota gram, sisa, reservasi dan kedaluwarsa | Indeks (kota,musim,status); reservasi berakhir dikembalikan sekali. |
| market_prices | (kota,produk,periode,versi), harga dasar, fluktuasi, demand, terjual | Lock kuota transaksi per produk/slot; validasi terjual ≤ demand. |
| game_transactions | PK event, FK user/receipt/musim/aturan, waktu efektif, debit/kredit bertipe, delta massa asal/pembantu, kategori terminal, referensi lot | Immutable; indeks (musim,kota,id), (user,waktu,id). Koreksi lewat entri kompensasi. |
| action_receipts | PK (user,key), hash niat, status, versi dan hasil ringkas, waktu | Deduplikasi atomik. Receipt online [U] 30 hari, setelah itu tombstone ekonomi sampai musim disegel; niat yang melewati usia berlaku ditolak. |
| missions, player_missions | Definisi berversi; penugasan unik (user,misi,periode), progres, saat klaim | Baca milik sendiri; hadiah dan status klaim satu transaksi. |
| seasons, player_contributions | PK musim, mulai/akhir/status; unik (musim,kota,user), gram sah, B3 aman, landfill, emisi, ranking | Indeks (musim,kota,kontribusi,user); agregasi oleh worker, hasil tertutup immutable. |
| global_snapshots, applied_events | Unik (musim,cakupan,kode_wilayah,versi), total penyusun, waktu; event terapan unik (konsumen,event) | Snapshot terbit publik. Deduplikasi dan subtotal atomik. Cakupan global memakai kode eksplisit. |
| achievements, story_progress | Prestasi unik (user,kode,lingkup); cerita PK user, onboarding_version, onboarding_step, intro_seen_at, tutorial_completed_at, bab; kota di state | Unlock lintas musim terpisah dari reward musiman. Simpan hadiah dan replay cerita terpisah. |
| game_config, education_sources | Versi aturan immutable + berlaku sejak; fakta unik (id,versi) dengan atribut §17.3, status, editor, jejak verifikasi | Publik hanya snapshot approved; admin menyunting draft. Resep/fakta lama dapat direproduksi. |
| reports, cosmetic_grants | ID laporan, target, alasan preset dan status; entitlement unik (penerbit,referensi,kosmetik) | Hanya moderator/admin terkait; kosmetik tidak memengaruhi mesin. Ditambahkan saat fasenya. |

## Matriks otorisasi
| Pelaku | Baca | Tulis |
|---|---|---|
| Tamu | Landing, cerita, fakta dan master terbit | Tidak ada operasi ekonomi |
| Pemain A | State, receipt, ledger, misi dan progres milik A; snapshot publik tersanitasi termasuk visit B | Hanya RPC niat berizin untuk A; tidak dapat menentukan user_id sumber |
| Pemain B | Proyeksi nama/kota dan ringkasan pabrik yang diizinkan | Tidak dapat mengubah pabrik A, harga, kontribusi atau profil privat |
| Worker | Ledger dan konfigurasi yang dibutuhkan | Subtotal, snapshot, finalisasi dan receipt hadiah; peran khusus per pekerjaan |
| Editor/moderator | Draft/provenance atau antrean laporan sesuai peran | Publikasi konten atau resolusi laporan tercatat; tidak mendapat izin saldo |

Terapkan RLS default tolak, cabut DML tabel dari anon/authenticated, batasi EXECUTE per fungsi. Fungsi hak tinggi hanya di schema privat, search_path kosong, nama objek berkualifikasi, cek auth.uid() dan kepemilikan eksplisit. Service key hanya di lingkungan server terbatas. View publik memakai proyeksi kolom eksplisit dan hak/RLS yang diuji sebagai anon/A/B. Riwayat dijelajahi via cursor (waktu,id), 25 item [U]; state client tidak menyimpan ledger lengkap. Snapshot kunjungan publik terpisah dari snapshot privat. Arsip ledger setelah rekonsiliasi dan jendela sengketa disepakati; umur simpan atribut pribadi, penghapusan akun dan arsip Hall of Eternity menunggu review. Backup terenkripsi, akses terbatas, restore staging dan bandingkan agregat sebelum rilis.

## Penambahan Kebun Gaia

Usulan D14 menambah satu state petak privat per pemain (`garden_plots`: user_id, varietas, status, sisa_detik, dipupuk, cursor, versi). Katalog, inventaris, misi dan hak varietas memakai entitas yang sudah ada; lihat KEBUN_GAIA.md.

## Penambahan DWE, DLE & Visual (v0.8 / DESIGN_SPEC v1.3)
Tabel usulan berikut mengikuti konvensi yang sama (UUID akun, bigint gram/subkoin, timestamptz UTC, CHECK nonnegatif, RLS default tolak). Tidak ada DDL produksi pada Fase 0.

| Entitas | Kunci, relasi dan data minimum | Jalur akses / indeks |
|---|---|---|
| waste_source_templates | PK `(kode, versi)`; tipe (`permukiman`/`pasar`/`komersial`/`industri`/`sungai`/`tpa`), profil komposisi (jumlah=100%), laju timbulan dasar, kontaminasi, syarat unlock | Master terbit read-only; validasi komposisi saat publikasi. |
| waste_source_state | PK `(scope, city_id, node_id)`; FK template; stok gram per fraksi, reservasi aktif gram, kapasitas gram, cursor UTC, versi | Lock urut `node_id`; fase 1 memakai scope privat deterministik, fase kota memakai scope kota bersama. |
| waste_origin_ledger | PK `origin_id`; sumber (node/kontrak/event), musim, gram awal, hak kredit tersisa, kategori terminal | Immutable; mencegah kredit ganda pada transfer, olah ulang, atau returned materials. |
| vehicles | PK `vehicle_id`; FK user, tipe (`gerobak`/`roda_tiga`/`pickup`/`truk`), kapasitas gram, biaya/km, kecepatan, status (`idle`/`in_transit`) | Indeks `(user_id, status)`; cek unik satu job aktif per kendaraan. |
| collection_jobs | PK `job_id`; FK user, node, vehicle, receipt; status (`offered`/`reserved`/`in_transit`/`arrived`/`received`/`cancelled`/`expired`), kargo gram per fraksi, biaya/imbalan, `expires_at`, `arrives_at` | Indeks `(user_id, status)`, `(node_id, status)`; TTL hanya melepas status `reserved`, bukan `in_transit`. |
| source_events | PK `event_id`; FK city/musim; tipe (`festival`/`panen_raya`/`banjir`/`kampanye`), pengganda laju/kontaminasi, rentang UTC, versi | Dibaca saat settlement node; transfer banjir tercatat di ledger tanpa menambah massa eksternal baru. |
| returned_material_cohorts | PK `cohort_id`; FK city/produk; gram terbit, umur pakai, tanggal kembali, status | Fase lanjutan; tidak menambah kredit musim yang sama secara otomatis. |
| environmental_event_templates | PK `(kode, versi)`; jenis (`npc_litter_river`/`vegetable_spill`/lanjutan), bobot, fraksi valid (non-B3), rentang gram, TTL detik | Master terbit read-only. |
| environmental_events | PK `event_id`; `scope`, `source_node`, `target_node`, `slot_utc`, `mass_g` per fraksi, `anchor_id`, `status` (`available`/`collected`/`expired`), `expires_at`, `claimed_by`, `receipt_id` | Unik `(scope, slot_utc, anchor_id)`; indeks `(scope, status, expires_at)`; klaim atomik sekali saja. |
| environmental_event_cursor | PK `scope`; `last_slot_utc`, `daily_utc_date`, `daily_count`, `daily_bonus_g`, `tutorial_guaranteed_used`, versi | Lock baris `scope` saat evaluasi slot & cek cap harian (6 insiden / 12 kg UTC). |
| avatar_config, cosmetic_catalog | `avatar_config` PK `user_id` (gender privat di profiles, slot ID rambut/pakaian/topi/kacamata/tas/aksesori, palette, versi); `cosmetic_catalog` PK `item_id` (slot, allowlist aset, entitlement) | Validasi allowlist ID di server; menolak URL aset dari pengguna; nol efek ekonomi. |
| layout_template, player_placements | `layout_template` berversi (grid, anchor permanen gerbang/jalan/sungai); `player_placements` (opsional jika pembangunan bebas disetujui: `object_id`, x/y, footprint, versi) | Fase 1 cukup template lokal deterministik; tidak menyimpan koordinat avatar per frame. |

---

## Sinkronisasi Feature Freeze v1.0 (27 November 2026)

> Sumber: `docs/TERRA_NOVA_FEATURE_FREEZE/docs/fase-0/DATABASE_SCHEMA_SYNC_v1.0.md` (digabung tanpa menimpa histori Fase 0).

# Database schema — proposed logical model
Reconcile actual schema and existing IDs before migration; no DDL executed. Preserve accounts/history and back up SQLite. Tables below logical names only.

| Entity | Key and invariant |
|---|---|
| catalog_material / catalog_machine / catalog_alias | stable IDs; alias FK canonical; price version, unit, availability |
| recipe / recipe_io | validated inputs outputs gram/Wh and external flows, version |
| player / wallet_ledger / inventory_lot | unique owner, integer nonnegative balance, source provenance |
| mass_event / energy_event | unique event, source/destination, conservation, allocation not duplicated |
| source_node / spawn_event / transport_contract | deterministic slot key, reservation, expiry/backlog, idempotent |
| machine_instance / placement / lease | owner, canonical ID, condition, footprint, status |
| market_quote / order / listing | version, expires_at, qty/price, atomic settlement |
| crop_type / plot / food_inventory / vitality | CR IDs, mature_at, harvest once, consume once |
| mission_def / achievement / grant / journal | unique player+grant_key, append history, no replay reward |
| energy_meter / battery_bucket | source provenance, Wh, losses, max capacity |
| config_version / admin_audit / event_schedule | immutable published version, actor, reason |
| media_manifest / sponsor_campaign | license, bytes, expiry, labels |
| public_profile / card_verify / ranking_snapshot | visibility, pseudonym, season, verified metric; no private fields |
| payment_order / payment_event | beta only, unique provider txn, exact SKU/amount, credit once |
| candidate_eval / wealth_snapshot | evidence version, provisional only, no final selector |
| feedback | category, consent, moderation, retention |

Unique request scope player+idempotency key, request fingerprint; retries with different payload rejected. Atomic balances, no cross-account access. Source-node mass debit before claim. Migration dry run copy, count/ID/FK/balance checks, rollback backup; old saves not eligible online. Profile deletion/retention and child safeguards before beta; no raw email in rank or QR. Secrets outside repo.
