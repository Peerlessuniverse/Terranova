# TERRA NOVA — Dynamic Waste Economy Engine v1.0
**Chapter I — The Calling of Gaia** | 26 November 2026 | Proposed extension to GAME_SPEC v0.8 and DESIGN_SPEC v1.3

## 1. Contract and priority
This package proposes new economy parameters, not an approval or direct edit of existing code. Preserve existing onboarding, DWE/DLE, five physical stages, nine spiritual tiers, Karma, seasonal ending, Gaia Garden, no pay-to-win, server authority and Lazy Tick cap 8h. If a parameter conflicts, report it for owner approval; do not silently overwrite. Read `02_TERRA_NOVA_DWE_MATERIAL_DATABASE_v1.0.md`, `03_TERRA_NOVA_PROGRESSION_MISSIONS_BADGES_v1.0.md`, `04_TERRA_NOVA_IMPLEMENTATION_QA_v1.0.md`. All money GC integer; 1 GC represents Rp1 for learning only; no cash redemption, token, speculation or real-world profit promise. Prices are simulation estimates, not verified live. Default starter 10,000 GC, 100 m², cart, warehouse, manual sorting, Awaken, Karma 0 (existing placeholder). Tutorial first meaningful action ≤3 min. Replay opening gives no rewards.

## 2. Economic loop
Source accrual → reservation → cargo → receipt → sorting → storage → direct sale OR reuse/repair OR processing → QC → industrial offtake → disposition → settled impact. Prevention reduces future source generation only, never creates fictitious diverted kg. Separate all fees, revenue, operating costs, CAPEX and reward subsidy. No perpetual buy/sell spread: buy from NPC at ask, sell at bid; tiers in catalog represent different actors, not simultaneous quotes to same actor. To access next tier quote require actual aggregation, quality check, minimum order and delivery fee. Raw inputs always sourced via documented contracts or DLE; optional market purchases limited to demand and stock. No cash from self-trading.

## 3. Price engine (daily deterministic, local timezone Asia/Jakarta; server time UTC)
For material m, city c, market tier t:
```
base = catalog[m,t]
D = clamp(0.70,1.30, 1 + 0.20*(unfilled_orders_g - available_g)/max(unfilled_orders_g+available_g,1))
R = city_factor[c]             # default 1, range .85–1.15
Q = grade_factor               # A 1.05, B 1, C .70; reject if below specification
S = seasonal_factor            # .90–1.10, predefined calendar
E = event_factor               # .90–1.10, approved exogenous shock
J = seeded_noise               # .98–1.02, hash(city,material,date,seed_version)
target = base * D * R * S * E * J
index = clamp(.65*base,1.45*base, clamp(.95*previous,1.05*previous,.75*previous+.25*target))
mid = round(index*Q)
bid = floor(mid*.96); ask = ceil(mid*1.04)
```
At initial price previous=base. Never multiply zero into a tradable value. Grade A contamination ≤2%; B ≤10%; C ≤25%; buyer-specific specs override. Apply mass discount for moisture by dry basis only where contract uses it; do not double discount contamination through weight and Q for same cause. Prices lock at order reservation (15 min), qty capped by buyer demand, settlement only upon receipt and QC. Material out of spec can be rejected, returned or regraded via explicit consent. Seller price per unit must be shown with grade, fees and valid time. NPC quote fee 2% of sale (ceil); no bid/ask for hazardous handling service (fixed tariff). No real-time external dependency. Daily market stock/demand generated deterministically with capacity ceilings and historical snapshots; no fabricated price history labelled real. City demand initialized by population bucket, not exact geolocation. Offline market price changes do not retroactively change locked contracts. Price override requires admin approval, version, effective_at and audit.

### Demand, grades and transport
| Buyer | Minimum lot | demand baseline per player fixture/day | fee per delivery | gate |
|---|---:|---:|---:|---|
| Bank sampah | 1 kg | 100 kg | 0 (walk-in) | F1 |
| Pengepul | 5 kg | 250 kg | 1000 GC | F1 |
| Bandar | 50 kg | 1000 kg | 10000 GC | F2 |
| Industrial recycler | 100 kg | 2000 kg | 25000 GC | F3 |
| Industrial offtake | 500 kg | 10000 kg | 75000 GC | F4 |
| Licensed partner | 1 kg | 500 kg | 5000 GC (waived first tutorial) | verified partner |
Quota applies per commodity family, not each SKU; phase city shared quota replaces private quota, never adds it. Specialty metal/e-waste/precious lot cap 1 kg/day F3; 10 kg/day F4, separate rare source availability. Price/demand changes must not be driven solely by a single player. No auto replenishment of buyers during same day. Buyer NPC budgets and material sinks recorded. A rejected order returns reserved stock once.

