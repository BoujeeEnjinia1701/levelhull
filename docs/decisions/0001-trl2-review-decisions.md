---
doc_id: LVH-DDR-001
title: LevelHull TRL 2 review decisions
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
  change: TRL 2 review items decided under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The scaffold (LVH-PRB-001, LVH-PRC-001 and LVH-REQ-001, all v0.1) described foam blocks or sealed chambers "strapped and fixed low along both inside faces" of a wooden canoe, sized by a sheet from the hull and motor. It left five open questions: whether low placement gives enough roll stability when swamped, foam or chambers, how much lift the wood gives and what the motor changes, a re-entry step, and promotion without implying that life jackets are optional. Populating the concept to TRL 2 meant settling these. Amish pre-approved every recommendation in this batch, so each item below is decided, not proposed. Items that touch safety take the conservative option and say what evidence would relax it. Partners are the first candidates to approach, not agreements.

## Options considered

*Table 1. Options.*

| # | Item | Options |
| --- | --- | --- |
| D1 | Where the modules go | (a) low along the sides or on the floor; (b) high under the gunwale, cutting the swamped waterline; (c) split between the two |
| D2 | Buoyancy material | (a) closed-cell polyethylene foam in covers; (b) sealed rigid chambers (drums, jerrycans, welded HDPE); (c) polystyrene or polyurethane foam |
| D3 | Lift from the wooden hull | (a) count a typical timber density; (b) count none (wet timber as dense as water) |
| D4 | Design case | (a) a generic sheet only; (b) one reference canoe checked in full, with a calculator for other hulls |
| D5 | Crew load | (a) crew aboard the swamped canoe; (b) crew in the water holding on, 20 % of body weight each |
| D6 | Re-entry step | (a) add one; (b) keep it parked |
| D7 | Something for the crew to hold | (a) the gunwale only; (b) grab lines along both sides |
| D8 | Life jacket message | (a) in the documents only; (b) in every document, the fitting guide and the swamp test rules |
| D9 | Co-design partner | Beach management units, fisheries research institutes, sea-safety programmes, canoe builders' groups |
| D10 | Requirements | Keep R1 to R10 and add reserve, damage tolerance and crew-on-one-side requirements |

## Decision

- **D1 (b).** Modules high under the gunwale. In LVH-CAL-001 the same foam on the floor gives 17 kg m per radian of roll stiffness against 742, and the canoe rolls over with the crew on one side. This is the conservative choice; it would be reconsidered only if a swamp test showed a low arrangement stable with the motor and crew on one side.
- **D2 (a).** Closed-cell polyethylene foam, about 30 kg/m3, in sewn PVC tarpaulin covers. A puncture loses no lift and nothing needs sealing. Polystyrene is excluded because fuel dissolves it, and open-cell or poured polyurethane because it soaks up water. Sealed chambers would be reconsidered only after pressure, drop and 12-month ageing tests show they hold air when knocked and sun-baked; they stay with the sibling LaneSkiff concept.
- **D3 (b).** No lift counted from the hull: wet timber is taken as exactly as dense as water. Conservative; it would be relaxed for a given canoe only by weighing the hull and measuring its timber volume, or by a float test of the bare hull.
- **D4 (b).** The reference canoe is 8.0 m long, 1.6 m in beam and 0.65 m deep, flared 31.6 deg, with a 15 hp outboard and four crew. `docs/04-calcs/sizing.py` is the open calculator for other hulls.
- **D5 (b).** Crew in the water holding on, 15 kg each at the gunwale. Bailing is checked with all crew back aboard.
- **D6 (b).** The re-entry step stays parked (scope unchanged since 2026-09-30).
- **D7 (b).** Grab lines of 12 mm polyester rope along both sides, on four through-bolted eye bolts a side above every waterline.
- **D8 (b).** "Never a substitute for life jackets" in every document and the fitting guide; the swamp test is run with every person in a life jacket and a safety boat standing by.
- **D9.** First candidates to approach, in order (none approached yet): a beach management unit on the Kenyan shore of Lake Victoria with the canoe builders at its landing site; a national fisheries research institute in the region for hull and load surveys; a sea-safety programme that trains fishers in life jacket use.
- **D10.** R1 to R10 kept with fixed targets on the reference canoe; R11 (reserve 1.5 times at 50 mm freeboard), R12 (afloat with the largest module lost and 5 % uptake) and R13 (heel within 10 deg with all crew on one side) added.
- **Unchanged:** the pitch, the problem, the passive no-inflation design-around, the open sizing method, and `budget_usd` (USD 1,000), now read as a value-engineering target.

## Consequences

- The modules take the upper sides of the canoe rather than the floor; they cover 7.6 % of the inside volume and leave 963 mm clear between their tops.
- The modules need a fixing that carries their lift into the frames: shelf battens, coach screws and straps (LVH-DDR-002).
- Kits for two canoes are estimated at USD 1,350, USD 350 over the value-engineering target; Amish's pre-approval accepts the overrun.
- The hull's own lift is an unclaimed margin (about 58 mm more freeboard with typical 750 kg/m3 timber).
