---
doc_id: LVH-REG-001
title: LevelHull regulatory and standards register
project: LevelHull
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade); sources checked 2026-10-25
---

# LevelHull regulatory and standards register

The rule most likely to apply is national small vessel safety law where the kit is fitted: in Kenya, the Merchant Shipping (Small Vessel Safety) Regulations of 2012 already ask some small vessels for buoyancy that keeps them afloat when swamped, and ask that modifications to approved plans be approved, so whether fitting LevelHull needs the maritime authority's approval is the first item **to assess** with the partner. The US level flotation rule and ISO 12217-1 are design benchmarks, not obligations, for these canoes. LevelHull is not lifesaving equipment and makes no such claim. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

> **Safety:** Nothing in this register makes LevelHull a substitute for life jackets. Life jacket rules (for example the Second Schedule of the Kenyan regulations) apply to the crew whether or not the kit is fitted.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Merchant Shipping (Small Vessel Safety) Regulations, Legal Notice 114 of 2012, under the Merchant Shipping Act | Kenya | Construction, equipment and safety of commercial small vessels; First Schedule item 1 asks for built-in buoyancy able to keep the vessel afloat "when fully flooded, swamped or capsized"; regulation 37(3)(a) asks some smaller vessels for "sufficient buoyancy to keep the vessel afloat when completely swamped"; regulation 4(2) asks that modifications to approved plans be approved | Fishing canoes at a Kenyan landing are likely commercial small vessels. LevelHull is the kind of buoyancy these clauses describe; whether a fitted kit counts toward them, and whether fitting needs approval, is not known | Partner liaison with the Kenya Maritime Authority | To assess |
| G2 | Small vessel safety rules of Uganda and Tanzania on Lake Victoria, and of other countries where the kit may be fitted | Uganda, Tanzania, others | Equivalent national rules | Same questions as G1 | Partner liaison | To assess |
| G3 | FAO, ILO and IMO, *Safety Recommendations for Decked Fishing Vessels of Less than 12 metres in Length and Undecked Fishing Vessels* (2012), including Annex 13, "Guidance on a practical buoyancy test" | International (voluntary) | Recommendations for new undecked fishing vessels, including a practical buoyancy test | Guidance for the swamp test method at TRL 4 and the case to fisheries departments; not binding | Design lead | Applies (as guidance) |
| G4 | 33 CFR 183, Subpart H and the level flotation test (183.220 to 183.235) | United States | Flotation of outboard boats under 20 ft (6.1 m); the boat is swamped "allowing water to flow between the inside and outside of the boat" and must float within 10 deg of heel | The 8 m canoes are outside its scope and outside the US; used as the design benchmark for "swamped" and "level" (PR-001 to PR-003) | Design lead | Does not apply (benchmark only) |
| G5 | ISO 12217-1:2022, *Small craft: Stability and buoyancy assessment and categorization, Part 1: Non-sailing boats of hull length greater than or equal to 6 m* | International | Stability and buoyancy of boats 6 to 24 m, flotation of boats that can be swamped, design categories A to D | Applies to recreational craft placed on markets that call it up; not to these fishing canoes. A useful benchmark for flotation reserve and swamped stability | Design lead | Does not apply (benchmark, to assess its flotation clauses at TRL 4) |
| G6 | Recreational Craft Directive 2013/53/EU | European Union | Recreational craft placed on the EU market | Not a recreational craft, not placed on the EU market | Design lead | Does not apply |
| G7 | Personal flotation device standards (ISO 12402 series) | International | Life jackets and buoyancy aids | LevelHull is not a personal flotation device and must never be presented as one (PR-015) | Design lead | Does not apply |
| G8 | EN 12087, *Thermal insulating products: Determination of long term water absorption by immersion* (as quoted on the foam data sheet), ISO 845 (apparent density of cellular plastics) | International | Test methods for foam water uptake and density | Test methods for the TRL 4 immersion test of PR-006 and the supplier check | Design lead | Applies (test method, TRL 4) |
| G9 | EN 1995-1-1, Eurocode 5, and EN 338 strength classes | Europe (used as engineering practice) | Timber connections and timber strength | Used for the screw and boom checks (LVH-STM-001 S11, S13, S14, S29); not a legal requirement here | Design lead | Applies (as practice) |
| G10 | Patent US9139267B2 (inflatable emergency float, active to about 2032) | United States | Inflatable flotation for a craft | Avoided by design: passive foam only (LVH-PRC-001) | Design lead | Met by design (not legal advice) |
| G11 | Open hardware licences: CERN-OHL-S-2.0 (hardware), MIT (calculator), REUSE | International | Licensing | Applies to the repository | Maintainer | Met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- Kenya, *The Merchant Shipping (Small Vessel Safety) Regulations*, Legal Notice 114 of 2012, Kenya Law, https://new.kenyalaw.org/akn/ke/act/ln/2012/114/eng@2022-12-31, accessed 2026-10-25.
- FAO, ILO and IMO, *Safety Recommendations for Decked Fishing Vessels of Less than 12 metres in Length and Undecked Fishing Vessels* (Rome: FAO, 2012), https://www.fao.org/4/i3108e/i3108e00.htm, accessed 2026-10-25.
- US Coast Guard, *Safe Boating: Flotation* guideline (33 CFR 183.220 to 183.235), https://www.uscgboating.org/assets/PDF/downloads/FLOTATION.pdf, accessed 2026-10-25.
- ISO 12217-1:2022, scope as listed by the Estonian Centre for Standardisation, https://www.evs.ee/en/iso-12217-1-2022, accessed 2026-10-25.
- Ravago Building Solutions, Ethafoam technical data sheet (EN 12087, ISO 845), https://ravagobuildingsolutions.com/gr/wp-content/uploads/sites/47/2022/01/tds-ethafoam-eng.pdf, accessed 2026-10-25.
- Google Patents, US9139267B2, https://patents.google.com/patent/US9139267B2/en (cited in LVH-PRB-001).
