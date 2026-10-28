"""LevelHull parametric model (build123d), TRL 3, constructable design (LVH-DDR-002); modules 220 mm wide (LVH-DDR-003).

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
  [12] bailers, 10 L buckets with lanyards, 4 (LVH-DEC-001 D-O3)
  [13] freeboard marks, painted (swamp test kit), 2
CONCEPT, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Face, Plane, Pos, Rot, Solid, Torus, Vector, Wire,
                       extrude, mirror, export_step, export_stl)

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad" / "src"), str(ROOT / ".kit")]

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
    "mod_w": 220.0,          # horizontal width of the module (and of every foam layer); 200 to 220 mm, LVH-DDR-003
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
    "bailers_x": [1800.0, 2400.0, 3600.0, 4200.0],   # four bailers, one per crew member (LVH-DEC-001 D-O3, 2026-10-25)
    "mark": (2900.0, 3300.0, 50.0, 20.0),  # x from, x to, top edge below gunwale, band height
    "gauge_t": 12.0,
    # option A detail (kit 1.9, LVH-DEC-001): fasteners and holes; no design dimension above changes
    "screw_washer": (8.4, 24.0, 2.0),     # coach screw washer: bore, outside diameter, thickness
    "screw_hole": 9.0,                    # clearance hole in the batten for the M8 coach screw
    "chock_screw": (5.0, 60.0),           # stainless wood screw, two per chock
    "chock_screw_e": (15.0, 35.0),        # their offsets from the frame face, square to it
    "chock_screw_dx": 8.0,                # and fore and aft of the chock centre
    "chock_cbore": (12.0, 30.0),          # counterbore diameter and depth along the screw (LVH-DEC-001 D-S1)
    "edge_r": 2.0,                        # edge break on battens and chocks
    # option B: external foam sponsons (concept option, LVH-OPT-001)
    "B_sponsons": [(260.0, 2650.0), (3350.0, 5740.0)],   # x ranges, each side
    "B_zb": 360.0, "B_zt": 560.0,         # sponson bottom and top above the outside of the bottom
    "B_w": 220.0,                         # sponson width, level
    "B_batten": (50.0, 70.0),             # outside shelf batten: thickness square to the planks, height
    "B_clamp": (20.0, 40.0),              # top clamp strip: thickness, height (up to the rubbing strake)
    "B_flange": 2.0,                      # cover flange (doubled tarpaulin) clamped under batten and strip
    # option C: double outrigger floats (concept option, LVH-OPT-001)
    "C_booms_x": [1200.0, 4800.0],        # over the aft and forward thwarts
    "C_boom": (120.0, 90.0, 4500.0),      # hardwood boom: width along the boat, depth, length across
    "C_saddle_t": 30.0,
    "C_float_y": 2100.0, "C_float_z": 350.0,
    "C_float": (250.0, 9.6, 4460.0),      # HDPE pipe PE100 SDR 26: outside diameter, wall, length
    "C_float_x0": 770.0,
    "C_cap_t": 20.0,
    "C_post": 75.0,                       # strut post section
    "C_foot": (320.0, 70.0),              # strut foot: length across, height
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
    # foam strips: the cores are cut from 2,000 x 1,000 mm sheets; four strips of the module width must
    # come from the width of one sheet (LVH-DDR-003), with 5 mm per saw cut
    across = int((1000.0 + 5.0) // (p["mod_w"] + 5.0))
    add("foam: four strips of the module width from a 1,000 mm sheet", across >= 4, f"{across} strips")
    return res


def export(p=PARAMS):
    """Legacy STEP set (assembly, kit, canoe, foam cores, chock, gauge) and STL of the made timber parts, from the
    detailed kit 1.9 parts. Per-part STEP files of every option come from python .kit/cad_check.py --export.
    STL chord tolerance 0.15 mm (STANDARDS section 24)."""
    step = ROOT / "cad" / "step"
    stl = ROOT / "cad" / "stl"
    step.mkdir(parents=True, exist_ok=True)
    stl.mkdir(parents=True, exist_ok=True)
    dk = detail_kit(p)
    kit = Compound([s for key in dk for _, s in dk[key]])
    export_step(Compound([kit, context_compound(p)]), str(step / "levelhull-assembly.step"))
    export_step(kit, str(step / "levelhull-kit.step"))
    export_step(context_compound(p), str(step / "reference-canoe-context.step"))
    k = build_kit(p)
    parts = {q["name"]: q["shape"] for q in option_a(p, with_hull=False)}
    tol = dict(tolerance=0.15, angular_tolerance=0.2)
    for i, L in enumerate(derived(p)["mod_len"]):
        export_step(k["cores"][i][1], str(step / f"foam-core-{i + 1}-{L:.0f}mm.step"))
        export_stl(parts[f"Shelf batten port {i + 1}"], str(stl / f"shelf-batten-{i + 1}.stl"), **tol)
    export_step(parts["End chock port 1 aft"], str(step / "end-chock.step"))
    export_step(gauge(p), str(step / "setting-gauge.step"))
    export_stl(gauge(p), str(stl / "setting-gauge.stl"), **tol)
    export_stl(parts["End chock port 1 aft"], str(stl / "end-chock.stl"), **tol)


# ================================================================ kit 1.9 interface (STANDARDS section 24)
# Every concept option is modelled at D3 with .kit/cad_parts.py and cad/src/lvh_parts.py. Option A is the
# design of LVH-DDR-002 and LVH-DDR-003 with its numbers unchanged; only the modelling is richer (holes,
# every fastener, edge breaks, separate foam layers). build_kit() above stays the envelope model that
# docs/04-calcs/sizing.py reads; detail_kit() gives the same pieces in the detailed form for the pictures.
import cad_parts as cp  # noqa: E402
import lvh_parts as lp  # noqa: E402

TITLE = "LevelHull"
OPTIONS = {"A": "Foam modules high inside", "B": "External foam sponsons", "C": "Double outrigger floats"}
PRINCIPLES = {
    "A": "Closed-cell foam strapped high under the gunwales inside the hull cuts the waterline of the swamped "
         "canoe along both sides, so it floats level on its own foam and can be bailed",
    "B": "The same foam carried outside the hull below the rubbing strake as a collar: lift and waterplane "
         "outboard of the planks, and extra roll stiffness for the dry canoe as it heels",
    "C": "Two sealed HDPE pipe floats on hardwood booms 2.1 m out from the centreline hold the swamped canoe "
         "up and upright by their lift and their long lever arm (as on an East African ngalawa)",
}
CHOSEN = "A"
OPTION_VIEWS = {
    "A": {"el": 24, "az": -55, "scale": "person", "keep_context": True, "ground_z": 0},
    "B": {"el": 24, "az": -55, "scale": "person", "keep_context": True, "ground_z": 0},
    "C": {"el": 24, "az": -55, "scale": "person", "keep_context": True, "ground_z": 0},
}
ALLOWED_CONTACTS = []

MAT = {"wood": "hardwood", "foam": "insulated_white", "cover": "canvas", "web": "canvas", "ss": "stainless",
       "galv": "galvanised", "rope": "rope", "ply": "plywood", "paint": "safety_red", "hdpe": "hdpe_black",
       "bucket": "hdpe_natural"}
COL = {"foam": "#EDE6C8", "cover": "#E2621B", "web": "#1E40AF", "bucket": "#16A34A", "rope": "#0F766E"}


def _ccw_mirror(shape, sgn):
    return shape if sgn > 0 else mirror(shape, about=Plane.XZ)


def _y(v, sgn):
    return v if sgn > 0 else -v


def hull_parts(p=PARAMS, motor=False):
    """The owner's canoe (context): planking, each frame, thwarts and rubbing strakes."""
    h = hull_context(p)
    out = [cp.part("Reference canoe planking (owner's boat)", h["shell"], "timber", kind="context", group="canoe",
                   color="#2F6E8F")]
    for i, f in enumerate(h["frames"]):
        out.append(cp.part(f"Canoe frame {i + 1} (owner's boat)", f, "timber", kind="context", group="canoe"))
    for i, t in enumerate(h["thwarts"]):
        out.append(cp.part(f"Canoe thwart {i + 1} (owner's boat)", t, "timber", kind="context", group="canoe"))
    for i, s in enumerate(h["strakes"]):
        out.append(cp.part(f"Rubbing strake {'port' if i == 0 else 'starboard'} (owner's boat)", s, "timber",
                           kind="context", group="canoe"))
    if motor:
        out.append(cp.part("15 hp outboard motor (owner's)", motor_context(p), "matte_black", kind="context",
                           group="canoe"))
    return out


