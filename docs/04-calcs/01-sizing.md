---
doc_id: LVH-CAL-001
title: LevelHull sizing calculations
project: LevelHull
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue at TRL 3, on the constructable design of LVH-DDR-002
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Modules widened from 200 to 220 mm (LVH-DDR-003, Amish's decision 10A); every result re-run; F20 and K3 added
---

# LevelHull sizing calculations

On paper, eight foam modules of 0.42 m3 in all, fitted high under the gunwales of the 8 m reference canoe, keep the swamped canoe afloat with its motor, gear, catch and four crew holding on, with 92 mm of freeboard at the lowest point of the gunwale, level within half a degree and with 2.45 times the needed lift in reserve at 50 mm freeboard. The same foam laid low on the floor would only just reach the water surface, would heel past the 10 degree limit with the crew on one side, and would lose all roll stiffness with 5 kg more load: that comparison is why the modules sit under the gunwale. The modules were widened from 200 to 220 mm on Amish's decision of 2026-10-03 (LVH-DDR-003) to give more margin in the two weakest cases: the low-side freeboard with all four crew on one side is now 44 mm (was 31 mm) and the damaged case with the largest module lost is now 25 mm (was 9 mm). The cost is USD 360 over the value-engineering target for two canoes.

Every figure comes from `docs/04-calcs/sizing.py`, which imports the parametric model (`cad/src/model.py`), so the sizes here are those of the STEP files, the drawings and the build plan. Tags in square brackets match the script output and `docs/04-calcs/results.csv`. The script is also the open sizing calculator for other hulls (section 8). These are screening estimates for a paper proof of concept; they do not replace the swamp test, which is TRL 4 work.

> **Safety:** LevelHull is flotation for a boat, not lifesaving equipment, and is never a substitute for life jackets. These numbers are for a design review. No fitted canoe is used for fishing before its fixings are pull-tested and it has passed a swamp test in sheltered, shallow water with a safety boat and every person in a life jacket.

## 1. Method and assumptions

The swamped canoe is treated as a set of solid bodies floating in the lake. The water inside the hull is part of the lake and carries nothing. Each body gives lift equal to the water its submerged part displaces and weighs its own mass; the canoe floats where total lift equals total weight. Small heel and trim follow from the second moments of the waterplane (the strips where the modules and planks cut the water surface) and the heights of the lift and the weights: roll stiffness = water density x waterplane moment + lift x height of the centre of lift - weight x height of the centre of weight.

*Table 1. Assumptions.*

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A1 | Water density | 1,000 kg/m3 (lakes); 1,025 kg/m3 checked | Design case is fresh water |
| A2 | Wet hull timber density | 1,000 kg/m3: no net lift from the hull | Conservative (LVH-DDR-001, D3); 750 kg/m3 reported as a margin |
| A3 | Crew holding on | 20 % of 75 kg each (15 kg), at the gunwale | Head and shoulders out of the water; four crew |
| A4 | Outboard motor | 36 kg at full weight, 0.25 m aft of the transom | 15 hp two-stroke; mostly above water when swamped |
| A5 | Gear and catch | 12 kg steel anchor, 40 kg nylon nets, 150 kg fish, full fuel tank | Net in water 10.5, 4.9, 7.1 and 0 kg (a full tank floats) |
| A6 | Foam | Closed-cell polyethylene, 30 kg/m3, under 1 % water uptake by volume | Supplier data to confirm |
| A7 | Kit hardware in water | Covers 9.3 kg PVC, steel 2.8 kg, straps 3.4 kg; battens neutral | Densities 1,300, 7,850 and 1,380 kg/m3 |
| A8 | Bailing | 100 L per minute per person with a 10 L bucket, two bailers, calm water | Estimate |
| A9 | Fixing strengths | Webbing 10 kN, D-ring pair 4 kN, M8 coach screw 1.5 kN sideways in hardwood | To confirm with real parts |

## 2. Geometry of the kit

*Table 2. Kit geometry (reference canoe).*

| Tag | Quantity | Value |
| --- | --- | --- |
| [G1] | Side flare of the canoe | 31.6 deg |
| [G2], [G3] | Modules | 8; 4.78 m a side (880, 1,400, 1,400 and 1,100 mm) |
| [G4] | Module section | 220 mm wide (level) x 200 mm high, a parallelogram matching the flare (was 200 x 200 mm; LVH-DDR-003) |
| [G5], [G6] | Module volume; foam inside the covers | 0.421 m3; 0.402 m3 (was 0.382 and 0.365 m3) |
| [G7] | Module bottom and top above the outside of the bottom | 420 and 620 mm (top 30 mm below the gunwale) |
| [G8], [G9] | Hull timber; dry hull mass at 750 kg/m3 | 0.586 m3; 439 kg |
| [K1] | Kit mass | 68.9 kg (battens and chocks 39.4 kg, foam 12.1 kg, covers 9.3 kg); was 67.4 kg |
| [K2], [K3] | Cover tarpaulin; strap webbing | 14.3 m2; 19.5 m |

## 3. Swamped, design load

*Table 3. Swamped canoe at the design load, fresh water.*

| Tag | Result | Value |
| --- | --- | --- |
| [L1] | Design net load | 118 kg |
| [F4] | Timber above the water, counted as load | 109 kg |
| [F1] | Freeboard amidships, level | 113 mm |
| [F3] | Trim | 0.39 deg stern down |
| [F2] | Lowest freeboard on the gunwale (transom) | 92 mm |
| [F5], [F6] | Metacentric height; roll stiffness | 3.1 m; 761 kg m per radian |
| [F7], [F8] | Net load carried at 50 mm freeboard; reserve | 290 kg; 2.45 times the design load |
| [F9] | No crew holding on | 128 mm lowest freeboard, 0 deg heel, 0.14 deg trim |

## 4. Off-design cases

*Table 4. Off-design cases.*

| Tag | Case | Result |
| --- | --- | --- |
| [F10], [F11] | All four crew holding the port grab line | 3.9 deg heel; low-side freeboard 44 mm (was 4.0 deg and 31 mm) |
| [F12] | Salt water | 98 mm lowest freeboard |
| [F13] | Foam lift down 5 % (the R6 limit) | 86 mm lowest freeboard |
| [F14], [F15] | Largest module (port 2) lost, and 5 % uptake | 25 mm lowest freeboard; 1.5 deg heel (was 9 mm) |
| [F16] | Typical 750 kg/m3 timber (lift not counted in the design) | 167 mm freeboard amidships |

With all four crew on one grab line the low-side gunwale is still under the 50 mm of R2, so the operating rule stays: crews spread along both grab lines. R13 itself asks only for heel within 10 deg and is met with a wide margin.

## 5. Why the modules are high: low placement compared

The TRL 1 concept placed the modules low along the sides. With the same 0.42 m3 of foam on the floor (85 to 285 mm up), the canoe floats with the top of the foam 1 mm under the water. The foam then cuts the waterline only by that knife edge: with four crew on one side it heels past the 10 degree limit, and 5 kg more load (one wet net, one more person's hand) puts the foam fully under water, where only the thin planks give any waterplane and the canoe has no roll stiffness left. (With the earlier 0.38 m3 of foam the floor arrangement was already in that state at the design load.)

*Table 5. Same foam, high or low.*

| Tag | Quantity | High under the gunwale | Low on the floor |
| --- | --- | --- | --- |
| [F6], [F17] | Roll stiffness, kg m per radian | 761 | 283, only while the foam top is at the water |
| [F5], [F18] | Metacentric height | 3.1 m | 0.68 m |
| [F10], [F19] | Four crew on one side | 3.9 deg heel | 10.6 deg heel, over the 10 deg limit |
| [F20] | Roll stiffness with 5 kg more load | 761 or more | None (foam fully under water) |

This is the result behind decision D1 in LVH-DDR-001. It matches the practice in the USCG level flotation method, where flotation that keeps a swamped boat upright sits high in the hull.

## 6. Space, bailing and the dry canoe

*Table 6. Space and bailing.*

| Tag | Quantity | Value |
| --- | --- | --- |
| [V1], [V2] | Inside volume below the gunwale; share taken by the modules | 5.01 m3; 8.4 % (was 7.6 %) |
| [B1] | Water inside the swamped canoe | 3.48 m3 |
| [B2] | Water that can stay aboard at 200 mm freeboard, all crew and gear aboard | 2.31 m3 |
| [B3], [B4] | Water to bail; time for two crew | 1.17 m3; about 5.9 minutes (estimate) |
| | Time to bail the canoe dry at the same rate | about 17 minutes (estimate) |
| [B5] | Dry canoe: added draft from the 69 kg kit | about 11 mm |

The clear width between the module tops is 923 mm (was 963 mm; the model checks at least 900 mm), and the modules take the upper side of the canoe, where little catch is stowed.

## 7. Fixings

The worst case for a fixing is a module pushed fully under water (a breaking wave or a canoe on its side), in salt water.

*Table 7. Fixing loads.*

| Tag | Quantity | Value | Factor (R7 needs 2) |
| --- | --- | --- | --- |
| [S1] | Largest module (1,400 mm), full lift | 0.601 kN | |
| [S2], [S3] | Per strap (two straps); each leg half of that | 0.301 kN | Webbing 66 |
| [S4] | D-ring pair, 4 kN to confirm | 0.301 kN | 13.3 |
| [S5], [S6] | Per coach screw, sideways (largest share, two screws) | 0.301 kN | 5.0 |
| [S7], [S8] | All modules fully under water; per frame | 4.11 kN; 0.205 kN | |

The frames take 0.205 kN each into their existing fastenings to the planks. The condition of those fastenings is checked on every hull before fitting (build plan, first checks).

## 8. Fitting time, cost and the sizing sheet

- [T1] Fitting on the canoe takes about 6.3 hours for a builder and a helper, with the foam cores and covers made beforehand (estimate): marking 40 minutes, battens 120, screws 60, chocks 40, straps and modules 50, eye bolts and grab lines 50, marks and bailers 20.
- [C1], [C2] Parts cost USD 682 for one kit and USD 1,360 for two canoes (one gauge). Value-engineering target: USD 1,000. Estimated cost of the constructable design: USD 1,360 (USD 360 over the target). [C3] Foam is 48 % of a kit. The wider modules still come four strips to a 1,000 mm sheet, so the six foam sheets are unchanged; the only added cost is 1 m2 more tarpaulin (USD 5 a kit).

The sizing sheet uses a simple prismatic estimate: modules 220 x 200 mm, top 30 mm below the gunwale, and enough run per side to carry 1.5 times the design net load plus the timber above the water at 50 mm freeboard.

*Table 8. Sizing sheet for other hulls (estimates; measure each hull).*

| Hull | Module run needed per side | Run free of thwarts |
| --- | --- | --- |
| 6.5 m paddle canoe, no motor, 3 crew | 2.5 m | 3.8 m |
| 8.0 m canoe, 15 hp, 4 crew (reference) | 3.8 m | 4.8 m fitted |
| 10 m canoe, 25 hp, 6 crew | 5.1 m | 6.4 m |

## 9. Results against the requirements

*Table 9. Results against LVH-REQ-001.*

| ID | Target | Result | Status |
| --- | --- | --- | --- |
| R1 | Afloat with design load | 2.45 times the design load carried at 50 mm freeboard | Met on paper |
| R2 | At least 50 mm freeboard | 92 mm lowest | Met on paper |
| R3 | Heel and trim within 10 deg | 0 deg heel, 0.39 deg trim | Met on paper |
| R4 | Bail in 15 min or less | About 6 minutes to 200 mm freeboard | Met on paper (estimate) |
| R5 | 10 % or less of inside volume | 8.4 % | Met |
| R6 | Under 5 % uptake | Under 1 % on supplier data | To confirm by test |
| R7 | Fixings 2 times their share | Lowest factor 5.0 (coach screw) | Met on paper |
| R8 | Fitted in a day | About 6.3 hours | Met on paper (estimate) |
| R9 | 12 months without loss | Not shown on paper | Needs field trial (TRL 4 and later) |
| R10 | Value-engineering target USD 1,000 for two canoes | USD 1,360 | Over the value-engineering target by USD 360 |
| R11 | Reserve 1.5 | 2.45 | Met on paper |
| R12 | Afloat with largest module lost | 25 mm freeboard (was 9 mm) | Met on paper |
| R13 | Heel within 10 deg, crew on one side | 3.9 deg; low side 44 mm (was 4.0 deg, 31 mm) | Met on paper |
