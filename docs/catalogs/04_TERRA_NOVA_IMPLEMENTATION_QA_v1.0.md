# TERRA NOVA — DWE Implementation Contract & QA v1.0
26 November 2026 | Proposed implementation, no live repo/DB changes.

## 1. Integration order
Read existing GAME_SPEC v0.8, DESIGN_SPEC v1.3 and current repository code/schema first. This package does not replace approved decisions. Diff existing starter, currency, points, recipe capacities, stage, Karma, ZWM/BHI, DLE, garden, mission and season systems; flag conflicts for owner review. Keep existing endpoints and table names where compatible; below names are logical entities, not migration commands. Implement behind feature flags. Do not delete old data, rewrite migrations, expose keys, or deploy production without explicit approval.

### Phase 0: validation before implementation
- Import Markdown tables as typed versioned seeds (explicit heading + column matching; no arbitrary Markdown execution). Validate IDs, uniqueness, prices integer nonnegative, units, yields 0–100, output foreign keys, all metric references, dependencies and feature flags. Percent converted into rational integer basis points; 0.03% = 3 bp. Parse condition text into manually reviewed typed AST, never eval. Reject unsupported condition syntax, unknown metric, unknown family, missing recipe, incompatible unit. Stage labels F1–F5 map to ordinal 1–5.
- Catalogue includes 158 kg raw entries, 5 unit-specific entries, 119 products; 100 missions, 92 badges. Disposal fees separate from price. Seed all entries but only enable tested routes. Default active fixture F1 only; advanced products visible in educational encyclopedia even when gameplay disabled.
- Price rows originally based on previous indicative conversation, all treated SIM_ESTIMATE. No claim of external validation or actual transaction. Preserve original source metadata if later researched. Rare metals, electronics, specialty contracts, thermal, food/feed, and hazardous routes require additional QA and partner gates.
- Resolve circular dependencies: e.g. F2 storage/scale must be purchasable or rentable at F1; F3 processing access available through F2 introductory partner before F3 gate; F4 control access rentable before F4 gate. F1 manual sorting + verified direct sale must satisfy recovery via NPC terminal receipt, not merely transfer. Industrial orders for F4 available at F3. Never require story multiplayer mission to unlock private prototype. For F2 compost sale, accessible buyer and small minimum lot required. If not affordable in simulation, adjust access, not hidden grants.

## 2. Logical data model
All IDs UUID except immutable catalog slugs; quantities bigint grams, GC bigint; dates UTC, period keys Asia/Jakarta. Money nonnegative balances; append-only events. Use existing schema equivalents if already present.

| Entity | Required fields / constraints |
|---|---|
| catalog_versions | version, effective_at, status, source_type, checksum; immutable published |
| materials | id, version, family, fraction, unit, density_g_per_l, mass_g_per_pcs, hazard_class, route_policy, enabled, source_confidence |
| material_prices | material_id, version, market_stage, base_gc_per_unit, provenance, observed_at nullable; unique key |
| recipes | id, version, facility_id, gate, duration_s, input array, output array, residue/disposition array, opex, enabled, safety_policy |
| price_snapshots | city_id, market_day, item_id, tier, version, index_gc, bid_gc, ask_gc, grade rules, demand_qty; unique key |
| buyers | city_id, tier, demand_family_cap, budget_gc, min_lot, required_grade, buyer_type |
| source_nodes | city_id, template_id, stock_g, cap_g, last_settled_at, version |
| origin_lots | origin_id, node_id, item_id, original_g, generated_at, grade, provenance_scope |
| inventory_lots | player_id, item_id, qty_g, native_qty, grade, origin allocation, reserved_g, location |
| collection_jobs | player_id, node_id, reservation_id, qty_g, contract_fee, vehicle, state, expires_at, receipt_id |
| dle_events | event_id, origin_id, event_type, qty_g, location_slot, state, expires_at, claimant_id |
| production_jobs | player_id, recipe_id/version, inputs_reserved, cost_reserved, start_at, end_at, cursor, state, result_receipt_id |
| market_orders | order_id, player_id, buyer_id, lot_allocations, locked_quote, fees, expires_at, state, settlement_id |
| disposition_receipts | receipt_id, origin allocations, actor, route, verified terminal status, recovered_g, safe_treated_g, landfill_g, emission_g, process_sink_g |
| wallet_ledger | entry_id, player_id, signed_gc, category, reference_type/id, idempotency_key, created_at; append only; unique key |
| player_state | wallet_cached_gc, last_settled_at, stage, tier, karma_bp, lifetime and season pointers, version |
| point_ledger | event_id, origin_id nullable, points_milli, reason, period, reference_id, unique key |
| origin_credit_ledger | origin_id, terminal_receipt_id, credited_g, credit_type; sum <= original mass, transactional lock |
| mission_defs | id, version, class, min_stage, condition_ast, dependency_ids, feature_flag, reward_gc, reward_milli_points, budget_bucket |
| mission_instances | player_id, mission_id, period_key, assigned_at, state, progress_snapshot, claim_key unique |
| badge_defs | id, version, rarity, scope, condition_ast, cosmetic_id |
| player_badges | player_id, badge_id, scope_key, acquired_at, evidence_ref; unique composite |
| metric_rollups | player_id, scope, scope_key, metric, dimension, value_int, updated_at; indexed |
| season_snapshots | season_id, city/global, cutoff, metric_version, BHI/ZWM, eligibility, immutable closure |
| reward_budgets | player_id, period_key, bucket, reserved_gc, granted_gc, reserved_points, granted_points |
| audit_events | actor, action, resource, reason, version, timestamp; redact secrets |