def layer_sections(sec, n):
    """Split a parallelogram section [(ob, zb), (ob, zt), (ib, zt), (ib, zb)] into n equal layers."""
    (y0, z0), (y1, z1), (y2, _), (y3, _) = sec
    out = []
    for i in range(n):
        za, zc = z0 + (z1 - z0) * i / n, z0 + (z1 - z0) * (i + 1) / n
        fa, fc = i / n, (i + 1) / n
        oa, oc = y0 + (y1 - y0) * fa, y0 + (y1 - y0) * fc
        ia, ic = y3 + (y2 - y3) * fa, y3 + (y2 - y3) * fc
        out.append([(oa, za), (oc, zc), (ic, zc), (ia, za)])
    return out


# ---------------------------------------------------------------- option A (chosen), detailed
def _chock_screw_axes(x_c, p=PARAMS):
    """Points on the chock top and the downward direction (parallel to the frame face) of its two screws,
    port side. Returns [(top point (x, y, z), direction (0, dy, dz))]."""
    d = derived(p)
    ca, sa = d["cos"], d["sin"]
    z1 = d["zb"] + p["chock"][1]
    down = (0.0, -sa, -ca)
    out = []
    for e, dx in zip(p["chock_screw_e"], (-p["chock_screw_dx"], p["chock_screw_dx"])):
        y = y_frame(z1, p) - e * ca + (e * sa / ca) * (-sa)
        z = z1 + e * sa - (e * sa / ca) * ca
        out.append(((x_c + dx, y, z), down))
    return out


