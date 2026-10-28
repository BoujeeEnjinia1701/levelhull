---
doc_id: LVH-MKT-001
title: LevelHull market and viability
project: LevelHull
doc_type: Market and viability
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade); prices checked 2026-10-25
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Kit cost USD 694 with four bailers (D-O3, 2026-10-25)'
---

# LevelHull market and viability

LevelHull is for the owners and crews of wooden fishing canoes on lakes and coasts, starting with the planked canoes of Lake Victoria, who today have no passive, retrofittable flotation for the boats they already own; it competes with nothing directly, only with doing nothing, and complements life jackets rather than replacing them. An open design matters because the kit must be sized and built locally for every hull, by builders and safety programmes rather than bought as a product. Prices and benchmarks are cited with the date they were checked; anything not found is "to assess". Method: STANDARDS section 23.

> **Safety:** LevelHull is never sold or promoted as lifesaving equipment or as an alternative to life jackets.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Planked motor canoes, 7 to 10 m | Owners and crews of fishing canoes on Lake Victoria (Kenya, Uganda, Tanzania) and similar lakes | No retrofit flotation kit found for these canoes. A USCG Type III foam life jacket: USD 28.49 each (Zoro, checked 2026-10-25), so four life jackets about USD 114 for a crew | 682 per canoe (BOM, reference canoe) | A refuge the crew can hold and bail, for the boat, alongside life jackets |
| Paddle canoes, 5 to 7 m | Small-scale fishers without motors | As above | Lower: the calculator gives 2.5 m of modules a side for a 6.5 m canoe against 3.8 m on the reference (LVH-CAL-001 Table 8); cost to assess | Same, at a smaller kit |
| Safety programmes and NGOs | Fisheries departments, BMUs, sea-safety NGOs buying for a fleet | Life jacket donation programmes (prices as above) | 694 per canoe, less with bulk foam (LVH-DEC-001 value engineering) | A measure to fund beside life jackets and weather warnings |
| Builders elsewhere | Open hardware builders and boatyards | Materials only: closed-cell PE foam sheet 2,000 x 1,200 x 50 mm at GBP 45 before VAT in the UK (KB Packaging, checked 2026-10-25), against the BOM's USD 55 for 2,000 x 1,000 x 50 mm | Local | A tested sizing method and drawings to adapt |

The foam is 48 % of a kit, so the foam price near the fishery decides the cost. The one UK listing found is in line with the BOM's assumption; a local East African price is still **to assess** (LVH-DEC-001, to confirm item 8).

## Value proposition against the alternatives

- **Do nothing.** The swamped canoe sinks or rolls; the crew is in the water.
- **Life jackets only.** The first line of defence and always needed; but many crews do not wear them, and a floating canoe keeps the crew together, out of the water in part, visible and able to bail and get home.
- **Inflatable floats.** Need an inflation system, and at least one design is under patent to about 2032 (LVH-REG-001 G10).
- **Built-in buoyancy in new boats.** Right for new boats; does nothing for the fleet afloat today. LevelHull's sizing method could inform new builds too.

## Open route

The kit spreads as a method, not a product: the open sizing calculator (MIT) and drawings (CERN-OHL-S-2.0) let a beach management unit, a fisheries institute or a sea-safety NGO train local boatbuilders to fit it, with foam, tarpaulin and webbing bought locally and covers sewn by tailors. The first step is one partner fishery (LVH-PRB-001, co-design) to measure real hulls and run the swamp test; a training pack for builders would follow at TRL 5 and later. The strong reciprocal licence keeps improvements open.

## Sources

- Zoro, "Onyx Life Jacket, Adult, Universal, 15.5 lb, Foam" (USCG Type III), USD 28.49, https://www.zoro.com/i/G305778328/, accessed 2026-10-25.
- KB Packaging, "Foam Sheet 2000mm x 1200mm x 50mm" (closed-cell polyethylene), GBP 45.00 excluding VAT, https://kbpackaging.com/product/foam-sheet-2000mm-x-1200mm-x-50mm/, accessed 2026-10-25.
- LevelHull bill of materials, `bom/bom.csv`, and calculation note LVH-CAL-001.
