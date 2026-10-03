"""LevelHull prototype build plan pictures (LVH-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png    one of each component pulled apart, numbered in build order
    cad/drawings/LVH-DWG-101 to 106    making sketches for the made components
    docs/05-build-plan/joint-NN.png    close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png     one picture per assembly step
The bay pictures show module 2 on the port side; the other seven bays are the same.
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Box, Compound, Pos  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
D = M.derived(P)
OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
K = M.build_kit(P)
H = M.hull_context(P)
CA, SA = D["cos"], D["sin"]

COL = {"gauge": "#D4A017", "batten": "#92400E", "screw": "#374151", "chock": "#78350F", "core": "#FACC15",
       "cover": "#EA580C", "strap": "#1D4ED8", "ring": "#6B7280", "eye": "#4B5563", "line": "#0F766E",
       "mark": "#DC2626", "bailer": "#16A34A", "hull": "#D6D3D1", "frame": "#A8A29E"}


def pick(key, *tokens):
    return Compound([s for n, s in K[key] if all(t in n.split() for t in tokens)])


def bay(key):
    return pick(key, "port", "2")


def window(x0, x1, y0=0.0, y1=1200.0, z0=-50.0, z1=800.0):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def canoe_window(win):
    shell = H["shell"] & win
    fr = Compound([f & win for f in H["frames"] if f.bounding_box().max.X > win.bounding_box().min.X
                   and f.bounding_box().min.X < win.bounding_box().max.X])
    th = [t & win for t in H["thwarts"] if t.bounding_box().max.X > win.bounding_box().min.X
          and t.bounding_box().min.X < win.bounding_box().max.X]
    st = H["strakes"][0] & win
    return Part("Canoe planking", shell, COL["hull"]), Part("Canoe frames and rubbing strake", Compound([fr, st] + th), COL["frame"])


X0, X1 = P["modules"][1]
BAYWIN = window(X0 - 250, X1 + 250)
HULL_BAY = canoe_window(BAYWIN)
NIN = (0, -CA, SA)                       # inward normal of the frame faces, port side


def mul(v, k):
    return tuple(c * k for c in v)


# components in build order (one of each; the names give the count)
def components():
    return [
        Part("Setting gauge (1, a tool)", M.gauge(P), COL["gauge"], 1, (-1300, 300, 450)),
        Part("Shelf battens (8)", bay("battens"), COL["batten"], 2, (0, -420, 0)),
        Part("Coach screws and washers (20)", bay("screws"), COL["screw"], 3, mul(NIN, 700)),
        Part("End chocks (16)", bay("chocks"), COL["chock"], 4, (0, -300, 300)),
        Part("Foam cores (8), four layers each", bay("cores"), COL["core"], 5, (0, -150, 1150)),
        Part("Covers (8)", bay("covers"), COL["cover"], 6, (0, -150, 700)),
        Part("Hold-down straps with D-rings (16)", Compound([bay("straps"), bay("rings")]), COL["strap"], 8, (0, -800, 250)),
        Part("Grab-line eye bolts (8)", pick("eyes", "port"), COL["eye"], 10, (0, 450, 0)),
        Part("Grab lines (2)", pick("grablines", "port"), COL["line"], 11, (0, 700, -250)),
        Part("Freeboard marks (2), painted", pick("marks", "port"), COL["mark"], 13, (0, 450, -400)),
        Part("Bailers (2)", Compound([s for _, s in K["bailers"]]), COL["bailer"], 12, (0, -400, -300)),
    ]


def overview():
    ps = components()
    # show the bay components and one example of the long items, near the bay
    ps[7].shape = Compound([s for s in [pick("eyes", "port")] ]) & window(X0 - 200, X1 + 900, 600, 1200)
    ps[8].shape = pick("grablines", "port") & window(X0 - 200, X1 + 900, 600, 1300, -200, 800)
    ps[9].shape = pick("marks", "port")
    ps[9].shape = Pos(-800, 0, 0) * ps[9].shape
    ps[10].shape = K["bailers"][0][1]
    bv.overview(ps, OUT / "overview.png", "LevelHull: the kit for one canoe, in build order",
                subtitle="One module bay of the eight shown, pulled apart; counts are for the whole canoe. "
                         "Plan, not yet built", elev=24, azim=-120, size=(11, 7.5), key=True)


def sheets():
    nb = [Part("Canoe", Compound([HULL_BAY[0].shape, HULL_BAY[1].shape]), "#D1D5DB")]
    g = M.gauge(P)
    gnb = [Part("Canoe", Compound([H["shell"] & window(1700, 2500), Compound([f & window(1700, 2500) for f in H["frames"] if 1700 < f.bounding_box().center().X < 2500]),
                                   H["strakes"][0] & window(1700, 2500)]), "#D1D5DB")]
    bv.component_sheet(Part("Setting gauge", g, COL["gauge"]), gnb, "LevelHull", "LVH-DWG-101",
                       "Setting gauge (fitting tool)", "12 mm exterior plywood",
                       ["Cut from 12 mm exterior plywood; one gauge per hull shape.",
                        "Long edge follows the slope of the frame faces (31.6 deg here).",
                        "Hook rests on the gunwale; the lip drops outside the strake.",
                        f"Notches mark the batten top ({P['D'] - D['zb']:.0f} below the gunwale)",
                        f"  and bottom ({P['D'] - D['bz0']:.0f} below the gunwale).",
                        "Make it on the first frame: offer up, trim the hook until the",
                        "  long edge lies flat on the frame face, then cut the notches.",
                        "Use: hook over the gunwale at each frame, mark both notches."],
                       DATE, inset_view=(24, -120))
    bat = bay("battens")
    bv.component_sheet(Part("Shelf batten", bat, COL["batten"]), nb, "LevelHull", "LVH-DWG-102",
                       "Shelf batten (8, four lengths)", "Durable hardwood, ripped from 50 x 100",
                       ["Rip 50 x 100 hardwood; plane top and bottom to the flare angle",
                        "  so the section is a 50 x 82 parallelogram, 70 high.",
                        "Lengths: 960 (2), 1,480 (4), 1,180 (2); module length + 80.",
                        "Drill 9 mm clearance square to the inboard face at every",
                        f"  frame it crosses, {P['screw_z']:.0f} below the top edge measured up the face.",
                        "Seal the ends and holes before fitting.",
                        "Fits: flat face on the frame faces, top edge on the gauge mark;",
                        "  one M8 x 100 coach screw into each frame (5.5 pilot, 50 deep)."],
                       DATE, inset_view=(24, -120))
    ch = pick("chocks", "port", "2", "aft")
    bv.component_sheet(Part("End chock", ch, COL["chock"]), nb, "LevelHull", "LVH-DWG-103",
                       "End chock (16)", "Batten offcut, hardwood",
                       ["Cut 40 long from batten offcut; 50 high, same slope as the batten.",
                        "Two 5 x 60 stainless wood screws down into the batten top.",
                        "Fits: on the batten top, tight against the module end,",
                        "  sloping face on the frame face.",
                        "Seal the cut ends."],
                       DATE, inset_view=(24, -120))
    core = bay("cores")
    bv.component_sheet(Part("Foam core", core, COL["core"]), nb, "LevelHull", "LVH-DWG-104",
                       "Foam core (8, four lengths)", "Closed-cell polyethylene foam, 50 mm sheet",
                       ["Four layers of 50 foam, each a strip 196 wide (inside the cover).",
                        "Cut both long edges of every strip at the flare angle, then stack",
                        "  so each layer sits 31 further outboard than the one below.",
                        "Lengths (cover inside): 876, 1,396 (two), 1,096; four layers each.",
                        "No glue: the cover and the straps hold the layers together.",
                        "Not polystyrene (fuel dissolves it); not open-cell foam.",
                        "Check: stack fits the cover with no gap at the corners."],
                       DATE, inset_view=(24, -120))
    cov = bay("covers")
    bv.component_sheet(Part("Cover", cov, COL["cover"]), nb, "LevelHull", "LVH-DWG-105",
                       "Cover sleeve (8)", "PVC-coated polyester tarpaulin 650 g/m2",
                       ["Sleeve 200 x 200 inside, module length long, with 150 end flaps.",
                        "Cut 1,000 wide; sew a 130 overlap along the top inboard corner",
                        "  with UV-stabilised thread, two rows of stitching.",
                        "End flaps: eight 10 eyelets each, laced shut with 4 cord.",
                        "Slide the stacked core in, lace both ends tight.",
                        "Fits: sits on the batten, outboard face on the frame faces."],
                       DATE, inset_view=(24, -120))
    st = pick("straps", "port", "2", "2400")
    bv.component_sheet(Part("Hold-down strap", Compound([st, pick("rings", "port", "2", "2400")]), COL["strap"]),
                       nb, "LevelHull", "LVH-DWG-106", "Hold-down strap with D-rings (16)",
                       "50 mm polyester webbing, stainless double D-rings",
                       ["Cut 1,200 of 50 webbing; heat-seal both ends.",
                        "Sew a pair of D-rings into one end: 60 fold, box-and-cross stitch.",
                        "Passes round the module and under the batten, in a bay between",
                        "  frames, outboard of the module through the gap at the planks.",
                        "Close: tail up through both rings, back over one, pull tight.",
                        "Tuck the tail; it must not slip when pulled by hand."],
                       DATE, inset_view=(24, -120))


def joints():
    hull, frm = HULL_BAY
    # 1 gauge hooked over the gunwale at a frame
    w = window(1950, 2250, 300, 1000, 250, 750)
    g = M.gauge(P)
    bv.joint([Part("Plank and rubbing strake", Compound([H["shell"] & w, H["strakes"][0] & w]), COL["hull"]),
              Part("Frame", H["frames"][3] & w, COL["frame"]),
              Part("Setting gauge", g, COL["gauge"])],
             OUT / "joint-01.png", "Joint 1: the gauge on a frame",
             "Hook on the gunwale, lip outside the strake, long edge flat on the frame face", elev=20, azim=-150)
    # 2 batten on a frame, cut through the coach screw at frame 2,100
    w = window(2000, 2100, 300, 1000, 250, 700)
    bv.joint([Part("Plank", H["shell"] & w, COL["hull"]), Part("Frame (cut)", (H["frames"][3] - bay("screws")) & w, COL["frame"]),
              Part("Shelf batten (cut)", (bay("battens") - bay("screws")) & w, COL["batten"]),
              Part("Coach screw and washer (cut)", bay("screws") & w, COL["screw"]),
              Part("Module (cut)", Compound([bay("covers"), bay("cores")]) & w, COL["cover"])],
             OUT / "joint-02.png", "Joint 2: batten to frame, cut through the screw",
             "Screw square to the batten face, 50 into the frame, stops 10 short of the plank", elev=8, azim=-12)
    # 3 chock at the module end
    w = window(1250, 1650, 300, 1000, 250, 700)
    bv.joint([Part("Plank", H["shell"] & w, COL["hull"]), Part("Frame", H["frames"][2] & w, COL["frame"]),
              Part("Shelf batten", bay("battens") & w, COL["batten"]),
              Part("End chock", pick("chocks", "port", "2", "aft"), COL["chock"]),
              Part("Module", bay("covers") & w, COL["cover"])],
             OUT / "joint-03.png", "Joint 3: end chock",
             "Chock screwed down into the batten, tight against the module end", elev=26, azim=-120)
    # 4 strap round module and batten, cut through the strap at 2,400
    w = window(2300, 2400, 300, 1000, 250, 750)
    bv.joint([Part("Plank", H["shell"] & w, COL["hull"]),
              Part("Shelf batten (cut)", bay("battens") & w, COL["batten"]),
              Part("Foam core (cut)", bay("cores") & w, COL["core"]),
              Part("Cover (cut)", bay("covers") & w, COL["cover"]),
              Part("Strap (cut)", bay("straps") & w, COL["strap"]),
              Part("D-rings", pick("rings", "port", "2", "2400"), COL["ring"])],
             OUT / "joint-04.png", "Joint 4: strap round module and batten, cut",
             "In a bay between frames; the strap runs outboard of the module, in the gap at the planks", elev=8, azim=-12)
    # 5 D-ring buckle on top
    w = window(2300, 2500, 300, 1000, 500, 750)
    bv.joint([Part("Module", bay("covers") & w, COL["cover"]), Part("Strap", bay("straps") & w, COL["strap"]),
              Part("D-ring buckle", pick("rings", "port", "2", "2400"), COL["ring"])],
             OUT / "joint-05.png", "Joint 5: D-ring buckle on top of the module",
             "Tail up through both rings, back over the first, pulled tight", elev=40, azim=-120)
    # 6 eye bolt through strake and plank, cut at 2,400
    w = window(2330, 2400, 550, 1000, 400, 720)
    bv.joint([Part("Plank (cut)", H["shell"] & w, COL["hull"]), Part("Rubbing strake (cut)", H["strakes"][0] & w, COL["frame"]),
              Part("Eye bolt, washers, nut (cut)", pick("eyes", "port") & w, COL["eye"]),
              Part("Grab line", pick("grablines", "port") & window(2100, 2700, 700, 1100, 300, 720), COL["line"])],
             OUT / "joint-06.png", "Joint 6: grab-line eye bolt, cut",
             "Through the rubbing strake and top plank, bedded, nyloc nut inside", elev=8, azim=-12)


def steps():
    hull, frm = HULL_BAY
    ctx = [hull, frm]
    bat = Part("Shelf batten", bay("battens"), COL["batten"], None, (0, -350, 0))
    scr = Part("Coach screws and washers", bay("screws"), COL["screw"], None, mul(NIN, 300))
    chk = Part("End chocks", bay("chocks"), COL["chock"], None, (0, 0, 250))
    stp = Part("Hold-down straps (open)", bay("straps"), COL["strap"], None, (0, -350, 0))
    mod = Part("Module (core in cover)", Compound([bay("covers"), bay("cores")]), COL["cover"], None, (0, -150, 450))
    rng = Part("D-rings closed", bay("rings"), COL["ring"], None, (0, 0, 150))
    g = Part("Setting gauge", M.gauge(P), COL["gauge"], None, (0, 0, 300))
    seq = [
        ([], [g], "Step 1: mark the batten heights with the gauge",
         "Hook over the gunwale at every frame; mark both notches on the frame face"),
        ([], [bat], "Step 2: hold each batten to its marks",
         "Flat face on the frame faces, top edge on the upper mark; clamp"),
        ([bat], [scr], "Step 3: drill and drive the coach screws",
         "One into every frame the batten crosses; bed each in sealer"),
        ([bat, scr], [chk], "Step 4: screw the end chocks to the batten",
         "Set the gap between chocks to the module length plus 5 mm"),
        ([bat, scr, chk], [stp], "Step 5: lay the straps",
         "Under the batten and up outboard, in the bays between frames"),
        ([bat, scr, chk, stp], [mod], "Step 6: set the module on the batten",
         "Outboard face on the frame faces, between the chocks"),
        ([bat, scr, chk, stp, mod], [rng], "Step 7: close the straps",
         "Pull each strap tight through its D-rings; tuck the tail"),
    ]
    for i, (done, new, title, sub) in enumerate(seq, 1):
        bv.step(done, new, OUT / f"step-{i:02d}.png", title, sub, context=ctx, elev=24, azim=-120)
    # whole-canoe steps
    full = M.context_compound(P, motor=False)
    kit_in = Compound([s for key in ("battens", "screws", "chocks", "covers", "straps", "rings") for _, s in K[key]])
    base = [Part("Modules fitted (all eight)", kit_in, "#D1D5DB")]
    canoe = [Part("Canoe", full, COL["hull"])]
    eyes = Part("Grab-line eye bolts (4 a side)", Compound([s for _, s in K["eyes"]]), COL["eye"], None, (0, 0, 500))
    lines = Part("Grab lines", Compound([s for _, s in K["grablines"]]), COL["line"], None, (0, 0, 500))
    marks = Part("Freeboard marks", Compound([s for _, s in K["marks"]]), COL["mark"], None, (0, 0, 0))
    bails = Part("Bailers on lanyards", Compound([s for _, s in K["bailers"]]), COL["bailer"], None, (0, 0, 500))
    bv.step(base, [eyes], OUT / "step-08.png", "Step 8: fit the grab-line eye bolts",
            "Four a side through the rubbing strake and top plank, between frames", context=canoe,
            elev=24, azim=-58, size=(9, 6), label_done=False)
    bv.step(base + [eyes], [lines], OUT / "step-09.png", "Step 9: reeve the grab lines",
            "One line a side through the eyes, hanging in bights about 150 mm deep", context=canoe,
            elev=24, azim=-58, size=(9, 6), label_done=False)
    bv.step(base + [eyes, lines], [marks, bails], OUT / "step-10.png",
            "Step 10: paint the freeboard marks, stow the bailers",
            "Mark top edge 50 mm below the gunwale amidships, both sides", context=canoe,
            elev=24, azim=-58, size=(9, 6), label_done=False)


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    for w in what:
        globals()[w]()
        print("done", w)