def option_a(p=PARAMS, with_hull=True):
    d = derived(p)
    msec, csec = module_section(p), module_section(p, p["cover_t"])
    bsec, ksec = batten_section(p), chock_section(p)
    so = strap_outline(p)
    so_out = offset_convex(so, p["strap_t"])
    wb_in, wb_out, wb_t = p["screw_washer"]
    cs_d, cs_l = p["chock_screw"]
    cb_d, cb_h = p["chock_cbore"]
    out = []
    for side, sgn in (("port", 1), ("starboard", -1)):
        S = lambda s: _ccw_mirror(s, sgn)  # noqa: E731
        for i, ((x0, x1), fr, sx) in enumerate(zip(p["modules"], d["frames_in"], d["straps"])):
            tag = f"{side} {i + 1}"
            bo = p["batten_over"]
            bat = cp.break_edges(prism(bsec, x0 - bo, x1 + bo), p["edge_r"])
            # coach screws, one into every frame the batten crosses
            for xf in fr:
                head, tip, n = screw_points(xf, p)
                bat = bat - lp.bore(head, (0, -n[0], -n[1]), p["screw_hole"], p["batten_t"] + 2, back=2)
                nn = (0, n[0], n[1])
                w = lp.place(lp.wide_washer(wb_in, wb_out, wb_t), head, nn)
                hp = (head[0], head[1] + n[0] * wb_t, head[2] + n[1] * wb_t)
                s = lp.place(cp.coach_screw(int(p["screw"][0]), p["screw"][1]), hp, nn)
                out.append(cp.part(f"Washer 8.4 x 24 {tag} frame {xf:.0f}", S(w), MAT["ss"], "fastener", bom=3,
                                   group="kit"))
                out.append(cp.part(f"Coach screw M8 x 100 {tag} frame {xf:.0f}", S(s), MAT["ss"], "fastener",
                                   bom=3, group="kit"))
            # end chocks, each with two counterbored wood screws driven parallel to the frame face
            for end, (c0, c1) in (("aft", (x0 - p["chock"][0], x0)), ("fwd", (x1, x1 + p["chock"][0]))):
                ch = cp.break_edges(prism(ksec, c0, c1), p["edge_r"] * 0.75)
                for k, (top, dn) in enumerate(_chock_screw_axes((c0 + c1) / 2, p)):
                    ch = ch - lp.bore(top, dn, cb_d, cb_h, back=5) - lp.bore(top, dn, cs_d + 0.5, cb_h + cs_l + 1)
                    bat = bat - lp.bore(top, dn, cs_d + 0.5, cb_h + cs_l + 1)
                    hp = (top[0], top[1] + dn[1] * cb_h, top[2] + dn[2] * cb_h)
                    ws = lp.place(lp.wood_screw(cs_d, cs_l), hp, (0, -dn[1], -dn[2]))
                    out.append(cp.part(f"Wood screw 5 x 60 chock {tag} {end} {k + 1}", S(ws), MAT["ss"], "fastener",
                                       bom=4, group="kit"))
                out.append(cp.part(f"End chock {tag} {end}", S(ch), MAT["wood"], "made", bom=4, group="kit"))
            out.append(cp.part(f"Shelf batten {tag}", S(bat), MAT["wood"], "made", bom=2, group="kit"))
            # foam core: four separate strips; cover sleeve round them
            for j, ls in enumerate(layer_sections(csec, p["layers"])):
                lay = cp.break_edges(prism(ls, x0 + p["cover_t"], x1 - p["cover_t"]), 1.5)
                out.append(cp.part(f"Foam strip {tag} layer {j + 1}", S(lay), MAT["foam"], "bought", bom=5,
                                   group="internal", color=COL["foam"]))
            env = prism(msec, x0, x1)
            core = prism(csec, x0 + p["cover_t"], x1 - p["cover_t"])
            out.append(cp.part(f"Cover {tag}", S(env - core), MAT["cover"], "made", bom=6, group="kit",
                               color=COL["cover"]))
            for xs in sx:
                wdt = p["strap_w"]
                loop = prism(so_out, xs - wdt / 2, xs + wdt / 2) - prism(so, xs - wdt / 2 - 1, xs + wdt / 2 + 1)
                out.append(cp.part(f"Hold-down strap {tag} at {xs}", S(loop), MAT["web"], "made", bom=8, group="kit",
                                   color=COL["web"]))
                yr = (msec[2][0] + msec[1][0]) / 2 - 40
                ring = Pos(xs, yr - 20, d["zt"] + p["strap_t"] + 0.3) * lp.d_ring_pair(wdt)
                out.append(cp.part(f"D-ring buckle {tag} at {xs}", S(ring), MAT["ss"], "bought", bom=9, group="kit"))
        # grab-line eye bolts through the rubbing strake and top plank, washers and nyloc nuts inside
        ez = p["eye_z"]
        yo = half(p["D"], 0, p) + p["strake"][0]
        yin = half(ez, p["t"], p)
        ring_y = None
        for xe in p["eyes_x"]:
            w_out = lp.place(cp.washer(8), (xe, yo, ez), (0, 1, 0))
            o = (xe, yo + cp.ISO[8][4], ez)
            eb = lp.place(lp.eye_bolt(8, 100, 24, 6), o, (0, 1, 0))
            w_in = lp.place(cp.washer(8), (xe, yin, ez), (0, -1, 0))
            nut = lp.place(lp.nyloc_nut(8), (xe, yin - cp.ISO[8][4], ez), (0, -1, 0))
            ring_y = o[1] + 5 + 15 + 3 - 1
            for nm, s in (("Eye bolt M8 x 100", eb), ("Washer M8 outside", w_out), ("Washer M8 inside", w_in),
                          ("Nyloc nut M8", nut)):
                out.append(cp.part(f"{nm} grab line {side} at {xe:.0f}", S(s), MAT["ss"], "fastener", bom=10,
                                   group="kit"))
        pts = []
        xs_ = p["eyes_x"]
        for a, b in zip(xs_[:-1], xs_[1:]):
            pts += [(a, ring_y, ez - 2), ((a + b) / 2, ring_y + 15, ez - 2 - p["rope_sag"])]
        pts.append((xs_[-1], ring_y, ez - 2))
        ends = [(xs_[0] - 120, ring_y, ez - 2 - 90)] + pts + [(xs_[-1] + 120, ring_y, ez - 2 - 90)]
        out.append(cp.part(f"Grab line {side}", S(cp.rope(ends, p["rope_d"])), MAT["rope"], "bought", bom=11,
                           group="kit", color=COL["rope"]))
        mx0, mx1, below, bh = p["mark"]
        ztop = p["D"] - below
        band = [(half(ztop - bh, 0, p), ztop - bh), (half(ztop, 0, p), ztop),
                (half(ztop, 0, p) + 1.2, ztop), (half(ztop - bh, 0, p) + 1.2, ztop - bh)]
        out.append(cp.part(f"Freeboard mark {side}", S(prism(band, mx0, mx1)), MAT["paint"], "made", bom=13,
                           group="kit"))
    # bailers on the floor between frames, lanyards to the middle thwart
    for xb in p["bailers_x"]:
        b = Solid.make_cone(110, 135, 260) - Pos(0, 0, 4) * Solid.make_cone(106, 131, 260)
        rim = Pos(0, 0, 252) * (Cylinder(139, 8) - Cylinder(131, 8))
        bucket = Pos(xb, 0, p["t"]) * (b + rim)
        out.append(cp.part(f"Bailer at {xb:.0f}", bucket, MAT["bucket"], "bought", bom=12, group="kit",
                           color=COL["bucket"]))
        tx = 3000.0 + (-110.0 if xb < 3000 else 110.0)
        sgn = 1 if xb < 3000 else -1
        sy = -1 if abs(xb - 3000.0) > 900.0 else 1     # the outer pair's lanyards run on the other side, clear of the inner buckets (D-O3)
        my = 220.0 if sy < 0 else 60.0
        lan = cp.rope([(xb + sgn * 146, 0, p["t"] + 262), ((xb + tx) / 2, sy * my, p["t"] + 200), (tx, sy * 120, 405)], 6)
        out.append(cp.part(f"Bailer lanyard at {xb:.0f}", lan, MAT["rope"], "bought", bom=12, group="kit"))
    # setting gauge: a fitting tool, shown lying flat on the ground beside the canoe
    g = gauge(p)
    bb = g.bounding_box()
    g = Rot(0, 90, 0) * Pos(-bb.center().X, -bb.center().Y, -bb.center().Z) * g
    gb = g.bounding_box()
    g = Pos(2100, 1500, -gb.min.Z) * g
    out.append(cp.part("Setting gauge (fitting tool, beside the canoe)", g, MAT["ply"], "made", bom=1, group="tool"))
    if with_hull:
        out += hull_parts(p)
    return out