## 4. Source generation and collection
MVP fixture: three source nodes, households, market, commercial; advanced city adds school, office, restaurant, retail, farm, construction, factory, repair shop, electronics depot, river and municipal partner. Seed values below are per node per game day, not statistics. For existing six-fraktion schema use organic, plastic, paper, metal_glass, residue, hazardous with category metadata; historical 5-fraktion distribution splits last 15% into residue 14%, hazardous 1% as proposal. Never use generic household RNG to spawn precious metals or regulated waste. Accrual capped by node capacity; overflow becomes city unmanaged burden with provenance, not player inventory. DLE draws from same source stock; cleanup moves material, no new mass. City supply ceilings scale on active player count as in v0.8. Initial solo private fixtures excluded from shared global stats until migrated.

| Source | kg/day | capacity kg | mixture % | compensation GC/kg (service paid to player) |
|---|---:|---:|---|---:|
| Household | 30 | 90 | organic 55/plastic 20/paper 12/metal_glass 3/residue 10 | 150 |
| Market | 60 | 180 | organic 75/plastic 10/paper 10/residue 5 | 200 |
| Commercial | 45 | 135 | paper 40/plastic 30/organic 15/metal_glass 5/residue 10 | 100 |
| School/office | 40 | 120 | paper 55/plastic 20/organic 15/residue 10 | 100 |
| Restaurant | 80 | 240 | organic 85/plastic 8/paper 5/residue 2 | 200 |
| Retail | 100 | 300 | paper 60/plastic 30/residue 10 | 100 |
| Farm | 150 | 450 | organic 95/plastic 5 | 0 |
| Construction | 300 | 900 | mineral 85/metal 10/wood 5 | 150 |
| Factory | 250 | 750 | plastic 30/paper 30/metal 30/residue 10 | 0 |
| Repair shop | 20 | 60 | metal 50/rubber 40/plastic 10 | 0 |
| Electronics depot | 10 | 30 | EW 100, licensed path | 0 |
| River litter | 15 | 45 | plastic 50/organic 25/paper 10/residue 15 | 200 |
| Municipal partner | 500 | 1500 | explicit audit lot incl regulated fraction | 250 |
Service fee only if contract specifies; source cannot both pay service and sell same material unless explicitly priced net; mission reward not counted as commodity revenue. Reserve available grams atomically, 15 min expiry until pickup; loaded cargo expiry does not destroy mass. Free tutorial supply capped 5 kg once. Reject hazardous mixed cargo at ordinary source; escalation to partner.

| Vehicle | Capacity kg | purchase GC | per trip GC | range km | stage |
|---|---:|---:|---:|---:|---|
| Cart | 25 | starter | 0 | 1 | F1 |
| Cargo bike | 60 | 1500000 | 1000 | 5 | F2 |
| Motor cart | 150 | 12000000 | 6000 | 15 | F2 |
| Pickup | 1000 | 140000000 | 45000 | 40 | F3 |
| Truck | 5000 | 450000000 | 150000 | 100 | F4 |
Use service rental alternative: 120 GC/kg (min 1000) F2, 150 GC/kg (min 15000) F3; assisted progression avoids mandatory vehicle purchase. Distances are game abstractions. Route cost includes trip cost + distance*vehicle rate (cart 0, bike 50, motor 300, pickup 1500, truck 3500 GC/km); quote before dispatch.

## 5. Facilities and recipe defaults
New cost/throughput proposals replace neither existing spec nor art. Real-scale CAPEX deliberately separated from accessible shared-machine rental: players need not own every machine to progress. Production only consumes reserved inputs; use pooled partner processing fee instead of machine opex if rented. No automatic upgrade on tier. F1 yard 100m², F2 bank sampah, F3 industry, F4 integrated park, F5 civilization. Water/energy constraints abstract and recorded. Values per kg INPUT unless noted; time = ceil(input_g / rated_g_per_hour *3600). Fixed maintenance 0.1% CAPEX/day only when machine active; rental fee = 1.25× direct variable cost, plus delivery; partner slot quota. For F1 manual sorting free first 5 kg, thereafter 50 GC/kg. Staff and costs no negative cash; reserve full cost before job. Tutorial and low cost routes always accessible.

