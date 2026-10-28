---
doc_id: LVH-PRS-001
title: LevelHull product requirements and specifications
project: LevelHull
doc_type: Product requirements and specifications
version: '0.5'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Initial scaffold (as LVH-REQ-001)
  - version: "0.2"
    date: '2026-10-03'
    author: Amish Chadha
    change: Targets fixed on the reference canoe; R11 to R13 added; TRL 3 status from LVH-CAL-001 (as LVH-REQ-001)
  - version: "0.3"
    date: '2026-10-03'
    author: Amish Chadha
    change: 'Modules widened 10 % for R12 and R13 on Amish''s decision of 2026-10-03 ("10A", LVH-DDR-003); targets unchanged (as LVH-REQ-001)'
  - version: "0.4"
    date: 2026-10-24
    author: Amish Chadha
    change: "Kit 1.8 migration: LVH-REQ-001 becomes LVH-PRS-001; R1 to R13 become PR-001 to PR-013 with the same targets, verification and status, traced to LVH-URS-001, with tolerances and units; PR-014 to PR-017 proposed for UR-014, UR-015, UR-016 and the hull-hole part of UR-008; PR-002 to PR-004 at risk for the sealed hull just after swamping (LVH-STM-001 S32 to S34, LVH-DEC-001 D-O2, D-O3)"
  - version: '0.5'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Amish''s decisions of 2026-10-25 ("i concur with your recommendations"): PR-002 and PR-003 stated for the free-flooding condition with the operating rule (D-O2), PR-002 at risk to met on paper; PR-004 for four crew with four bailers from brim-full (D-O3), at risk to met on paper; PR-014 to PR-017 accepted (D-R1); PR-010 USD 1,384'
---

# LevelHull product requirements and specifications

What the kit must do, each requirement traced to a user need in LVH-URS-001. Targets are for the kit fitted to the reference canoe (8.0 m, 1.6 m beam, 0.65 m deep, 15 hp outboard, four crew) and are proposals for review with a co-design partner; other hulls are sized to the same requirements with the calculator. Status is the paper result at TRL 3 from LVH-CAL-001 and LVH-STM-001; every requirement is verified by test at TRL 4. PR-001 to PR-013 carry the targets of R1 to R13 unchanged ("Was" column). PR-014 to PR-017 are new with this migration; Amish accepted all four on 2026-10-25 (LVH-DEC-001 D-R1). Method: STANDARDS section 22.