# ---------------------------------------------------------------- option B, external sponsons
def option_b(p=PARAMS, with_hull=True):
    k, ca, sa, a = slope(p)
    zb, zt, W = p["B_zb"], p["B_zt"], p["B_w"]
    fl = p["B_flange"]
    bt, bh = p["B_batten"]
    ct, chh = p["B_clamp"]
    m_out = (ca, -sa)                          # outward normal of the planks (y, z), port side
    off = lambda z, e: half(z, 0, p) + e / ca  # noqa: E731  (point offset e outward, square to the planks)
    sec = [(off(zb, 0), zb), (off(zt, 0), zt), (off(zt, 0) + W, zt), (off(zb, 0) + W, zb)]
    csec = [(sec[0][0] + 2 / ca, zb + 2), (sec[1][0] + 2 / ca, zt - 2), (sec[2][0] - 2 / ca, zt - 2),
            (sec[3][0] - 2 / ca, zb + 2)]
    bsec = [(off(zb - bh, fl), zb - bh), (off(zb, fl), zb), (off(zb, fl + bt), zb), (off(zb - bh, fl + bt), zb - bh)]
    ksec = [(off(zt, fl), zt), (off(zt + chh, fl), zt + chh), (off(zt + chh, fl + ct), zt + chh), (off(zt, fl + ct), zt)]
    fsec_b = [(off(zb - bh, 0), zb - bh), (off(zb, 0), zb), (off(zb, fl), zb), (off(zb - bh, fl), zb - bh)]
    fsec_t = [(off(zt, 0), zt), (off(zt + chh, 0), zt + chh), (off(zt + chh, fl), zt + chh), (off(zt, fl), zt)]
    grip_in = p["t"] + p["frame_moulded"]
    out = []
    for side, sgn in (("port", 1), ("starboard", -1)):
        S = lambda s: _ccw_mirror(s, sgn)  # noqa: E731
        for i, (x0, x1) in enumerate(p["B_sponsons"]):
            tag = f"{side} {i + 1}"
            bat = cp.break_edges(prism(bsec, x0, x1), p["edge_r"])
            clamp = cp.break_edges(prism(ksec, x0, x1), 1.5)
            env = prism(sec, x0, x1)
            core = prism(csec, x0 + 2, x1 - 2)
            cover = (env - core) + prism(fsec_b, x0, x1) + prism(fsec_t, x0, x1)
            for xf in [f for f in p["frames"] if x0 + 40 < f < x1 - 40]:
                for zc, thick, name in ((zb - bh / 2, bt, "batten"), (zt + chh / 2, ct, "clamp strip")):
                    y_pl = half(zc, 0, p)
                    face = (xf, y_pl + (fl + thick) * m_out[0], zc + (fl + thick) * m_out[1])
                    grip = fl + thick + grip_in
                    hole = lp.bore(face, (0, -m_out[0], -m_out[1]), 9.0, grip + 2, back=2)
                    if name == "batten":
                        bat = bat - hole
                    else:
                        clamp = clamp - hole
                    cover = cover - hole
                    for nm, s in cp.hex_bolt_set(8, grip):
                        out.append(cp.part(f"{nm} sponson {tag} {name} frame {xf:.0f}",
                                           S(lp.place(s, face, (0, m_out[0], m_out[1]))), MAT["galv"], "fastener",
                                           group="kit"))
            for j, ls in enumerate(layer_sections(csec, 4)):
                lay = cp.break_edges(prism(ls, x0 + 2, x1 - 2), 1.5)
                out.append(cp.part(f"Sponson foam strip {tag} layer {j + 1}", S(lay), MAT["foam"], "bought",
                                   group="internal", color=COL["foam"]))
            out.append(cp.part(f"Sponson cover with flanges {tag}", S(cover), MAT["cover"], "made", group="kit",
                               color=COL["cover"]))
            out.append(cp.part(f"Outside shelf batten {tag}", S(bat), MAT["wood"], "made", group="kit"))
            out.append(cp.part(f"Top clamp strip {tag}", S(clamp), MAT["wood"], "made", group="kit"))
    if with_hull:
        out += hull_parts(p)
    return out


