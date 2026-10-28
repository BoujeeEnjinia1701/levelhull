"""LevelHull product model for the photoreal renders (kit 1.9.1), built from components(CHOSEN) in model.py.

Every kit piece is the detailed option A part of cad/src/model.py (battens with their coach screws and washers,
chocks with their counterbored screws, foam strips, covers, straps and D-ring buckles, eye bolts, nyloc nuts,
grab lines, freeboard marks, bailers and lanyards), fitted in the reference canoe (8.0 m, 1.6 m beam, 0.65 m deep).
Context added for the renders only, as recorded in docs/REVIEW.md: the 15 hp outboard tilted up as it is on the
beach, a sand beach at the landing (site) and a 1.75 m person standing on the sand (scale). Ground level is z = 0,
the outside of the canoe's bottom, where the canoe rests on the sand. The setting gauge (a fitting tool) is left
out of the pictures. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (kit pieces), "internal" (foam strips), "canoe" (the owner's canoe and motor), "context" (beach and
person), "bay" (the detail view: port module 2 with the canoe cut back round it).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Pos, Rot  # noqa: E402
import cad_parts as cp  # noqa: E402
import model as M  # noqa: E402

TITLE = "LevelHull: passive flotation retrofit for a wooden fishing canoe"

_SITE = ["--scene=outdoor", "--ground=sand", "--ground-z=0", "--sun=38,-48", "--lens=35"]

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "canoe", "context"], "explode": False, "el": 16, "az": -36,
     "args": _SITE,
     "note": "Site render at a beach landing from the starboard bow, about 16 deg elevation: the 8 m reference canoe on the "
             "sand with eight orange buoyancy modules strapped high under the gunwales, grab lines along both sides, the "
             "freeboard mark amidships and the outboard tilted up; 1.75 m person standing on the sand for scale"},
    {"name": "studio", "groups": ["shell", "internal", "canoe"], "explode": False, "el": 30, "az": -40,
     "note": "Studio render from the starboard bow and above, about 30 deg elevation: the kit fitted in the reference "
             "canoe, modules on their shelf battens, straps and D-rings, grab lines, bailers on the floor"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 28, "az": -30,
     "note": "Exploded view from the front right and above, about 28 deg elevation: shelf battens with coach screws, end "
             "chocks with their screws, foam strips, covers, straps and D-rings, eye bolts and grab lines, freeboard marks "
             "and bailers lifted out of their places; canoe not shown"},
    {"name": "detail", "groups": ["bay"], "explode": False, "el": 22, "az": -120,
     "note": "Detail of one module bay from inside the canoe (from the starboard side, aft and above, about 22 deg "
             "elevation): the module in its tarpaulin cover on a hardwood shelf batten coach-screwed to the frames, two "
             "webbing straps with D-ring buckles, and the counterbored end chocks"},
]

EXPLODE = [("Shelf batten", (0, 0, 500)), ("Coach screw", (0, 0, 600)), ("Washer 8.4", (0, 0, 600)),
           ("End chock", (0, 0, 700)), ("Wood screw", (0, 0, 760)), ("Foam strip", (0, 0, 1100)),
           ("Cover", (0, 0, 850)), ("Hold-down strap", (0, 0, 1300)), ("D-ring", (0, 0, 1350)),
           ("Grab line", (0, 0, 300)), ("Eye bolt", (0, 0, 400)), ("Washer M8", (0, 0, 400)),
           ("Nyloc", (0, 0, 400)), ("Freeboard mark", (0, 0, 200)), ("Bailer", (0, 0, 900))]


def _explode(name):
    for prefix, v in EXPLODE:
        if name.startswith(prefix):
            return v
    return (0, 0, 0)


def tilted_motor(p=M.PARAMS):
    """The 15 hp outboard tilted up 70 deg about its transom clamp, as it is on the beach (all above the sand)."""
    D = p["D"]
    return Pos(-40, 0, D) * Rot(0, 70, 0) * Pos(40, 0, -D) * M.motor_context(p)


def product_parts(p=M.PARAMS):
    out = []
    for q in M.components(M.CHOSEN, p):
        if q["group"] == "tool":
            continue
        r = dict(q)
        if q["kind"] == "context":
            r["group"] = "canoe"
        else:
            r["group"] = "internal" if q["group"] == "internal" else "shell"
            r["explode"] = _explode(q["name"])
        out.append(r)
    out.append(cp.part("15 hp outboard motor, tilted up (owner's)", tilted_motor(p), "matte_black", kind="context",
                       group="canoe"))
    out.append(cp.part("Beach sand at the landing (site)", Pos(3500, 0, -150) * Box(16000, 9000, 300), "sand",
                       kind="context", group="context"))
    from context_parts import mannequin
    person = Pos(3300, 1700, 0) * mannequin(1750, "stand")
    out.append(cp.part("Person, 1.75 m, standing on the sand (scale)", person, "skin", kind="context", group="context"))
    # detail bay: port module 2 with the canoe cut back round it
    x0, x1 = p["modules"][1]
    win = Pos((x0 + x1) / 2, 600, 375) * Box(x1 - x0 + 500, 1200, 850)
    h = M.hull_context(p)
    frames = Compound([f & win for f in h["frames"] if x0 - 300 < f.bounding_box().center().X < x1 + 300])
    out.append(cp.part("Bay: canoe planking", h["shell"] & win, "timber", kind="context", group="bay", color="#2F6E8F"))
    out.append(cp.part("Bay: frames and strake", Compound([frames, h["strakes"][0] & win]), "timber", kind="context",
                       group="bay"))
    for q in M.components(M.CHOSEN, p):
        n = q["name"]
        if q["kind"] != "context" and " port 2" in n and not n.startswith("Freeboard"):
            r = dict(q)
            r["group"], r["name"] = "bay", "Bay: " + n
            out.append(r)
    return out


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(q["group"] for q in ps)))
    mz = min(q["shape"].bounding_box().min.Z for q in ps if q["group"] in ("shell", "internal", "canoe"))
    print(f"lowest point of the canoe, kit and motor: z = {mz:.1f} mm (ground at 0)")
