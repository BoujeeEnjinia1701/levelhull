"""LevelHull parametric model (build123d), TRL 3, constructable design (LVH-DDR-002).

Run from the repo root:  python cad/src/model.py [--check] [--export]
  --check   run the constructability checks (overlaps, contacts, screw depth, clearances)
  --export  write cad/step/*.step and cad/stl/*.stl

The kit is a passive flotation retrofit for a planked wooden fishing canoe. The canoe itself
(planking, frames, thwarts, rubbing strakes, outboard motor) is CONTEXT: it is the owner's boat,
modelled as the reference design canoe (8.0 m, 1.6 m beam, 0.65 m deep, 15 hp outboard) so that
the kit can be sized and checked against it. Other hulls are sized with docs/04-calcs/sizing.py.

Coordinates in mm. X along the boat from the outer face of the transom (x = 0) to the stem
(x = 8,000); Y across, port side positive; Z up from the outside of the bottom (z = 0).
The kit is the same on both sides; it is built on the port side and mirrored.

Kit, per canoe (BOM line numbers in brackets, see bom/bom.csv):
  [1]  setting gauge (12 mm plywood), a tool used to mark the batten height on every frame
  [2]  shelf battens, hardwood, 8 (one under each module)
  [3]  coach screws M8 x 100 with washers, one into every frame a batten crosses (20)
  [4]  end chocks, hardwood, 16 (one at each end of each module)
  [5]  buoyancy cores, closed-cell polyethylene foam, 4 layers of 50 mm, 8 modules
  [6]  covers, PVC-coated polyester tarpaulin sleeves, 8 (sewn with line 7)
  [8]  hold-down straps, 50 mm polyester webbing loops, 16
  [9]  double D-ring buckles, stainless, 16 pairs
  [10] grab-line eye bolts, M8 stainless, 8
  [11] grab lines, 12 mm polyester rope, 2
  [12] bailers, 10 L buckets with lanyards, 2
  [13] freeboard marks, painted (swamp test kit), 2
CONCEPT, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Face, Plane, Pos, Rot, Solid, Torus, Vector, Wire,
                       extrude, mirror, export_step, export_stl)

ROOT = Path(__file__).resolve().parents[2]

PARAMS = {
    # reference design canoe (context, to be measured on each real hull)
    "L_prism": 6200.0,       # transom to the start of the bow taper
    "L": 8000.0,             # overall length
    "half_bot": 400.0,       # outer half width of the flat bottom
    "half_top": 800.0,       # outer half beam at the gunwale
    "D": 650.0,              # depth amidships, outside of bottom to top of gunwale
    "bow": (20.0, 220.0, 40.0, 760.0),   # outer stem section: half bottom, z bottom, half top, z top
    "t": 25.0,               # plank thickness
    "transom_t": 40.0,
    "frame_sided": 50.0,     # frame thickness along the boat
    "frame_moulded": 60.0,   # frame depth from the planks inward
    "frame_top_gap": 20.0,   # frame heads stop this far below the gunwale
    "frames": [300.0 + 600.0 * i for i in range(10)],   # 300 to 5,700
    "thwarts": [1200.0, 3000.0, 4800.0],
    "thwart": (200.0, 30.0, 400.0),     # width along the boat, thickness, height of top face
    "strake": (40.0, 50.0),             # rubbing strake: thickness outboard, height
    # kit
    "modules": [(120.0, 1000.0), (1400.0, 2800.0), (3200.0, 4600.0), (5000.0, 6100.0)],  # x ranges
    "mod_top_gap": 30.0,     # module top below the gunwale
    "layers": 4,             # 50 mm foam layers
    "layer_t": 50.0,
    "mod_w": 200.0,          # horizontal width of the module (and of every foam layer)
    "cover_t": 2.0,
    "batten_t": 50.0,        # batten thickness square to the frame faces
    "batten_h": 70.0,        # vertical height of the batten
    "batten_over": 40.0,     # batten runs past each module end (room for the chock)
    "chock": (40.0, 50.0),   # chock length along the boat, height above the batten
    "screw": (8.0, 100.0),   # coach screw diameter and length
    "screw_z": 45.0,         # screw centre on the frame face, below the batten top
    "strap_w": 50.0,
    "strap_t": 2.5,
    "eyes_x": [600.0, 2400.0, 3600.0, 5400.0],
    "eye_z": 625.0,
    "rope_d": 12.0,
    "rope_sag": 150.0,
    "bailers_x": [2400.0, 4200.0],
    "mark": (2900.0, 3300.0, 50.0, 20.0),  # x from, x to, top edge below gunwale, band height
    "gauge_t": 12.0,
}


# ---------------------------------------------------------------- section geometry
def slope(p=PARAMS):
    """Side flare: horizontal run per mm of height, and the cosine of the flare angle."""
    k = (p["half_top"] - p["half_bot"]) / p["D"]
    a = math.atan(k)
    return k, math.cos(a), math.sin(a), a


def half(z, d=0.0, p=PARAMS):
    """Half width at height z of the plane offset d (mm, square to the side) inward from the outside."""
    k, ca, _, _ = slope(p)
    return p["half_bot"] + k * z - d / ca


def y_frame(z, p=PARAMS):
    """Half width of the frames' inner faces at height z (the plane the kit bears on)."""
    return half(z, p["t"] + p["frame_moulded"], p)


