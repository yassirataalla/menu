import json, os, random
TL = json.load(open(TIMELINE)); NF = TL["frames"]
import json, os, random
def F(sec): return max(1, int(round(sec * FPS)) + 1)
random.seed(7)
_M = {}
def MT(name, color=None, rough=0.5, emit=None, es=0.0, alpha=None):
    if name not in _M:
        m = mat(name, color, rough, emit)
        b = m.node_tree.nodes["Principled BSDF"]
        if emit: b.inputs["Emission Strength"].default_value = es
        if alpha is not None: b.inputs["Alpha"].default_value = alpha
        _M[name] = m
    return _M[name]
def BS(m): return m.node_tree.nodes["Principled BSDF"]
def emis_key(m, frame, v):
    s = BS(m).inputs["Emission Strength"]; s.default_value = v; s.keyframe_insert("default_value", frame=frame)
def col_key(m, frame, c, inp="Base Color"):
    s = BS(m).inputs[inp]; s.default_value = (*c, 1); s.keyframe_insert("default_value", frame=frame)
FONT = bpy.data.fonts.load("/root/.fonts/Poppins-ExtraBold.ttf")
def txt(name, body, loc, size, m, parent=None, rot=(90, 0, 0), ext=0.004):
    bpy.ops.object.text_add(location=loc, rotation=[math.radians(a) for a in rot])
    o = bpy.context.object; o.name = name; o.data.body = body; o.data.font = FONT
    o.data.align_x, o.data.align_y = "CENTER", "CENTER"; o.data.size, o.data.extrude = size, ext
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def cable(name, pts, m, r=0.02, parent=None):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 3
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); scene.collection.objects.link(o); cu.materials.append(m)
    if parent: o.parent = parent
    return o
def heart(name, loc, size, m, parent=None):
    pts = []
    for i in range(48):
        t = 2 * math.pi * i / 48
        pts.append((16 * math.sin(t) ** 3 / 17, (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17))
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "2D"
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts): p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True; cu.fill_mode = "BOTH"; cu.extrude = 0.1; cu.bevel_depth = 0.025; cu.bevel_resolution = 3
    o = bpy.data.objects.new(name, cu); scene.collection.objects.link(o)
    o.location = loc; o.rotation_euler = (math.radians(90), 0, 0); o.scale = (size, size, size); cu.materials.append(m)
    if parent: o.parent = parent
    return o
SNAP = []; CUTF = set()
def vis(o, ranges):
    """ranges: list of (on_frame, off_frame or None); snaps scale 0/1"""
    SNAP.append(o)
    if not ranges or ranges[0][0] > 1: key(o, 1, scale=(0, 0, 0))
    for a, b in ranges:
        key(o, max(1, a), scale=(1, 1, 1))
        if b is not None: key(o, b, scale=(0, 0, 0))
def light(name, kind, loc, aim, energy, color, size=1.0):
    d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = color
    if kind == "AREA": d.size = size
    else: d.shadow_soft_size = size
    o = bpy.data.objects.new(name, d); scene.collection.objects.link(o); o.location = loc
    if aim is not None:
        o.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o
def lkey(l, frame, e):
    l.data.energy = e; l.data.keyframe_insert("energy", frame=frame)