Material quantity in native units and grams must be internally consistent. Liquid mL and energy Wh integer; gas volume has recipe-specific reference conditions. For unit goods count integer and actual lot mass. Catalog product only can lack recipe, must be disabled for crafting until validation. Ancillary seed IDs (hardware, packaging, seed, water) separate non-waste catalog, explicit prices and mass; not counted as diverted waste. Families derive from material metadata; split battery and electronics subfamilies for mission metrics. Mixed metal/glass combined only for base point weight, retain granular categories.

## 3. Atomic settlement & API contracts
Server authoritative; all mutations authenticate player, validate ownership and state/version, use idempotency key; duplicate returns original receipt. Use row locks or optimistic concurrency with retry; no client-supplied price, reward, elapsed time, grade, or completion. RLS restrict private rows; service role only on server. Suggested API capability names, align with actual existing API conventions: GET catalog/prices, GET sources, POST reserve/pickup/deliver, POST sort, POST production/start, POST market/quote/sell, POST disposition, POST dle/claim, POST mission/claim, GET progression/badges, POST settlement. No direct write to wallets/points/inventory from browser.

```text
settle(player, now_server, key):
  begin transaction; lock player and affected inventory/job rows
  if receipt(key): return stored receipt
  dt = clamp(now_server - last_settled_at, 0, 8h)
  settle eligible jobs in chronological order within capped simulation horizon
  consume reservations only once; verify output+remainder mass
  post costs, output lots, disposition, terminal origin credits, points
  update metric rollups; evaluate eligible missions/badges from typed rules
  evaluate tier + God gates, reserve/issue explicit grants once
  advance cursor (discard offline excess per existing Lazy Tick policy)
  store immutable receipt; commit
```
Absolute job end time cannot bypass cap: progress accumulated from eligible active simulated time. Idle cap must not create/deallocate material; timers for real-world expiry use server wall clock and explicit release/overflow events, not simulated progress. For source accrual follow existing source policy; player idle cap cannot be used to reset shared node. DLE expiry transitions to burden exactly once. Background city processing aggregated, no per-NPC timers; snapshots ≤20 KB per base spec. Event retries do not reroll rare seeds or prices. Market orders hold inventory and buyer quota; expiry releases both. Costs prepaid or reserved; settlement validates before debit. Mission claim reserve budget on assignment, release on expiry; story auto grant and claim cannot both pay. Reward grants separate from operating profit. Tier reward keys lifetime `(player,tier,grant_type)`; mission keys use scope as defined, not arbitrary version changes. Badge no money. Season closure uses server cutoff and immutable snapshot; disallow later credit into closed season, preserve audit and history.

## 4. Mission DSL example (not executable source)
```json
{"id":"DA01","scope":"day","minStage":1,"condition":{"op":"gte","metric":"sorted_g","value":5000},"reward":{"gc":300,"pointsMilli":30000},"feature":"sorting"}
```
Allowed operators `gte,lte,eq,gt,lt,and,or`; boolean predicates typed. Field selectors become dimensions, e.g. `recovered_family_g:plastic` becomes metric `recovered_family_g`, dimension `plastic`. Mission conditions are server-defined, not raw expressions accepted from clients. Rules evaluate after transaction or outbox exactly-once, with stale state labelled pending. For season badge/ceremony consume approved snapshot, not client data. For origin credit check terminal beneficial route, do not use production as recovery. Conditions for story dependencies, lifetime vs period, current vs longest streak explicitly encoded.