def derived(p=PARAMS):
    k, ca, sa, a = slope(p)
    zt = p["D"] - p["mod_top_gap"]
    zb = zt - p["layers"] * p["layer_t"]
    bz0 = zb - p["batten_h"]
    bw = p["batten_t"] / ca                     # horizontal width of the batten
    mods = p["modules"]
    frames_in = [[f for f in p["frames"] if x0 - p["batten_over"] < f < x1 + p["batten_over"]] for x0, x1 in mods]
    run = sum(x1 - x0 for x0, x1 in mods)
    area = p["mod_w"] * (zt - zb)
    straps = []
    for (x0, x1), fr in zip(mods, frames_in):
        edges = sorted([x0] + [f for f in fr if x0 < f < x1] + [x1])
        bays = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
        bays = [b for b in bays if b[1] - b[0] - p["frame_sided"] >= p["strap_w"] + 40]
        bays = sorted(bays, key=lambda b: -(b[1] - b[0]))[:2]
        xs = []
        for b0, b1 in sorted(bays):
            lo = b0 + (p["frame_sided"] / 2 if b0 in p["frames"] else 0)
            hi = b1 - (p["frame_sided"] / 2 if b1 in p["frames"] else 0)
            xs.append(round((lo + hi) / 2))
        straps.append(xs)
    return {
        "angle_deg": math.degrees(a), "cos": ca, "sin": sa, "k": k,
        "zt": zt, "zb": zb, "bz0": bz0, "bw": bw,
        "frames_in": frames_in, "straps": straps,
        "run_side": run, "area": area,
        "vol_total": 2 * run * area / 1e9,          # m3, module envelopes, both sides
        "n_modules": 2 * len(mods),
        "mod_len": [x1 - x0 for x0, x1 in mods],
        "batten_len": [x1 - x0 + 2 * p["batten_over"] for x0, x1 in mods],
        "n_screws": 2 * sum(len(f) for f in frames_in),
        "n_straps": 2 * sum(len(s) for s in straps),
    }


# ---------------------------------------------------------------- helpers
def prism(poly_yz, x0, x1):
    """Extrude a polygon given in (y, z) from x0 to x1."""
    w = Wire.make_polygon([Vector(x0, y, z) for y, z in poly_yz], close=True)
    return extrude(Face(w), amount=x1 - x0, dir=(1, 0, 0))


def trap(d, z0, z1, p=PARAMS):
    """Hull cross-section bounded by the planes offset d, from z0 to z1 (both sides)."""
    return [(-half(z0, d, p), z0), (half(z0, d, p), z0), (half(z1, d, p), z1), (-half(z1, d, p), z1)]


def section_wire(x, hb, zb, ht, zt):
    return Wire.make_polygon([Vector(x, -hb, zb), Vector(x, hb, zb), Vector(x, ht, zt), Vector(x, -ht, zt)], close=True)


def rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    v = b - a
    L = v.length
    c = Cylinder(r, L)
    # Cylinder is along Z, centred; rotate Z onto v
    z = Vector(0, 0, 1)
    ax = z.cross(v)
    if ax.length < 1e-9:
        rot = c if v.Z > 0 else Rot(180, 0, 0) * c
    else:
        ang = math.degrees(math.acos(max(-1, min(1, z.dot(v) / L))))
        rot = c.rotate(axis_from(ax), ang)
    return Pos(*(a + v * 0.5)) * rot


def axis_from(v):
    from build123d import Axis
    return Axis((0, 0, 0), (v.X, v.Y, v.Z))


def port_and_starboard(shape):
    return [shape, mirror(shape, about=Plane.XZ)]


def fuse(shapes):
    return Compound(list(shapes))


def offset_convex(pts, d):
    """Offset a clockwise or counter-clockwise convex polygon outward by d."""
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    s = -1 if area < 0 else 1                   # outward normal sign
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = s * dy / L, -s * dx / L
        lines.append(((x0 + nx * d, y0 + ny * d), (dx, dy)))
    out = []
    for i in range(n):
        (p1, d1), (p2, d2) = lines[i - 1], lines[i]
        den = d1[0] * d2[1] - d1[1] * d2[0]
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
        out.append((p1[0] + d1[0] * t, p1[1] + d1[1] * t))
    return out


# ---------------------------------------------------------------- the canoe (context)
def hull_context(p=PARAMS):
    D = p["D"]
    t = p["t"]
    hb, zb, ht, zt = p["bow"]
    Lp, L = p["L_prism"], p["L"]
    outer = prism(trap(0, 0, D, p), 0, Lp) + Solid.make_loft(
        [section_wire(Lp, p["half_bot"], 0, p["half_top"], D), section_wire(L, hb, zb, ht, zt)], ruled=True)
    f = (L - 120 - Lp) / (L - Lp)
    ohb, ozb = p["half_bot"] + (hb - p["half_bot"]) * f, zb * f
    oht, ozt = p["half_top"] + (ht - p["half_top"]) * f, D + (zt - D) * f
    sl = (oht - ohb) / (ozt - ozb)
    ihb, izb, izt = ohb - t, ozb + t, 900.0
    iht = ohb + sl * (izt - ozb) - t
    inner = prism(trap(t, t, D + 100, p), p["transom_t"], Lp) + Solid.make_loft(
        [section_wire(Lp, half(t, t, p), t, half(D + 100, t, p), D + 100), section_wire(L - 120, ihb, izb, iht, izt)],
        ruled=True)
    shell = outer - inner
    # frames: U-shaped, from the planks inward by the moulded depth, heads below the gunwale
    fr = []
    ztop = D - p["frame_top_gap"]
    m = t + p["frame_moulded"]
    for xf in p["frames"]:
        x0, x1 = xf - p["frame_sided"] / 2, xf + p["frame_sided"] / 2
        fr.append(prism(trap(t, t, ztop, p), x0, x1) - prism(trap(m, m, D + 100, p), x0 - 1, x1 + 1))
    # thwarts, between frames, ends cut to the planks
    th = []
    tw, tt, tz = p["thwart"]
    for xt in p["thwarts"]:
        th.append(prism(trap(t, tz - tt, tz, p), xt - tw / 2, xt + tw / 2))
    # rubbing strakes, outside the top plank, prismatic run only
    so, sh = p["strake"]
    yo = half(D, 0, p) + so
    strake_poly = [(half(D - sh, 0, p), D - sh), (yo, D - sh), (yo, D), (half(D, 0, p), D)]
    strakes = port_and_starboard(prism(strake_poly, p["transom_t"], Lp))
    return {"shell": shell, "frames": fr, "thwarts": th, "strakes": strakes}