> **Safety:** These requirements describe flotation for the boat, not for people. Life jackets remain the first line of defence; the swamp tests behind PR-001 to PR-004 and PR-011 to PR-013 are run in sheltered, shallow water with a safety boat and every person in a life jacket.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Afloat when swamped | The swamped canoe shall stay afloat with the design net load (crew holding on, motor, gear, catch) for at least 1 h | 118 | min | kg net load | Analysis (LVH-CAL-001), TRL 3; swamp test based on the USCG level flotation method, TRL 4 | Met on paper: carries 2.45 times the design load at 50 mm freeboard | R1 |
| PR-002 | UR-002 | Performance | Freeboard when swamped | The lowest point of the gunwale shall stay above the water when swamped at the design load in fresh water, judged in the free-flooding condition of the USCG level flotation method (water inside at the lake level); with a sealed hull the crew hold on, then bail at once, seated (operating rule; restated by Amish, 2026-10-25, LVH-DEC-001 D-O2) | 50 | min | mm | Analysis (LVH-CAL-001), TRL 3; measured in the swamp test, TRL 4 | Met on paper in the free-flooding condition: 92 mm lowest, 113 mm amidships; 75 mm with timber at 1,100 kg/m3; brim-full straight after swamping a sealed hull floats about 24 mm level and about 3 mm at the lowest point until the crew bail (LVH-STM-001 S2, S32) | R2 |
| PR-003 | UR-003 | Performance | Floats level | Heel and trim of the swamped canoe shall each stay within the limit, crew not holding on and crew holding on both sides, judged in the free-flooding condition of the USCG method (restated by Amish, 2026-10-25, LVH-DEC-001 D-O2) | 10 | max | deg | Analysis (LVH-CAL-001), TRL 3; inclinometer in the swamp test, TRL 4 | Met on paper with the water inside flowing freely: 0.0 deg heel, 0.39 deg trim; brim-full a sealed hull is near neutral in roll and lolls a degree or two until it spills (LVH-STM-001 S33, to confirm by test) | R3 |
| PR-004 | UR-004 | Usability | Bail-out | The four crew, each with one of the kit's four bailers (LVH-DEC-001 D-O3, decided by Amish 2026-10-25), shall bail the swamped canoe from brim-full to 200 mm freeboard in calm water within the time | 15 | max | min | Analysis (LVH-CAL-001, estimate), TRL 3; timed trial, TRL 4 | Met on paper (estimate): about 11 min from brim-full at a sustained 50 L/min each (LVH-STM-001 S34); about 3 min from the lake-level condition at 100 L/min each; rate to measure in the trial (S17) | R4 |
| PR-005 | UR-005 | Physical architecture | Working space | The kit shall take no more than the share of the inside volume below the gunwale | 10 | max | % | Analysis (LVH-CAL-001), TRL 3; measured on the fitted canoe, TRL 4 | Met: 8.4 % | R5 |
| PR-006 | UR-006 | Materials | Water uptake | The foam shall lose less than the share of its lift to water uptake after 30 days immersed | 5 | max | % of lift | Data sheet (LVH-STM-001 S8), TRL 3; immersion and weighing of samples, TRL 4 | Met on supplier data (under 2 % by volume, about 2 % of lift); to confirm by test | R6 |
| PR-007 | UR-007 | Safety | Fixing strength | Each fixing shall hold its share of the full lift times the factor without pull-out | 2 | min | factor | Analysis (LVH-CAL-001, LVH-STM-001 S11 to S13), TRL 3; CalRig proof load of a batten, screws and strap, TRL 4 | Met on paper: lowest factor 5.0 (coach screw); chock screws now 31 mm into the batten | R7 |
| PR-008 | UR-008 | Usability | Fitting time | A local builder and a helper shall fit the kit with hand tools, modules made beforehand, within the time | 8 | max | h | Analysis (LVH-CAL-001, estimate), TRL 3; timed fitting with the partner builder, TRL 4 | Met on paper (estimate): about 6.7 h | R8 |
| PR-009 | UR-009, UR-006 | Materials | Durability | The kit shall show no cracking, tearing or loss of lift after the period of normal use | 12 | min | months | Field inspection of pilot canoes, TRL 5 and later | To verify at TRL 4: cannot be shown on paper (LVH-STM-001 S10, S23) | R9 |
| PR-010 | UR-010 | Cost | Cost | Parts for kits on two canoes shall be reported against the value-engineering target | 1,000 | target | USD | Costed bill of materials, TRL 3 | Over target: USD 1,384, over the value-engineering target by USD 384 (four bailers per canoe since D-O3) | R10 |
| PR-011 | UR-011, UR-001 | Performance | Reserve lift | The swamped canoe shall carry at least the multiple of the design net load at 50 mm freeboard | 1.5 | min | times | Analysis (LVH-CAL-001), TRL 3; swamp test with added weights, TRL 4 | Met on paper: 2.45 | R11 |
| PR-012 | UR-012 | Safety | Damage tolerance | The canoe shall still float with the largest module lost and 5 % water uptake | 0 | min | mm lowest freeboard | Analysis (LVH-CAL-001), TRL 3; swamp test with one module removed, TRL 4 | Met on paper: 25 mm, 1.5 deg heel | R12 |
| PR-013 | UR-013 | Safety | Crew on one side | Heel shall stay within the limit with all four crew holding one grab line | 10 | max | deg | Analysis (LVH-CAL-001), TRL 3; swamp test, TRL 4 | Met on paper: 3.9 deg (low-side freeboard 44 mm) | R13 |
| PR-014 | UR-014, UR-005 | Physical architecture | Inside the hull lines | No buoyancy part or fixing of the kit shall stand outside the canoe's beam over the rubbing strakes (the grab lines and their eyes, which are hand holds, may stand up to 50 mm outside) | 0 | max | mm outside | Inspection of the model and drawing (LVH-DWG-001), TRL 3; inspection of the fitted canoe, TRL 4 | Met by design: modules, battens and straps inside the hull; grab lines and eyes stand about 45 mm outside the strake | new |
| PR-015 | UR-015 | Safety | Life jacket message | Every document, the fitting guide and the kit itself shall state that the kit never replaces life jackets | 100 | min | % of documents and kits | Inspection, TRL 3 (documents) and TRL 4 (kit marking) | Met by design for the documents; kit marking to add with the freeboard marks at TRL 4 | new |
| PR-016 | UR-016 | Software | Sizing calculator | An open calculator shall give the module run per side for another hull from its length free of thwarts, beam, depth, motor and crew | 1 | min | calculator | Inspection of `docs/04-calcs/sizing.py` (LVH-CAL-001 section 8), TRL 3; check against measured hulls, TRL 4 | Met by design: sizing sheet for 6.5, 8.0 and 10 m canoes | new |
| PR-017 | UR-008 | Physical architecture | No holes below the waterline | No new hole in the hull shall lie below the loaded waterline of the dry canoe | 0 | max | holes | Analysis on the model (LVH-STM-001 S19), TRL 3; inspection, TRL 4 | Met on paper: only the eight eye bolt holes, 450 mm above the 175 mm loaded waterline; coach screws stop 12 mm short of the planks | new |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Modules 220 mm wide by 200 mm high (widened from 200 mm on Amish's decision 10A of 2026-10-03: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A").
- Reference canoe: planked, flat bottom 0.8 m wide, sides flared 31.6 deg, frames 50 x 60 mm at 600 mm, thwarts at 1.2, 3.0 and 4.8 m from the transom.
- Wet hull timber is counted as exactly as dense as water (no net lift from the hull).
- A crew member holding on with head and shoulders out puts 20 % of a 75 kg body on the canoe.
- Closed-cell polyethylene foam of about 30 kg/m3 with low water uptake is available to the first partner (data sheets give under 2 % by volume after 28 days).
- "Swamped" means the water inside flows freely between the inside and outside of the canoe, as in the USCG level flotation test (33 CFR 183.220(g)).
- Owners accept 8.4 % of the inside volume, high along the sides, in exchange for flotation.
- The USCG level flotation method is adapted as a design benchmark only; the kit is not certified to it.