| Facility | Stage | CAPEX GC | kg/h | variable GC/kg | rental available |
|---|---|---:|---:|---:|---|
| Manual sort | F1 | starter | 20 | 50 | yes |
| Compost bin | F1 | 5000 | 2 | 120 | yes |
| Wash/sort station | F2 | 2500000 | 100 | 400 | yes |
| Baler | F2 | 25000000 | 150 | 180 | yes |
| BSF module | F2 | 5000000 | 10 | 250 | yes |
| Plastic shred/wash | F3 | 85000000 | 100 | 1200 | yes |
| Pellet line | F3 | 250000000 | 100 | 1800 | yes |
| Paper pulp line | F3 | 350000000 | 150 | 1500 | yes |
| Glass crusher | F3 | 65000000 | 120 | 250 | yes |
| Textile fiber | F3 | 120000000 | 80 | 800 | yes |
| Rubber crumb | F3 | 180000000 | 80 | 1500 | yes |
| Wood chip/mill | F3 | 45000000 | 120 | 300 | yes |
| Food/feed approved partner | F3 | 0 | 50 | 1000 | partner only |
| Metal separation | F3 | 95000000 | 150 | 500 | yes |
| Smelter partner | F4 | 0 | 300 | 3500 | partner only |
| Electronics recovery partner | F3 | 0 | 30 | 6000 | partner only |
| Precious refining partner | F4 | 0 | 5 | 50000 | partner only |
| UCO purification | F3 | 45000000 | 80 | 700 | yes |
| RDF/SRF line | F4 | 300000000 | 150 | 300 | yes |
| Biomass line | F3 | 120000000 | 100 | 600 | yes |
| Biochar partner | F4 | 0 | 50 | 1300 | partner only |
| Anaerobic digester | F4 | 350000000 | 100 | 400 | yes |
| IPAL / emission control | F4 | 150000000 | 200 | 250 | yes |
| Waste-to-energy (abstract) | F4 | 1500000000 | 120 | 900 | partner only in beta |
| Alchemy research | F5 | per approved §7f | n/a | per recipe | no until review |

Routing: PET/HD/PP/PE/PV/PS/AB/HI/PC → plastic shred/wash; plastic mixed and laminated → RDF only if eligible after sorting (reject PVC, hazardous and wet matter); paper bale → baler, paper fiber → pulp line; ME01–08 except zinc → metal separation, ME09–29 → metal/precious partner as appropriate; GL01–10 → glass crusher/aggregate; EW all → licensed electronics partner; OR food/feed only approved partner; OR compost → bin, OR biomass → corresponding wood/biomass/char; TX → textile fiber; WO → wood; RU → rubber; RS/HZ → disposition, construction aggregates only clean and QC. Explicit recipe mapping required before enabling. Default primary route from catalog yield; remainder remains residue, wastewater or documented process gas/moisture; never deleted. For compost use delayed maturation 24 game hours (compressed, not real biology). BSF 48h, garden 24h default. For high price specialty rows, disable automatic trading until QA; proxies not recipes for actual extraction. A route can run at loss; warn and allow deliberate environmental action only with cash reserve. No buy feedstock solely for RDF when resale negative without fee contract.

