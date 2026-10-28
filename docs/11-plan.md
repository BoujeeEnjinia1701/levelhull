---
doc_id: LVH-PLN-001
title: LevelHull project plan
project: LevelHull
doc_type: Project plan
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade)
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'D-O2, D-O3 and D-R1 decided by Amish (2026-10-25); freeing-port study at TRL 4'
---

# LevelHull project plan

LevelHull is at TRL 3 and stage P3 (design outputs): model at D3 for all three concept options, drawings, priced BOM, build plan and the pipeline documents exist. The next gate is P4 (verification), which is on hold under the portfolio cap; the decisions requested of Amish now are the concept choice between options A and B (LVH-DEC-001 D-O1), which scored within 10 % of each other. D-O2, D-O3 and D-R1 were decided by Amish on 2026-10-25. Method: STANDARDS sections 19 and 23.

> **Safety:** P4 work (pull tests, swamp tests) only starts on Amish's go and only under the safety stops of LVH-BLD-001 section 6: sheltered shallow water, a safety boat and every person in a life jacket.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept choice | Amish | Decision D-O1 (A or B) | Awaiting Amish |
| Design and model | Design lead | `cad/src/model.py`, D3 for A, B and C | Done (P3) |
| Calculations and STEM check | Design lead | LVH-CAL-001, LVH-STM-001 | Done; three field items open |
| Requirements and traceability | Design lead | LVH-URS-001, LVH-PRS-001, LVH-RTM-001 | Done; PR-014 to PR-017 accepted by Amish, 2026-10-25 |
| Build plan | Design lead | LVH-BLD-001 | Done (plan, not yet built) |
| Partner and approvals | Project lead | A partner BMU; the KMA question (LVH-REG-001 G1) | Not started |
| Renders and storefront | Coordinator | Options picture, product renders, cards (on Amish's Mac) | To do |

## Resources needed

Table 2. Resources (P4 and later on hold).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Co-design partner (BMU and canoe builders) | Hull and load survey; first fitting | 5 to 10 days | To assess |
| Kit parts for two canoes | Prototype kits | | 1,360 (BOM; value-engineering target 1,000) |
| CalRig proof-load rig | Fixing pull and proof tests (P4) | 2 days | To assess |
| Safety boat and crew | Swamp tests (P4) | 2 days | To assess |
| Regulatory adviser | KMA approval question | 1 to 2 days | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Done (2026-10-24) |
| P1 Definition | URS, PRS draft, RSK with hazards, MKT | Done (2026-10-24) |
| P2 Design inputs | PRS with targets, CAL, RTM, concept selection DDR, STEM check closed where calculation can close it | Done; concept choice awaiting Amish (LVH-DDR-004) |
| P3 Design outputs | Model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability | Done (2026-10-24) |
| P4 Verification | Pull tests, proof load, swamp tests, immersion of foam samples (TST) | On hold (cap P3) |
| P5 Validation | Field trial with a partner fishery, durability over 12 months (PR-009) | On hold |
| P6 Commercialization | Builder training pack, only with a named deployment partner | On hold |

## Next steps and decision requested

1. **Amish:** choose between option A (the design) and option B (external sponsons), or keep A and consider lowering its modules by about 40 mm (B's lesson); LVH-DEC-001 D-O1, LVH-DDR-004.
2. Done 2026-10-25: R2 and R3 stated for the free-flooding condition with the operating rule (D-O2; freeing ports studied at TRL 4 with the partner), four bailers (D-O3), PR-014 to PR-017 accepted (D-R1).
3. **TRL 4, with the partner:** study one-way freeing ports (D-O2 (a)) and time the bail-out from brim-full with four bailers.
4. Coordinator: render the options picture and product renders from the exported scenes.
5. When the cap allows: approach the first partner candidate and put the KMA question.

## References

- FAO, ILO and IMO. *Safety Recommendations for Decked Fishing Vessels of Less than 12 metres in Length and Undecked Fishing Vessels*. Rome: FAO, 2012. https://www.fao.org/4/i3108e/i3108e00.htm. Accessed October 25, 2026.
- Google Patents. "US9139267B2." https://patents.google.com/patent/US9139267B2/en.
- ISO. *ISO 12217-1:2022, Small craft: Stability and buoyancy assessment and categorization, Part 1*. Scope at https://www.evs.ee/en/iso-12217-1-2022. Accessed October 25, 2026.
- KB Packaging. "Foam Sheet 2000mm x 1200mm x 50mm." https://kbpackaging.com/product/foam-sheet-2000mm-x-1200mm-x-50mm/. Accessed October 25, 2026.
- Kenya. *The Merchant Shipping (Small Vessel Safety) Regulations*. Legal Notice 114 of 2012. https://new.kenyalaw.org/akn/ke/act/ln/2012/114/eng@2022-12-31. Accessed October 25, 2026.
- Ravago Building Solutions. "Ethafoam Technical Data Sheet." https://ravagobuildingsolutions.com/gr/wp-content/uploads/sites/47/2022/01/tds-ethafoam-eng.pdf. Accessed October 25, 2026.
- RNLI. "Sustainable Lifesaving Equipment." https://rnli.org/what-we-do/international/lifesaving-interventions/sustainable-lifesaving-equipment.
- The Conversation. "Lake Victoria: Why So Many Fishers Are Dying and What Can Be Done about It." https://theconversation.com/lake-victoria-why-so-many-fishers-are-dying-and-what-can-be-done-about-it-232006.
- US Coast Guard. *Safe Boating: Flotation* (33 CFR 183.220 to 183.235). https://www.uscgboating.org/assets/PDF/downloads/FLOTATION.pdf. Accessed October 25, 2026.
- Winter, David A. *Biomechanics and Motor Control of Human Movement*. 4th ed. Hoboken: Wiley, 2009.
- Zoro. "Onyx Life Jacket, Adult, Universal, 15.5 lb, Foam." https://www.zoro.com/i/G305778328/. Accessed October 25, 2026.
- CEN. EN 1995-1-1, *Eurocode 5: Design of Timber Structures, Part 1-1*; EN 338, *Structural Timber: Strength Classes*.
