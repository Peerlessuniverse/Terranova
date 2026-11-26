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
