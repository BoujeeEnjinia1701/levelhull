"""LevelHull sizing calculations (LVH-CAL-001) and the open sizing calculator.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every result with a tag ([A1], [F3] ...) used in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv. Geometry comes from the parametric model (cad/src/model.py), so the
module sizes here are the sizes in the STEP files, drawings and build plan.

The method treats the swamped canoe as a set of solid bodies in water: the water inside the hull
is part of the sea and carries nothing. Every body gives buoyancy for its submerged volume and
weighs its own mass. Wet hull timber is taken as exactly as dense as water (1,000 kg/m3), so it
gives no net lift and only the timber above the water is a load (conservative; a lighter timber
adds lift that is reported but not counted). Small heel and trim come from the waterplane
second moments of the foam modules and planks, and the heights of all buoyancy and weights.

Screening estimates for a paper proof of concept; not a substitute for the swamp test (TRL 4).
Software license MIT (the sizing calculator), see LICENSE-SOFTWARE.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad" / "src")]
import model as M  # noqa: E402

P = M.PARAMS
D = M.derived(P)
OUT = []

# ------------------------------------------------------------------ assumptions
A = {
    "rho_fresh": 1000.0,        # kg/m3, design case (lakes)
    "rho_salt": 1025.0,
    "rho_wood_design": 1000.0,  # wet hull timber, conservative: no net lift from the hull
    "rho_wood_typical": 750.0,  # wet hardwood, typical, used for the dry hull mass and the wood-credit check
    "rho_foam": 30.0,           # closed-cell polyethylene foam
    "cover_kg_m2": 0.65, "rho_pvc": 1300.0,
    "rho_batten": 900.0,
    "crew_n": 4, "crew_kg": 75.0,
    "crew_hold_frac": 0.20,     # share of a person's weight on the boat while holding on, head and shoulders out
    "engine_kg": 36.0,          # 15 hp two-stroke outboard, counted at full weight (it sits mostly above water)
    "fuel_kg_net": 0.0,         # a full 25 L tank floats; counted as zero
    "anchor_kg": 12.0, "rho_steel": 7850.0,
    "nets_kg": 40.0, "rho_nylon": 1140.0,
    "catch_kg": 150.0, "rho_fish": 1050.0,
    "fuel_kg": 20.5,
    "freeboard_req": 50.0,      # mm, R2
    "heel_trim_req": 10.0,      # deg, R3
    "reserve_req": 1.5,         # capacity at 50 mm freeboard over the design net load
    "bail_rate_lpm": 100.0,     # litres per minute per person with a 10 L bucket, calm water (estimate)
    "bailers": 2,
    "work_freeboard": 200.0,    # mm, freeboard at which the canoe can be worked and motored home
    "uptake": 0.05,             # R6 limit: foam loses up to 5 % of its lift to water uptake
    "webbing_kN": 10.0, "dring_kN": 4.0, "screw_shear_kN": 1.5,
}


def out(tag, text, value=None, unit="", req=None, status=None):
    OUT.append({"tag": tag, "item": text, "value": "" if value is None else value, "unit": unit,
                "requirement": req or "", "status": status or ""})
    v = "" if value is None else (f"{value:,.3g}" if isinstance(value, float) and abs(value) < 100 else
                                  (f"{value:,.0f}" if isinstance(value, (int, float)) else str(value)))
    print(f"[{tag}] {text}: {v} {unit}" + (f"  ({req}: {status})" if req else ""))


# ------------------------------------------------------------------ hull timber above a waterline
def _wood_shapes():
    h = M.hull_context(P)
    return [h["shell"]] + h["frames"] + h["thwarts"] + h["strakes"]


WOOD = None


def wood_above(hz):
    """Volume (m3) and centroid (x, z in mm) of hull timber above height hz (level waterline)."""
    global WOOD
    from build123d import Box, Pos
    if WOOD is None:
        WOOD = _wood_shapes()
    cut = Pos(4000, 0, hz + 1000) * Box(12000, 4000, 2000)
    v = 0.0
    mx = mz = 0.0
    for s in WOOD:
        r = s & cut
        if r is None:
            continue
        vol = r.volume
        if vol < 1:
            continue
        c = r.center()
        v += vol
        mx += vol * c.X
        mz += vol * c.Z
    return v / 1e9, (mx / v if v else 0.0), (mz / v if v else 0.0)


def wood_total():
    if WOOD is None:
        wood_above(-1e4)
    return sum(s.volume for s in WOOD) / 1e9


_WA = {}


def wood_above_interp(hz):
    """Interpolate wood_above on a 25 mm grid (the boolean is slow)."""
    lo = math.floor(hz / 25.0) * 25.0
    for z in (lo, lo + 25.0):
        if z not in _WA:
            _WA[z] = wood_above(z)
    f = (hz - lo) / 25.0
    a, b = _WA[lo], _WA[lo + 25.0]
    return tuple(a[i] + f * (b[i] - a[i]) for i in range(3))


# ------------------------------------------------------------------ buoyancy of the foam modules
def modules(p=P, skip=()):
    """List of modules: (side sign, x0, x1). skip: indices to leave out (damaged case)."""
    ms = []
    for s in (1, -1):
        for i, (x0, x1) in enumerate(p["modules"]):
            j = (0 if s > 0 else len(p["modules"])) + i
            if j not in skip:
                ms.append((s, x0, x1))
    return ms


def foam(hz, ms, p=P, zb=None, zt=None, low=False):
    """Buoyancy (kg per unit water density, i.e. m3), its centroid and the waterplane terms."""
    zb = D["zb"] if zb is None else zb
    zt = D["zt"] if zt is None else zt
    W = p["mod_w"] / 1000.0
    V = Mx = My = Mz = 0.0
    It = Il = Aw = Mxw = 0.0
    for s, x0, x1 in ms:
        L = (x1 - x0) / 1000.0
        top = min(hz, zt)
        if top <= zb:
            continue
        hsub = (top - zb) / 1000.0
        if low:
            yc = 0.25 * s
        else:
            yc = s * (M.y_frame((zb + top) / 2, p) - p["mod_w"] / 2) / 1000.0
        v = L * W * hsub
        V += v
        Mx += v * (x0 + x1) / 2000.0
        My += v * yc
        Mz += v * (zb + top) / 2000.0
        if zb < hz < zt:
            yw = s * (M.y_frame(hz, p) - p["mod_w"] / 2) / 1000.0
            It += L * W ** 3 / 12 + L * W * yw ** 2
            a = L * W
            Aw += a
            Mxw += a * (x0 + x1) / 2000.0
            Il += W * L ** 3 / 12 + a * ((x0 + x1) / 2000.0) ** 2
    return {"V": V, "x": Mx / V if V else 0, "y": My / V if V else 0, "z": Mz / V if V else 0,
            "It": It, "Il_origin": Il, "Aw": Aw, "Mxw": Mxw}


def plank_It(hz, p=P):
    """Transverse second moment (m4) of the planks cut by the waterline (prism and bow)."""
    k, ca, _, _ = M.slope(p)
    wst = p["t"] / ca / 1000.0
    It = 0.0
    hb, zb, ht, zt = p["bow"]
    for i in range(80):
        x = (i + 0.5) * 100.0
        if x <= p["L_prism"]:
            y = M.half(hz, 0, p)
        else:
            f = (x - p["L_prism"]) / (p["L"] - p["L_prism"])
            hb_ = p["half_bot"] + (hb - p["half_bot"]) * f
            zb_ = zb * f
            ht_ = p["half_top"] + (ht - p["half_top"]) * f
            zt_ = p["D"] + (zt - p["D"]) * f
            if hz < zb_:
                continue
            y = hb_ + (ht_ - hb_) * (hz - zb_) / (zt_ - zb_)
        It += 2 * 0.1 * wst * (y / 1000.0) ** 2
    return It


# ------------------------------------------------------------------ weights
def loads(case="level", A=A):
    """Net weights in water (kg) with their positions (x, y, z in m). Fresh water densities."""
    rw = 1000.0
    g = []
    hold = A["crew_kg"] * A["crew_hold_frac"]
    yg = (M.half(P["D"], 0, P) + P["strake"][0] + 30) / 1000.0
    if case == "level":
        crew = [(1.5, yg), (4.0, yg), (1.5, -yg), (4.0, -yg)]
    elif case == "one_side":
        crew = [(0.6, yg), (2.4, yg), (3.6, yg), (5.4, yg)]
    else:
        crew = []
    for x, y in crew:
        g.append(("crew holding on", hold, x, y, P["D"] / 1000.0))
    g.append(("outboard motor", A["engine_kg"], -0.25, 0.0, (P["D"] + 150) / 1000.0))
    g.append(("anchor and chain", A["anchor_kg"] * (1 - rw / A["rho_steel"]), 7.3, 0.0, 0.25))
    g.append(("nets", A["nets_kg"] * (1 - rw / A["rho_nylon"]), 1.7, 0.0, 0.15))
    g.append(("catch", A["catch_kg"] * (1 - rw / A["rho_fish"]), 3.5, 0.0, 0.15))
    g.append(("fuel tank", A["fuel_kg_net"], 0.6, 0.0, 0.2))
    return g


def kit_masses():
    """Kit masses (kg) and their net weight in water, battens taken as neutral when submerged."""
    k = M.build_kit(P)
    v_core = sum(s.volume for _, s in k["cores"]) / 1e9
    v_bat = sum(s.volume for _, s in k["battens"]) / 1e9 + sum(s.volume for _, s in k["chocks"]) / 1e9
    cover_area = 0.0
    for x0, x1 in P["modules"]:
        L = (x1 - x0) / 1000.0
        sec = M.module_section(P)
        per = sum(math.dist(sec[i], sec[(i + 1) % 4]) for i in range(4)) / 1000.0
        cover_area += 2 * (L * (per + 0.13) + 2 * 0.3 * per)
    m = {
        "foam": v_core * A["rho_foam"],
        "covers": cover_area * A["cover_kg_m2"],
        "battens and chocks": v_bat * A["rho_batten"],
        "screws, eye bolts, D-rings": 20 * 0.06 + 8 * 0.08 + 16 * 0.06,
        "straps": 19.2 * 0.05 * 0.0025 * 1380,
        "grab lines": 11.0 * 0.09,
        "bailers": 2 * 0.5,
    }
    net = {
        "covers": m["covers"] * (1 - 1000 / A["rho_pvc"]),
        "steel": m["screws, eye bolts, D-rings"] * (1 - 1000 / A["rho_steel"]),
        "straps": m["straps"] * (1 - 1000 / 1380),
    }
    return m, net, v_core, cover_area


KM, KNET, V_CORE, COVER_A = kit_masses()


def solve(ms, case="level", rho=1000.0, wood_rho=None, factor=1.0, extra=0.0, low=False, zb=None, zt=None):
    """Level waterline height hz (mm) where lift equals weight; then heel and trim."""
    wood_rho = A["rho_wood_design"] if wood_rho is None else wood_rho
    L = loads(case)
    kit_net = sum(KNET.values())
    zb_ = D["zb"] if zb is None else zb
    zt_ = D["zt"] if zt is None else zt

    def balance(hz):
        f = foam(hz, ms, zb=zb_, zt=zt_, low=low)
        lift = rho * f["V"] * factor
        foam_w = A["rho_foam"] * f_vol(ms, zb_, zt_)
        va, _, _ = wood_above_interp(hz)
        vt = wood_total()
        wood_net = wood_rho * vt - rho * (vt - va)     # weight of all timber less lift of the submerged part
        return lift - foam_w - wood_net - sum(w for _, w, *_ in L) - kit_net - extra
    lo, hi = 100.0, P["D"] + 150
    if balance(hi) < 0:
        return None
    for _ in range(50):
        mid = (lo + hi) / 2
        if balance(mid) > 0:
            hi = mid
        else:
            lo = mid
    hz = (lo + hi) / 2
    f = foam(hz, ms, zb=zb_, zt=zt_, low=low)
    va, xa, za = wood_above_interp(hz)
    vt = wood_total()
    B = rho * f["V"] * factor
    # weights: loads, foam, timber above water (and lift of timber below if lighter than water)
    Wt = [(w, x, y, z) for _, w, x, y, z in L]
    fv = f_vol(ms, zb_, zt_)
    fx = sum((x0 + x1) / 2000 * (x1 - x0) for s, x0, x1 in ms) / sum((x1 - x0) for s, x0, x1 in ms)
    fy = sum(s * (x1 - x0) for s, x0, x1 in ms) / sum((x1 - x0) for s, x0, x1 in ms) * (M.y_frame((zb_ + zt_) / 2) - P["mod_w"] / 2) / 1000
    Wt.append((A["rho_foam"] * fv, fx, fy if not low else 0.0, (zb_ + zt_) / 2000))
    Wt.append((rho * va, xa / 1000, 0.0, za / 1000))             # timber above water, at design density
    if wood_rho < rho:
        Wt.append(((wood_rho - rho) * vt, 3.4, 0.0, 0.30))       # lighter timber: net lift (negative weight)
    Wt.append((kit_net + extra, 3.1, 0.0, 0.45))
    Wsum = sum(w for w, *_ in Wt)
    zG = sum(w * z for w, _, _, z in Wt) / Wsum
    xG = sum(w * x for w, x, _, _ in Wt) / Wsum
    yG = sum(w * y for w, _, y, _ in Wt) / Wsum
    It = f["It"] + plank_It(hz)
    if f["Aw"] > 0:
        lcf = f["Mxw"] / f["Aw"]
        Il = f["Il_origin"] - f["Aw"] * lcf ** 2
    else:
        lcf, Il = 3.1, 0.0
    KT = rho * It + B * f["z"] - Wsum * zG
    KL = rho * Il + B * f["z"] - Wsum * zG
    heel = math.degrees((Wsum * yG - B * f["y"]) / KT) if KT > 0 else float("nan")
    trim = math.degrees((Wsum * xG - B * f["x"]) / KL) if KL > 0 else float("nan")   # positive: bow down
    # lowest freeboard on the gunwale (transom, prism end, stem) with trim and heel
    th = math.radians(trim) if trim == trim else 0.0
    ph = math.radians(heel) if heel == heel else 0.0
    fb = []
    for xg, zg in ((0.0, P["D"]), (P["L_prism"], P["D"]), (P["L"], P["bow"][3])):
        dz = (xg / 1000 - lcf) * math.tan(th) * 1000 + abs(math.tan(ph)) * M.half(P["D"])
        fb.append(zg - hz - dz)
    return {"hz": hz, "freeboard_level": P["D"] - hz, "freeboard_min": min(fb), "B": B, "W": Wsum,
            "heel": heel, "trim": trim, "KT": KT, "KL": KL, "GMt": KT / Wsum, "zB": f["z"], "zG": zG,
            "wood_above_kg": rho * va, "lcf": lcf}


def f_vol(ms, zb, zt):
    return sum((x1 - x0) / 1000 * P["mod_w"] / 1000 * (zt - zb) / 1000 for s, x0, x1 in ms)


def capacity_at(hz, ms, rho=1000.0):
    """Net weight the canoe can carry with its level waterline at hz."""
    f = foam(hz, ms)
    va, _, _ = wood_above_interp(hz)
    return rho * f["V"] - A["rho_foam"] * f_vol(ms, D["zb"], D["zt"]) - rho * va - sum(KNET.values())


# ------------------------------------------------------------------ hull volumes for bailing and space
def hull_volumes():
    from build123d import Box, Pos, Solid
    h = M.hull_context(P)
    outer = M.prism(M.trap(0, 0, P["D"], P), 0, P["L_prism"]) + Solid.make_loft(
        [M.section_wire(P["L_prism"], P["half_bot"], 0, P["half_top"], P["D"]),
         M.section_wire(P["L"], *P["bow"])], ruled=True)
    solid_in = Compound_([h["shell"]] + h["frames"] + h["thwarts"])

    def below(sh, z):
        r = sh & (Pos(4000, 0, z - 1500) * Box(12000, 4000, 3000))
        return (r.volume if r is not None else 0.0) / 1e9
    res = {}
    for z in (P["D"], P["D"] - A["work_freeboard"]):
        res[z] = below(outer, z)
    res["outer_D"] = res[P["D"]]
    res["shell_D"] = below(h["shell"], P["D"])
    res["timber_D"] = below(solid_in, P["D"])
    return res, outer, solid_in, below


def Compound_(shapes):
    from build123d import Compound
    return Compound(list(shapes))


# ------------------------------------------------------------------ sizing calculator for other hulls
def size_other(name, L_run, half_bot, half_top, depth, engine_kg, crew, gear_net=25.0, wood_above_kg=None):
    """Simple prismatic estimate: module run per side (4 layers, 200 mm wide, top 30 mm below the
    gunwale) for 50 mm freeboard at 1.5 times the design net load, with timber at 1,000 kg/m3.
    L_run: length of side free of thwarts available for modules (m)."""
    k = (half_top - half_bot) / depth
    plank_above = 2 * L_run * 1.25 * (0.050 / math.cos(math.atan(k))) * 0.025 + 2 * L_run * 1.25 * 0.040 * 0.050
    wa = (plank_above * 1000) if wood_above_kg is None else wood_above_kg
    net = crew * A["crew_kg"] * A["crew_hold_frac"] + engine_kg + gear_net + 7 + 5
    need = A["reserve_req"] * net + wa
    per_m = 2 * 0.2 * 0.15 * 1000 - 2 * 0.2 * 0.2 * A["rho_foam"]   # both sides, submerged 150 mm at 50 mm freeboard
    run = need / per_m
    return {"name": name, "net_kg": net, "wood_above_kg": wa, "run_per_side_m": run, "run_avail_m": L_run,
            "foam_m3": 2 * run * 0.2 * 0.2, "fits": run <= L_run}


# ------------------------------------------------------------------ run
def main():
    print("LevelHull sizing (LVH-CAL-001); all masses net in fresh water unless stated\n")
    ms = modules()
    out("G1", "Side flare of the reference canoe", round(D["angle_deg"], 1), "deg")
    out("G2", "Modules per canoe", D["n_modules"], "")
    out("G3", "Module run per side (four lengths)", D["run_side"], "mm")
    out("G4", "Module section, 200 mm wide x 200 mm high (four 50 mm layers)", D["area"] / 1e6, "m2")
    out("G5", "Module envelope volume, both sides", round(D["vol_total"], 3), "m3")
    out("G6", "Foam core volume (inside the covers)", round(V_CORE, 3), "m3")
    out("G7", "Module bottom and top above the outside of the bottom", f"{D['zb']:.0f} and {D['zt']:.0f}", "mm")
    vt = wood_total()
    out("G8", "Hull timber volume (planks, frames, thwarts, strakes)", round(vt, 3), "m3")
    out("G9", "Dry hull mass at 750 kg/m3 (typical)", round(vt * A["rho_wood_typical"]), "kg")
    for kname, v in KM.items():
        out("K", f"Kit mass, {kname}", round(v, 1), "kg")
    kit_mass = sum(KM.values())
    out("K1", "Kit mass in all", round(kit_mass, 1), "kg")
    out("K2", "Cover area, eight sleeves with end flaps", round(COVER_A, 1), "m2")
    L = loads("level")
    net = sum(w for _, w, *_ in L)
    for name, w, *_ in L:
        out("L", f"Design net weight, {name}", round(w, 1), "kg")
    out("L1", "Design net load (crew holding on, motor, gear, catch)", round(net, 1), "kg")

    r = solve(ms)
    out("F1", "Swamped, design load, fresh water: freeboard amidships (level)", round(r["freeboard_level"]), "mm")
    out("F2", "Swamped, design load: lowest freeboard on the gunwale with trim", round(r["freeboard_min"]), "mm",
        "R2", "met" if r["freeboard_min"] >= A["freeboard_req"] else "NOT MET")
    out("F3", "Swamped, design load: trim (positive bow down)", round(r["trim"], 2), "deg",
        "R3", "met" if abs(r["trim"]) <= A["heel_trim_req"] else "NOT MET")
    out("F4", "Swamped, design load: timber above water (counted as load)", round(r["wood_above_kg"], 1), "kg")
    out("F5", "Swamped, design load: transverse metacentric height", round(r["GMt"], 2), "m")
    out("F6", "Swamped, design load: roll stiffness", round(r["KT"]), "kg m per rad")
    cap = capacity_at(P["D"] - A["freeboard_req"], ms)
    out("F7", "Net load the swamped canoe carries at 50 mm freeboard", round(cap), "kg")
    out("F8", "Reserve: capacity at 50 mm freeboard over design net load", round(cap / net, 2), "",
        "R1", "met" if cap / net >= A["reserve_req"] else "NOT MET")
    r0 = solve(ms, case="none")
    out("F9", "Swamped, no crew holding on: freeboard, heel, trim",
        f"{r0['freeboard_min']:.0f} mm, {abs(r0['heel']):.1f} deg, {r0['trim']:.2f} deg", "",
        "R3", "met" if max(abs(r0["heel"]), abs(r0["trim"])) <= A["heel_trim_req"] else "NOT MET")
    r1 = solve(ms, case="one_side")
    out("F10", "Four crew holding the port grab line: heel", round(r1["heel"], 1), "deg",
        "R3", "met" if abs(r1["heel"]) <= A["heel_trim_req"] else "NOT MET")
    out("F11", "Four crew on one side: lowest freeboard", round(r1["freeboard_min"]), "mm")
    rs = solve(ms, rho=A["rho_salt"])
    out("F12", "Salt water, design load: lowest freeboard", round(rs["freeboard_min"]), "mm")
    ra = solve(ms, factor=1 - A["uptake"])
    out("F13", "Foam lift down 5 % (R6 limit): lowest freeboard", round(ra["freeboard_min"]), "mm")
    rd = solve(modules(skip=(1,)), factor=1 - A["uptake"])
    out("F14", "Largest module lost (port 2) and 5 % uptake: lowest freeboard", round(rd["freeboard_min"]), "mm")
    out("F15", "Largest module lost: heel", round(rd["heel"], 1), "deg")
    rw = solve(ms, wood_rho=A["rho_wood_typical"])
    out("F16", "With typical 750 kg/m3 timber (lift not counted in design): freeboard amidships",
        round(rw["freeboard_level"]), "mm")
    # comparison: the same foam fitted low on the floor (the TRL 1 arrangement)
    rl = solve(ms, low=True, zb=85.0, zt=285.0)
    if rl:
        out("F17", "Same foam fitted low on the floor: roll stiffness", round(rl["KT"]), "kg m per rad")
        out("F18", "Same foam fitted low: metacentric height", round(rl["GMt"], 2), "m")
        out("F19", "Same foam fitted low: heel with four crew on one side",
            round(solve(ms, case="one_side", low=True, zb=85.0, zt=285.0)["heel"], 1), "deg")
    # dry condition
    hv, outer, solid_in, below = hull_volumes()
    out("V1", "Hull inside volume below the gunwale", round(hv["outer_D"] - hv["shell_D"], 2), "m3")
    frac = D["vol_total"] / (hv["outer_D"] - hv["shell_D"])
    out("V2", "Module volume as a share of the inside volume", round(frac * 100, 1), "%",
        "R5", "met" if frac <= 0.10 else "NOT MET")
    # bailing: water to remove from swamped to working freeboard, all crew aboard
    hz = r["hz"]
    v_in = below(outer, hz) - below(solid_in, hz) - f_vol(ms, D["zb"], min(hz, D["zt"])) - \
        sum(s.volume for _, s in M.build_kit(P)["battens"]) / 1e9
    gross = vt * A["rho_wood_typical"] + kit_mass + A["engine_kg"] + A["fuel_kg"] + A["anchor_kg"] + A["nets_kg"] + \
        A["catch_kg"] + A["crew_n"] * A["crew_kg"]
    disp_work = 1000 * hv[P["D"] - A["work_freeboard"]]
    water_ok = max(disp_work - gross, 0.0) / 1000
    out("B1", "Water inside the swamped canoe", round(v_in, 2), "m3")
    out("B2", "Water that may stay aboard at 200 mm freeboard, all crew aboard", round(water_ok, 2), "m3")
    v_bail = v_in - water_ok
    t = v_bail * 1000 / (A["bail_rate_lpm"] * A["bailers"])
    out("B3", "Water to bail out", round(v_bail, 2), "m3")
    out("B4", "Bail-out time, two crew at 100 L/min each (estimate)", round(t, 1), "min",
        "R4", "met (estimate)" if t <= 15 else "NOT MET")
    out("B5", "Dry canoe: draft added by the kit (waterplane about 6.4 m2)", round(kit_mass / 6.4), "mm")
    # fixings, full submergence (worst case: canoe rolled or a wave buries the module)
    big = max(D["mod_len"]) / 1000 * 0.2 * 0.2 * (1025 - A["rho_foam"]) * 9.81 / 1000
    out("S1", "Largest module, full lift in salt water", round(big, 3), "kN")
    per_strap = big / 2
    out("S2", "Per strap (two straps, both legs)", round(per_strap, 3), "kN")
    out("S3", "Webbing factor (10 kN webbing, one leg carries half)", round(A["webbing_kN"] / (per_strap / 2), 1), "",
        "R7", "met" if A["webbing_kN"] / (per_strap / 2) >= 2 else "NOT MET")
    out("S4", "D-ring buckle factor (4 kN, to confirm)", round(A["dring_kN"] / per_strap, 1), "",
        "R7", "met" if A["dring_kN"] / per_strap >= 2 else "NOT MET")
    per_screw = max(big / len(f) for f in D["frames_in"])
    out("S5", "Largest share on one coach screw (sideways)", round(per_screw, 3), "kN")
    out("S6", "Coach screw factor (1.5 kN sideways in hardwood)", round(A["screw_shear_kN"] / per_screw, 1), "",
        "R7", "met" if A["screw_shear_kN"] / per_screw >= 2 else "NOT MET")
    total_lift = D["vol_total"] * (1025 - A["rho_foam"]) * 9.81 / 1000
    out("S7", "Total lift of all modules fully submerged (into the frames)", round(total_lift, 2), "kN")
    out("S8", "Per frame, 10 frames per side", round(total_lift / 20, 3), "kN")
    # fitting time (R8), minutes, estimate for one builder and one helper
    tasks = [("mark batten heights on 20 frame faces with the gauge", 40), ("cut, plane and seal 8 battens", 120),
             ("drill and screw 20 coach screws", 60), ("cut and screw 16 chocks", 40),
             ("lay 16 straps, fit 8 modules, close straps", 50), ("drill and fit 8 eye bolts, reeve grab lines", 50),
             ("paint freeboard marks, tie bailers", 20)]
    tf = sum(m for _, m in tasks)
    out("T1", "Fitting time on the canoe, foam cores and covers made beforehand (estimate)", round(tf / 60, 1), "h",
        "R8", "met (estimate)" if tf <= 8 * 60 else "NOT MET")
    # cost
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    kit = sum(float(x["qty"]) * float(x["unit_cost_usd"]) for x in rows)
    out("C1", "Parts cost of one kit", round(kit, 2), "USD")
    two = 2 * kit - float(rows[0]["qty"]) * float(rows[0]["unit_cost_usd"])
    out("C2", "Parts for two canoes (one gauge)", round(two, 2), "USD",
        "R10", f"over the value-engineering target by USD {two - 1000:,.0f}" if two > 1000 else "met")
    foam_cost = [float(x["qty"]) * float(x["unit_cost_usd"]) for x in rows if x["line"] == "5"][0]
    out("C3", "Foam share of one kit", round(foam_cost / kit * 100), "%")
    # sizing sheet for other hulls
    for c in (size_other("6.5 m paddle canoe, no motor, 3 crew", 3.8, 350, 650, 550, 0.0, 3),
              size_other("8.0 m canoe, 15 hp, 4 crew (reference)", D["run_side"] / 1000, 400, 800, 650, 36.0, 4),
              size_other("10 m canoe, 25 hp, 6 crew", 6.4, 450, 950, 750, 52.0, 6)):
        out("Z", f"Sizing sheet, {c['name']}: module run needed per side (available {c['run_avail_m']:.1f} m)",
            round(c["run_per_side_m"], 2), "m")
    with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["tag", "item", "value", "unit", "requirement", "status"])
        w.writeheader()
        w.writerows(OUT)
    return OUT


if __name__ == "__main__":
    main()
