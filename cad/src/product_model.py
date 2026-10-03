"""LevelHull product appearance model (build123d), TRL 3, constructable design (LVH-DDR-002).

Finished-product look for photoreal renders, built from the constructable model: every kit piece of
cad/src/model.py build_kit() is used as it is (battens, coach screws, chocks, foam cores, covers,
straps and D-rings, eye bolts, grab lines, freeboard marks, bailers), fitted in the reference canoe
of model.hull_context() with its 15 hp outboard (model.motor_context()). Only the look is added, as
recorded in docs/REVIEW.md: a sand beach slab under the canoe and a 1.75 m mannequin standing beside
it for scale; the detail view repeats one module bay (port module 2) with the canoe cut back.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X from the transom forward, Y to port, Z up from the outside of the bottom.
Groups: "shell" (kit pieces seen from outside), "internal" (foam cores), "context" (canoe, motor,
beach, mannequin), "bay" (the detail view only).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Pos, Rot  # noqa: E402
import model as M  # noqa: E402

TITLE = "LevelHull: passive flotation retrofit for a wooden fishing canoe"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 28, "az": -30,
     "note": "Product render from the front right and above (about 28 deg elevation): the reference 8 m canoe on the beach "
             "with eight orange buoyancy modules strapped high under the gunwales, grab lines along both sides and the "
             "freeboard mark amidships; 1.75 m person standing beside the canoe for scale"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 28, "az": -30,
     "note": "Exploded view from the front right and above (about 28 deg elevation): shelf battens and coach screws, end "
             "chocks, foam cores, covers, straps and D-rings, eye bolts and grab lines, freeboard marks and bailers lifted "
             "out of their places; canoe not shown"},
    {"name": "detail", "groups": ["bay"], "explode": False, "el": 22, "az": -120,
     "note": "Detail of one module bay from inside the canoe (from the starboard side, aft and above, about 22 deg "
             "elevation): the foam module in its tarpaulin cover on a hardwood shelf batten screwed to the frames, "
             "two webbing straps with D-ring buckles, and the end chocks"},
]

C_WOOD = "#8A5A2B"
C_HULL = "#6E4A2E"
C_PAINT = "#2F6E8F"       # painted topsides of the canoe
C_FOAM = "#F2D04B"
C_COVER = "#E2621B"
C_STRAP = "#1E40AF"
C_STEEL = "#A9B0B8"
C_ROPE = "#0F766E"
C_MARK = "#DC2626"
C_BUCKET = "#16A34A"
C_MOTOR = "#2B2F36"
C_SAND = "#D8C7A3"
C_CLAY = "#B9B4AC"

LOOK = {  # kit key: (name, color, material, explode)
    "battens": ("Shelf battens, hardwood", C_WOOD, "wood", (0, 0, 500)),
    "screws": ("Coach screws M8 x 100", C_STEEL, "metal", (0, 0, 600)),
    "chocks": ("End chocks", C_WOOD, "wood", (0, 0, 700)),
    "cores": ("Foam cores, closed-cell PE", C_FOAM, "rubber", (0, 0, 1100)),
    "covers": ("Covers, PVC tarpaulin", C_COVER, "fabric", (0, 0, 850)),
    "straps": ("Hold-down straps, polyester webbing", C_STRAP, "fabric", (0, 0, 1300)),
    "rings": ("D-ring buckles, stainless", C_STEEL, "metal", (0, 0, 1350)),
    "eyes": ("Grab-line eye bolts, stainless", C_STEEL, "metal", (0, 0, 400)),
    "grablines": ("Grab lines, polyester rope", C_ROPE, "fabric", (0, 0, 300)),
    "marks": ("Freeboard marks, orange enamel", C_MARK, "painted", (0, 0, 200)),
    "bailers": ("Bailers, 10 L buckets", C_BUCKET, "painted", (0, 0, 900)),
}


def product_parts(p=M.PARAMS):
    k = M.build_kit(p)
    h = M.hull_context(p)
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(explode)})

    for key, (name, color, mat, ex) in LOOK.items():
        group = "internal" if key == "cores" else "shell"
        add(name, Compound([s for _, s in k[key]]), color, mat, M.BOM[key][0], group, ex)
    add("Canoe planking (owner's boat)", h["shell"], C_PAINT, "painted", None, "context")
    add("Canoe frames and thwarts", Compound(h["frames"] + h["thwarts"]), C_HULL, "wood", None, "context")
    add("Rubbing strakes", Compound(h["strakes"]), C_HULL, "wood", None, "context")
    add("15 hp outboard motor", M.motor_context(p), C_MOTOR, "painted", None, "context")
    add("Sand beach", Pos(3500, 0, -40) * Box(13000, 6000, 80), C_SAND, "clay", None, "context")
    from context_parts import mannequin
    person = Pos(3300, 1500, 0) * mannequin(1750, "stand")       # faces -Y, toward the canoe
    add("Person, 1.75 m (scale), standing beside the canoe", person, C_CLAY, "clay", None, "context")
    # detail bay: port module 2 with the canoe cut back around it
    x0, x1 = p["modules"][1]
    win = Pos((x0 + x1) / 2, 600, 375) * Box(x1 - x0 + 500, 1200, 850)
    sel = lambda key: Compound([s for n, s in k[key] if n.split()[1:3] == ["port", "2"]])  # noqa: E731
    frames = Compound([f & win for f in h["frames"] if x0 - 300 < f.bounding_box().center().X < x1 + 300])
    add("Bay: canoe planking", h["shell"] & win, C_PAINT, "painted", None, "bay")
    add("Bay: frames and strake", Compound([frames, h["strakes"][0] & win]), C_HULL, "wood", None, "bay")
    for key in ("battens", "screws", "chocks", "covers", "straps", "rings"):
        name, color, mat, _ = LOOK[key]
        add(f"Bay: {name}", sel(key), color, mat, M.BOM[key][0], "bay")
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:55s} {q['group']:9s} {q['material']:8s} vol={s.volume / 1000:10.1f} cm3")
