"""Read the shipped STEP files and write assets/model.json for index.html.

Everything in model.json is measured from the STEP geometry (bounding box, volume, plan outlines,
wall thickness). Nothing here is typed in by hand except the part labels.

Run with a Python that has build123d and shapely installed:  python tools/inspect_cad.py
"""
import json
import math
from pathlib import Path

from build123d import Axis, import_step
from OCP.BRepTools import BRepTools_WireExplorer
from shapely.geometry import LinearRing, Polygon

ROOT = Path(__file__).resolve().parent.parent
PARTS = [
    ("cutter_1_benzene_ring", "Cutter 1", "Hexagonal ring cutter"),
    ("cutter_2_octagram_star", "Cutter 2", "Eight-point star cutter"),
    ("cutter_3_erlenmeyer_flask", "Cutter 3", "Erlenmeyer flask cutter"),
]


def wire_points(wire, arc_steps=48):
    """Ordered polyline for a wire. Straight edges keep their two end points."""
    from build123d import Edge
    exp = BRepTools_WireExplorer(wire.wrapped)
    pts = []
    while exp.More():
        edge = Edge(exp.Current())
        if edge.geom_type.name == "LINE":
            seg = [edge @ 0, edge @ 1]
        else:
            seg = [edge @ (i / arc_steps) for i in range(arc_steps + 1)]
        if pts:
            last = pts[-1]
            if (seg[0] - last).length > (seg[-1] - last).length:
                seg.reverse()
        pts.extend(seg if not pts else seg[1:])
        exp.Next()
    return [[round(p.X, 4), round(p.Y, 4)] for p in pts]


def plan_faces(shape):
    out = []
    for face in shape.faces():
        n = face.normal_at()
        if abs(n.Z) < 0.999 or n.Z < 0:
            continue
        out.append(dict(z=round(face.center().Z, 4),
                        area=round(face.area, 4),
                        outer=wire_points(face.outer_wire()),
                        holes=[wire_points(w) for w in face.inner_wires()]))
    out.sort(key=lambda f: f["z"])
    return out


def wall_stats(top_face):
    outer = Polygon(top_face["outer"])
    inner = Polygon(top_face["holes"][0])
    ring_o, ring_i = LinearRing(top_face["outer"]), LinearRing(top_face["holes"][0])
    from shapely.geometry import Point
    ds = [ring_i.distance(Point(p)) for p in top_face["outer"]] + [ring_o.distance(Point(p)) for p in top_face["holes"][0]]
    mean = (outer.area - inner.area) / ((outer.exterior.length + inner.exterior.length) / 2)
    return dict(min=round(min(ds), 3), mean=round(mean, 3))


def describe(shape):
    bb = shape.bounding_box()
    return dict(
        bbox_min=[round(bb.min.X, 3), round(bb.min.Y, 3), round(bb.min.Z, 3)],
        bbox_max=[round(bb.max.X, 3), round(bb.max.Y, 3), round(bb.max.Z, 3)],
        size=[round(bb.size.X, 2), round(bb.size.Y, 2), round(bb.size.Z, 2)],
        volume_mm3=round(shape.volume, 1),
        valid=bool(shape.is_valid),
        solids=len(shape.solids()),
        faces=len(shape.faces()),
    )


def main():
    parts = []
    for stem, label, title in PARTS:
        shape = import_step(str(ROOT / f"{stem}.step"))
        plan = plan_faces(shape)
        blade_top = max(plan, key=lambda f: f["z"])
        parts.append(dict(id=stem, label=label, title=title, **describe(shape), plan=plan,
                          levels=sorted({f["z"] for f in plan}),
                          wall=wall_stats(blade_top) if blade_top["holes"] else None))
    assembly = import_step(str(ROOT / "bakebuild_3_cookie_cutters_set.step"))
    model = dict(parts=parts, set=dict(file="bakebuild_3_cookie_cutters_set.step", **describe(assembly)),
                 limit_mm=100)
    (ROOT / "assets" / "model.json").write_text(json.dumps(model))
    for p in parts:
        print(p["label"], p["size"], p["volume_mm3"], p["valid"], "levels", p["levels"], "wall", p["wall"])
    print("set", model["set"]["size"], model["set"]["solids"], "solids")


if __name__ == "__main__":
    main()
