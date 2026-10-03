"""LevelHull general arrangement sheet LVH-DWG-001, Rev P3 (TRL 3; LVH-DDR-002 and LVH-DDR-003 applied).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/LVH-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py: the kit fitted in the reference canoe (top, front and right views at 1:50),
section A-A across the canoe through module 2 at 1:20, and the main sizes. Dimensions come from
PARAMS and derived(), so they follow any parameter change. The concept blueprint in media/ is
LVH-DWG-010; the making sketches are LVH-DWG-101 onward (cad/src/build_plan_media.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Compound, Pos  # noqa: E402
from drawing import Sheet, _t, project_views, INK, MUTED  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
DATE = "2026-10-03"
SEC_X = 2400.0          # section A-A: through module 2 and its aft strap
SEC_K = 0.05            # 1:20


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = M.derived(P)
    work = ROOT / "cad" / "drawings" / "_ga_views"
    asm = M.assembly(P, with_hull=True)
    views = project_views(asm, work)
    slab = Pos(SEC_X - 145, 0, 400) * Box(350, 4000, 2000)   # takes in the frame at 2,100 and the strap at 2,400
    sec = Compound([asm & slab])
    sv = project_views(sec, work / "sec")
    sb = sec.bounding_box()
    s = Sheet(project="LevelHull", title="Flotation retrofit in the reference canoe: general arrangement",
              dwg_no="LVH-DWG-001", rev="P3", author="Amish Chadha", date=DATE, scale=0.02,
              material="Kit per bom/bom.csv; canoe is the owner's boat (reference shown). PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "LVH-DDR-002: design for construction", DATE, "AC"),
                         ("P3", "LVH-DDR-003: modules widened to 220", DATE, "AC")])
    s.add_ortho(views)
    # section A-A at 1:20, left-aligned in the right column
    vw = (sb.max.Y - sb.min.Y) * SEC_K
    vh = (sb.max.Z - sb.min.Z) * SEC_K
    x0, y0 = 279.0, 40.0
    s.add_svg(sv["right"], x0, y0, vw, vh, scale=SEC_K)
    L = [_t(x0 + vw / 2, y0 + vh + 6, "SECTION A-A", 2.8, 600, INK, "middle"),
         _t(x0 + vw / 2, y0 + vh + 10, f"Scale 1:20; looking aft (along -X), {SEC_X / 1000:.1f} m from the transom (frame at 2.1 m behind)", 2.2, 400, MUTED, "middle")]
    cy, cz = (sb.min.Y + sb.max.Y) / 2, (sb.min.Z + sb.max.Z) / 2
    X = lambda y: x0 + vw / 2 + (y - cy) * SEC_K   # noqa: E731
    Z = lambda z: y0 + vh / 2 - (z - cz) * SEC_K   # noqa: E731
    tx = x0 + vw + 4
    ms = M.module_section(P)
    yc = sum(q[0] for q in ms) / 4
    zc = (D["zb"] + D["zt"]) / 2
    L += leader(X(yc), Z(zc), tx, 47, "FOAM CORE (5) IN COVER (6)")
    bs = M.batten_section(P)
    L += leader(X(sum(q[0] for q in bs) / 4), Z((D["zb"] + D["bz0"]) / 2), tx, 54, "SHELF BATTEN (2), M8 SCREW (3)")
    L += leader(X(ms[2][0] + 20), Z(D["zt"] + 2), tx, 40, "STRAP (8), D-RINGS (9)")
    yo = M.half(P["D"], 0, P) + P["strake"][0] + 26
    L += leader(X(yo), Z(P["eye_z"]), tx, 33, "EYE BOLT (10), GRAB LINE (11)")
    L += leader(X(M.y_frame(250)), Z(250), tx, 61, "FRAME (OWNER'S CANOE)")
    # module and freeboard sizes on the port side
    s._dim(X(ms[1][0]), Z(D["zt"]), X(ms[1][0]), Z(D["zb"]), f"{D['zt'] - D['zb']:.0f}", "left", off=4)
    s._layers += L
    s.add_notes("Main sizes and figures (mm unless stated)", [
        "Reference canoe 8,000 long, beam 1,600, depth 650, flare 31.6 deg",
        f"8 modules, 4 a side: {', '.join(f'{v:,.0f}' for v in D['mod_len'])} long",
        f"Module {P['mod_w']:.0f} wide x {D['zt'] - D['zb']:.0f} high, top {P['mod_top_gap']:.0f} below gunwale",
        "Module = four 50 PE foam layers in a tarpaulin sleeve (5, 6)",
        f"Battens 50 thick, {P['batten_h']:.0f} high, {P['batten_over']:.0f} past each module end",
        f"{D['n_screws']} coach screws M8 x 100, one into every frame crossed",
        f"{D['n_straps']} straps, 50 webbing, in the bays between frames",
        "Chocks 40 long, 50 high, at both ends of every module",
        f"Eye bolts at {', '.join(f'{v:,.0f}' for v in P['eyes_x'])} from transom",
        "Freeboard mark: top edge 50 below the gunwale, amidships",
        "Swamped, design load: 113 freeboard amidships, 92 lowest",
        "Third-angle; X from transom, Y to port; (n) = BOM line",
    ], x=276, y=112, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "LVH-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
