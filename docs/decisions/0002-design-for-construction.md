---
doc_id: LVH-DDR-002
title: LevelHull design for construction
project: LevelHull
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Design made constructable; changes C1 to C12 and assumptions A1 to A5 decided under Amish's 2026-10-03 pre-approval
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: C3 cross-referenced to LVH-DDR-003 (modules widened to 220 mm)
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

STANDARDS section 18 asks that every part can be made by a stated process and fits and fastens to its neighbours. The TRL 1 concept named "foam blocks in protective covers, strapped and fixed" with "fixing straps and cleats", but said nothing about what the straps pull against, how a block sits on a flared side, or where the lift goes into the hull. The constructability review of the model (`cad/src/model.py`, 126 checks: overlaps with planks, frames and thwarts; contact between module, batten and frames; screw depth in the frames; straps clear of the frames; eye bolts through the strake; gauge fit) led to the changes below. None changes what the product does or its pitch. C1 follows D1 of LVH-DDR-001.

## Changes

*Table 1. Changes made for construction.*

| # | The concept had | The constructable design has | Why |
| --- | --- | --- | --- |
| C1 | Blocks low along the inside faces | Modules high under the gunwale, top 30 mm below it, outboard face on the frames' inner faces | Roll stability when swamped (D1); the frame faces form a flat, regular bearing surface |
| C2 | One block per side, size open | Four modules a side between the thwarts: 880, 1,400, 1,400 and 1,100 mm | Thwarts stay in place; each module is light (under 4 kg) and handled by one person |
| C3 | Rectangular blocks | Parallelogram section 200 x 200 mm (widened to 220 mm by LVH-DDR-003): four equal 50 mm strips with both long edges cut at the flare angle, each layer set 31 mm further out | Sits flat on the sloping frame faces; every strip is the same cut |
| C4 | "Cleats" | A hardwood shelf batten under each module, 50 mm thick square to the frame faces, 70 mm high, 40 mm past each module end | Gives the module a seat and the straps an anchor, and spreads the lift over two or three frames |
| C5 | Fixings unspecified | One M8 x 100 coach screw into every frame a batten crosses, square to the batten face, 50 mm into the frame, tip 10 mm short of the planks | No new holes in the planking below the waterline; screw factor 5.5 on the full lift |
| C6 | Nothing stopping fore and aft movement | End chocks 40 mm long and 50 mm high screwed to the batten at both ends of each module | The straps alone could let a module creep along the batten |
| C7 | "Fixing straps" | Closed loops of 50 mm polyester webbing round module and batten, two per module, in the bays between frames, running outboard of the module in the 60 mm gap at the planks; stainless double D-ring friction buckles | A loop needs no anchor of its own; D-rings have no spring or cam to corrode |
| C8 | Foam blocks | Layers held by the cover and straps, no glue | Polyethylene foam does not glue reliably with common adhesives |
| C9 | Protective covers | Sewn PVC-coated polyester tarpaulin sleeves, 150 mm end flaps laced through eyelets | A tailor or sail maker can make and replace them; foam can be inspected |
| C10 | Hull sizes taken by hand | A plywood setting gauge hooked over the gunwale marks the batten top and bottom on every frame | Every batten at the same height on a hull without drawings |
| C11 | Nothing to hold | Four M8 eye bolts a side through the rubbing strake and top plank, between frames, and a 12 mm grab line in bights | D7; above every waterline |
| C12 | "Freeboard mark", "bailer" | A painted band whose top edge is 50 mm below the gunwale amidships, both sides; two 10 L buckets on lanyards stowed between frames | The R2 check is visible in the swamp test; bailers cannot float away |

## Assumptions decided with the changes

- **A1.** The canoe's frames are at most 600 mm apart and at least 60 mm deep from the planks, so each batten crosses two frames and each screw has 50 mm of wood. Conservative: on a hull with shallower frames the screw is shortened to keep 10 mm clear of the planks and a third frame is added to the batten; never through the planking.
- **A2.** Wet hull timber is as dense as water (D3). Relaxed only by weighing and measuring the hull.
- **A3.** Frame-to-plank fastenings are sound. Each frame takes at most 0.19 kN of lift; fastenings are inspected before fitting and any loose or rotten frame is repaired first.
- **A4.** Foam density 30 kg/m3 and water uptake under 1 % by volume, to confirm from the supplier's data sheet and by immersion at TRL 4.
- **A5.** Strengths of the webbing (10 kN), D-ring pair (4 kN) and coach screw (1.5 kN sideways) to confirm with the parts bought.

## Consequences

- The kit has 13 kinds of part, five of them made (gauge, battens, chocks, cores, covers) with saws, a plane, a drill, a knife and a sewing machine.
- Kit mass 67 kg; the battens are the heaviest part (39 kg with the chocks).
- The general arrangement LVH-DWG-001 is at Rev P2; making sketches LVH-DWG-101 to 106; build plan LVH-BLD-001.
- `design_state: constructable` in `project.yaml`.

> **Safety:** The fixings carry the full lift of a module pushed under water. Every batten is pull-tested by hand and one bay per canoe is proof-loaded to twice its share before the swamp test (LVH-BLD-001, sections 5 and 6).
