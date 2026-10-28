"""LevelHull repo-specific parts and placement helpers (kit 1.9 detailed CAD).

Small hardware that .kit/cad_parts.py does not supply (wide washers, eye bolts, nyloc nuts, wood screws,
D-ring buckles, U-bolts) and helpers that put a fastener built along +Z onto any axis. Every function
returns a build123d solid or compound in millimetres. Kept in the repo's cad/src, never in .kit.
CONCEPT, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import (Axis, Compound, Cylinder, Location, Plane, Pos, Rot, Sketch, Circle, Torus, Vector,  # noqa: E402
                       chamfer, extrude)
import cad_parts as cp  # noqa: E402


def place(shape, origin, z_dir):
    """Move a part built along +Z (head on z = 0, shank down -Z) so its local +Z points along z_dir and its
    origin sits at 'origin'. The shank then runs from origin along -z_dir."""
    z = Vector(*z_dir).normalized()
    return Location(Plane(origin=tuple(origin), z_dir=(z.X, z.Y, z.Z))) * shape


def bore(origin, direction, d, length, back=0.0):
    """A cylinder of diameter d from 'back' mm behind origin to 'length' mm along direction (for holes)."""
    u = Vector(*direction).normalized()
    c = Pos(0, 0, -(length + back) / 2 + back) * Cylinder(d / 2, length + back)
    # built along -Z from +back to -length, then turned so -Z points along u
    return place(c, origin, (-u.X, -u.Y, -u.Z))


def wide_washer(d_in, d_out, t):
    """Plain wide (penny) washer, from z 0 to t."""
    return extrude(Sketch() + Circle(d_out / 2) - Circle(d_in / 2), t)


def nyloc_nut(d):
    """ISO 7040 prevailing-torque nut: an ISO 4032 hex body with a nylon collar, from z 0 up."""
    s, m = cp.ISO[d][0], cp.ISO[d][2]
    body = cp.hex_nut(d)
    collar = Pos(0, 0, m + 0.3 * d / 2) * (Cylinder(s * 0.45, 0.3 * d) - Cylinder(d / 2, 0.3 * d))
    return body + collar


def eye_bolt(d, length, eye_id, eye_wire):
    """Forged eye bolt: shank along -Z from z 0 to -length, eye ring above in the XZ plane."""
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    try:
        shank = chamfer(shank.edges().sort_by(Axis.Z)[0], d * 0.1)
    except Exception:
        pass
    collar = Pos(0, 0, 2.5) * Cylinder(d * 0.9, 5)
    R = eye_id / 2 + eye_wire / 2
    ring = Pos(0, 0, 5 + R + eye_wire / 2 - 1) * Rot(90, 0, 0) * Torus(R, eye_wire / 2)
    return shank + collar + ring


def wood_screw(d, length):
    """Pan-head stainless wood screw: head z 0 to 0.7 d, shank to -length with a pointed tip."""
    head = Pos(0, 0, 0.35 * d) * Cylinder(d, 0.7 * d)
    try:
        head = chamfer(head.edges().sort_by(Axis.Z)[-1], 0.25 * d)
    except Exception:
        pass
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    try:
        shank = chamfer(shank.edges().sort_by(Axis.Z)[0], d * 0.45)
    except Exception:
        pass
    return head + shank


def d_ring_pair(width, wire_d=5.0, depth=34.0):
    """Two stainless D-rings for webbing of the given width, lying flat in the XY plane on z = 0 (wire centre
    at z = wire_d / 2): straight bar along X, the curve towards +Y; the second ring 9 mm further along +Y."""
    out = []
    for k in range(2):
        y0 = k * 9.0
        w = width + 6
        pts = [(-w / 2, y0, wire_d / 2)]
        for i in range(11):
            a = math.pi * i / 10
            pts.append((-w / 2 * math.cos(a), y0 + depth * math.sin(a) * 0.8 + 4, wire_d / 2))
        pts.append((w / 2, y0, wire_d / 2))
        pts.append((-w / 2, y0, wire_d / 2))
        out.append(cp.rope(pts, wire_d))
    return Compound([s for r in out for s in r.solids()])


def u_bolt(pipe_od, d, leg, clearance=3.0):
    """U-bolt round a pipe whose axis is along X through the origin; legs up +Z to z = pipe_od / 2 + leg."""
    R = pipe_od / 2 + clearance + d / 2
    pts = [(0, -R, R + leg)]
    for i in range(13):
        a = math.pi * i / 12
        pts.append((0, -R * math.cos(a), -R * math.sin(a)))
    pts.append((0, R, R + leg))
    return cp.rope(pts, d), R


def ring_bead(r_in, width, height):
    """A ring-shaped weld bead (butt-fusion bead) round a pipe along +Z, centred on z = 0."""
    return Pos(0, 0, -width / 2) * extrude(Sketch() + Circle(r_in + height) - Circle(r_in), width)
