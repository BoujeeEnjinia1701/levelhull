---
doc_id: LVH-DEC-001
title: LevelHull design decisions register
project: LevelHull
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; all decisions made under Amish's 2026-10-03 pre-approval
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Decision 10A recorded (modules widened for R12 and R13, LVH-DDR-003); value engineering updated
---

# LevelHull design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several entries below set safety limits (where the modules sit, no credit for the wood, screws kept out of the planking, the pull test and the swamp test rules). Each takes the conservative option and names the evidence that would relax it. LevelHull is never a substitute for life jackets.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval and his requirement decisions of 2026-10-03.

## To confirm when parts are bought

These are facts that can only be settled with real parts, a real canoe or the first partner. None changes a decision; each may change a size or a limit.

*Table 1. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Foam: density about 30 kg/m3, water uptake under 1 % by volume, fuel resistance, on the supplier's data sheet; then 30 days immersion of samples | R6, and every freeboard figure | LVH-CAL-001, A6; LVH-DDR-002, A4 |
| 2 | First canoes: frame spacing (600 mm assumed) and depth (60 mm), side slope, thwart positions, timber, gunwale and strake sizes | Batten height, screw length, module lengths and the gauge | LVH-DDR-002, A1 |
| 3 | Hull mass and timber volume of the first canoes | Size of the unclaimed wood margin (D3) | LVH-DDR-001, D3 |
| 4 | Condition of the frame-to-plank fastenings | Each frame takes up to 0.19 kN of lift | LVH-DDR-002, A3 |
| 5 | Webbing breaking strength (10 kN assumed), D-ring pair (4 kN) and coach screw sideways strength in the canoe's timber (1.5 kN) | R7 factors | LVH-CAL-001, section 7 |
| 6 | Real motor mass and the gear, catch and crew of the partner's fishery | Design net load of 118 kg | LVH-CAL-001, A3 to A5 |
| 7 | Bailing rate with the local bailer (100 L per minute per person assumed) | R4 | LVH-CAL-001, A8 |
| 8 | Price of polyethylene foam sheet near the first fishery (USD 55 a sheet assumed) | Foam is 48 % of the kit cost | `bom/bom.csv`, line 5 |

## Value engineering

Value-engineering target: USD 1,000 (a hypothetical control target, not a limit) for the kits for two prototype canoes. Estimated cost of the constructable design: USD 1,360 (USD 360 over the target); one kit is USD 682. Main cost drivers and savings worth trying:

- The largest lines are the foam (USD 330 a kit, six sheets), the tarpaulin covers and their sewing parts (USD 100), the battens (USD 56) and the coach screws (USD 43).
- Savings worth trying: buy foam by the block from a fishing-float or packaging maker and cut it locally (perhaps USD 100 a kit); hot-galvanised screws and D-rings in place of stainless where the canoe is used in fresh water (about USD 30); covers from used truck tarpaulin in good condition (about USD 50); a three-layer module on hulls whose weighed timber gives a proven wood margin (D3), cutting foam by a quarter.
- The gauge is made once per hull shape and the calculator is free, so a builder fitting a fleet of the same canoe spreads those costs.

## Decisions made

*Table 2. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D10: modules high under the gunwale, not low; closed-cell polyethylene foam in covers, not chambers or polystyrene; no lift counted from the hull timber; one reference canoe (8.0 m, 15 hp, four crew) with an open calculator for others; crew in the water at 20 % of body weight; re-entry step stays parked; grab lines along both sides; life jacket message in every document and test; first co-design candidates (a beach management unit on the Kenyan shore of Lake Victoria with its canoe builders, a regional fisheries research institute, a sea-safety programme; none approached yet); R11 to R13 added; pitch, problem, design-arounds and budget unchanged | Amish, pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | LVH-DDR-001 |
| 2026-10-03 | Design for construction, changes C1 to C12: modules high on the frame faces; four modules a side between thwarts; parallelogram stacks of equal strips; shelf battens; coach screws into frames only, 10 mm short of the planks; end chocks; webbing loops with D-ring buckles in the bays; no glue; sewn tarpaulin covers; setting gauge; grab-line eye bolts above the waterline; freeboard marks and bailers | Amish, same pre-approval | LVH-DDR-002 |
| 2026-10-03 | Assumptions A1 to A5: frames at most 600 mm apart and 60 mm deep, else shorter screws and a third frame, never through the planks; timber as dense as water; sound frame fastenings checked before fitting; foam data to confirm; fixing strengths to confirm | Amish, same pre-approval | LVH-DDR-002 |
| 2026-10-03 | No fishing use before the batten pull test, a one-bay proof load to twice the full lift, and a swamp test in sheltered shallow water with a safety boat and every person in a life jacket (conservative; a gate, not relaxed) | Amish, same pre-approval | LVH-BLD-001, sections 5 and 6 |
| 2026-10-03 | Crews spread along both grab lines: with all four on one side the low gunwale comes within 31 mm of the water (44 mm with the wider modules of LVH-DDR-003) (conservative; relaxed only if a swamp test shows more) | Amish, same pre-approval | LVH-CAL-001, section 4 |
| 2026-10-03 | Appearance model departures: a sand beach slab and a 1.75 m mannequin beside the canoe, and a repeated cut-back module bay for the detail view, drawn for the renders only; canoe topsides shown painted | Amish, same pre-approval | docs/REVIEW.md, TRL 3 section |
| 2026-10-03 | Decision 10A for R12 and R13: foam modules enlarged about 10 % by widening them from 200 to 220 mm (height, lengths, positions and fixings unchanged). R12: 25 mm lowest freeboard with the largest module lost (was 9 mm); R13: 3.9 deg heel, 44 mm on the low side (was 4.0 deg, 31 mm); kit 68.9 kg; USD 1,360 for two canoes | Amish, 2026-10-03: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | LVH-DDR-003 |
