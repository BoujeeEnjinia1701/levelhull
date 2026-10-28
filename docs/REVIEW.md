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

## Session 2026-10-24: kit 1.9.1 upgrade

Run on Amish's instructions of 2026-10-24 ("Kit 1.9.1 rollout - proceed to rollout across the other repos"; "I want detailed TRL3 CAD"; "Detail every option") and his standing instruction of 2026-10-23 (fix a failed STEM row in the same session). Kit 1.9.1 was installed by the coordinator. Committed, not pushed.

### What was added

- **STEM check:** `docs/01b-stem-check.md` (LVH-STM-001 v0.1) with `docs/04-calcs/stem_check.py`, `stem_results.csv` and `options_results.csv`: 34 claims across physics, chemistry, biology, mathematics and engineering, for option A (the design) and options B and C.
- **Concept options:** `docs/02a-concept-options.md` (LVH-OPT-001), `docs/decisions/0004-concept-selection.md` (LVH-DDR-004). A is the existing design; B, external foam sponsons; C, double outrigger floats.
- **Requirements:** `docs/03a-user-requirements.md` (LVH-URS-001, 16 URs), `docs/03-requirements.md` migrated from LVH-REQ-001 to LVH-PRS-001 v0.4 (R1 to R13 become PR-001 to PR-013 with the same targets; PR-014 to PR-017 proposed), `docs/03b-traceability.md` (LVH-RTM-001, generated, 0 gaps). Users-and-needs and stakeholder tables added to `docs/01-problem.md` (v0.4).
- **Pipeline documents:** `docs/07-regulatory.md` (REG), `docs/08-feasibility.md` (FEA), `docs/09-risk.md` (RSK with hazard analysis and design FMEA), `docs/10-market.md` (MKT), `docs/11-plan.md` (PLN). Regulatory and market facts cited with links, checked 2026-10-25.
- **Detailed CAD (kit 1.9):** `cad/src/model.py` now defines `PARAMS`, `OPTIONS`, `PRINCIPLES`, `CHOSEN = "A"`, `OPTION_VIEWS` and `components(option)`; repo helpers in `cad/src/lvh_parts.py` (wide washers, eye bolts, nyloc nuts, wood screws, D-ring buckles, U-bolts, fusion beads). Option A keeps every design dimension; the envelope model (`build_kit`) that `sizing.py` reads is unchanged, and `detail_kit()` gives the drawing and picture scripts the detailed parts. `cad/fidelity.json` passes at D3; per-part STEP in `cad/step/A/`, assemblies `cad/step/A-assembly.step`, `B-assembly.step`, `C-assembly.step`; STL at 0.15 mm chord.
- **Regenerated from the model:** `cad/drawings/LVH-DWG-001` Rev P4 (section A-A moved clear of the revision table), making sketches LVH-DWG-101 to 106, the build plan overview, joints and steps, concept media (`media/hero.png`, `cutaway.png`, `exploded.png`, blueprint, `model.glb` and `viewer.html`).
- **Product model:** `cad/src/product_model.py` rebuilt from `components(CHOSEN)`: RENDER_VIEWS `hero` (site scene on a sand beach, `--scene=outdoor --ground=sand --ground-z=0 --sun=38,-48 --lens=35`, outboard tilted up, 1.75 m mannequin standing on the sand), `studio`, `exploded`, `detail`. Ground level is z = 0, the outside of the canoe's bottom. Appearance departures (render only), **proposed, awaiting Amish**: beach slab, mannequin, tilted motor, canoe topsides painted blue.
- **Other updates:** LVH-CAL-001 v0.3 (section 10, corrections), LVH-PRC-001 v0.4, LVH-BLD-001 v0.3 (chock screws, A4 only), LVH-DEC-001 v0.3, `bom/bom.csv` converted to the kit 1.9 `item` format (two rows with unquoted commas repaired; line 3 A4 only; line 4 counterbored screws), README in the house structure (stage badge, links line, STEM check and Concept options sections; the broken Zenodo badge, which held a GitHub API error message, replaced by the DOI badge for 10.5281/zenodo.23128819), `project.yaml` (`stage: P3`, `stem_check: open`, `concept_options: [A, B, C]`, `concept_chosen: A (proposed)`, evidence).

### STEM verdicts and fixes