# ---------------------------------------------------------------- option C, double outrigger floats
def option_c(p=PARAMS, with_hull=True):
    bw, bd, bl = p["C_boom"]
    D = p["D"]
    st = p["C_saddle_t"]
    zb0 = D + st                                       # boom underside
    yf, zf = p["C_float_y"], p["C_float_z"]
    od, wall, fl = p["C_float"]
    R = od / 2
    fx0 = p["C_float_x0"]
    pw = p["C_post"]
    foot_l, foot_h = p["C_foot"]
    y_in = half(D, p["t"], p) + 0.5
    yo = half(D, 0, p) + p["strake"][0]
    yb = half(D, 0, p) + p["strake"][0] / 2              # vertical bolt line through the strake
    foot_z0 = zf + R - 20
    foot_z1 = foot_z0 + foot_h
    out = []
    for bi, bx in enumerate(p["C_booms_x"]):
        boom = cp.break_edges(Pos(bx, 0, zb0 + bd / 2) * Box(bw, bl, bd), 3.0)
        for sgn in (1, -1):
            side = "port" if sgn > 0 else "starboard"
            sad = cp.break_edges(Pos(bx, _y((y_in + yo) / 2, sgn), D + st / 2) * Box(bw, yo - y_in, st), 1.5)
            grip = bd + st + p["strake"][1]
            for dx in (-35.0, 35.0):
                top = (bx + dx, _y(yb, sgn), zb0 + bd)
                hole = lp.bore(top, (0, 0, -1), 11.0, grip + 2, back=2)
                boom = boom - hole
                sad = sad - hole
                for nm, s in cp.hex_bolt_set(10, grip):
                    out.append(cp.part(f"{nm} boom {bi + 1} {side} saddle {dx:+.0f}", lp.place(s, top, (0, 0, 1)),
                                       MAT["galv"], "fastener", group="kit"))
            out.append(cp.part(f"Gunwale saddle boom {bi + 1} {side}", sad, MAT["wood"], "made", group="kit"))
            # strut: post and foot in one hardwood piece, against the forward face of the boom
            xp0, xp1 = bx + bw / 2, bx + bw / 2 + pw
            xc = (xp0 + xp1) / 2
            yc = _y(yf, sgn)
            post = Pos(xc, yc, (foot_z1 + zb0 + bd) / 2) * Box(pw, pw, zb0 + bd - foot_z1)
            foot = Pos(xc, yc, (foot_z0 + foot_z1) / 2) * Box(pw, foot_l, foot_h)
            pipe_cut = Pos(xc, yc, zf) * Rot(0, 90, 0) * Cylinder(R, pw + 10)
            strut = cp.break_edges(post + foot, 1.5) - pipe_cut
            grip = pw + bw
            for zz in (zb0 + 22.0, zb0 + bd - 22.0):
                face = (xp1, yc, zz)
                hole = lp.bore(face, (-1, 0, 0), 11.0, grip + 2, back=2)
                strut = strut - hole
                boom = boom - hole
                for nm, s in cp.hex_bolt_set(10, grip):
                    out.append(cp.part(f"{nm} strut {bi + 1} {side} z{zz:.0f}", lp.place(s, face, (1, 0, 0)),
                                       MAT["galv"], "fastener", group="kit"))
            ub_leg = foot_z1 + 2 + 8.4 + 6 - zf
            for dx in (-18.0, 18.0):
                ub, Ru = lp.u_bolt(od, 10, ub_leg - (R + 3 + 5))
                out.append(cp.part(f"U-bolt M10 strut {bi + 1} {side} {dx:+.0f}", Pos(xc + dx, yc, zf) * ub,
                                   MAT["ss"], "fastener", group="kit"))
                for yy in (yc - Ru, yc + Ru):
                    strut = strut - lp.bore((xc + dx, yy, foot_z1), (0, 0, -1), 11.0, foot_h + 30, back=2)
                    out.append(cp.part(f"Washer M10 U-bolt {bi + 1} {side} {dx:+.0f} {yy:.0f}",
                                       Pos(xc + dx, yy, foot_z1) * cp.washer(10), MAT["ss"], "fastener", group="kit"))
                    out.append(cp.part(f"Nyloc nut M10 U-bolt {bi + 1} {side} {dx:+.0f} {yy:.0f}",
                                       Pos(xc + dx, yy, foot_z1 + cp.ISO[10][4]) * lp.nyloc_nut(10), MAT["ss"],
                                       "fastener", group="kit"))
            out.append(cp.part(f"Float strut boom {bi + 1} {side}", strut, MAT["wood"], "made", group="kit"))
        out.append(cp.part(f"Outrigger boom {bi + 1}", boom, MAT["wood"], "made", group="kit"))
    for sgn in (1, -1):
        side = "port" if sgn > 0 else "starboard"
        yc = _y(yf, sgn)
        tube = Pos(fx0, yc, zf) * Rot(0, 90, 0) * cp.round_tube(od, wall, fl)
        out.append(cp.part(f"Float pipe {side}, HDPE 250 SDR 26", tube, MAT["hdpe"], "bought", group="kit"))
        for end, xe in (("aft", fx0), ("fwd", fx0 + fl)):
            x_cap = xe - p["C_cap_t"] if end == "aft" else xe
            cap = cp.break_edges(Pos(x_cap, yc, zf) * Rot(0, 90, 0) * Pos(0, 0, p["C_cap_t"] / 2) *
                                 Cylinder(R, p["C_cap_t"]), 2.0)
            out.append(cp.part(f"Float end cap {side} {end}", cap, MAT["hdpe"], "made", group="kit"))
            bead = Pos(xe, yc, zf) * Rot(0, 90, 0) * lp.ring_bead(R, 6.0, 3.0)
            out.append(cp.part(f"Butt-fusion bead {side} {end}", bead, MAT["hdpe"], "weld", group="kit"))
    if with_hull:
        out += hull_parts(p)
    return out