## 5. QA matrix / acceptance criteria
| Test | Expected result |
|---|---|
| QA01 seed referential integrity | all IDs unique, product refs exist or NONE; no unresolved condition silently enabled |
| QA02 price determinism | same version/day/city returns same quote; daily index max 5% movement (grade change separate) |
| QA03 zero-value material | no positive buy/sell quote; disposition fee explicit |
| QA04 market arbitrage | buy/sell same actor loses spread+fees; aggregation requires real costs and demand |
| QA05 mass balance | all integer gram remainder allocated; no negative stock; kWh excluded from mass |
| QA06 unit conversion | 10 L UCO=9200g; 9L output=8280g; 920g residue |
| QA07 two tabs sale | one settlement; same receipt on retry |
| QA08 concurrent source reserve | combined allocation ≤ available mass |
| QA09 expiry | order releases once; loaded cargo preserved; DLE expired stock moves to burden |
| QA10 offline 72h | processing progress max 8h per existing cap; no reset farming |
| QA11 origin transfer | repeated sale/processing cannot duplicate recovery credit |
| QA12 terminal partner receipt | safe treatment separately labelled, no automatic material recycling |
| QA13 hazardous mixed cargo | block ordinary route; show partner/report; no unsafe instructions |
| QA14 thermal gates | controls + QC required; no untreated emission bypass; no energy double sale |
| QA15 zero cash | rescue job available once/24h, no negative balance, no forced payment |
| QA16 tier promotion | thresholds exact; God fails each missing gate independently |
| QA17 reincarnation | tier reset but no repeated lifetime reward |
| QA18 mission reward race | exactly once; scope caps enforced before assignment |
| QA19 daily/weekly boundary | Jakarta period key consistent, no client clock exploit |
| QA20 badge | evidence validated, no money; season history retained |
| QA21 season cutoff | global private fixture excluded, ceremony only approved snapshot |
| QA22 garden | rare unlock once; growth inputs separate; no waste impact for harvest |
| QA23 DLE | two concurrent claims cannot duplicate origin; roads remain during upgrade |
| QA24 NPC price outlier | specialty materials gated, no accidental household gold spawn |
| QA25 UI | currency labelled virtual; fees, price assumptions, disabled reasons visible |
| QA26 accessibility | keyboard, touch, text alternative, reduced motion; no color-only status |
| QA27 RLS | cross-player inventory and grants denied; admin writes audited |
| QA28 payload | base snapshot ≤20KB; paginated catalog and event aggregation |
| QA29 fallback | city with zero users playable; shared quota not added to private fixture |
| QA30 repeatability | stable seed/version, no migration regrant; rollback tested |
| QA31 margin check | PET example and negative RDF example match ledger exactly |
| QA32 no blocked progression | rental access before gates, optional multiplayer and thermal, no paid requirement |
| QA33 price revision | immutable old quote/receipt; new seed effective date respected |
| QA34 BHI/Karma | approved baseline parity; new proposed metrics disabled unless approved |
| QA35 offboarding | player inactive no accrual beyond cap, no orphan reserved items |

## 6. 90-day balancing experiment (not executed)
Build seeded simulation harness (e.g. 100 agents per scenario, fixed PRNG, per-day snapshots; no browser). Strategies: manual collection, paper/plastic, organic/garden, mixed material, reuse/upcycle, licensed e-waste, integrated with controlled thermal, nonthermal F5. Activity 15/30/60 min/day, idle 8h, churn 10–30%, price shock ±20%, city demand constraints, low-capital player, full storage, rejected grade, late season join, season rollover. Compare no paid purchases. Track GC cash p10/p50/p90, operating profit net of grants, first sale time, stranded days, stage/tier attainment day, kg recovered vs handled, material recovery vs diversion, untreated emissions, Karma, source overflow, market stock, price index, concentration of revenue, mission grant share, double credit violations. Target initial meaningful action <=3 min; at least one viable route from zero cash; no negative mass/cash; zero duplicate rewards; God reachable around day 60–90 for active balanced play, not guaranteed; no single thermal strategy dominates cash+points+impact. Tune rental/access and volume before changing real-scale prices. Require measured evidence before claiming balance. This file is specification only; no 90-day simulation performed.

## 7. Rollout and blockers
1. Review baseline conflicts and approve GC conversion, new cost model, additional stage gates, grant schedule, grade/demand rules, mission points cap, exact Karma/BHI/ZWM definitions, evidence rules, season resets.
2. Import catalog/mission/badge disabled flags; schema migration dry run and seed integrity tests.
3. Enable three source fixture nodes, F1 sorting/direct sales, DLE, garden, starter missions and tier display; verify first sale and rescue.
4. Add F2/F3 partner rental, recipes and buyer demand; then shared city; only enable advanced routes after safety and balance QA. Keep WTE, alchemy, food-grade, regulated paths gated by owner and technical review.
5. Synchronize GAME_SPEC, DESIGN_SPEC, technical design, schema, economy model, test plan, performance budget and changelog; do not silently change previous owner decisions. Use versioned migrations with backup and rollback.
6. Production deploy requires actual tests, regulatory/safety review for educational claims, privacy/age review, accessibility, load test and owner approval.

## 8. Ready-to-copy implementation instruction
Read all four Markdown files in order. Audit current TERRA NOVA repository and baseline specs first. Return a conflict matrix (existing behavior vs proposal vs recommended resolution), seed validation report, feature flag mapping, migration plan and 90-day simulation plan. Do not deploy or modify production DB. Do not treat proposed prices, rewards, thresholds or costs as approved merely because present in these files. Use real rupiah-scale GC nominal simulation without real cash value. Preserve nine tier names, points, God gates, DWE/DLE, Gaia Garden and five physical stages. Implement only owner-approved changes; report unimplemented routes or missing metrics explicitly. No fake real-world environmental claims. Keep server authoritative, Lazy Tick and mass/credit conservation.