def motor_context(p=PARAMS):
    """15 hp outboard motor on the transom (massing only)."""
    D = p["D"]
    clamp = Pos(-40, 0, D - 50) * Box(80, 180, 140)
    head = Pos(-280, 0, D + 230) * Box(360, 300, 420)
    leg = Pos(-260, 0, D - 330) * Box(110, 70, 700)
    cav = Pos(-260, 0, D - 650) * Box(260, 30, 40)
    prop = Pos(-150, 0, D - 610) * Rot(0, 90, 0) * Cylinder(110, 20)
    tiller = Pos(80, 0, D + 260) * Rot(0, 80, 0) * Cylinder(18, 600)
    return Compound([clamp, head, leg, cav, prop, tiller])


# ---------------------------------------------------------------- the kit
def module_section(p=PARAMS, shrink=0.0):
    d = derived(p)
    ca = d["cos"]
    zb, zt = d["zb"] + shrink, d["zt"] - shrink
    s = shrink / ca
    W = p["mod_w"]
    return [(y_frame(zb, p) - s, zb), (y_frame(zt, p) - s, zt), (y_frame(zt, p) - W + s, zt), (y_frame(zb, p) - W + s, zb)]


def batten_section(p=PARAMS):
    d = derived(p)
    zb, z0, bw = d["zb"], d["bz0"], d["bw"]
    return [(y_frame(z0, p), z0), (y_frame(zb, p), zb), (y_frame(zb, p) - bw, zb), (y_frame(z0, p) - bw, z0)]


def chock_section(p=PARAMS):
    d = derived(p)
    zb, bw = d["zb"], d["bw"]
    z1 = zb + p["chock"][1]
    return [(y_frame(zb, p), zb), (y_frame(z1, p), z1), (y_frame(z1, p) - bw, z1), (y_frame(zb, p) - bw, zb)]


def strap_outline(p=PARAMS):
    """Convex outline the strap is pulled tight around: batten and module together (port side)."""
    m = module_section(p)
    b = batten_section(p)
    # b: outboard bottom, outboard top, inboard top, inboard bottom; m: outboard bottom, outboard top, inboard top, inboard bottom
    return [b[0], b[3], m[3], m[2], m[1]]


def screw_points(xf, p=PARAMS):
    """Head point (on the batten's inboard face) and tip of the coach screw into frame xf (port side)."""
    d = derived(p)
    ca, sa = d["cos"], d["sin"]
    z0 = d["zb"] - p["screw_z"]
    y0 = y_frame(z0, p)
    n = (-ca, sa)                               # inward normal of the frame faces (y, z)
    bt = p["batten_t"]
    L = p["screw"][1]
    head = (xf, y0 + n[0] * bt, z0 + n[1] * bt)
    tip = (xf, head[1] - n[0] * L, head[2] - n[1] * L)
    return head, tip, n


def coach_screw(xf, p=PARAMS):
    head, tip, n = screw_points(xf, p)
    dia = p["screw"][0]
    shank = rod(head, tip, dia / 2)
    w0 = head
    w1 = (head[0], head[1] + n[0] * 2.0, head[2] + n[1] * 2.0)
    h1 = (head[0], w1[1] + n[0] * 5.5, w1[2] + n[1] * 5.5)
    return Compound([shank, rod(w0, w1, 12.0), rod(w1, h1, 7.5)])


