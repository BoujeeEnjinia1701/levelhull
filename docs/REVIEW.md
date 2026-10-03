# Review note: LevelHull

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (LVH-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (LVH-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (LVH-REQ-001 v0.1): 10 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## Session 2026-10-03: TRL 2 (populate)

Run as the first half of `/to-trl3` under Amish's pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Kit 1.7.0 installed.

### What was done

- `docs/01-problem.md` (LVH-PRB-001 v0.2): constraints restated (value-engineering target, no new holes below the waterline), open questions settled, first co-design candidates, safety section.
- `docs/02-concept.md` (LVH-PRC-001 v0.2): how it works, components with BOM numbers, key design choices, first-order numbers, design-arounds kept, safety.
- `docs/03-requirements.md` (LVH-REQ-001 v0.2): 13 measurable requirements (R11 to R13 added) with TRL 3 status.
- Concept media from `cad/src/concept_media.py`: `media/hero.png` (1.75 m person for scale), `media/cutaway.png` (a cut across the canoe), `media/exploded.png` (one module bay with BOM callouts), `media/concept-blueprint.png`, `.pdf` and `.svg` (LVH-DWG-010), `media/model.glb` (3.4 MB, coarse tessellation) and `media/viewer.html`. No flow diagram: the kit moves no energy or material.
- `bom/bom.csv`: 14 priced lines.

### Results

- The TRL 1 arrangement (foam low along the sides) does not work: with the same foam on the floor the swamped canoe has almost no roll stiffness and rolls over with the crew on one side. Modules high under the gunwale fix this.

### Requirements not met

- R10: over the value-engineering target (see TRL 3).
- R9 cannot be shown on paper.

### Decisions made under the pre-approval

LVH-DDR-001, items D1 to D10: modules high under the gunwale; closed-cell polyethylene foam in covers; no lift counted from the hull timber; one reference canoe with an open calculator; crew in the water at 20 % of body weight; re-entry step stays parked; grab lines; life jacket message everywhere; first co-design candidates (not approached); R11 to R13 added.

### Safety concerns

- A swamped canoe that floats is still dangerous in breaking waves, at night and in cold water; the kit is never a substitute for life jackets, and it must not be promoted as one.

## Session 2026-10-03: TRL 3 (advance and build plan)

Run as the second half of `/to-trl3` under the same pre-approval, which counts as the TRL 2 approval. Not committed or pushed (batch run).

### What was done

- `cad/src/model.py`: parametric build123d model of the kit in the reference canoe (8.0 m, 1.6 m beam, 0.65 m deep, flared 31.6 deg, 15 hp outboard); 126 of 126 constructability checks pass (overlaps with planks, frames and thwarts; module, batten and chock contact; screw depth in the frames and clear of the planks; straps in the bays; eye bolts through the strake; gauge fit; clear width). Exports `cad/step/levelhull-assembly.step`, `levelhull-kit.step`, `reference-canoe-context.step`, the four foam cores, chock and gauge, and STL of the battens, chock and gauge.
- `docs/04-calcs/01-sizing.md` (LVH-CAL-001 v0.1) with `docs/04-calcs/sizing.py` (also the MIT sizing calculator) and `results.csv`: swamped equilibrium, heel and trim, off-design cases, high against low placement, space and bailing, fixings, fitting time, cost and a sizing sheet for other hulls.
- `cad/src/sheets.py`: general arrangement `cad/drawings/LVH-DWG-001` (SVG, PDF, PNG) at Rev P2, with section A-A at 1:20.
- `cad/src/build_plan_media.py`: `docs/05-build-plan/overview.png`, 6 making sketches `cad/drawings/LVH-DWG-101` to `106`, 6 joint close-ups and 10 step pictures.
- `docs/05-build-plan.md` (LVH-BLD-001 v0.1), `docs/06-design-decisions.md` (LVH-DEC-001 v0.1), `docs/decisions/0001-trl2-review-decisions.md` (LVH-DDR-001) and `docs/decisions/0002-design-for-construction.md` (LVH-DDR-002).
- `cad/src/product_model.py` (appearance model) and render scenes exported with `.kit/export_views.py` to `/home/claude/renders/levelhull` for hero, exploded and detail views; photoreal renders and cards are made on Amish's Mac.
- `project.yaml`: trl 3, trl_target 3, `design_state: constructable`, evidence listed; `budget_usd` unchanged. README leads with `media/render-hero.png` and has a "Building the prototype" section.

### Results

- Eight modules, 200 x 200 mm, 4.78 m a side, 0.38 m3 of foam; kit 67 kg; 7.6 % of the inside volume.
- Swamped at the design load (118 kg net: four crew holding on, 36 kg motor, gear, catch), fresh water, no lift counted from the timber: 105 mm freeboard amidships, 80 mm at the lowest point, trim 0.45 deg; roll stiffness 742 kg m per radian; 2.2 times the design load carried at 50 mm freeboard.
- Same foam on the floor: 17 kg m per radian; rolls over with four crew on one side.
- Four crew on one side: 4.0 deg heel, 31 mm low-side freeboard. Largest module lost and 5 % uptake: still afloat with 9 mm. Typical 750 kg/m3 timber would add about 58 mm.
- Bailing to 200 mm freeboard: about 6 minutes for two crew (estimate). Fixing factors: coach screw 5.5, D-ring 14.6, webbing 73. Fitting about 6.3 hours.
- Value-engineering target: USD 1,000. Estimated cost of the constructable design: USD 1,350 for two canoes (USD 350 over the target); USD 677 for one kit.

### Requirements not met

- R10: over the value-engineering target by USD 350. Foam is 49 % of a kit; the overrun is accepted under the pre-approval and `budget_usd` is unchanged.
- R9 (12 months without loss of lift) and the test half of R6 cannot be shown on paper.
- R12 is met with a small margin (9 mm), and R13 leaves only 31 mm on the low side; both are recorded as operating rules, not redesigned.

### Decisions made under the pre-approval

- LVH-DDR-002: design for construction, changes C1 to C12 and assumptions A1 to A5.
- No fishing use before the pull test, a one-bay proof load and a swamp test with a safety boat and life jackets.
- Crews spread along both grab lines.
- Appearance model departures (renders only): a sand beach slab under the canoe, a 1.75 m mannequin standing beside it, a repeated cut-back module bay for the detail view, and the canoe topsides shown painted blue.

### Build plan findings

- Design changes for construction (2026-10-03), all in LVH-DDR-002: modules high on the frame faces; four modules a side between the thwarts; parallelogram stacks of equal foam strips, no glue; shelf battens; coach screws into the frames only, tips 10 mm short of the planks; end chocks; webbing loops with D-ring buckles in the bays between frames; sewn tarpaulin covers with laced ends; a plywood setting gauge; grab-line eye bolts above the waterline; freeboard marks and bailers on lanyards.
- The only new holes in the hull are the eight eye bolt holes in the top plank, above every waterline.
- Items to confirm with real parts and hulls (foam data, frame sizes, hull mass, frame fastenings, fixing strengths, real loads, bailing rate, foam price) are in LVH-DEC-001.

### Safety concerns

- Flotation for the boat, not for people: never a substitute for life jackets, not certified. Safety stops S1 to S5 in LVH-BLD-001 gate drilling, the first swamp test, entering the water, filling the canoe and fishing use.
- A floating swamped canoe can still roll in breaking waves; the kit buys time to bail and be seen.
- With all crew on one side the low gunwale is 31 mm from the water; crews must spread out.
- The fixings must not tear free: each carries at least twice its share of the full lift on paper, and the pull test and proof load confirm it before any swamp test.

### Recommended next step

The design looks ready for TRL 4 once Amish chooses to start it: fit one kit to a partner's canoe, pull-test and proof-load the fixings with CalRig, and run the first checks in LVH-BLD-001 section 5 in sheltered water with the first co-design candidate.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.

2026-10-03: hero render reframed so the product fills the frame (levelhull).

## 2026-10-03: Amish's requirement decisions carried out

Amish chose option A on every requirement decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". For LevelHull this is decision 10A (R12 and R13): enlarge the foam modules about 10 %. Not committed or pushed (batch run).

### Changes

- Modules widened from 200 to 220 mm (level width), 200 mm high as before; lengths, positions, battens, chocks, screws and eye bolts unchanged (`cad/src/model.py`). 0.42 m3 of module in all (was 0.38 m3). New model check: four strips of the module width come from a 1,000 mm foam sheet. 127 of 127 constructability checks pass. STEP and STL regenerated.
- `docs/04-calcs/sizing.py` takes the module width from the model everywhere (fixing loads, sizing sheet) and now computes the strap webbing (K3) and the floor comparison with 5 kg more load (F20). `docs/04-calcs/01-sizing.md` v0.2 and `results.csv` re-run.
- `bom/bom.csv`: foam strips 216 mm wide, four to a sheet, still six sheets (no spare strip); tarpaulin 14 to 15 m2 at the same USD 5.00 per m2; straps cut 1.25 m (20 m of the 25 m bought).
- `docs/03-requirements.md` v0.3 (targets unchanged, status updated), `docs/02-concept.md` v0.3, `docs/01-problem.md` v0.3, `docs/05-build-plan.md` v0.2 (foam strips, cover panel 1,040 mm wide, straps 1.25 m), README figures, `docs/decisions/0002-design-for-construction.md` v0.2 (cross-reference), new `docs/decisions/0003-wider-modules-r12-r13.md` (LVH-DDR-003), `docs/06-design-decisions.md` v0.2.
- Pictures: general arrangement `cad/drawings/LVH-DWG-001` at Rev P3; making sketches LVH-DWG-101 to 106, overview, joints and steps regenerated (foam core, cover and strap sketches carry the new sizes); concept media (hero, cutaway, exploded, blueprint, `model.glb`). Appearance model scenes re-exported to `/home/claude/renders/levelhull` (hero, exploded, detail).

### New results

- R12 (still floats with the largest module lost and 5 % uptake): 25 mm lowest freeboard, 1.5 deg heel (was 9 mm). Met on paper with a usable margin.
- R13 (heel within 10 deg with all four crew on one grab line): 3.9 deg, low-side freeboard 44 mm (was 4.0 deg and 31 mm). Met on paper; the low side is still under 50 mm, so the rule that crews spread along both grab lines stays.
- Also changed: R2 92 mm lowest freeboard (was 80); R1 and R11 reserve 2.45 (was 2.17); R3 trim 0.39 deg; R5 8.4 % of the inside volume (was 7.6 %); R7 lowest factor 5.0 (coach screw, was 5.5); R4 about 6 minutes; clear width between module tops 923 mm (check 900 mm).
- Kit mass 68.9 kg (was 67.4 kg).
- Value-engineering target: USD 1,000. Estimated cost of the constructable design: USD 1,360 (USD 360 over the target); USD 682 for one kit. `budget_usd` unchanged.
- Floor comparison: with 0.42 m3 the same foam on the floor just reaches the surface (283 kg m per radian, 10.6 deg with the crew on one side, over the 10 deg limit) and has no roll stiffness with 5 kg more load. The case for the high modules (LVH-DDR-001, D1) stands; the "rolls over" wording is replaced in the documents.

### For Amish

- No new decisions. The photoreal renders (`media/render-*.png`), card and social preview still show the 200 mm modules (a 20 mm change, hardly visible at this scale); re-render on the Mac from the re-exported scenes when convenient.

### Safety

- Unchanged: LevelHull is never a substitute for life jackets; swamp tests only in sheltered, shallow water with a safety boat and everyone in life jackets.

## 2026-10-03: photoreal renders redone after Amish's requirement decisions

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
