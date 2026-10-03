---
doc_id: LVH-CAL-001
title: LevelHull sizing calculations
project: LevelHull
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue at TRL 3, on the constructable design of LVH-DDR-002
---

# LevelHull sizing calculations

On paper, eight foam modules of 0.38 m3 in all, fitted high under the gunwales of the 8 m reference canoe, keep the swamped canoe afloat with its motor, gear, catch and four crew holding on, with 80 mm of freeboard at the lowest point of the gunwale, level within half a degree and with 2.2 times the needed lift in reserve at 50 mm freeboard. The same foam laid low on the floor would leave the swamped canoe almost neutral in roll, and it would roll over with the crew on one side: that comparison is why the modules sit under the gunwale. The weak points are the low-side freeboard with all four crew on one side (31 mm), the damaged case (9 mm with the largest module lost) and the cost, which is USD 350 over the value-engineering target for two canoes.

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
| A7 | Kit hardware in water | Covers 8.9 kg PVC, steel 2.8 kg, straps 3.3 kg; battens neutral | Densities 1,300, 7,850 and 1,380 kg/m3 |
| A8 | Bailing | 100 L per minute per person with a 10 L bucket, two bailers, calm water | Estimate |
| A9 | Fixing strengths | Webbing 10 kN, D-ring pair 4 kN, M8 coach screw 1.5 kN sideways in hardwood | To confirm with real parts |

## 2. Geometry of the kit

*Table 2. Kit geometry (reference canoe).*

| Tag | Quantity | Value |
| --- | --- | --- |
| [G1] | Side flare of the canoe | 31.6 deg |
| [G2], [G3] | Modules | 8; 4.78 m a side (880, 1,400, 1,400 and 1,100 mm) |
| [G4] | Module section | 200 mm wide (level) x 200 mm high, a parallelogram matching the flare |
| [G5], [G6] | Module volume; foam inside the covers | 0.382 m3; 0.365 m3 |
| [G7] | Module bottom and top above the outside of the bottom | 420 and 620 mm (top 30 mm below the gunwale) |
| [G8], [G9] | Hull timber; dry hull mass at 750 kg/m3 | 0.586 m3; 439 kg |
| [K1] | Kit mass | 67.4 kg (battens and chocks 39.4 kg, foam 10.9 kg, covers 8.9 kg) |

## 3. Swamped, design load

*Table 3. Swamped canoe at the design load, fresh water.*

| Tag | Result | Value |
| --- | --- | --- |
| [L1] | Design net load | 118 kg |
| [F4] | Timber above the water, counted as load | 104 kg |
| [F1] | Freeboard amidships, level | 105 mm |
| [F3] | Trim | 0.45 deg stern down |
| [F2] | Lowest freeboard on the gunwale (transom) | 80 mm |
| [F5], [F6] | Metacentric height; roll stiffness | 3.1 m; 742 kg m per radian |
| [F7], [F8] | Net load carried at 50 mm freeboard; reserve | 257 kg; 2.17 times the design load |
| [F9] | No crew holding on | 119 mm lowest freeboard, 0 deg heel, 0.17 deg trim |

## 4. Off-design cases

*Table 4. Off-design cases.*

| Tag | Case | Result |
| --- | --- | --- |
| [F10], [F11] | All four crew holding the port grab line | 4.0 deg heel; low-side freeboard 31 mm |
| [F12] | Salt water | 87 mm lowest freeboard |
| [F13] | Foam lift down 5 % (the R6 limit) | 74 mm lowest freeboard |
| [F14], [F15] | Largest module (port 2) lost, and 5 % uptake | 9 mm lowest freeboard; 1.5 deg heel |
| [F16] | Typical 750 kg/m3 timber (lift not counted in the design) | 163 mm freeboard amidships |

## 5. Why the modules are high: low placement compared

The TRL 1 concept placed the modules low along the sides. With the same 0.38 m3 of foam on the floor (85 to 285 mm up), the foam is fully under water and cuts no waterline, so only the thin planks give any waterplane, while the motor and the crew's hands act high on the canoe.

*Table 5. Same foam, high or low.*

| Tag | Quantity | High under the gunwale | Low on the floor |
| --- | --- | --- | --- |
| [F6], [F17] | Roll stiffness, kg m per radian | 742 | 17 |
| [F5], [F18] | Metacentric height | 3.1 m | 0.04 m |
| [F10], [F19] | Four crew on one side | 4.0 deg heel | Rolls over (small-angle heel beyond 90 deg) |

