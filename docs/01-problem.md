---
doc_id: LVH-PRB-001
title: LevelHull problem statement
project: LevelHull
doc_type: Problem statement
version: "0.2"
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
  change: TRL 2 and 3 update; constraints restated, open questions settled (LVH-DDR-001), first co-design candidates, safety section
---

# LevelHull problem statement

When a wooden fishing canoe swamps, the crew loses the boat as a refuge just when they need it most. A small amount of well-placed buoyancy could change that.

## The problem

Deaths cluster in bad weather and at night, when waves swamp boats and rescue is least likely ([The Conversation](https://theconversation.com/lake-victoria-why-so-many-fishers-are-dying-and-what-can-be-done-about-it-232006)). Life jackets are the first line of defence, but many fishers do not wear them. A boat with enough built-in buoyancy to float level when swamped gives a second chance, which is what the US level flotation test checks ([USCG](https://www.uscgboating.org/assets/PDF/downloads/FLOTATION.pdf)).

Existing answers do not fit these boats. The US test is a benchmark for boats, not a method for retrofitting wooden fishing canoes. Inflatable emergency floats exist but depend on an inflation mechanism, and at least one such design is under patent until about 2032 ([US9139267B2](https://patents.google.com/patent/US9139267B2/en)). What is missing is an open, passive retrofit kit, with a sizing method, that a local builder can fit to the boats fishers already own.

## Users and context

*Table 1. Users.*

| User | Need | Context |
| --- | --- | --- |
| Canoe fishers and crews | A boat that stays afloat and level when swamped, so they can hold on and bail | Lakes, rivers and coasts; storms and night fishing; often no life jacket |
| Canoe owners | A retrofit that is affordable, lasts, and takes little space from the catch | Wooden canoes of many sizes, often with outboard motors |
| Local boatbuilders | A sizing sheet and fitting guide for different hulls | Beach yards with hand tools |
| Fisheries departments, beach management units and NGOs | A measure to promote alongside life jackets and weather warnings | Safety at sea programmes |

## Operating environment

- Fresh and salt water; lakes, estuaries and near-shore coastal waters.
- Strong sun and heat; boats beached and left in the open.
- Wooden hulls that take on water and are often wet inside.
- Fuel, fish slime, nets and abrasion from gear.
- Loads of crew, catch, gear and sometimes an outboard motor.

## Constraints

- Value-engineering target: USD 1,000 for the kits for two prototype canoes (a hypothetical control target, not a spending limit; STANDARDS section 18).
- Passive only: closed-cell foam or sealed rigid chambers; no inflation.
- Must not take up so much volume that it blocks work or catch storage.
- Fitted with hand tools by a local boatbuilder, without changing the hull shape and without new holes below the waterline.
- Materials must resist UV, fuel and abrasion and must not soak up water.
- Open design: hardware under CERN-OHL-S-2.0, sizing calculator under MIT.

## Out of scope

- Life jackets and personal flotation.
- New hull designs.
- Engines, propulsion and navigation equipment.
- Certification as lifesaving equipment.

## Prior work

*Table 2. Prior work.*

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| US Coast Guard level flotation test | Test method checking that a swamped small boat floats approximately level | A test benchmark, not a retrofit method or kit for wooden fishing canoes | [link](https://www.uscgboating.org/assets/PDF/downloads/FLOTATION.pdf) |
| US9139267B2, inflatable float (active to about 2032) | Emergency float that inflates to keep a craft afloat | Active inflation mechanism and patent restrictions; LevelHull stays passive | [link](https://patents.google.com/patent/US9139267B2/en) |
| RNLI sustainable lifesaving equipment | Programme supporting locally made lifesaving equipment in lower-income countries | Not a boat flotation retrofit | [link](https://rnli.org/what-we-do/international/lifesaving-interventions/sustainable-lifesaving-equipment) |

## Co-design

The first candidates to approach, in order (none approached yet): a beach management unit on the Kenyan shore of Lake Victoria, working with the canoe builders at its landing site; a national fisheries research institute in the region, for hull and load surveys; and a sea-safety programme that already trains fishers in the use of life jackets, so the kit is promoted alongside them. With the partner, measure real hulls (frame spacing and depth, flare, timber, motor) and loads, and swamp-test fitted canoes in sheltered, shallow water.

## Questions settled at TRL 2

These were the open questions of v0.1. Each is decided in LVH-DDR-001 under Amish's pre-approval of 2026-10-03; the numbers are in LVH-CAL-001.

*Table 3. Questions settled.*

| Question | Answer |
| --- | --- |
| Low along the sides, or higher under the gunwales? | High, under the gunwales, so the modules cut the waterline when the canoe is swamped. The same foam fitted low on the floor gives almost no roll stiffness (17 kg m per radian against 742) and the canoe rolls over with the crew on one side. |
| Foam or sealed chambers? | Closed-cell polyethylene foam in tarpaulin covers. A puncture loses no lift and nothing needs sealing; chambers are kept for the sibling LaneSkiff concept. |
| How much lift does the wood give, and what does the motor change? | The design takes no credit for the wood: wet hull timber is counted as exactly as dense as water. A typical 750 kg/m3 hardwood would add about 58 mm of freeboard. The motor is counted at its full 36 kg at the transom; other motors are sized with the calculator. |
| Re-entry step? | Still parked; scope unchanged. Grab lines along both sides give the crew something to hold while they are in the water. |
| Promotion without implying life jackets are optional | Every document, the fitting guide and the kit itself carry "never a substitute for life jackets"; the swamp test is run with every person in a life jacket. |

## Safety

> **Safety:** LevelHull is flotation for a boat, not lifesaving equipment for people. It is never a substitute for life jackets, and it is not certified. A swamped canoe that floats can still roll in breaking waves and cannot protect the crew from cold water, night or exhaustion; the kit buys time to bail and to be seen. Fitted canoes are swamp-tested in sheltered, shallow water with a safety boat and every person in a life jacket before they go fishing.
