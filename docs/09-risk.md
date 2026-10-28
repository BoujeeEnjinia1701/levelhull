---
doc_id: LVH-RSK-001
title: LevelHull risk register and hazard analysis
project: LevelHull
doc_type: Risk register and hazard analysis
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade) with project risks, preliminary hazard analysis and a first-pass design FMEA
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'H2 and H6 controls as decided by Amish (D-O2, D-O3), 2026-10-25'
---

# LevelHull risk register and hazard analysis

The top risks are that crews treat the kit as a reason not to wear life jackets (risk compensation), that covers and straps degrade in the sun until a module tears free when it is needed, and that the canoe is nearly awash in the first moments after swamping (about 24 mm freeboard until the water evens out). The design FMEA's highest RPNs are covers degrading unseen under the straps (RPN 75) and strap webbing losing strength in the sun (RPN 60); both are controlled by inspection, not by calculation. Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high; for detection, 5 is hardest to detect).

> **Safety:** LevelHull is flotation for the boat, never a substitute for life jackets. Every hazard below assumes life jackets are worn; the residual ratings do not hold if they are not.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner | No BMU or institute takes part | No real hulls, loads or swamp test; stays at TRL 3 | 3 | 4 | Project lead | Approach the three candidates in LVH-PRB-001 in order |
| P2 | Owners reject the lost space | 8.4 % of the inside volume high on the sides | Kits removed or never fitted | 3 | 4 | Design lead | Show option B to Amish (LVH-OPT-001); measure acceptance in the pilot |
| P3 | Approval needed and slow | Kenyan rules on modifications (LVH-REG-001 G1) | Delay or redesign | 3 | 3 | Partner liaison | Ask the Kenya Maritime Authority early; offer the swamp test as evidence |
| P4 | Foam not available at the assumed grade or price | Local supply of closed-cell PE sheet | Cost or lift changes | 3 | 3 | Design lead | Data sheet and samples before buying; calculator re-run for any density |
| P5 | Cost over the value-engineering target | Foam is 48 % of the kit | USD 360 over for two canoes | 4 | 2 | Design lead | Savings in LVH-DEC-001 (bulk foam, used tarpaulin, galvanised in fresh water) |
| P6 | Misleading promotion | Kit described as lifesaving | Fewer life jackets worn; liability | 2 | 5 | Project lead | PR-015: life jacket message on every document and kit |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Risk compensation | Crews feel safe without life jackets | Drowning if thrown clear of the canoe | 5 | 3 | Message in every document and on the kit; promotion only with life jacket programmes (PR-015, UR-015) | Medium |
| H2 | Canoe nearly awash just after swamping | Water inside trapped above the lake level (LVH-STM-001 S2) | Crew panic, further swamping in waves | 4 | 3 | Operating rule "hold on, then bail at once, seated" (LVH-DEC-001 D-O2, decided 2026-10-25); four bailers, about 11 min from brim-full (D-O3); 92 mm once the water evens out; freeing ports studied at TRL 4 | Medium |
| H3 | Module tears free | Strap, D-ring or cover failure; screws pull out | Loss of lift on one side, heel | 5 | 2 | Fixings at 5 or more times their share (S11, S12); pull test and proof load before use; annual inspection | Low |
| H4 | Capsize in breaking waves | Waves larger than any passive flotation can resist | Crew in the water | 5 | 2 | Kit buys time, not safety; weather warnings; life jackets | Medium |
| H5 | All crew on one side | Crowding at one grab line | Low-side gunwale 44 mm from the water | 3 | 3 | Grab lines on both sides; training to spread out | Low |
| H6 | Instability while bailing | Free surface of the water inside (S18, 0.14 m metacentric height) | Re-swamping, capsize | 4 | 2 | Bail seated and low, two each side with the four bailers (D-O3) | Low |
| H7 | Swamp test accident | Testing a filled canoe | Drowning, cold | 5 | 1 | Safety stops S1 to S5 in LVH-BLD-001: shallow sheltered water, safety boat, life jackets | Low |
| H8 | Workshop injury | Saws, drills, solvents | Cuts, eye injury, fumes | 3 | 2 | Eye protection, ventilation (LVH-BLD-001) | Low |
| H9 | Hull damage when fitting | Screw through the planking | Leak below the waterline | 3 | 2 | Screws stop 12 mm short of the planks; depth flag on the drill (S14, PR-017) | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Foam strips | Give lift | Water uptake, crushing | Less freeboard | Wrong foam grade; open cells; heat | 4 | 2 | 3 | 24 | Supplier data sheet; immersion samples (PR-006); 5 % uptake checked in CAL [F13] |
| F2 | Foam strips | Give lift | Dissolved or swollen by fuel | Less lift | Polystyrene bought by mistake; fuel spill | 4 | 2 | 2 | 16 | Specify polyethylene, never polystyrene (BOM line 5); covers keep fuel off |
| F3 | Covers | Shield the foam, hold the strips | UV breakdown, tearing | Foam exposed, strips lost | Tropical sun; abrasion by nets | 5 | 3 | 2 | 30 | Annual inspection; replace covers (tailor-made) |
| F4 | Covers | Shield the foam | Covers degrade unnoticed under the straps | Module splits when loaded | UV and wear hidden at the strap | 5 | 3 | 5 | 75 | Inspection at each refit with the straps opened; spare covers; S10 open |
| F5 | Straps | Hold the module down | Webbing loses strength | Module floats free when swamped | UV degradation of polyester | 5 | 3 | 4 | 60 | Replace straps on a schedule set from field data (PR-009); hand-pull check |
| F6 | D-ring buckles | Close the strap | Slip | Strap loosens | Tail not tucked; worn webbing | 4 | 2 | 3 | 24 | Strap hold check (LVH-BLD-001 section 5) |
| F7 | Coach screws | Carry the batten | Pull-out or corrosion | Batten and module free | Rot in the frame; weak frame timber; galvanised screws in tannin-rich hardwood | 5 | 2 | 4 | 40 | A4 stainless in salt water (S22); sealed holes; pull test; check frame fastenings (LVH-DEC-001 to confirm item 4) |
| F8 | End chocks | Stop fore and aft creep | Chock splits or loosens | Module creeps against a thwart | Screws too short (fixed by D-S1) | 2 | 2 | 2 | 8 | Counterbored screws 31 mm into the batten (D-S1) |
| F9 | Battens | Carry the module | Rot | Screw pull-out | Wet timber, unsealed ends | 4 | 2 | 4 | 32 | Durable hardwood, sealed ends and holes (BOM line 14) |
| F10 | Grab lines and eye bolts | Something to hold | Line chafes through | Crew lose their hold | Abrasion on the strake | 4 | 2 | 2 | 16 | Inspect; replace rope |
| F11 | Whole kit | Float level | Fitted at the wrong height | Less roll stiffness or interference with thwarts | Gauge not made for that hull | 3 | 2 | 2 | 12 | Setting gauge per hull shape; fit check (PR-005) |

F4 and F5 lead because degradation under a strap is nearly invisible without opening it; the response is an inspection routine, set from field data at TRL 4 and later.