This is the result behind decision D1 in LVH-DDR-001. It matches the practice in the USCG level flotation method, where flotation that keeps a swamped boat upright sits high in the hull.

## 6. Space, bailing and the dry canoe

*Table 6. Space and bailing.*

| Tag | Quantity | Value |
| --- | --- | --- |
| [V1], [V2] | Inside volume below the gunwale; share taken by the modules | 5.01 m3; 7.6 % |
| [B1] | Water inside the swamped canoe | 3.57 m3 |
| [B2] | Water that can stay aboard at 200 mm freeboard, all crew and gear aboard | 2.31 m3 |
| [B3], [B4] | Water to bail; time for two crew | 1.26 m3; about 6.3 minutes (estimate) |
| | Time to bail the canoe dry at the same rate | about 18 minutes (estimate) |
| [B5] | Dry canoe: added draft from the 67 kg kit | about 11 mm |

The clear width between the module tops is 963 mm, and the modules take the upper side of the canoe, where little catch is stowed.

## 7. Fixings

The worst case for a fixing is a module pushed fully under water (a breaking wave or a canoe on its side), in salt water.

*Table 7. Fixing loads.*

| Tag | Quantity | Value | Factor (R7 needs 2) |
| --- | --- | --- | --- |
| [S1] | Largest module (1,400 mm), full lift | 0.547 kN | |
| [S2], [S3] | Per strap (two straps); each leg half of that | 0.273 kN | Webbing 73 |
| [S4] | D-ring pair, 4 kN to confirm | 0.273 kN | 14.6 |
| [S5], [S6] | Per coach screw, sideways (largest share, two screws) | 0.273 kN | 5.5 |
| [S7], [S8] | All modules fully under water; per frame | 3.73 kN; 0.187 kN | |

The frames take 0.187 kN each into their existing fastenings to the planks. The condition of those fastenings is checked on every hull before fitting (build plan, first checks).

## 8. Fitting time, cost and the sizing sheet

- [T1] Fitting on the canoe takes about 6.3 hours for a builder and a helper, with the foam cores and covers made beforehand (estimate): marking 40 minutes, battens 120, screws 60, chocks 40, straps and modules 50, eye bolts and grab lines 50, marks and bailers 20.
- [C1], [C2] Parts cost USD 677 for one kit and USD 1,350 for two canoes (one gauge). Value-engineering target: USD 1,000. Estimated cost of the constructable design: USD 1,350 (USD 350 over the target). [C3] Foam is 49 % of a kit.

The sizing sheet uses a simple prismatic estimate: modules 200 x 200 mm, top 30 mm below the gunwale, and enough run per side to carry 1.5 times the design net load plus the timber above the water at 50 mm freeboard.

*Table 8. Sizing sheet for other hulls (estimates; measure each hull).*

| Hull | Module run needed per side | Run free of thwarts |
| --- | --- | --- |
| 6.5 m paddle canoe, no motor, 3 crew | 2.7 m | 3.8 m |
| 8.0 m canoe, 15 hp, 4 crew (reference) | 4.2 m | 4.8 m fitted |
| 10 m canoe, 25 hp, 6 crew | 5.6 m | 6.4 m |

## 9. Results against the requirements

*Table 9. Results against LVH-REQ-001.*

| ID | Target | Result | Status |
| --- | --- | --- | --- |
| R1 | Afloat with design load | 2.2 times the design load carried at 50 mm freeboard | Met on paper |
| R2 | At least 50 mm freeboard | 80 mm lowest | Met on paper |
| R3 | Heel and trim within 10 deg | 0 deg heel, 0.45 deg trim | Met on paper |
| R4 | Bail in 15 min or less | About 6 minutes to 200 mm freeboard | Met on paper (estimate) |
| R5 | 10 % or less of inside volume | 7.6 % | Met |
| R6 | Under 5 % uptake | Under 1 % on supplier data | To confirm by test |
| R7 | Fixings 2 times their share | Lowest factor 5.5 (coach screw) | Met on paper |
| R8 | Fitted in a day | About 6.3 hours | Met on paper (estimate) |
| R9 | 12 months without loss | Not shown on paper | Needs field trial (TRL 4 and later) |
| R10 | Value-engineering target USD 1,000 for two canoes | USD 1,350 | Over the value-engineering target by USD 350 |
| R11 | Reserve 1.5 | 2.17 | Met on paper |
| R12 | Afloat with largest module lost | 9 mm freeboard | Met on paper, small margin |
| R13 | Heel within 10 deg, crew on one side | 4.0 deg; low side 31 mm | Met on paper |