def components(option=CHOSEN, p=PARAMS):
    """kit 1.9: the parts of one concept option as cad_parts.part() dicts (context: the owner's canoe)."""
    return {"A": option_a, "B": option_b, "C": option_c}[option](p)


KEYMAP = [("Shelf batten", "battens", "batten"), ("Coach screw", "screws", "screw"), ("Washer 8.4", "screws", "screw"),
          ("End chock", "chocks", "chock"), ("Wood screw", "chocks", "chock"), ("Foam strip", "cores", "core"),
          ("Cover", "covers", "cover"), ("Hold-down strap", "straps", "strap"), ("D-ring buckle", "rings", "D-rings"),
          ("Grab line", "grablines", "grab line"), ("Freeboard mark", "marks", "freeboard mark"),
          ("Bailer", "bailers", "bailer")]


def detail_kit(p=PARAMS):
    """The detailed option A pieces grouped like build_kit(): {key: [(label, shape)]}, one entry per batten,
    chock, module, strap and so on, with its fasteners fused in; labels keep build_kit's words ("batten port 2",
    "screw port 2 frame 2100", "strap port 2 at 2400") so the picture scripts can pick pieces by token."""
    parts = [q for q in option_a(p, with_hull=False) if q["group"] != "tool"]
    out = {k: [] for k in ("battens", "screws", "chocks", "cores", "covers", "straps", "rings", "eyes", "grablines",
                           "bailers", "marks")}
    import re
    groups = {}
    for q in parts:
        n = q["name"]
        if "grab line" in n and q["kind"] == "fastener":
            side = n.split("grab line ")[1].split()[0]
            groups.setdefault(("eyes", f"eye bolts {side}"), []).append(q["shape"])
            continue
        for prefix, key, word in KEYMAP:
            if n.startswith(prefix):
                rest = n[len(prefix):].strip()
                if key == "screws":
                    rest = re.sub(r"^(M8 x 100|x 24)\s*", "", rest)
                if key == "chocks":
                    m = re.search(r"(port|starboard) (\d) (aft|fwd)", rest)
                    label = f"chock {m.group(1)} {m.group(2)} {m.group(3)}"
                elif key == "cores":
                    label = "core " + re.sub(r" layer \d", "", rest)
                elif key == "bailers":
                    label = "bailer " + rest.replace("lanyard ", "")
                else:
                    label = f"{word} {rest}"
                groups.setdefault((key, label), []).append(q["shape"])
                break
    for (key, label), shapes in groups.items():
        out[key].append((label, shapes[0] if len(shapes) == 1 else Compound(shapes)))
    return out


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