def build_kit(p=PARAMS):
    """Every kit piece, port side first then starboard, as lists of (label, shape)."""
    d = derived(p)
    msec, csec = module_section(p), module_section(p, p["cover_t"])
    bsec, ksec = batten_section(p), chock_section(p)
    out = {k: [] for k in ("battens", "screws", "chocks", "cores", "covers", "straps", "rings",
                           "eyes", "grablines", "bailers", "marks")}
    so = strap_outline(p)
    so_out = offset_convex(so, p["strap_t"])
    for side, sgn in (("port", 1), ("starboard", -1)):
        def S(shape):
            return shape if sgn > 0 else mirror(shape, about=Plane.XZ)
        for i, ((x0, x1), fr, sx) in enumerate(zip(p["modules"], d["frames_in"], d["straps"])):
            tag = f"{side} {i + 1}"
            env = prism(msec, x0, x1)
            core = prism(csec, x0 + p["cover_t"], x1 - p["cover_t"])
            out["cores"].append((f"core {tag}", S(core)))
            out["covers"].append((f"cover {tag}", S(env - core)))
            bo = p["batten_over"]
            out["battens"].append((f"batten {tag}", S(prism(bsec, x0 - bo, x1 + bo))))
            out["chocks"].append((f"chock {tag} aft", S(prism(ksec, x0 - p["chock"][0], x0))))
            out["chocks"].append((f"chock {tag} fwd", S(prism(ksec, x1, x1 + p["chock"][0]))))
            for xf in fr:
                out["screws"].append((f"screw {tag} frame {xf:.0f}", S(coach_screw(xf, p))))
            for xs in sx:
                w = p["strap_w"]
                loop = prism(so_out, xs - w / 2, xs + w / 2) - prism(so, xs - w / 2 - 1, xs + w / 2 + 1)
                out["straps"].append((f"strap {tag} at {xs}", S(loop)))
                yr = (msec[2][0] + msec[1][0]) / 2 - 40
                ring = Pos(xs, yr, d["zt"] + p["strap_t"] + 3) * Box(w + 8, 34, 6)
                out["rings"].append((f"D-rings {tag} at {xs}", S(ring)))
        # grab line eye bolts through the rubbing strake and top plank, and the line between them
        ez = p["eye_z"]
        yo = half(p["D"], 0, p) + p["strake"][0]
        yin = half(ez, p["t"], p)
        eyes = []
        for xe in p["eyes_x"]:
            shank = rod((xe, yin - 10, ez), (xe, yo + 6, ez), 4.0)
            nut = rod((xe, yin - 10, ez), (xe, yin, ez), 8.0)
            ring = Pos(xe, yo + 26, ez) * Rot(0, 90, 0) * Torus(16, 4)
            eyes.append(Compound([shank, nut, ring]))
        out["eyes"].append((f"eye bolts {side}", S(Compound(eyes))))
        yr_ = yo + 26
        pts = []
        xs_ = p["eyes_x"]
        for a, b in zip(xs_[:-1], xs_[1:]):
            pts += [(a, yr_, ez - 16), ((a + b) / 2, yr_ + 15, ez - 16 - p["rope_sag"])]
        pts.append((xs_[-1], yr_, ez - 16))
        segs = [rod(pts[i], pts[i + 1], p["rope_d"] / 2) for i in range(len(pts) - 1)]
        out["grablines"].append((f"grab line {side}", S(Compound(segs))))
        # painted freeboard mark: band whose top edge is the mark, outside the hull amidships
        mx0, mx1, below, bh = p["mark"]
        ztop = p["D"] - below
        band = [(half(ztop - bh, 0, p), ztop - bh), (half(ztop, 0, p), ztop),
                (half(ztop, 0, p) + 1.2, ztop), (half(ztop - bh, 0, p) + 1.2, ztop - bh)]
        out["marks"].append((f"freeboard mark {side}", S(prism(band, mx0, mx1))))
    # bailers on the floor, on the centreline between frames
    for xb in p["bailers_x"]:
        b = Solid.make_cone(110, 135, 260)
        b = b - Pos(0, 0, 8) * Solid.make_cone(102, 127, 260)
        out["bailers"].append((f"bailer at {xb:.0f}", Pos(xb, 0, p["t"]) * b))
    return out


def gauge(p=PARAMS):
    """Setting gauge, 12 mm plywood: hooks over the gunwale and lies on a frame's inner face.
    Two notches mark the top and bottom of the batten. Drawn at frame x = 2,100 on the port side,
    lying against the aft side of the frame's inner face."""
    d = derived(p)
    D = p["D"]
    z0 = d["bz0"] - 20
    w = 70.0
    yo = half(D, 0, p) + p["strake"][0]
    body = [(y_frame(z0, p), z0), (y_frame(D, p), D), (y_frame(D, p) - w, D), (y_frame(z0, p) - w, z0)]
    hook = [(y_frame(D, p) - w, D), (yo + p["gauge_t"], D), (yo + p["gauge_t"], D + 30), (y_frame(D, p) - w, D + 30)]
    lip = [(yo, D - 35), (yo + p["gauge_t"], D - 35), (yo + p["gauge_t"], D), (yo, D)]
    x0 = 2100.0 - p["frame_sided"] / 2 - p["gauge_t"]
    x1 = x0 + p["gauge_t"]
    g = prism(body, x0, x1) + prism(hook, x0, x1) + prism(lip, x0, x1)
    for zn in (d["zb"], d["bz0"]):
        notch = [(y_frame(zn - 3, p) + 1, zn - 3), (y_frame(zn + 3, p) + 1, zn + 3),
                 (y_frame(zn + 3, p) - 12, zn + 3), (y_frame(zn - 3, p) - 12, zn - 3)]
        g = g - prism(notch, x0 - 1, x1 + 1)
    return g


