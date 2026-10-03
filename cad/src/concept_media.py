"""LevelHull concept media (TRL 3, constructable design of LVH-DDR-002), generated from the model.

Run from the repo root:  python cad/src/concept_media.py
Takes the kit and the reference canoe from cad/src/model.py and renders the media set with
.kit/concept.py: media/hero.png (with a 1.75 m person), media/cutaway.png (a cut across the canoe), media/exploded.png
(one module bay pulled apart, numbers match bom/bom.csv), media/concept-blueprint.png, .pdf and .svg
(LVH-DWG-010), media/model.glb and media/viewer.html. Grey parts are context (the owner's canoe and
outboard motor) with no BOM number. No flow diagram: the kit moves no energy or material.
Figures on the sheet come from docs/04-calcs/results.csv (LVH-CAL-001).
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import concept as K  # noqa: E402
from concept import Part, render_all  # noqa: E402
from build123d import Box, Compound, Plane, Pos, mirror  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
D = M.derived(P)
PROJECT = "LevelHull"
TITLE = "Passive flotation retrofit for a wooden fishing canoe"

COLORS = {"gauge": "#D4A017", "battens": "#92400E", "screws": "#374151", "chocks": "#78350F",
          "cores": "#FACC15", "covers": "#EA580C", "straps": "#1D4ED8", "rings": "#6B7280",
          "eyes": "#4B5563", "grablines": "#0F766E", "bailers": "#16A34A", "marks": "#DC2626"}
HULL = "#D6D3D1"
WOODC = "#A8A29E"


def R():
    rows = {r["tag"]: r for r in csv.DictReader((ROOT / "docs" / "04-calcs" / "results.csv").open())}
    return lambda t: rows[t]["value"]


def kit_parts(comps, keys=None):
    out = []
    for key, (num, name) in M.BOM.items():
        if key == "gauge" or (keys and key not in keys):
            continue
        out.append(Part(name, comps[key], COLORS[key], num))
    return out


def canoe_parts(motor=True):
    h = M.hull_context(P)
    ps = [Part("Reference canoe planking (owner's boat)", h["shell"], HULL, None),
          Part("Canoe frames, thwarts and rubbing strakes", Compound(h["frames"] + h["thwarts"] + h["strakes"]), WOODC, None)]
    if motor:
        ps.append(Part("15 hp outboard motor (context)", M.motor_context(P), "#6B7280", None))
    return ps


def exploded_bay():
    """One module bay on the port side (module 2), pulled apart, seen from the starboard side."""
    k = M.build_kit(P)
    h = M.hull_context(P)
    x0, x1 = P["modules"][1]
    win = Pos((x0 + x1) / 2, 600, 400) * Box(x1 - x0 + 500, 1200, 1000)
    shell = h["shell"] & win
    frames = Compound([f & win for f in h["frames"] if x0 - 300 < (f.bounding_box().min.X + 25) < x1 + 300])
    strake = h["strakes"][0] & win
    sel = lambda key: Compound([s for n, s in k[key] if n.split()[1:3] == ["port", "2"]])  # noqa: E731
    up, inb = 1.0, -1.0
    parts = [
        Part("Canoe planking (context)", shell, HULL, None),
        Part("Canoe frames (context)", Compound([frames, strake]), WOODC, None),
        Part("Shelf batten", sel("battens"), COLORS["battens"], 2, (0, inb * 260, -60)),
        Part("Coach screws M8 x 100", sel("screws"), COLORS["screws"], 3, (0, inb * 520, -60)),
        Part("End chocks", sel("chocks"), COLORS["chocks"], 4, (0, inb * 260, 140 * up)),
        Part("Foam core, four 50 mm layers", sel("cores"), COLORS["cores"], 5, (0, inb * 120, 900 * up)),
        Part("Cover", sel("covers"), COLORS["covers"], 6, (0, inb * 120, 480 * up)),
        Part("Hold-down straps", sel("straps"), COLORS["straps"], 8, (0, inb * 700, 200)),
        Part("D-ring buckles", sel("rings"), COLORS["rings"], 9, (0, inb * 700, 420)),
    ]
    return parts


def cross_section(parts, xc=2250.0):
    """Cutaway across the canoe through module 2, looking aft from the bow side."""
    cutter = Pos(xc - 6000, 0, 400) * Box(12000, 4000, 3000)
    out = []
    for q in parts:
        if "motor" in q.name:
            continue
        s = q.shape & cutter
        if s is not None and s.volume > 1:
            out.append(Part(q.name, s, q.color, q.bom))
    return out


def web(parts):
    """Coarse glTF tessellation (1 mm chord, 0.35 rad) keeps media/model.glb a few MB."""
    import functools
    import build123d as bd
    orig = bd.export_gltf
    bd.export_gltf = functools.partial(orig, linear_deflection=1.0, angular_deflection=0.35)
    try:
        return K.export_web_model(parts, "media", title=f"{PROJECT}: {TITLE}")
    finally:
        bd.export_gltf = orig


def main():
    r = R()
    comps = M.build_components(P)
    parts = canoe_parts() + kit_parts(comps)
    render_all(
        parts, project=PROJECT, title=f"{TITLE} concept", dwg_no="LVH-DWG-010",
        key_figures=[
            "Reference canoe 8.0 x 1.6 x 0.65 m, 15 hp outboard; each hull sized with the calculator",
            f"8 modules of closed-cell PE foam, 200 x 200 mm, {D['run_side'] / 1000:.2f} m a side; {D['vol_total']:.2f} m3",
            "Fitted high under the gunwale on shelf battens screwed to the frames",
            f"Swamped, design load: {float(r('F1')):.0f} mm freeboard amidships, {float(r('F2')):.0f} mm lowest",
            f"Roll stiffness {float(r('F6')):.0f} kg m/rad; same foam on the floor {float(r('F17')):.0f}: capsizes",
            f"Kit {float(r('K1')):.0f} kg, USD {float(r('C1')):.0f} per canoe; never a substitute for life jackets",
        ],
        scale_figure=True, web_model=False, cut=False,
        cut_exclude=("15 hp outboard motor (context)",),
    )
    # exploded close-up of one module bay (replaces the whole-boat exploded view, where the kit is too small to read)
    K._render(exploded_bay(), ROOT / "media" / "exploded.png", offsets=True, labels=True, elev=22, azim=-118,
              size=(10, 7.5), title=f"{PROJECT}: exploded view of one module bay",
              note="Port side, module 2 of 4, seen from inside the canoe (from the starboard side, aft and above, "
                   "22 deg elevation); numbers match bom/bom.csv; grey is the owner's canoe")
    K._render(cross_section(parts), ROOT / "media" / "cutaway.png", elev=12, azim=8, size=(10, 7.5),
              title=f"{PROJECT}: cutaway across the canoe",
              note="Cut across the canoe 2.25 m forward of the transom, through module 2 on each side; seen from forward and "
                   "slightly to port, 12 deg elevation. The modules sit high under the gunwale, so when the canoe is swamped "
                   "they cut the waterline and hold it upright")
    web(parts)
    import shutil
    for d in ("_views", "_views_fig"):
        shutil.rmtree(ROOT / "media" / d, ignore_errors=True)


if __name__ == "__main__":
    main()
