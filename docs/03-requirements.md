---
doc_id: LVH-REQ-001
title: LevelHull requirements
project: LevelHull
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Targets fixed on the reference canoe; R11 to R13 added; TRL 3 status from LVH-CAL-001
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: 'Modules widened 10 % for R12 and R13 on Amish''s decision of 2026-10-03 ("10A", LVH-DDR-003); targets unchanged; TRL 3 status updated from LVH-CAL-001 v0.2'
---

# LevelHull requirements

Requirements for the kit fitted to the reference canoe (8.0 m, 1.6 m beam, 0.65 m deep, 15 hp outboard, four crew). Other hulls are sized to the same requirements with the calculator. Status is the paper result at TRL 3 from LVH-CAL-001; every requirement is verified by test at TRL 4.

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 4) | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Swamped canoe stays afloat with its design load | Design net load 118 kg (crew holding on, motor, gear, catch) carried for at least 1 h | Swamp test in sheltered water, based on the USCG level flotation method | Met on paper: carries 2.45 times the design load at 50 mm freeboard |
| R2 | Freeboard when swamped | At least 50 mm at the lowest point of the gunwale, design load, fresh water | Measured during swamp test | Met on paper: 92 mm (113 mm amidships) |
| R3 | Floats level when swamped | Heel and trim each within 10 deg, crew in the water not holding on, and with crew holding on both sides | Inclinometer reading during swamp test | Met on paper: 0.0 deg heel, 0.14 deg trim; 0.39 deg trim with crew holding on |
| R4 | Crew can bail the swamped canoe | Two crew bail to 200 mm freeboard in 15 min or less, calm water | Timed bail-out trial | Met on paper (estimate): about 6 min |
| R5 | Volume taken from the working space | 10 % or less of the inside volume | Measured on the fitted canoe | Met: 8.4 % |
| R6 | Material water uptake | Foam gains less than 5 % of its lift in mass after 30 days immersed | Immersion and weighing of samples | Met on supplier data (under 1 % by volume); to confirm by test |
| R7 | Fixing strength | Each fixing holds 2 times its share of the full lift without pull-out | CalRig proof-load of a batten, screws and strap in a test panel | Met on paper: screw factor 5.0, D-ring 13.3, webbing 66 |
| R8 | Fitting | A local builder fits the kit in one working day with hand tools, modules made beforehand | Timed fitting with the partner builder | Met on paper (estimate): about 6.3 h |
| R9 | Durability | No cracking or loss of lift after 12 months of normal use | Field inspection of pilot canoes | Cannot be shown on paper |
| R10 | Cost | Parts for kits on two canoes against the value-engineering target of USD 1,000 | Costed bill of materials | USD 1,360: over the value-engineering target by USD 360 |
| R11 | Reserve lift | At least 1.5 times the design net load carried at 50 mm freeboard | Swamp test with added weights | Met on paper: 2.45 |
| R12 | Damage tolerance | Still floats with the largest module lost and 5 % water uptake | Swamp test with one module removed | Met on paper: 25 mm freeboard, 1.5 deg heel (was 9 mm before the modules were widened) |
| R13 | Crew on one side | Heel within 10 deg with all four crew holding one grab line | Swamp test | Met on paper: 3.9 deg (low-side freeboard 44 mm, was 31 mm) |

## Assumptions

- Modules 220 mm wide by 200 mm high (widened from 200 mm on Amish's decision 10A of 2026-10-03: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A").
- Reference canoe: planked, flat bottom 0.8 m wide, sides flared 31.6 deg, frames 50 x 60 mm at 600 mm, thwarts at 1.2, 3.0 and 4.8 m from the transom.
- Wet hull timber is counted as exactly as dense as water (no net lift from the hull).
- A crew member holding on with head and shoulders out puts 20 % of a 75 kg body on the canoe.
- Closed-cell polyethylene foam of about 30 kg/m3 with under 1 % water uptake by volume is available to the first partner.
- Owners accept 8.4 % of the inside volume, high along the sides, in exchange for flotation.
- The USCG level flotation method is adapted as a design benchmark only; the kit is not certified to it.

> **Safety:** These requirements describe flotation for the boat, not for people. Life jackets remain the first line of defence; the swamp tests behind R1 to R4 and R11 to R13 are run in sheltered, shallow water with a safety boat and every person in a life jacket.
