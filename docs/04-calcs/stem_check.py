"""LevelHull STEM check (LVH-STM-001), calculations for every claim, with .kit/stem_check.py.

Run from the repo root:  python3 docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv (one row per claim) and docs/04-calcs/options_results.csv (first-order
numbers for concept options A, B and C), and fills the claims table in docs/01b-stem-check.md between its
STM_TABLE markers. Option A figures are read from docs/04-calcs/results.csv (LVH-CAL-001, sizing.py) and
re-derived here by independent hand checks where a first-order check exists. Options B and C are solved
with the same swamped-equilibrium method as LVH-CAL-001 (sizing.solve), with their own buoyancy geometry.

Screening calculations for a paper proof of concept. Software license MIT.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs" / "04-calcs"), str(ROOT / "cad" / "src")]
from stem_check import Check, limits, G, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402,F401
import sizing as S  # noqa: E402
import model as M  # noqa: E402
from build123d import Box, Pos  # noqa: E402

P, D, A = M.PARAMS, M.derived(M.PARAMS), S.A
RES = {r["tag"]: r for r in csv.DictReader((ROOT / "docs/04-calcs/results.csv").open())}


def r(tag):
    v = RES[tag]["value"]
    try:
        return float(v)
    except ValueError:
        return v


OPT = []


def opt(key, item, value, unit=""):
    OPT.append({"option": key, "item": item, "value": value, "unit": unit})
    print(f"  [{key}] {item}: {value} {unit}")


# ------------------------------------------------------------------ hull helpers
HV, OUTER, SOLID_IN, BELOW = S.hull_volumes()


def outer_waterplane(z):
    """Outer waterplane area (m2) of the hull at height z (mm), from a 1 mm slice of the model."""
    return (BELOW(OUTER, z + 0.5) - BELOW(OUTER, z - 0.5)) / 0.001


def dry_draft(mass_kg, rho=1000.0):
    lo, hi = 0.0, P["D"]
    for _ in range(30):
        mid = (lo + hi) / 2
        if BELOW(OUTER, mid) * rho > mass_kg:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ------------------------------------------------------------------ alternative buoyancy for options B and C
def foam_sponson(hz, ms, p=P, zb=None, zt=None, low=False):
    """Option B: foam sponsons outside the planks, horizontal width B_w, inboard face on the planking."""
    zb = p["B_zb"] if zb is None else zb
    zt = p["B_zt"] if zt is None else zt
    W = p["B_w"] / 1000.0
    V = Mx = My = Mz = It = Il = Aw = Mxw = 0.0
    for s, x0, x1 in ms:
        L = (x1 - x0) / 1000.0
        top = min(hz, zt)
        if top <= zb:
            continue
        hsub = (top - zb) / 1000.0
        yc = s * (M.half((zb + top) / 2, 0, p) + p["B_w"] / 2) / 1000.0
        v = L * W * hsub
        V += v; Mx += v * (x0 + x1) / 2000.0; My += v * yc; Mz += v * (zb + top) / 2000.0
        if zb < hz < zt:
            yw = s * (M.half(hz, 0, p) + p["B_w"] / 2) / 1000.0
            a = L * W
            It += L * W ** 3 / 12 + a * yw ** 2
            Aw += a; Mxw += a * (x0 + x1) / 2000.0
            Il += W * L ** 3 / 12 + a * ((x0 + x1) / 2000.0) ** 2
    return {"V": V, "x": Mx / V if V else 0, "y": My / V if V else 0, "z": Mz / V if V else 0,
            "It": It, "Il_origin": Il, "Aw": Aw, "Mxw": Mxw}


def foam_floats(hz, ms, p=P, zb=None, zt=None, low=False):
    """Option C: two sealed pipe floats along X at y = +-C_float_y, centre height C_float_z."""
    R = p["C_float"][0] / 2.0
    zf = p["C_float_z"]
    V = Mx = My = Mz = It = Il = Aw = Mxw = 0.0
    for s, x0, x1 in ms:
        L = (x1 - x0) / 1000.0
        h = min(max(hz - (zf - R), 0.0), 2 * R)
        if h <= 0:
            continue
        if h >= 2 * R:
            area, zc = math.pi * R * R, zf
        else:
            th = 2 * math.acos((R - h) / R)
            area = R * R / 2 * (th - math.sin(th))
            dz = 4 * R * math.sin(th / 2) ** 3 / (3 * (th - math.sin(th)))
            zc = zf - dz
        v = L * area / 1e6
        yc = s * p["C_float_y"] / 1000.0
        V += v; Mx += v * (x0 + x1) / 2000.0; My += v * yc; Mz += v * zc / 1000.0
        if zf - R < hz < zf + R:
            w = 2 * math.sqrt(R * R - (hz - zf) ** 2) / 1000.0
            a = L * w
            It += L * w ** 3 / 12 + a * yc ** 2
            Aw += a; Mxw += a * (x0 + x1) / 2000.0
            Il += w * L ** 3 / 12 + a * ((x0 + x1) / 2000.0) ** 2
    return {"V": V, "x": Mx / V if V else 0, "y": My / V if V else 0, "z": Mz / V if V else 0,
            "It": It, "Il_origin": Il, "Aw": Aw, "Mxw": Mxw}


class swap:
    """Temporarily replace sizing.foam (and the foam density) so sizing.solve runs another option."""
    def __init__(self, fn, rho_foam=None):
        self.fn, self.rho = fn, rho_foam

    def __enter__(self):
        self.old, self.old_rho = S.foam, S.A["rho_foam"]
        S.foam = self.fn
        if self.rho is not None:
            S.A["rho_foam"] = self.rho

    def __exit__(self, *a):
        S.foam, S.A["rho_foam"] = self.old, self.old_rho


def ms_of(ranges):
    return [(s, x0, x1) for s in (1, -1) for x0, x1 in ranges]


def main():
    c = Check(ROOT / "docs/04-calcs/stem_results.csv")
    ms = S.modules()
    rho = 1000.0
    net = r("L1")
    print("LevelHull STEM check (LVH-STM-001)\n")

    # ================================================================ option A (the design)
    # S1 swamped equilibrium: hand check of the level waterline from the foam waterplane
    wp_foam = 2 * D["run_side"] / 1000 * P["mod_w"] / 1000                 # m2, both sides
    lift_needed = net + r("F4") + sum(S.KNET.values()) + A["rho_foam"] * S.f_vol(ms, D["zb"], D["zt"])
    depth = lift_needed / rho / wp_foam * 1000                              # mm of foam under water
    fb_hand = P["D"] - (D["zb"] + depth)
    c.order_of_magnitude("S1", f"Swamped canoe at the design load ({net:.0f} kg net) floats with {r('F1'):.0f} mm freeboard "
                         f"amidships, {r('F2'):.0f} mm at the lowest point, with the water inside level with the lake (the "
                         "USCG swamped condition)", "Physics", "Fluid mechanics", claimed=r("F1"), estimate=fb_hand,
                         unit="mm", factor=1.25,
                         law="Archimedes: lift of the foam and timber below the waterline equals the net weight; water "
                             "inside the flooded hull carries nothing while it flows freely in and out (33 CFR 183.220(g))",
                         closed_by="LVH-CAL-001 [F1], [F2]")
    # S2 just after swamping, hull brim-full (water trapped above the outside level)
    cap0 = S.capacity_at(P["D"], ms)
    F0 = cap0 - net
    A_out = outer_waterplane(P["D"] - 1)
    fb_brim = F0 / (rho * A_out) * 1000
    c.claim("S2", f"Straight after swamping, with the hull brim-full and the water trapped above the lake level, the canoe "
            f"still floats ({fb_brim:.0f} mm freeboard) and rises as the crew bail", "Physics", "Fluid mechanics",
            law=f"Reserve at zero freeboard {F0:.0f} kg over the outer waterplane {A_out:.1f} m2 (trapped water rises "
                "with the hull, level canoe); a sealed hull drains only over the gunwale, so this is the state until the "
                "crew bail (see S32 to S34)",
            value=fb_brim, limit=0.0, unit="mm", rule="above", closed_by="This check; LVH-CAL-001 v0.3 section 10")
    opt("A", "Freeboard brim-full straight after swamping", round(fb_brim), "mm")
    # S3 roll stiffness
    yw = M.y_frame(P["D"] - r("F1"), P) - P["mod_w"] / 2
    It_hand = 2 * D["run_side"] / 1000 * (P["mod_w"] / 1000) * (yw / 1000) ** 2 + S.plank_It(P["D"] - r("F1"))
    c.order_of_magnitude("S3", f"Swamped roll stiffness {r('F6'):.0f} kg m per radian, metacentric height {r('F5'):.1f} m",
                         "Physics", "Mechanics and statics", claimed=r("F6"), estimate=rho * It_hand, unit="kg m/rad",
                         factor=1.25, law="Lost-buoyancy method (water inside flowing freely): K = rho I_T + B z_B - W z_G; "
                                         "hand estimate: rho I_T of the foam strips and planks only. The 3.1 m is K over the "
                                         "net weight carried, not a metacentric height of the whole displacement",
                         closed_by="LVH-CAL-001 [F5], [F6]")
    # S4 high, not low
    c.claim("S4", "The same foam laid on the floor gives no roll stiffness with 5 kg more load, so the modules must sit "
            "high (roll stiffness of the floor arrangement)", "Physics", "Mechanics and statics",
            law="Foam fully under water leaves only the planks' waterplane; K = rho I_T + B z_B - W z_G",
            value=r("F20"), limit=0.0, unit="kg m/rad", rule="below", closed_by="LVH-CAL-001 [F17] to [F20]")
    # S5 crew on one side
    yg = (M.half(P["D"], 0, P) + P["strake"][0] + 30) / 1000
    heel_hand = math.degrees(4 * A["crew_kg"] * A["crew_hold_frac"] * yg / r("F6"))
    c.order_of_magnitude("S5", f"All four crew holding one grab line heel the swamped canoe {r('F10'):.1f} deg (limit 10)",
                         "Physics", "Mechanics and statics", claimed=r("F10"), estimate=heel_hand, unit="deg", factor=1.5,
                         law="Heel = heeling moment / roll stiffness (small angles)", closed_by="LVH-CAL-001 [F10], [F11]")
    # S6 damaged
    c.claim("S6", f"With the largest module lost and 5 % uptake the canoe still floats ({r('F14'):.0f} mm lowest freeboard)",
            "Physics", "Fluid mechanics", law="Archimedes with one 1,400 mm module removed and foam lift down 5 %",
            value=r("F14"), limit=0.0, unit="mm", rule="above", closed_by="LVH-CAL-001 [F14], [F15]")
    # S7 sensitivity
    rs = S.solve(ms, factor=1 - A["uptake"], extra=0.2 * net)
    c.claim("S7", "Lowest freeboard stays at or above 50 mm with the design net load 20 % higher and foam lift 5 % lower",
            "Mathematics", "Statistics and uncertainty",
            law="Re-solve of the LVH-CAL-001 equilibrium with both inputs at their pessimistic values",
            value=round(rs["freeboard_min"], 1), limit=50.0, unit="mm", rule="above",
            closed_by="This check; LVH-CAL-001 v0.3 section 10")
    opt("A", "Lowest freeboard, load +20 % and foam -5 %", round(rs["freeboard_min"]), "mm")
    # S8 foam water uptake
    c.claim("S8", "Closed-cell polyethylene foam loses under 5 % of its lift to water uptake after 30 days immersed",
            "Chemistry", "Materials and polymer chemistry",
            law="Closed-cell PE foam sheet, 33 kg/m3: water absorption under 2 % by volume after 28 days (EN 12087), "
                "Ravago Ethafoam data sheet; lift lost = absorbed volume x 1,000 / net lift of 970 kg/m3",
            value=round(2.0 * 1000 / (1000 - 33), 2), limit=5.0, unit="% of lift", rule="below",
            closed_by="Cited data sheet; immersion test at TRL 4 (R6)")
    c.cited("S9", "Polyethylene foam is not dissolved by petrol, diesel or fish slime (polystyrene is excluded for that reason)",
            "Chemistry", "Organic", "Polymer solubility: polyethylene dissolves only in hot aromatic or chlorinated solvents "
            "(above about 80 C); at ambient low-density PE swells and softens a little in petrol; polystyrene dissolves",
            "The foam is about 3 % polymer by volume, so swelling does not change its lift; softening and diesel and "
            "fish-slime exposure are covered by the cover and the R6 immersion test at TRL 4", WITHIN,
            "LVH-DDR-001 D2")
    c.cited("S10", "PVC-coated tarpaulin covers and polyester webbing keep their strength for 12 months in tropical sun "
            "and water", "Chemistry", "Materials and polymer chemistry",
            "UV photo-degradation of PVC coatings and polyester fibres; UV-stabilised grades are sold for outdoor use, "
            "but strength retention after a year in equatorial sun depends on the grade",
            "Cannot be shown by calculation; strap and cover inspection in field use (R9, TRL 4 and later)", PLAUSIBLE, "")
    # S11, S12 fixings
    big = r("S1")
    per_screw = r("S5")
    ca, sa = D["cos"], D["sin"]
    shear, pull = per_screw * ca, per_screw * sa
    rho_k = 600.0
    f_ax = 0.52 * 8 ** -0.5 * 48 ** -0.1 * rho_k ** 0.8                       # N/mm2, screws in timber
    R_ax = f_ax * 8 * 48 / 1000.0                                             # kN, 48 mm in the frame
    inter = (2 * pull / R_ax) ** 2 + (2 * shear / A["screw_shear_kN"]) ** 2
    c.claim("S11", f"Each M8 coach screw carries twice its share of the full lift ({per_screw:.2f} kN): at twice the load "
            f"{2 * per_screw:.2f} kN, of which {2 * shear:.2f} kN along the frame face and {2 * pull:.2f} kN pulling the "
            "batten off it (static; wave slam not included)",
            "Engineering and technology", "Standards practice",
            law=f"Interaction (F_ax / R_ax)^2 + (F_v / R_v)^2 <= 1 at twice the load; R_v 1.5 kN (LVH-CAL-001 A9, "
                "conservative against a Johansen estimate of about 5 kN), "
                f"R_ax {R_ax:.1f} kN from the EN 1995-1-1 withdrawal expression for screws, 600 kg/m3 hardwood, 48 mm "
                "penetration", value=round(inter, 3), limit=1.0, unit="", rule="below",
            closed_by="LVH-CAL-001 [S5], [S6]; pull test at TRL 4 (R7)")
    c.claim("S12", "Webbing and D-ring buckles carry twice the full lift of the largest module (lowest factor, D-rings)",
            "Physics", "Strength of materials", law="Load per strap = full lift / 2; parts specified at 10 kN webbing "
            "and 4 kN D-ring pair (BOM lines 8, 9, to confirm with real parts)",
            value=r("S4"), limit=2.0, unit="", rule="above", closed_by="LVH-CAL-001 [S3], [S4]")
    # S13 chock screws (fix rule)
    cb_d, cb_h = P["chock_cbore"]
    slope_len = P["chock"][1] / ca
    pen = cb_h + P["chock_screw"][1] - slope_len
    pen_old = P["chock_screw"][1] - P["chock"][1]
    c.claim("S13", f"End chock screws (5 x 60 mm) bite far enough into the batten: {pen:.0f} mm (was {pen_old:.0f} mm when "
            "driven straight down through the 50 mm chock)", "Engineering and technology", "Standards practice",
            law="Pointside penetration of at least 6 d (30 mm for a 5 mm screw), EN 1995-1-1 practice for laterally "
                "loaded nails and screws; screws now driven parallel to the frame face in 12 mm counterbores 30 mm deep; "
                "margin 1.3 mm, so the counterbore depth is a making check (LVH-DWG-103)",
            value=round(pen, 1), limit=6 * P["chock_screw"][0], unit="mm", rule="above",
            closed_by="LVH-DEC-001 D-S1 (was Fails, fix proposed: 10 mm)")
    pen_cs = P["screw"][1] - P["batten_t"] - P["screw_washer"][2]
    c.claim("S14", f"Coach screws go {pen_cs:.0f} mm into the frames and stop {P['frame_moulded'] - pen_cs:.0f} mm short of "
            "the planking (no new hole below the waterline)", "Engineering and technology", "Manufacturing tolerances",
            law="Penetration at least 6 d = 48 mm (EN 1995-1-1 practice); frame moulded depth 60 mm; planking untouched; "
                "no margin either way, so each frame's depth is measured and the screw length chosen to suit (LVH-DEC-001, "
                "to confirm item 2)",
            value=pen_cs, limit=6 * P["screw"][0], unit="mm", rule="above", closed_by="Model check (cad/src/model.py)")
    yo = M.half(P["D"], 0, P) + P["strake"][0]
    yin = M.half(P["eye_z"], P["t"], P)
    stack = (yo - yin) + 2 * 1.6 + 6.8 + 2.4
    c.claim("S15", f"Grab-line eye bolt (M8 x 100) passes through strake, plank, two washers and a nyloc nut with thread "
            f"to spare ({100 - stack:.1f} mm)", "Engineering and technology", "Manufacturing tolerances",
            law="Grip at 625 mm: strake and top plank; ISO 7089 washers 1.6 mm, ISO 7040 nut 9.2 mm; at least one "
                "1.25 mm pitch beyond the nut", value=round(100 - stack, 1), limit=1.25, unit="mm", rule="above",
            closed_by="Model check (cad/src/model.py)")
    # S16 crew holding on
    held = (0.081 + 0.05) * A["crew_kg"]
    c.order_of_magnitude("S16", "A crew member holding on with head and shoulders out puts about 15 kg (20 % of 75 kg) on the "
                         "canoe", "Biology", "Human physiology and biomechanics", claimed=A["crew_kg"] * A["crew_hold_frac"],
                         estimate=held, unit="kg",
                         law="Body segment masses (Winter): head and neck 8.1 %, forearms and hands on the gunwale about "
                             "5 %; the body below the water is close to neutral", closed_by="LVH-CAL-001 A3")
    # S17 bailing
    lift_w = 10 * 0.7 * G * 0.7 * (A["bail_rate_lpm"] / (10 * 0.7)) / 60
    c.cited("S17", f"{A['bailers']} crew bail at 100 L per minute each ({r('B3'):.2f} m3 in about {r('B4'):.0f} min)", "Biology",
            "Ergonomics", "Lifting work is small (about " + f"{lift_w:.0f}" + " W against 75 W sustained); the limit is "
            "the cycle: 100 L/min is about 14 scoops a minute for many minutes; sustained rates of 30 to 50 L/min are "
            "more usual (independent review)", "Rate to measure in the bail-out trial (R4, TRL 4); see S34", PLAUSIBLE, "")
    # S18 partly bailed: positive stability with the free surface of the water inside
    zfb = P["D"] - A["work_freeboard"]
    V450 = BELOW(OUTER, zfb)
    wt = S.wood_above(-1e4)
    hull_kg = S.wood_total() * A["rho_wood_typical"]
    water = r("B2") * 1000
    disp = V450 * 1000
    # water level inside (prism approximation over 7.0 m of inside length)
    Lin = 7.0
    zw = P["t"]
    while Lin * sum(2 * M.half(z, P["t"], P) / 1000 * 0.001 for z in range(int(P["t"]), int(zw))) < water / 1000 and zw < zfb:
        zw += 2.0
    b_in = 2 * M.half(zw, P["t"], P) / 1000
    i_fs = Lin * b_in ** 3 / 12
    w_prism = 2 * M.half(zfb, 0, P) / 1000
    It_wp = P["L_prism"] / 1000 * w_prism ** 3 / 12 + (P["L"] - P["L_prism"]) / 1000 * w_prism ** 3 / 48
    KB = (OUTER & (Pos(4000, 0, zfb / 2) * Box(12000, 4000, zfb))).center().Z / 1000
    W = [(hull_kg, wt[2] / 1000), (r("K1"), 0.52), (A["crew_n"] * A["crew_kg"], 0.68), (A["engine_kg"], 0.80),
         (A["fuel_kg"], 0.20), (A["anchor_kg"], 0.25), (A["nets_kg"], 0.15), (A["catch_kg"], 0.15),
         (water, (P["t"] + zw) / 2000)]
    Wsum = sum(w for w, _ in W)
    KG = sum(w * z for w, z in W) / Wsum
    GM = KB + It_wp / (disp / 1000) - KG - i_fs / (disp / 1000)
    c.claim("S18", f"Partly bailed to 200 mm freeboard with all crew aboard and {r('B2'):.1f} m3 of water still inside, the "
            f"canoe keeps a positive metacentric height ({GM:.2f} m after the free-surface loss)", "Physics",
            "Mechanics and statics", law=f"GM = KB + I_T / V - KG - i_fs / V: KB {KB:.2f} m, waterplane I_T {It_wp:.2f} m4, "
            f"free surface i_fs {i_fs:.2f} m4 of a {b_in:.2f} m wide pool, KG {KG:.2f} m with crew seated (CG 0.68 m)",
            value=round(GM, 3), limit=0.0, unit="m", rule="above", closed_by="This check; LVH-CAL-001 v0.3 section 10")
    opt("A", "GM partly bailed, 200 mm freeboard, free surface included", round(GM, 2), "m")
    # S19 holes above the waterline
    dry = hull_kg + r("K1") + A["crew_n"] * A["crew_kg"] + A["engine_kg"] + A["fuel_kg"] + A["anchor_kg"] + \
        A["nets_kg"] + A["catch_kg"]
    dz = dry_draft(dry)
    c.claim("S19", f"The only new hull holes (eye bolts, {P['eye_z']:.0f} mm up) stay above the loaded waterline of the dry "
            f"canoe ({dz:.0f} mm)", "Engineering and technology", "Standards practice",
            law=f"Dry displacement {dry:.0f} kg (timber at 750 kg/m3, crew, motor, fuel, gear, catch, kit) on the model hull",
            value=P["eye_z"] - dz, limit=0.0, unit="mm above", rule="above", closed_by="Model (cad/src/model.py)")
    opt("A", "Loaded dry draft (all aboard)", round(dz), "mm")
    # S20 volume, mass, width
    c.claim("S20", f"Modules take {r('V2'):.1f} % of the inside volume below the gunwale", "Mathematics",
            "Units and dimensional analysis", law="0.421 m3 of module envelope over 5.01 m3 inside volume",
            value=round(D["vol_total"] / r("V1") * 100, 1), limit=10.0, unit="%", rule="below", closed_by="LVH-CAL-001 [V2]")
    est = 0.402 * 30 + 10.2 * 0.050 * 0.082 * 900 + 16 * 0.04 * 0.082 * 0.05 * 900 + 14.3 * 0.65 + 20 * 0.06 + 8 * 0.08 + \
        16 * 0.06 + 19.5 * 0.17 + 1.0 + 1.0
    c.order_of_magnitude("S21", f"Kit mass {r('K1'):.0f} kg per canoe", "Mathematics", "Orders of magnitude",
                         claimed=r("K1"), estimate=est, unit="kg", factor=1.3,
                         law="Sum of stock quantities in the BOM times densities", closed_by="LVH-CAL-001 [K1]")
    c.claim("S22", "Stainless kit hardware does not corrode the fixings away in wet hardwood in fresh or salt water",
            "Chemistry", "Electrochemistry and batteries", law="All metal in contact is A4 stainless (screws, D-rings, eye "
            "bolts): no galvanic couple. A4 can suffer crevice corrosion in wet, salty, airless timber, so screws are "
            "inspected at each refit; zinc coatings are attacked by tannins in fresh water too, so the BOM's hot-dip "
            "galvanised alternative is withdrawn in favour of A4 (LVH-DEC-001 D-S2)", value=0.0, limit=0.0,
            unit="dissimilar couples", rule="below", closed_by="BOM lines 3, 10; LVH-DEC-001 D-S2")
    c.cited("S23", "Fungal decay does not start at the new screw holes in the frames within the kit's life", "Biology",
            "Microbiology", "Wood-decay fungi need timber moisture above about 20 %; frames of a working canoe are wet, so "
            "the holes are sealed with preservative or epoxy (BOM line 14) and inspected",
            "Depends on timber and care; inspection at each refit", PLAUSIBLE, "")
    c.order_of_magnitude("S24", f"A builder and a helper fit the kit in about {r('T1'):.1f} h", "Engineering and technology",
                         "Manufacturing tolerances", claimed=r("T1"),
                         estimate=(20 * 2 + 8 * 15 + 20 * 4 + 16 * 4 + 16 * 2 + 8 * 6 + 20) / 60, unit="h", factor=2.0,
                         law="Bottom-up count by the author (not independent): 20 marks, 8 battens, 20 screws, 16 counterbored "
                             "chocks, 16 straps, 8 eye bolts, marks; sealer cure not included",
                         closed_by="LVH-CAL-001 [T1] (estimate, R8)")

    # S31 timber density sweep
    rw11 = S.solve(ms, wood_rho=1100.0)
    rw12 = S.solve(ms, wood_rho=1200.0)
    c.claim("S31", f"Lowest freeboard stays at or above 50 mm if the wet hull timber is denser than water, 1,100 kg/m3 "
            f"({rw11['freeboard_min']:.0f} mm; {rw12['freeboard_min']:.0f} mm at 1,200 kg/m3)", "Physics", "Fluid mechanics",
            law="Saturated hardwood can exceed 1,000 kg/m3, so A2 is neutral, not conservative; re-solve at 1,100 and "
                "1,200 kg/m3; the real hull is weighed before fitting (LVH-DEC-001, to confirm item 3)",
            value=round(rw11["freeboard_min"]), limit=50.0, unit="mm", rule="above", closed_by="This check")
    opt("A", "Lowest freeboard, timber 1,100 / 1,200 kg/m3", f"{rw11['freeboard_min']:.0f} / {rw12['freeboard_min']:.0f}", "mm")
    # S32 to S34: the sealed hull (no free exchange of water) after swamping
    drop = r("F1") - r("F2")
    fb_brim_low = fb_brim - drop
    c.cited("S32", "R2 as restated for the free-flooding condition: the lowest point keeps 50 mm with the water inside at the lake level; brim-full, a sealed hull still floats and the crew bail at once, seated",
            "Physics", "Fluid mechanics", "Brim-full freeboard (S2) less the trim drop to the lowest point of LVH-CAL-001 "
            f"({drop:.0f} mm)", f"{fb_brim:.0f} mm level, about {fb_brim_low:.0f} mm at the lowest point brim-full; R2 is "
            "met once the water inside is down to the lake level (by bailing or by water spilling out as the canoe "
            "rolls). Amish decided on 2026-10-25 to keep the hull sealed and state R2 and R3 for the free-flooding "
            "condition of the USCG method, with the operating rule \"hold on, then bail at once, seated\"; freeing ports "
            "studied at TRL 4 (LVH-DEC-001 D-O2)", WITHIN, "LVH-DEC-001 D-O2")
    # roll stiffness of the sealed hull with the water inside trapped (free surface acts)
    def kt_sealed(hz_out, z_in):
        w_out = 2 * M.half(hz_out, 0, P) / 1000
        I_out = P["L_prism"] / 1000 * w_out ** 3 / 12 + (P["L"] - P["L_prism"]) / 1000 * w_out ** 3 / 48
        if z_in > D["zt"]:
            b_fs = 2 * M.half(z_in, P["t"], P) / 1000
            i_fs = (P["L_prism"] - P["transom_t"]) / 1000 * b_fs ** 3 / 12 + (P["L"] - 120 - P["L_prism"]) / 1000 * b_fs ** 3 / 48
        else:
            b_fs = 2 * (M.y_frame(z_in, P) - P["mod_w"]) / 1000
            i_fs = 2 * D["run_side"] / 1000 * b_fs ** 3 / 12 + (P["L"] - P["L_prism"]) / 1000 * b_fs ** 3 / 48
        vo = BELOW(OUTER, hz_out)
        zo = (OUTER & (Pos(4000, 0, hz_out / 2) * Box(12000, 4000, hz_out))).center().Z / 1000
        # weights: everything that floats, with the trapped water; KG from the interior water volume and the rest
        v_in_tot = BELOW(OUTER, z_in) - BELOW(SOLID_IN, z_in) - S.f_vol(ms, D["zb"], min(z_in, D["zt"]))
        zi = (OUTER & (Pos(4000, 0, z_in / 2) * Box(12000, 4000, z_in))).center().Z / 1000
        w_water = 1000 * v_in_tot
        w_rest = 1000 * vo - w_water
        zg_rest = 0.40
        KT = 1000 * (I_out - i_fs) + 1000 * vo * zo - (w_water * zi * 0.98 + w_rest * zg_rest)
        return KT, I_out, i_fs
    kt_b, Io_b, ifs_b = kt_sealed(P["D"] - fb_brim, P["D"])
    kt_e, Io_e, ifs_e = kt_sealed(P["D"] - r("F1"), P["D"] - r("F1"))
    c.cited("S33", "The swamped canoe floats level (R3) whether or not the water inside can flow in and out", "Physics",
            "Mechanics and statics", f"Sealed hull, water trapped: K = rho (I_out - i_fs) + B z_B - W z_G; brim-full: "
            f"I_out {Io_b:.2f} m4, free surface {ifs_b:.2f} m4; at the lake level: I_out {Io_e:.2f} m4, free surface "
            f"{ifs_e:.2f} m4 between the modules",
            f"Roll stiffness about {kt_b:.0f} kg m/rad brim-full (near neutral; the estimate of the centre of weight is "
            f"good to about +-200) and {kt_e:.0f} kg m/rad once the water inside is down to the lake level, where the "
            "modules cut its free surface. Brim-full, the canoe lolls a degree or two until the low gunwale dips and "
            "water spills out, which lowers the inside level and stiffens it; to confirm in the swamp test of a sealed "
            "hull (R3, TRL 4)", PLAUSIBLE, "")
    opt("A", "Roll stiffness, sealed hull brim-full / trapped at lake level", f"{kt_b:.0f} / {kt_e:.0f}", "kg m/rad")
    v_brim = BELOW(OUTER, P["D"]) - BELOW(SOLID_IN, P["D"]) - D["vol_total"] - \
        sum(q.volume for _, q in M.build_kit(P)["battens"]) / 1e9
    nb = A["bailers"]
    t50 = (v_brim - r("B2")) * 1000 / (nb * 50.0)
    c.cited("S34", f"The four crew, each with a bailer, bail the brim-full canoe to 200 mm freeboard within 15 min (R4) at a sustained 50 L/min each",
            "Biology", "Ergonomics", f"Brim-full water {v_brim:.2f} m3 less the {r('B2'):.2f} m3 that may stay aboard",
            f"{v_brim - r('B2'):.2f} m3 at {nb} x 50 L/min takes about {t50:.0f} min (two bailers took about {t50 * nb / 2:.0f} min). "
            "Four bailers decided by Amish on 2026-10-25 (LVH-DEC-001 D-O3); rate to measure in the bail-out trial",
            WITHIN if t50 <= 15 else FIX, "LVH-DEC-001 D-O3" if t50 <= 15 else "")
    opt("A", f"Bail from brim-full to 200 mm, {nb} x 50 L/min", round(t50), "min")

    # ================================================================ option B, external sponsons
    print("\nOption B, external foam sponsons")
    msB = ms_of(P["B_sponsons"])
    with swap(foam_sponson):
        rb = S.solve(msB, zb=P["B_zb"], zt=P["B_zt"])
        rb1 = S.solve(msB, case="one_side", zb=P["B_zb"], zt=P["B_zt"])
        rbd = S.solve([m for m in msB if not (m[0] == 1 and m[1] == P["B_sponsons"][0][0])], factor=1 - A["uptake"],
                      zb=P["B_zb"], zt=P["B_zt"])
    vB = sum((x1 - x0) for _, x0, x1 in msB) / 1000 * P["B_w"] / 1000 * (P["B_zt"] - P["B_zb"]) / 1000
    opt("B", "Foam volume", round(vB, 3), "m3")
    opt("B", "Swamped lowest freeboard", round(rb["freeboard_min"]), "mm")
    opt("B", "Swamped roll stiffness", round(rb["KT"]), "kg m/rad")
    opt("B", "Four crew on one side: heel, low-side freeboard", f"{abs(rb1['heel']):.1f} deg, {rb1['freeboard_min']:.0f} mm")
    opt("B", "One sponson lost and 5 % uptake: lowest freeboard", round(rbd["freeboard_min"]) if rbd else "sinks", "mm")
    c.claim("S25", f"Option B: swamped canoe on external sponsons floats with {rb['freeboard_min']:.0f} mm lowest freeboard",
            "Physics", "Fluid mechanics", law="Same equilibrium as LVH-CAL-001 with the foam outside the planks, 360 to 560 "
            "mm up", value=round(rb["freeboard_min"]), limit=50.0, unit="mm", rule="above", closed_by="This check")
    beam_B = 2 * (M.half(P["B_zt"], 0, P) + P["B_w"])
    opt("B", "Overall beam over the sponsons", round(beam_B), "mm")
    bolt_z = P["B_zb"] - P["B_batten"][1] / 2
    c.claim("S26", f"Option B: the new bolt holes through the planks ({bolt_z:.0f} mm up) and the sponson bottoms "
            f"({P['B_zb']:.0f} mm) stay above the loaded dry waterline", "Engineering and technology", "Standards practice",
            law="Dry loaded draft on the model hull, as S19. The holes are below the swamped waterline, so they must be "
            "bedded watertight or they leak while the canoe is bailed", value=round(bolt_z - dz), limit=0.0, unit="mm above",
            rule="above", closed_by="This check")
    opt("B", "Sponson bottom above the loaded dry waterline", round(P["B_zb"] - dz), "mm")
    c.cited("S27", "Option B: sponsons survive beaching, rafting alongside other canoes and wave slap", "Engineering and "
            "technology", "Standards practice", "External fenders and sponsons on working boats wear and tear at the "
            "chine and ends; the tarpaulin cover is the only skin", "Abrasion life to establish in field use",
            PLAUSIBLE, "")

    # ================================================================ option C, double outrigger floats
    print("\nOption C, double outrigger floats")
    od, wall, fl = P["C_float"]
    msC = ms_of([(P["C_float_x0"], P["C_float_x0"] + fl)])
    m_float = math.pi / 4 * (od ** 2 - (od - 2 * wall) ** 2) * fl / 1e9 * 950 + 4 * math.pi / 4 * od ** 2 * P["C_cap_t"] / 1e9 * 950
    bw, bd, bl = P["C_boom"]
    m_booms = 2 * bw * bd * bl / 1e9 * 800
    m_struts = 4 * (P["C_post"] ** 2 * 245 + P["C_post"] * P["C_foot"][0] * P["C_foot"][1]) / 1e9 * 800
    m_steel = 16 * 0.25 + 8 * 0.35
    kitC = m_float + m_booms + m_struts + m_steel
    with swap(foam_floats, rho_foam=0.0):
        extra = kitC - sum(S.KNET.values())
        rc = S.solve(msC, extra=extra, zb=P["C_float_z"] - od / 2, zt=P["C_float_z"] + od / 2)
        rc1 = S.solve(msC, case="one_side", extra=extra, zb=P["C_float_z"] - od / 2, zt=P["C_float_z"] + od / 2)
        rcd = S.solve(msC[:1], extra=extra, zb=P["C_float_z"] - od / 2, zt=P["C_float_z"] + od / 2)
    vC = 2 * math.pi / 4 * od ** 2 * fl / 1e9
    opt("C", "Float volume (both)", round(vC, 3), "m3")
    opt("C", "Kit mass (floats, booms, struts, steel)", round(kitC, 1), "kg")
    opt("C", "Swamped lowest freeboard", round(rc["freeboard_min"]), "mm")
    opt("C", "Swamped roll stiffness", round(rc["KT"]), "kg m/rad")
    opt("C", "Four crew on one side: heel, low-side freeboard", f"{abs(rc1['heel']):.1f} deg, {rc1['freeboard_min']:.0f} mm")
    opt("C", "One float lost: result", "capsizes or heels past 10 deg" if (rcd is None or abs(rcd["heel"]) > 10 or rcd["heel"] != rcd["heel"]) else f"{rcd['heel']:.1f} deg", "")
    opt("C", "Overall beam over the floats", round(2 * (P["C_float_y"] + od / 2)), "mm")
    c.claim("S28", f"Option C: swamped canoe hung between two pipe floats has {rc['freeboard_min']:.0f} mm lowest freeboard",
            "Physics", "Fluid mechanics", law="Same equilibrium with two 250 mm floats 2.1 m off the centreline; booms "
            "and struts counted as weight", value=round(rc["freeboard_min"]), limit=50.0, unit="mm", rule="above",
            closed_by="This check")
    lift_f = rho * G * math.pi / 4 * od ** 2 * fl / 1e9 / 1000             # kN, one float fully pushed under
    arm = P["C_float_y"] - (M.half(P["D"], 0, P) + P["strake"][0] / 2)
    sig = lift_f / 2 * arm / (bw * bd ** 2 / 6) * 1000                      # MPa
    c.claim("S29", f"Option C: each boom carries half the full lift of one float pushed under by a wave ({lift_f:.2f} kN) "
            f"at {arm:.0f} mm from the gunwale bolts: {sig:.1f} MPa", "Physics", "Strength of materials",
            law="Cantilever, sigma = M / Z, Z = b d^2 / 6 (the boom is continuous across the canoe, so the gunwale bolts "
                "take the uplift of the couple, about M / 1.64 m); hardwood of strength class D30, 30 MPa characteristic, "
                "design value about 30 x 0.7 / 1.3 = 16 MPa (EN 338, EN 1995-1-1 modification and material factors)",
            value=round(sig, 1), limit=16.0, unit="MPa", rule="below", closed_by="This check")
    E_lt = 200.0
    pc = 2 * E_lt / (1 - 0.4 ** 2) * (1 / (od / wall - 1)) ** 3
    c.claim("S30", f"Option C: the SDR 26 float pipe does not collapse when pushed 0.5 m under ({pc * 100:.1f} m of water "
            "collapse head)", "Physics", "Strength of materials",
            law="Ring buckling of an unsupported pipe p_c = 2 E / (1 - nu^2) (t / (D - t))^3, long-term E of PE100 "
                "about 200 MPa, nu 0.4", value=round(pc * 100, 2), limit=0.5, unit="m of water", rule="above",
            closed_by="This check")
    state = c.write()
    with (ROOT / "docs/04-calcs/options_results.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["option", "item", "value", "unit"])
        w.writeheader()
        w.writerows(OPT)
    fill_doc(c.rows)
    return state


def fill_doc(rows):
    doc = ROOT / "docs/01b-stem-check.md"
    if not doc.exists():
        return
    t = doc.read_text(encoding="utf-8")
    a, b = "<!-- STM_TABLE -->", "<!-- /STM_TABLE -->"
    if a not in t:
        return
    head = ["| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    body = [f"| {q['id']} | {q['claim']} | {q['field']} | {q['branch']} | {q['law']} | {q['check']} | {q['verdict']} | "
            f"{q['closed_by'] or 'Open: needs field data (TRL 4 and later)'} |" for q in rows]
    new = t.split(a)[0] + a + "\n" + "\n".join(head + body) + "\n" + b + t.split(b)[1]
    doc.write_text(new, encoding="utf-8")
    print("filled the claims table in docs/01b-stem-check.md")


if __name__ == "__main__":
    main()
