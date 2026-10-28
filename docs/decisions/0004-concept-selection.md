---
doc_id: LVH-DDR-004
title: LevelHull concept selection
project: LevelHull
doc_type: Design decision record
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: Concept selection argued (kit 1.9.1 upgrade); A and B within 10 %, both to Amish
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Option A cost USD 694 (four bailers, D-O3); the selection itself stays proposed, awaiting Amish (no pick)'
---

# 0004: Concept selection

- **Date:** 2026-10-24
- **Status:** proposed. **Proposed, awaiting Amish.** No option is picked: options A and B scored within 10 % of each other, so both go to Amish (STANDARDS section 21). Until he decides, the repo stays on option A, its existing design.

> **Safety:** Whichever option is chosen, it is flotation for the boat and never a substitute for life jackets.

## Context

LevelHull was designed before kit 1.8, so its existing design (foam modules high inside the hull, LVH-DDR-001 to LVH-DDR-003) is option A. Kit 1.8 asks for at least two concepts with different working principles, scored against the user requirements (LVH-URS-001). Two more were developed and modelled at D3 in `cad/src/model.py`: B, the same foam carried outside the hull as sponsons, and C, double outrigger floats. Their swamped performance was solved with the method of LVH-CAL-001 (`docs/04-calcs/stem_check.py`).

## Options considered

Table 1. Summary (full scoring in LVH-OPT-001 Table 2).

| | A: foam modules high inside | B: external foam sponsons | C: double outrigger floats |
| --- | --- | --- | --- |
| Weighted score (of 215) | 172 (80 %) | 163 (76 %) | 148 (69 %) |
| Swamped lowest freeboard | 92 mm | 158 mm | 160 mm |
| Roll stiffness | 761 kg m per radian | 1,546 | 6,313 |
| Largest unit lost | Afloat, 25 mm | Gunwale 32 mm under | Capsizes |
| Inside volume taken | 8.4 % | None | None |
| Beam | 1.68 m | 1.93 m | 4.45 m |
| New hull holes | 8 in the top plank | 32 through the planks | 16 through the strakes |
| Cost per canoe | USD 694 | About USD 620 (estimate) | Pipe price to assess |

## Recommendation

Both A and B go to Amish:

- **A** if keeping the canoe's lines, the fewest hull holes and survival with one module lost matter most. It is already constructable, priced and planned.
- **B** if freeboard, roll stiffness and an empty inside matter most, accepting 32 bolt holes through the planks, a wider canoe, exposed covers and a redesign of the sponson split to meet R12.

C is not put forward: it scores lowest, a lost float capsizes the canoe, and its 4.45 m beam and booms conflict with landing and net handling; its strength, intact stability, needs the outriggers themselves and cannot be grafted.

**Graft from the runner-up (for Amish with this decision).** B shows that the same foam gives more freeboard when it sits lower while still cutting the waterline. Lowering A's modules and battens by about 40 mm (top 70 mm below the gunwale) would raise A's swamped freeboard at some cost in clear width and roll stiffness; it changes a design dimension, so it is offered as an option to the decision, not made.

## Consequences

- `project.yaml`: `concept_options: [A, B, C]`; `concept_chosen` left as "A (proposed)".
- LVH-DEC-001: open decision D-O1.
- The drawing, priced BOM and build plan stay on option A until Amish decides; if he picks B, those are redone for B and a design-for-construction record follows.