### Secondary recipes — seeded examples
All masses per batch. Water and ancillary inputs included where material; outputs and residues balance. Time compressed game assumptions, not engineering guidance. Gas, wastewater, moisture, ash are ledger sinks, not invisible losses. For user-facing education show real-world duration as separate researched field.
| Recipe | Input | Output | Other mass | GC cost/batch | time h | stage |
|---|---|---|---|---:|---:|---|
| R-PETP | PETF 10 kg | PETP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-HDPP | HDF 10 kg | HDP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-PPPP | PPF 10 kg | PPP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-PEPP | PEF 10 kg | PEP 9.4 kg | 0.6 kg residue | 18000 | 1 | F3 |
| R-PVPP | PVF 10 kg | PVP 9.4 kg | 0.6 kg residue | 18000 | 1 | F3 |
| R-ABPP | ABF 10 kg | ABP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-HIPP | HIF 10 kg | HIP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-PCPP | PCF 10 kg | PCP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-PSPP | PSF 10 kg | PSP 9.5 kg | 0.5 kg residue | 18000 | 1 | F3 |
| R-PULP | OCC 10 kg | PULP 7 kg | 3 kg reject | 15000 | 2 | F3 |
| R-DIP | SOP 10 kg | DIP 7 kg | 3 kg reject | 15000 | 2 | F3 |
| R-BSF | OR03 10 kg | MAG 1.5 kg + KAS 3 kg | 5.5 kg moisture/gas | 2500 | 48 | F2 |
| R-MAGD | MAG 10 kg | MAGD 3 kg | 7 kg moisture | 8000 | 3 | F3 |
| R-COCO | OR17 10 kg | COCOF 4 kg + COCOP 4 kg | 2 kg residue | 4000 | 2 | F3 |
| R-UCO | UCO 10 L (9.2 kg) | UCOF 9 L (8.28 kg) | 0.92 kg reject | 7000 | 2 | F3 |
| R-AGG | RS07 10 kg | AGG 8.5 kg | 1.5 kg residue | 1000 | 1 | F3 |
| R-COMP-P | COMP 10 kg + packaging 0.2 kg | COMPP 10 kg net | 0.2 kg packaging mass in sold lot | 3000 | 1 | F2 |
| R-BIOPEL | CHIP 10 kg | BIOPEL 8 kg | 2 kg moisture/reject | 6000 | 2 | F3 |
| R-WTE | eligible RDF 10 kg | ELEC 5 kWh | 10 kg input-origin ash/gas stream (separate oxygen ledger in advanced model) | 9000 | 1 | F4 |
WTE illustrative output, not engineering efficiency; no real combustion instructions. Energy counted separately; no double credit RDF sale plus energy generated from same input. WTE only residual after recycling, emissions control and confirmed disposition. Energy export ≤ grid quota; default WTE may operate at loss without waste service fee. Use renewables first where viable. Product rows without recipe: external quote / future locked, cannot craft yet (e.g. food-grade, gold beyond partner, biodiesel, biomethane, advanced textile). For all recipe outputs, enforce grades and actual QC; no silent upgrading food safety. Default recipes for primary rows must assign mass remainder by process category and be validated individually; no claim of real-world technical yield.

### Upcycling BOM (game examples)
| Product | Input kg | output net kg per pcs | residue kg | cost GC/pcs |
|---|---|---:|---:|---:|
| BAG | clean PE 0.25 | .20 | .05 | 5000 |
| POT | PET01 .10 | .09 | .01 | 500 |
| PAV | eligible PE/PP .5 + clean aggregate 1.5 | 1.9 | .1 | 2500 |
| PALF | WO01 8 + hardware .3 | 7.3 | 1 | 50000 |
| DRUM | ME08 .3 | .27 | .03 | 3000 |
| BOX | PA01 .4 | .35 | .05 | 1200 |
| SANDAL | RU01 .8 | .55 | .25 | 9000 |
| PENCIL | PET01 .1 | .09 | .01 | 1500 |
| TOY | PP05 .3 | .25 | .05 | 4000 |
| LAPBAG | TX02 .6 + hardware .1 | .6 | .1 | 18000 |
| LAMP | GLREUSE .35 + certified assembly .15 | .5 | 0 | 17000 |
| RACK | PV01 2 + hardware .2 | 2 | .2 | 23000 |
| CANDLE | ME08 .2 | .18 | .02 | 2000 |
| CRAFT | PA06 .3 | .25 | .05 | 5000 |
Ancillary purchased stock must be recorded; no free hardware or packaging. All products have limited demand (default 5 pcs/day each, max 20 total/day), QC, safety locks for children/toys/electrical/structural use. Recipes are simulation abstraction, not DIY instructions. Stage F2 workshop; craft time default 30 min/pcs, PALF 4h. Explicit player price includes fees and input opportunity cost. Do not imply recycled products universally safe or suitable for structural use.