- 27 within known science, 5 plausible (S10 cover and webbing UV life, S17 sustained bailing rate, S23 decay at screw holes, S27 option B abrasion, S33 roll of a sealed hull brim-full), 2 fail with a fix proposed to Amish (S32, S34), 0 fail. `stem_check: open`.
- Fixed under the standing instruction (LVH-DEC-001): **D-S1**, end chock screws went 10 mm into the batten; now driven parallel to the frame face in 12 mm counterbores 30 mm deep, 31 mm into the batten, no cost change. **D-S2**, galvanised coach screws withdrawn (tannins attack zinc); A4 only.
- New results: straight after swamping, a sealed canoe filled to the brim floats about 24 mm up level, about 3 mm at its lowest point, and is near neutral in roll until bailed or until it spills over the low gunwale (S2, S32, S33); 76 mm with 20 % more load and 5 % less foam lift (S7); 75 and 57 mm with wet timber at 1,100 and 1,200 kg/m3 (S31); partly bailed metacentric height 0.14 m (S18); loaded dry draft 175 mm, eye bolt holes 450 mm above it (S19).
- Independent review: a separate headless Claude session (`claude -p`, no tools) saw only the STEM check, CAL, PRS and `sizing.py`. It upheld the arithmetic and refuted or weakened several rows; changes are in LVH-STM-001 "Independent review". Main consequences: the sealed-hull rows S32 to S34; S2 wording; timber density sweep S31; corrected floor comparison in `sizing.py` (the floor case used the high modules' waterplane: now 135 kg m per radian and 22 deg, was 283 and 10.6 deg); denser-than-water timber now carries its weight moment in the trim; fitting time 6.7 h with the counterbores; S11 and S9 text; D-S2. Not checked yet (open items): dynamic slam loads on the fixings, frame-to-plank fastenings, foam creep under strap tension, dry-canoe stability with the kit.

### Option scores (LVH-OPT-001)

| Option | Score (of 215) | Parts (D3) | Model mass |
| --- | --- | --- | --- |
| A, foam modules high inside (the design) | 172 | 209 | 99.3 kg |
| B, external foam sponsons | 163 | 124 | 98.7 kg |
| C, double outrigger floats | 148 | 124 | 159.9 kg |

A and B are within 10 % (5.2 %), so both go to Amish without a pick. Model masses come from `cad/fidelity.json`; they overstate the foam, which the kit's material list has only at 120 kg/m3 (real 30 kg/m3): the calculated kit mass of A is 68.9 kg.

### Requirements not met or at risk

- PR-002 (R2, 50 mm freeboard) and PR-004 (R4, bail in 15 min): **at risk** for a sealed hull just after swamping (about 3 mm at the lowest point brim-full; about 22 min to bail from brim-full at 50 L/min each). Met on paper in the free-flooding condition of the USCG method.
- PR-003 (R3, level): met with free exchange; brim-full roll behaviour to confirm by test.
- PR-010 (R10): over the value-engineering target: USD 1,360 for two canoes against USD 1,000 (USD 360 over); USD 682 per kit. `budget_usd` unchanged.
- PR-009 (R9) and the test half of PR-006: cannot be shown on paper.

### Decisions awaiting Amish (LVH-DEC-001)

- **D-O1** concept choice: A or B (or A with its modules about 40 mm lower, B's lesson).
- **D-O2** sealed hull after swamping: freeing ports with one-way flaps above the dry waterline, or R2 and R3 restated for the free-flooding condition with an operating rule.
- **D-O3** bailing from brim-full: four bailers (about USD 12 more) or R4 restated.
- **D-R1** PR-014 to PR-017, added in the migration.
- Appearance departures of the product model (above).
- REG G1: whether fitting needs Kenya Maritime Authority approval, to assess with a partner.

### Safety

- Unchanged: flotation for the boat, never a substitute for life jackets; swamp tests only in sheltered shallow water with a safety boat and everyone in life jackets. New: crews should expect a canoe nearly awash straight after swamping and should bail at once, seated (RSK H2, H6).

### Kit bugs met

- `cad_check.py` reads BOM line numbers only from an `item` column that starts with the number; kit 1.7 BOMs use a separate `line` column, so every part reads as missing until the BOM is converted. Converted in the repo; `sizing.py` updated.
- `cad_parts.MATERIALS` has no closed-cell foam (about 30 kg/m3), so foam is modelled as `insulated_white` (120 kg/m3) and `fidelity.json` masses overstate the foam about fourfold.
- build123d 0.13 reports zero volume for a compound that contains a compound, so `build_views._has_volume` and `concept._render` drop or fail on such parts (an exploded view failed with a broadcast error). Worked around in the repo by flattening compounds to their solids (`lvh_parts.d_ring_pair`, `build_plan_media.CF`, `concept_media`).
- `render.py --check` requires `media/options.png`, which only `options.py` (Blender, on Amish's Mac) makes; the repo had none, so the check fails on that line until the coordinator renders it. Option scenes are exported for the coordinator (see the final report).

### Recommended next step

Amish decides D-O1 to D-O3; the coordinator renders the options picture and the product renders. TRL 4 work (pull tests, swamp test of a sealed hull) waits for his go.

## Session 2026-10-25: decisions

Amish, 2026-10-25 10:19 CT, after a report listing each repo's proposed decisions and recommendations: "i concur with your recommendations". Every decision that carried a recommendation is recorded as decided with the option recommended; every decision without a pick stays open.

### Decided by Amish, 2026-10-25

- **D-O2 sealed hull after swamping:** option (b). PR-002 and PR-003 are stated for the free-flooding condition of the USCG method, with the operating rule "hold on, then bail at once, seated" (build plan step 10; RSK H2). PR-002 **at risk to met on paper** (92 mm lowest in the free-flooding condition; brim-full still about 24 mm level and 3 mm at the lowest point until bailed). STEM S32 from "fails, fix proposed" to Within known science. Freeing ports studied at TRL 4 (PLN).
- **D-O3 bailing from brim-full:** option (a), four bailers. `cad/src/model.py` `bailers_x` 2400, 4200 to 1800, 2400, 3600, 4200 mm (two more buckets and lanyards in the D3 model); `bom/bom.csv` line 12 qty 2 to 4 (USD 6 each, +USD 12 a kit); `sizing.py` `bailers` 2 to 4: B4 from the lake-level condition 5.9 to **2.9 min**; brim-full at 50 L/min each 22 to **about 11 min** against 15 (STEM S34 now Within). PR-004 restated for the four crew with four bailers, from brim-full, **at risk to met on paper**. Kit USD 682 to **USD 694**, two canoes USD 1,360 to **USD 1,384** (USD 384 over the USD 1,000 target; `budget_usd` unchanged). Build plan section 3.9, step 10, bail-out check and the overview picture.
- **D-R1:** PR-014 to PR-017 accepted as written.
- **Appearance departures of the product model** (beach slab, mannequin, tilted outboard, blue topsides): accepted. No change.
- Documents: LVH-PRS-001 v0.5, LVH-STM-001 v0.2 (29 within, 5 plausible, 0 fail; `stem_check` stays open on the plausible rows), LVH-CAL-001 v0.4, LVH-DEC-001 v0.4, LVH-BLD-001 v0.4, LVH-RSK-001 v0.2, LVH-PRC-001 v0.5, LVH-OPT-001 v0.2, LVH-DDR-004 v0.2, LVH-MKT-001 v0.2, LVH-PLN-001 v0.2, README.

### Still open (no recommendation to concur with)

- **D-O1 concept:** A (172) and B (163) are within 10 % and went to Amish without a pick; `concept_chosen` stays "A (proposed)".
- **REG G1:** whether fitting needs Kenya Maritime Authority approval, to assess with a partner (no recommended answer).

### Checks

Run in this order on 2026-10-25 after the last edit to `cad/src/` and `bom/bom.csv`:

- Regenerated: LVH-DWG-001 Rev P5 (four bailers), build plan overview and steps, concept media.
- First `cad_check.py --export` after adding the two bailers failed: the outer bailers' lanyards ran through the inner buckets (about 410 to 450 mm3). Fixed in `cad/src/model.py`: the outer pair's lanyards run on the other side of the centreline to the thwart; the GA was redrawn after the fix.
- `python3 docs/04-calcs/sizing.py`: runs; B4 2.9 min, kit USD 694, two canoes USD 1,384.
- `python3 docs/04-calcs/stem_check.py`: open, 29 within, 5 plausible, 0 fail.
- `python3 .kit/trace.py`: RTM up to date, 0 gaps.
- `python3 .kit/cad_check.py --export`: PASS at D3 (option A 213 parts).
- `python3 .kit/render.py` and `python3 .kit/render.py --check`: the only FAIL is the expected missing `media/options.png` (Mac render); `render.py` stops there, so `docs/pdf/` is not refreshed.
- `python3 -m reuse lint`: compliant.
- Em and en dash scan outside `.kit/` and `LICENSES/`: none.
