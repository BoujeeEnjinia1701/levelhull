---
doc_id: LVH-DDR-003
title: LevelHull wider foam modules for R12 and R13
project: LevelHull
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Decision 10A recorded and carried into the model, calculations, bill of materials, drawings and build plan
---

# 0003: Wider foam modules for R12 and R13

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish on 2026-10-03, choosing option A on every requirement decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". This record carries decision 10A.

## Context

At TRL 3 (LVH-CAL-001 v0.1) R12 and R13 were met on paper, but with little margin. With the largest module lost and 5 % water uptake the lowest point of the gunwale was only 9 mm above the water (R12). With all four crew holding one grab line the heel was 4.0 deg, inside the 10 deg of R13, but the low-side gunwale was only 31 mm above the water. Both had been handled as operating rules rather than by the design.

## Options considered

- **A. Enlarge the foam modules about 10 % (chosen).** More lift and more waterplane along both sides for a small rise in foam, cover and mass.
- **B.** Keep the modules and keep the operating rules (crews spread out, no fishing with a module missing).

## Decision

Option A. The modules are widened from 200 to 220 mm (level width), keeping the 200 mm height of four 50 mm layers, the lengths, the positions high under the gunwale and every fixing. That is 10 % more foam: 0.42 m3 of module in all, against 0.38 m3.

Width rather than height or length was chosen because:

- A fifth layer would add 25 %, not 10 %, and would bring the module bottom down towards the floor, where it adds less roll stiffness.
- The lengths are already set by the thwarts and frames.
- Four 220 mm strips still come from the 1,000 mm width of one foam sheet, so the six sheets per kit stay the same. A new model check confirms it.
- The battens, chocks and screws are unchanged. Each strap goes 40 mm further round the module, so straps are cut 1.25 m long instead of 1.2 m (20 m of the 25 m bought), and each cover panel is cut 1,040 mm wide instead of 1,000 mm.

## Results (LVH-CAL-001 v0.2)

| Requirement | Target | Before | After |
| --- | --- | --- | --- |
| R12 | Still floats with the largest module lost and 5 % uptake | 9 mm lowest freeboard, 1.5 deg heel | 25 mm lowest freeboard, 1.5 deg heel |
| R13 | Heel within 10 deg, all four crew on one grab line | 4.0 deg; low side 31 mm | 3.9 deg; low side 44 mm |
| R1, R11 | Afloat with design load; reserve at least 1.5 | 2.17 | 2.45 |
| R2 | At least 50 mm freeboard | 80 mm | 92 mm |
| R5 | 10 % or less of the inside volume | 7.6 % | 8.4 % |
| R7 | Fixings at least 2 times their share | Lowest 5.5 | Lowest 5.0 |
| R10 | Value-engineering target USD 1,000 for two canoes | USD 1,350 | USD 1,360 |

Kit mass rises from 67.4 to 68.9 kg (foam 12.1 kg, covers 9.3 kg). The clear width between the module tops falls from 963 to 923 mm, still above the 900 mm the model checks. The model passes 127 of 127 constructability checks.

## Consequences

- Value-engineering target: USD 1,000. Estimated cost of the constructable design: USD 1,360 (USD 360 over the target). The only added cost is 1 m2 more tarpaulin a kit (USD 5); the foam strips come from the same six sheets, so no spare strip is left.
- With all four crew on one side the low gunwale is still under 50 mm from the water, so the operating rule that crews spread along both grab lines stays.
- The comparison with the same foam on the floor changes: the larger volume now just reaches the surface on the floor, but it heels 10.6 deg with the crew on one side and has no roll stiffness left with 5 kg more load. The case for fitting the modules high (LVH-DDR-001, D1) stands.
- The cores, covers, general arrangement (Rev P3), making sketches of the cores and covers, the module joint pictures, the step pictures and the concept media are redrawn from the model.

> **Safety:** Wider modules give more margin when the canoe is swamped; they do not make it safe. LevelHull is never a substitute for life jackets, and the swamp test rules in the build plan are unchanged.