BOM = {  # key: (BOM line, name)
    "gauge": (1, "Setting gauge"),
    "battens": (2, "Shelf battens"),
    "screws": (3, "Coach screws M8 x 100"),
    "chocks": (4, "End chocks"),
    "cores": (5, "Foam cores"),
    "covers": (6, "Covers"),
    "straps": (8, "Hold-down straps"),
    "rings": (9, "D-ring buckles"),
    "eyes": (10, "Grab-line eye bolts"),
    "grablines": (11, "Grab lines"),
    "bailers": (12, "Bailers"),
    "marks": (13, "Freeboard marks"),
}


def build_components(p=PARAMS):
    """One compound per BOM line (the kit) plus the context pieces."""
    k = build_kit(p)
    comps = {key: Compound([s for _, s in k[key]]) for key in k}
    comps["gauge"] = gauge(p)
    return comps


def build_parts(p=PARAMS):
    return build_components(p)


def context_compound(p=PARAMS, motor=True):
    h = hull_context(p)
    parts = [h["shell"]] + h["frames"] + h["thwarts"] + h["strakes"]
    if motor:
        parts.append(motor_context(p))
    return Compound(parts)


def assembly(p=PARAMS, with_hull=True, with_gauge=False):
    c = build_components(p)
    keys = [k for k in BOM if k != "gauge" or with_gauge]
    parts = [c[k] for k in keys]
    if with_hull:
        parts.append(context_compound(p, motor=False))
    return Compound(parts)


# ---------------------------------------------------------------- constructability checks
def _vol(a, b):
    try:
        r = a & b
        return r.volume if r is not None else 0.0
    except Exception:
        return float("nan")


def _dist(a, b):
    return a.distance_to(b)