## 6. Gaia Garden and DLE
Gaia gives once: 3 common seed units, 1 starter plot, no sale of starter seed. Input seed mass default 1g/seed; plant biomass growth from environmental inputs (water, carbon, nutrients) recorded as separate modeled source, not waste diversion. Harvest 0.5 kg/plant at 24h; compost 100g/plant optional reduces duration by 20% (min 12h), not instant money. Irrigation operating cost 100 GC/plant; seed replacement 200 GC/unit. First successful compost-assisted harvest unlocks one rare seed variety deterministically selected per player, once; subsequent rare seeds from missions with caps. Rare harvest 0.4 kg/plant, 48h, seed cost 600, daily market cap 5 kg. Plot expansion 5000 GC per plot, max F1=3/F2=10/F3=30. Harvest not environmental diversion credit; compost counted only at verified use. Safe material only; contaminated roadside vegetables compost only, not food.
DLE NPC litter river and vegetable truck drop road preserve position after facility upgrade. Example event templates: river litter 0.2–1kg, vegetable spill 1–3kg, fallen cardboard 0.5–2kg, windblown plastic .1–.5kg; 2–6 opportunities/day, max 10kg/day per player; deterministic event ID, expiry 2h, source reservation, collect once. Cleanup provides material plus 50–200 GC municipal service where eligible, cap 500 GC/day (mission bonus separate capped). Expiry moves stock to unmanaged burden; not disappear. NPC is decorative, no punitive interaction. No direct handling of hazardous or sharp objects in DLE; report to partner. Early garden and cleanup aid liquidity but cannot infinitely respawn.

## 7. Ledger, environment and profitability
```
profit_operating = sales + contracted_service_fees - purchase - logistics - processing - QC - disposal - maintenance - fees
cash_delta = profit_operating + mission_subsidy - capex + other_explicit_ledger_transfers
mass_in + auxiliary_in = products + residues + wastewater + vapor/gas + WIP_delta
```
Store integer grams (round output down, remainder to residue), integer GC, rational conversion for liters, count separate kWh; preserve provenance per origin lot and fractional allocation. Energy cannot close material mass. Simplified mass boundary tracks input-origin mass only; if complete chemistry modeled include atmospheric O2 etc explicitly. Impact recognized only on verified terminal beneficial use or accepted licensed treatment per metric; transfer/re-sorting/processing intermediate not credit. Origin credit budget ≤ original grams; allocated to processor of terminal disposition, collection contributors may get separate non-mass mission points. Track landfill, open leakage, emissions, in-process inventory, treated non-recovered waste separately. Diversion = verified material/organic recovery + qualifying controlled energy recovery / eligible handled original waste mass; exclude untreated stock from numerator and include it denominator; hazardous safe treatment tracked separate (not automatically recycled); energy diversion capped to actual accepted eligible mass net ash sent landfill. Publish both material recovery rate and total diversion; no 100% claim from energy alone. Prevented kg via counterfactual scenario displayed separately. BHI/ZWM definitions in base spec require owner calibration, no automatic reinterpretation. Karma thresholds and reinkarnation preserved; no uncontrolled emissions actual operation. Record educational scenario outcomes (sim only). No real CO2 claim without verified factors; use generic impact points.

### Example accounting
10 kg PET01 purchased at bank baseline 3000/kg = 30000; 8 kg PETF, 2 kg residue; processing 12000, transport 1000, disposal 1000; sale bid assumed 10560/kg ×8 = 84480, fee 1690; direct surplus 38790 GC (before fixed costs), if buyer minimum 100kg then batch must aggregate/partner offtake or no sale. An unprofitable example: 10kg PL02 at 100/kg, RDF output 6.5kg ×432 =2808, processing 3000 + disposal 1750 + fee 57 + transport 1000 = net -3999 GC. Service contract may offset, not magic payout.

## 8. Balancing and fallback
Mission coins are transparent Gaia/municipal education grants, not commodity price. Starter cash can be exhausted; once per 24h rescue contract offers zero input cost 5kg sorted municipal material, paid 500 GC on verified delivery; no advance, no reset farming. Free public drop-off quota 2kg/day for orphan residue; excess requires paid disposal, report warning. No negative balance, no forced real payment; player can pause machine, sell at bank or rent service. F1 early economy use small lots; all CAPEX quoted; stage progression via owned or contracted capacity. Grants daily cap 2000 GC for repeatable missions plus DLE separate; milestone awards one-time. Market supply caps and sinks prevent runaway. 90-day active target God is a test goal, not validated. Need actual simulations before tuning. Test alternative paths (material, organics, mixed, thermal); no thermally dominant strategy, no pay-to-win. If target unreachable with 10k starter and real-scale CAPEX, adjust rental access/contract throughput not inflate material prices. Tier progression does not require ownership of massive plant. Physical stage criteria and rewards in file 03.