def checks(p=PARAMS):
    """Return a list of (name, passed, detail). Overlap tolerance 1 mm3, contact tolerance 0.5 mm."""
    d = derived(p)
    h = hull_context(p)
    k = build_kit(p)
    res = []

    def add(name, ok, detail):
        res.append((name, bool(ok), detail))

    planks = h["shell"]
    frames = Compound(h["frames"])
    thwarts = Compound(h["thwarts"])
    strakes = Compound(h["strakes"])
    n = len(p["modules"])
    for side in range(2):
        for i in range(n):
            j = side * n + i
            tag = k["cores"][j][0].replace("core ", "")
            env = Compound([k["cores"][j][1], k["covers"][j][1]])
            bat = k["battens"][j][1]
            v = max(_vol(env, planks), _vol(env, frames), _vol(env, thwarts))
            add(f"module {tag}: no overlap with planks, frames or thwarts", v < 1.0, f"{v:.1f} mm3")
            add(f"module {tag}: bears on the frames", _dist(env, frames) < 0.5, f"gap {_dist(env, frames):.2f} mm")
            add(f"module {tag}: sits on its batten", _dist(env, bat) < 0.5 and _vol(env, bat) < 1.0,
                f"gap {_dist(env, bat):.2f} mm")
            v = max(_vol(bat, planks), _vol(bat, frames), _vol(bat, thwarts))
            add(f"batten {tag}: no overlap with the canoe", v < 1.0, f"{v:.1f} mm3")
            nf = len(d["frames_in"][i])
            add(f"batten {tag}: crosses at least two frames", nf >= 2, f"{nf} frames")
            add(f"batten {tag}: bears on the frames", _dist(bat, frames) < 0.5, f"gap {_dist(bat, frames):.2f} mm")
            for c in (2 * j, 2 * j + 1):
                ch = k["chocks"][c][1]
                ok = _dist(ch, bat) < 0.5 and _dist(ch, env) < 0.5 and _vol(ch, env) < 1 and _vol(ch, bat) < 1
                ok = ok and max(_vol(ch, frames), _vol(ch, thwarts), _vol(ch, planks)) < 1
                add(f"{k['chocks'][c][0]}: on the batten, against the module end, clear of the canoe", ok, "")
    for name, s in k["screws"]:
        vf = _vol(s, frames)
        vp = _vol(s, planks)
        add(f"{name}: into the frame, not through the plank", vf > 1000 and vp < 1.0,
            f"{vf / 1000:.1f} cm3 in frame, {vp:.1f} mm3 in plank")
    mods = Compound([s for _, s in k["covers"]])
    for name, s in k["straps"]:
        v = max(_vol(s, frames), _vol(s, planks), _vol(s, thwarts))
        add(f"{name}: in a bay between frames, clear of the canoe", v < 1.0, f"{v:.1f} mm3")
        add(f"{name}: tight on the module", _dist(s, mods) < 0.5, f"gap {_dist(s, mods):.2f} mm")
    for name, s in k["eyes"]:
        v = max(_vol(s, frames), _vol(s, mods))
        add(f"{name}: clear of frames and modules", v < 1.0, f"{v:.1f} mm3")
        add(f"{name}: through the rubbing strake", _vol(s, strakes) > 100, "")
    for name, s in k["grablines"]:
        v = max(_vol(s, planks), _vol(s, strakes))
        add(f"{name}: hangs clear of the hull", v < 1.0, f"{v:.1f} mm3")
    for name, s in k["bailers"]:
        v = max(_vol(s, frames), _vol(s, thwarts), _vol(s, planks))
        add(f"{name}: stows on the floor between frames", v < 1.0, f"{v:.1f} mm3")
    g = gauge(p)
    v = max(_vol(g, planks), _vol(g, frames), _vol(g, strakes))
    add("setting gauge: hooks over the gunwale and lies on the frame face", v < 1.0 and _dist(g, frames) < 0.5,
        f"{v:.1f} mm3, gap {_dist(g, frames):.2f} mm")
    # space between the modules for work and catch (at the module tops)
    clear = 2 * (y_frame(d["zt"], p) - p["mod_w"])
    add("clear width between module tops at least 900 mm", clear >= 900, f"{clear:.0f} mm")
    return res


def export(p=PARAMS):
    step = ROOT / "cad" / "step"
    stl = ROOT / "cad" / "stl"
    step.mkdir(parents=True, exist_ok=True)
    stl.mkdir(parents=True, exist_ok=True)
    c = build_components(p)
    kit = Compound([c[k] for k in BOM if k != "gauge"])
    export_step(Compound([kit, context_compound(p)]), str(step / "levelhull-assembly.step"))
    export_step(kit, str(step / "levelhull-kit.step"))
    export_step(context_compound(p), str(step / "reference-canoe-context.step"))
    k = build_kit(p)
    for i, L in enumerate(derived(p)["mod_len"]):
        export_step(k["cores"][i][1], str(step / f"foam-core-{i + 1}-{L:.0f}mm.step"))
        export_stl(k["battens"][i][1], str(stl / f"shelf-batten-{i + 1}.stl"), tolerance=0.5, angular_tolerance=0.3)
    export_step(k["chocks"][0][1], str(step / "end-chock.step"))
    export_step(gauge(p), str(step / "setting-gauge.step"))
    export_stl(gauge(p), str(stl / "setting-gauge.stl"), tolerance=0.5, angular_tolerance=0.3)
    export_stl(k["chocks"][0][1], str(stl / "end-chock.stl"), tolerance=0.5, angular_tolerance=0.3)


if __name__ == "__main__":
    d = derived()
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()})
    if "--check" in sys.argv:
        r = checks()
        for name, ok, det in r:
            if not ok:
                print("FAIL", name, det)
        print(f"{sum(ok for _, ok, _ in r)} of {len(r)} constructability checks pass")
    if "--export" in sys.argv:
        export()
        print("exported STEP and STL")
