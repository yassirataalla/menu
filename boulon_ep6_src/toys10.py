import bpy, math, sys
from mathutils import Vector

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/frames/f_"
ENGINE = sys.argv[sys.argv.index("--") + 2] if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 2 else "CYCLES"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
import json as _j
TIMELINE = '/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep6/timeline.json'
FPS = 24
END = _j.load(open(TIMELINE))['frames']
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, END


# ---------- helpers ----------
def mat(name, color, rough=0.5, emit=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = 0.0
    return m


def give(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj


def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True


def bevel(obj, w=0.05, seg=4):
    mod = obj.modifiers.new("bev", "BEVEL")
    mod.width, mod.segments = w, seg


def cube(name, loc, scale, m, bev=0.05, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name, o.scale = name, scale
    bpy.ops.object.transform_apply(scale=True)
    if bev:
        bevel(o, bev)
    give(o, m)
    if parent:
        o.parent = parent
    return o


def sphere(name, loc, r, m, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    o = bpy.context.object
    o.name, o.scale = name, scale
    smooth(o)
    give(o, m)
    if parent:
        o.parent = parent
    return o


def cyl(name, loc, r, d, m, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=24)
    o = bpy.context.object
    o.name = name
    smooth(o)
    give(o, m)
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
    o.location = loc
    return o


def key(obj, frame, loc=None, rot=None, scale=None):
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert("location", frame=frame)
    if rot is not None:
        obj.rotation_euler = [math.radians(a) for a in rot]
        obj.keyframe_insert("rotation_euler", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert("scale", frame=frame)


def ease_all():
    for o in bpy.data.objects:
        ad = o.animation_data
        if ad and ad.action:
            for layer in getattr(ad.action, "layers", []):
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        for fc in cb.fcurves:
                            for kp in fc.keyframe_points:
                                kp.interpolation = "BEZIER"
                                kp.easing = "AUTO"


# ================= EPISODE 6 — « ভাষার আড়ালে » (Derrière la langue) =================
import json, os, random
TL = json.load(open(TIMELINE)); NF = TL["frames"]; LN = {l["key"]: l for l in TL["lines"]}
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

# ---------------- time marks (seconds) ----------------
T_INT1 = 17.0; T_L3 = 21.2; T_EXT2 = 24.7; T_HANDS = 29.6; T_FACE = 33.2; T_SIDE = 37.4; T_PILE = 41.0
T_C1 = 44.9; T_C2 = 48.3; T_C3 = 52.6; T_C4 = 56.3; T_C5 = 60.1; T_C6 = 63.2
T_V1 = 69.0; T_V2 = 72.8; T_V3 = 77.0; T_V4 = 80.9; T_V5 = 85.1; T_REUSE = 93.6
T_LAPSE = 124.0; T_DANCE = 136.0; T_O1 = 147.8; T_O2 = 152.8
INT_R = [(F(T_INT1), F(T_EXT2)), (F(T_HANDS), None)]
EXT_R = [(1, F(T_INT1)), (F(T_EXT2), F(T_HANDS))]

# ================= SETS =================
bpy.ops.mesh.primitive_plane_add(size=400); give(bpy.context.object, MT("ground", (0.025, 0.03, 0.045), 0.22))
EX = 40.0
# ---- exterior: Paris street at night
def tower(name, loc, h, m):
    x, y, z = loc
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = h * 0.0065; cu.bevel_resolution = 1
    def rad(u): return h * (0.2 * (1 - u) ** 2.6 + 0.012 * (1 - u) + 0.004)
    def poly(pts, cyc=False):
        sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
        for p, q in zip(sp.points, pts): p.co = (*q, 1)
        sp.use_cyclic_u = cyc
    def corner(u, k, ins=1.0):
        r = rad(u) * ins; a = math.pi / 4 + k * math.pi / 2
        return (r * math.cos(a) * 1.414, r * math.sin(a) * 1.414, u * h)
    US = [0, 0.06, 0.12, 0.19, 0.26, 0.33, 0.40, 0.48, 0.56, 0.64, 0.72, 0.80, 0.88, 0.95]
    for k in range(4):
        poly([corner(i / 40, k) for i in range(41)])
        for ins in (0.72,): poly([corner(i / 40, k, ins) for i in range(8)] + [corner(0.19, k)])
    for i, u in enumerate(US):
        poly([corner(u, k) for k in range(4)], True)
        if i + 1 < len(US):
            for k in range(4):
                poly([corner(u, k), corner(US[i + 1], (k + 1) % 4)]); poly([corner(u, (k + 1) % 4), corner(US[i + 1], k)])
    o = bpy.data.objects.new(name, cu); scene.collection.objects.link(o); o.location = (x, y, z); cu.materials.append(m)
    for u, t in ((0.19, 0.014), (0.40, 0.011), (0.88, 0.008)):
        cube(name + f"p{u}", (x, y, z + h * u), (rad(u) * 1.12, rad(u) * 1.12, h * t), m, 0)
    sphere(name + "top", (x, y, z + h * 1.0), h * 0.012, MT("beacon", (1, 1, 1), 0.3, (1, 0.95, 0.8), 30))
    return o
TOW = MT("tower", (0.9, 0.55, 0.15), 0.5, (1.0, 0.58, 0.16), 3.2)
tower("eiffel", (37.6, 16, 0), 12, TOW)
sphere("moonX", (41.2, 40, 15.5), 1.1, MT("moon", (1, 1, 1), 0.5, (0.95, 0.97, 1.0), 6))
STAR = MT("star", (1, 1, 1), 0.5, (1, 1, 1), 12)
for i in range(46):
    sphere(f"st{i}", (random.uniform(26, 54), 45, random.uniform(5, 30)), random.uniform(0.035, 0.075), STAR)
STONE = MT("stone", (0.07, 0.065, 0.075), 0.8)
cube("facade", (42.1, 2.3, 1.9), (3.0, 0.3, 1.9), STONE, 0)
cube("door", (40.55, 1.985, 1.05), (0.46, 0.02, 1.05), MT("doorG", (0.9, 0.55, 0.2), 0.4, (1.0, 0.6, 0.22), 2.2), 0)
cube("doorF", (40.55, 1.97, 1.05), (0.03, 0.03, 1.05), STONE, 0)
cube("winE", (42.3, 1.985, 1.5), (0.7, 0.02, 0.55), MT("doorG"), 0)
NEONG = MT("neonG", (0.1, 1.0, 0.45), 0.3, (0.1, 1.0, 0.45), 7)
txt("signE", "LIBAN SUR SEINE", (40.6, 1.95, 2.72), 0.25, NEONG, ext=0.03)
txt("signE2", "cuisine libanaise", (40.6, 1.95, 2.36), 0.13, MT("tW", (1, 1, 1), 0.4, (1, 1, 1), 2.5), ext=0.01)
cyl("lampPost", (38.9, 1.3, 1.7), 0.045, 3.4, MT("iron", (0.03, 0.03, 0.035), 0.4))
sphere("lampHead", (38.9, 1.3, 3.5), 0.16, MT("lampG", (1, 0.8, 0.5), 0.3, (1.0, 0.75, 0.4), 14))
light("lampL", "POINT", (38.9, 0.9, 3.3), None, 420, (1.0, 0.72, 0.42), 0.3)
light("doorL", "POINT", (40.5, 1.2, 1.4), None, 160, (1.0, 0.6, 0.25), 0.4)
light("moonL", "AREA", (35.5, -6, 8), (39.9, 0.4, 1.0), 2600, (0.5, 0.66, 1.0), 6)
light("extFill", "AREA", (43, -6, 3), (39.9, 0.4, 1.2), 380, (0.35, 0.45, 1.0), 5)
chev = empty("chevalet", (40.95, 0.05, 0)); chev.rotation_euler = (0, 0, math.radians(-22))
SLATE = MT("slate", (0.03, 0.035, 0.04), 0.6)
b1 = cube("chevF", (0, 0, 0), (0.3, 0.02, 0.44), SLATE, 0.01, chev); b1.location = (0, -0.1, 0.44); b1.rotation_euler = (math.radians(-12), 0, 0)
b2 = cube("chevB", (0, 0, 0), (0.3, 0.02, 0.44), SLATE, 0.01, chev); b2.location = (0, 0.1, 0.44); b2.rotation_euler = (math.radians(12), 0, 0)
TY = MT("tY", (1.0, 0.78, 0.05), 0.4, (1.0, 0.78, 0.05), 4)
txt("chevT1", "ON RECRUTE", (0, -0.155, 0.66), 0.082, TY, chev, rot=(78, 0, 0))
txt("chevT2", "PLONGEUR", (0, -0.135, 0.5), 0.1, MT("tW"), chev, rot=(78, 0, 0))
txt("chevT3", "(urgent !)", (0, -0.115, 0.36), 0.06, MT("tW"), chev, rot=(78, 0, 0))

# ---- interior: Lebanese kitchen
WX, WZ = -0.9, 2.05
cube("kfloor", (0, -2.2, 0.004), (5, 4.8, 0.004), MT("kfloor", (0.05, 0.042, 0.04), 0.25), 0)
WALL = MT("kwall", (0.012, 0.075, 0.062), 0.75); TILE = MT("tile", (0.5, 0.46, 0.38), 0.35)
cube("wL", ((-5 + WX - 0.6) / 2, 2.6, 4.0), ((WX - 0.6 + 5) / 2, 0.05, 4.0), WALL, 0)
cube("wR", ((5 + WX + 0.6) / 2, 2.6, 4.0), ((5 - WX - 0.6) / 2, 0.05, 4.0), WALL, 0)
cube("wB", (WX, 2.6, (WZ - 0.55) / 2), (0.6, 0.05, (WZ - 0.55) / 2), WALL, 0)
cube("wT", (WX, 2.6, (WZ + 0.55 + 8.0) / 2), (0.6, 0.05, (8.0 - WZ - 0.55) / 2), WALL, 0)
cube("tiles", (0, 2.54, 0.62), (5, 0.012, 0.62), TILE, 0)
for dx, dz, sx, sz in ((0, 0.55, 0.64, 0.035), (0, -0.55, 0.64, 0.035), (-0.6, 0, 0.035, 0.58), (0.6, 0, 0.035, 0.58), (0, 0, 0.018, 0.55), (0, 0, 0.6, 0.018)):
    cube("wf", (WX + dx, 2.53, WZ + dz), (sx, 0.04, sz), MT("white", (0.95, 0.95, 0.93), 0.5), 0)
SKY = MT("sky", (0.01, 0.02, 0.06), 0.9, (0.03, 0.06, 0.2), 1.0)
cube("skyP", (WX, 4.2, 2.0), (3.2, 0.02, 2.2), SKY, 0)
tower("eiffelW", (WX + 0.18, 3.5, 1.2), 1.25, TOW)
moonW = sphere("moonW", (WX - 0.32, 3.9, 2.38), 0.075, MT("moon"))
sunW = sphere("sunW", (0, 0, 0), 0.2, MT("sun", (1, 0.6, 0.2), 0.4, (1.0, 0.5, 0.12), 22))
STEEL = MT("steel", (0.36, 0.38, 0.4), 0.2)
cube("backC", (0.3, 2.2, 0.42), (2.8, 0.33, 0.42), STEEL, 0.02)
cube("island", (0, -0.45, 0.35), (1.9, 0.36, 0.35), MT("cab", (0.16, 0.17, 0.19), 0.4), 0.02)
cube("islTop", (0, -0.45, 0.705), (1.94, 0.4, 0.015), STEEL, 0.008)
cube("sink", (-0.05, -0.47, 0.718), (0.4, 0.25, 0.006), MT("water", (0.25, 0.5, 0.6), 0.08), 0.003)
FOAM = MT("foam", (1, 1, 1), 0.35)
for i in range(16):
    sphere(f"foam{i}", (-0.05 + random.uniform(-0.36, 0.36), -0.47 + random.uniform(-0.2, 0.2), 0.73), random.uniform(0.03, 0.065), FOAM)
cable("faucet", [(-0.52, -0.16, 0.72), (-0.52, -0.16, 1.08), (-0.45, -0.3, 1.14), (-0.38, -0.4, 1.02)], STEEL, 0.022)
cube("crate", (-0.05, 0.25, 0.07), (0.4, 0.3, 0.07), MT("box", (0.5, 0.36, 0.2), 0.8), 0.015)
# pot + steam on the back counter
cyl("pot", (0.45, 2.15, 0.99), 0.2, 0.28, MT("potM", (0.75, 0.3, 0.1), 0.25))
PUFF = MT("puff", (0.9, 0.9, 0.92), 0.9, alpha=0.5)
for i in range(3):
    p = sphere(f"potS{i}", (0, 0, 0), 0.09, PUFF)
    f = 1 + i * 16
    while f < NF:
        key(p, f, loc=(0.45, 2.15, 1.15), scale=(0.3,) * 3); key(p, f + 30, loc=(0.45 + 0.08 * math.sin(f), 2.15, 1.65), scale=(1.1,) * 3); key(p, f + 47, loc=(0.45, 2.15, 1.95), scale=(0, 0, 0)); f += 48
# clock
CK = (0.3, 2.5, 2.85)
cyl("clockF", CK, 0.28, 0.04, MT("white"), rot=(math.radians(90), 0, 0)); cyl("clockR", (CK[0], CK[1] + 0.012, CK[2]), 0.31, 0.04, MT("iron"), rot=(math.radians(90), 0, 0))
hH = empty("hourH", (CK[0], CK[1] - 0.03, CK[2])); hM = empty("minH", (CK[0], CK[1] - 0.04, CK[2]))
cube("hourM", (0, 0, 0.07), (0.016, 0.006, 0.08), MT("iron"), 0, hH); cube("minM", (0, 0, 0.105), (0.011, 0.006, 0.115), MT("neonR", (1, 0.06, 0.05), 0.3, (1, 0.06, 0.05), 2), 0, hM)
def clock_min(t):
    if t < T_LAPSE: return 23 * 60 + 10 + (t - T_INT1) * 1.3
    if t < T_DANCE: return 23 * 60 + 10 + (T_LAPSE - T_INT1) * 1.3 + (t - T_LAPSE) * 21
    return 23 * 60 + 10 + (T_LAPSE - T_INT1) * 1.3 + 12 * 21 + (t - T_DANCE) * 1.3
for t in [T_INT1 + i * 0.5 for i in range(int((NF / FPS - T_INT1) * 2))]:
    mn = clock_min(t); f = F(t)
    hM.rotation_euler = (0, math.radians(mn * 6), 0); hM.keyframe_insert("rotation_euler", frame=f)
    hH.rotation_euler = (0, math.radians(mn * 0.5), 0); hH.keyframe_insert("rotation_euler", frame=f)
txt("signI", "LIBAN SUR SEINE", (0.3, 2.5, 3.42), 0.25, NEONG, ext=0.025)
# pendant lamp
cyl("cord", (0, -0.5, 5.5), 0.012, 4.2, MT("iron"))
bpy.ops.mesh.primitive_cone_add(radius1=0.34, radius2=0.08, depth=0.26, location=(0, -0.5, 3.36)); give(bpy.context.object, MT("shade", (0.75, 0.2, 0.1), 0.4)); smooth(bpy.context.object)
sphere("bulbP", (0, -0.5, 3.26), 0.09, MT("lampG"))
# plates
def plate_mesh(name, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.02, vertices=28); o = bpy.context.object; smooth(o); give(o, m)
    me = o.data; me.name = name; bpy.data.objects.remove(o); return me
PD = plate_mesh("plateD", MT("plateD", (0.86, 0.8, 0.68), 0.3)); PC = plate_mesh("plateC", MT("plateC", (0.98, 0.98, 1.0), 0.12))
def plate(name, me, loc, parent=None, rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot]
    if parent: o.parent = parent
    return o
DIRTY = []   # (z order key, obj)
def pile(name, x, y, z0, n, lean=0.0):
    e = empty(name, (x, y, z0)); lst = []
    for i in range(n):
        p = plate(f"{name}_{i}", PD, (random.uniform(-0.02, 0.02) + lean * i, random.uniform(-0.02, 0.02), 0.012 + i * 0.03), e, (random.uniform(-3, 3), random.uniform(-3, 3), 0))
        lst.append(p); DIRTY.append((i + random.random(), p))
    return e, lst
pA, _ = pile("pileA", -1.22, -0.6, 0.72, 38, 0.0012)
pB, pBl = pile("pileB", -0.84, -0.5, 0.72, 50, -0.0009)
pC, _ = pile("pileC", -1.04, -0.2, 0.72, 30)
pile("pileD", 0.62, 2.15, 0.84, 30); pile("pileE", -1.7, 2.15, 0.84, 34); pile("pileF", -0.25, 2.2, 0.84, 22)
for e, ph in ((pA, 0.0), (pB, 1.3), (pC, 2.2)):
    f = F(T_INT1); a = ph
    while f < F(T_LAPSE): key(e, f, rot=(0, 1.1 * math.sin(a), 0)); f += 22; a += 1.0
    key(e, F(T_LAPSE), rot=(0, 0, 0))
# the plate that drops on the mountain (line 2)
drop = plate("dropP", PD, (0, 0, 0), pB, (0, 0, 0)); TOPB = 0.012 + 50 * 0.03
key(drop, 1, loc=(0, 0, 3.4), rot=(25, 0, 0)); key(drop, F(18.85), loc=(0.05, 0, 3.4), rot=(25, 0, 0)); key(drop, F(19.15), loc=(0, 0, TOPB), rot=(0, 0, 0))
DIRTY.append((51, drop))
for k, a in enumerate((0, 5, -4, 3, -1.5, 0)): key(pB, F(19.15) + k * 3, rot=(0, a, 0))
# clean stacks (grow during the time-lapse)
CLEAN = []
for i in range(44): CLEAN.append(plate(f"cl{i}", PC, (0.92, -0.52, 0.732 + i * 0.024)))
for i in range(30): CLEAN.append(plate(f"cm{i}", PC, (1.3, -0.48, 0.732 + i * 0.024)))
order = sorted(DIRTY, key=lambda d: -d[0])
for j, (_, p) in enumerate(order):
    vis(p, [(1, F(T_LAPSE + 0.6 + 10.6 * j / len(order)))])
for j, p in enumerate(CLEAN):
    if j < 5: continue
    idx = j - 5 if j < 44 else j - 5
    vis(p, [(F(T_LAPSE + 0.9 + 10.5 * (j - 5) / (len(CLEAN) - 5)), None)])

# interior lights
pend = light("pend", "AREA", (0, -1.2, 3.2), (0, 0, 1.0), 300, (1.0, 0.74, 0.48), 1.2)
keyI = light("keyI", "AREA", (1.8, -5.2, 3.4), (0, 0, 1.3), 330, (1.0, 0.9, 0.78), 3.0)
fillI = light("fillI", "AREA", (-3.6, -4, 2.8), (0, 0, 1.2), 170, (0.35, 0.5, 1.0), 4)
rimI = light("rimI", "AREA", (0.6, 2.2, 3.7), (0, 0.2, 1.4), 260, (0.25, 1.0, 0.6), 2.5)
dawnL = light("dawnL", "AREA", (WX, 2.35, WZ + 0.1), (0.2, -1.5, 1.2), 0, (1.0, 0.42, 0.1), 1.1)
dawnL.visible_camera = False
dreamL = light("dreamL", "POINT", (-0.05, -1.0, 2.4), None, 0, (1.0, 0.7, 0.4), 0.5)
rageL = light("rageL", "POINT", (0.85, -0.2, 2.2), None, 0, (1.0, 0.1, 0.05), 0.4)

# ================= ROBOTS =================
class Bot:
    def __init__(s, name, mats, label=None, antenna=True, sc=1.0):
        s.root = empty(name, (0, 0, 0)); s.rig = empty(name + "Rig"); s.rig.parent = s.root; s.rig.scale = (sc, sc, sc); r = s.rig; s.m = mats
        cube(name + "body", (0, 0, 0.95), (0.42, 0.32, 0.45), mats["body"], 0.08, r)
        s.head = empty(name + "head", (0, 0, 1.4)); s.head.parent = r
        cube(name + "headbox", (0, 0, 0.3), (0.34, 0.3, 0.26), mats["head"], 0.08, s.head)
        cube(name + "visor", (0, -0.29, 0.3), (0.27, 0.03, 0.14), MT("dark", (0.05, 0.05, 0.07), 0.4), 0.05, s.head)
        s.eyeL = sphere(name + "eyeL", (0, 0, 0), 0.065, mats["eye"], parent=s.head); s.eyeL.location = (-0.12, -0.31, 0.3)
        s.eyeR = sphere(name + "eyeR", (0, 0, 0), 0.065, mats["eye"], parent=s.head); s.eyeR.location = (0.12, -0.31, 0.3)
        s.browL = cube(name + "browL", (0, 0, 0), (0.062, 0.012, 0.011), mats["eye"], 0.004, s.head)
        s.browR = cube(name + "browR", (0, 0, 0), (0.062, 0.012, 0.011), mats["eye"], 0.004, s.head)
        if antenna:
            cyl(name + "ant", (0, 0, 0.7), 0.02, 0.3, mats["metal"], parent=s.head); sphere(name + "antball", (0, 0, 0.88), 0.07, mats["bulb"], parent=s.head)
        if label:
            t = txt(name + "lbl", label, (0, -0.33, 0.64), 0.13, MT("white"), r, ext=0.008)
        s.armL = empty(name + "armL", (-0.47, 0, 1.25)); s.armL.parent = r
        cyl(name + "armLm", (0, 0, -0.25), 0.07, 0.5, mats["metal"], parent=s.armL); sphere(name + "handL", (0, 0, -0.52), 0.1, mats["hand"], parent=s.armL)
        s.armR = empty(name + "armR", (0.47, 0, 1.25)); s.armR.parent = r
        cyl(name + "armRm", (0, 0, -0.25), 0.07, 0.5, mats["metal"], parent=s.armR); sphere(name + "handR", (0, 0, -0.52), 0.1, mats["hand"], parent=s.armR)
        for x in (-0.22, 0.22):
            cube(f"{name}leg{x}", (x, 0, 0.3), (0.12, 0.14, 0.2), mats["metal"], 0.04, r)
            cube(f"{name}foot{x}", (x, -0.05, 0.08), (0.16, 0.22, 0.08), MT("dark"), 0.04, r)
    def R(s, t, loc, rz=0, sc=(1, 1, 1), tilt=0): key(s.root, F(t) if not isinstance(t, int) else max(1, t), loc=loc, rot=(tilt, 0, rz), scale=sc)
    def H(s, t, rot): key(s.head, F(t), rot=rot)
    def A(s, t, L, Rr): key(s.armL, F(t), rot=(L[0], L[1], 0)); key(s.armR, F(t), rot=(Rr[0], Rr[1], 0))
    def AL(s, t, L): key(s.armL, F(t), rot=(L[0], L[1], 0))
    def AR(s, t, Rr): key(s.armR, F(t), rot=(Rr[0], Rr[1], 0))
    def EY(s, t, z):
        for e in (s.eyeL, s.eyeR): key(e, F(t), scale=(1, 1, z))
    def BR(s, t, l=0.0, r=0.0, tilt=0.0):
        key(s.browL, F(t), loc=(-0.12, -0.325, 0.395 + l), rot=(0, -tilt, 0)); key(s.browR, F(t), loc=(0.12, -0.325, 0.395 + r), rot=(0, tilt, 0))
    def face(s, t, ey=1.0, br=0.0, tilt=0.0): s.EY(t, ey); s.BR(t, br, br, tilt)
    def nod(s, t0, n, base=(0, 0, 0), per=0.42, amp=15):
        for i in range(n):
            s.H(t0 + i * per, (base[0] + 3, base[1], base[2])); s.H(t0 + i * per + per * 0.5, (base[0] - amp, base[1], base[2]))
        s.H(t0 + n * per, base)
    def blink(s, t, back=1.0): s.EY(t - 0.06, back); s.EY(t, 0.08); s.EY(t + 0.1, back)

BM = dict(body=MT("robot", (0.15, 0.45, 0.85), 0.3), head=MT("metal", (0.8, 0.8, 0.82), 0.25), metal=MT("metal"),
          eye=MT("eye", (0.1, 0.1, 0.1), 0.2, (0.3, 1.0, 0.9), 10), bulb=MT("bulb", (0.9, 0.2, 0.1), 0.3, (1.0, 0.25, 0.1), 10), hand=MT("robot"))
B = Bot("Boulon", BM, "BOULON")
cube("panel", (0, -0.33, 0.95), (0.22, 0.02, 0.16), MT("metal"), 0.03, B.rig)
for i, c in enumerate([(0.95, 0.3, 0.25), (0.3, 0.75, 0.35), (0.98, 0.78, 0.15)]): sphere(f"btn{i}", (-0.12 + 0.12 * i, -0.36, 0.98), 0.04, MT(f"b{i}", c, 0.5), parent=B.rig)
mouth = cube("mouth", (0, -0.315, 0.185), (0.1, 0.02, 0.03), BM["eye"], 0.01, B.head)
for i, a in enumerate(TL["amp"]):
    if i % 2 == 0: mouth.scale = (1 + 0.25 * a, 1, 0.12 + 1.25 * a); mouth.keyframe_insert("scale", frame=i + 1)
GLOVE = MT("glove", (1.0, 0.8, 0.1), 0.45)
for arm in (B.armL, B.armR):
    g = sphere("glove", (0, 0, 0), 0.118, GLOVE, parent=arm); g.location = (0, 0, -0.52); vis(g, INT_R)
    c = cyl("cuff", (0, 0, 0), 0.085, 0.1, GLOVE, parent=arm); c.location = (0, 0, -0.4); vis(c, INT_R)
sponge = cube("sponge", (0, 0, 0), (0.07, 0.045, 0.03), MT("sponge", (0.2, 0.85, 0.35), 0.8), 0.015, B.armR); sponge.location = (-0.03, -0.08, -0.6); vis(sponge, INT_R)
suit = empty("suitcase", (0.64, 0, 0.42)); suit.parent = B.rig; vis(suit, EXT_R)
cube("suitB", (0, 0, 0), (0.09, 0.2, 0.16), MT("suit", (0.5, 0.26, 0.12), 0.6), 0.02, suit); cube("suitS", (0, 0, 0), (0.095, 0.03, 0.165), MT("iron"), 0.005, suit)
bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.012, location=(0, 0, 0.19), rotation=(0, math.radians(90), 0)); o = bpy.context.object; give(o, MT("iron")); o.parent = suit
# plate in Boulon's hands
hp = plate("handPlate", PC, (0, 0, 0), B.rig)
WASH = ((0.0, -0.5, 1.0), (62, 0, 0)); SHOW = ((-0.5, -0.3, 1.78), (90, 0, 12)); INSP = ((-0.36, -0.52, 1.52), (90, 0, 28))
def HP(t, pose): key(hp, F(t), loc=pose[0], rot=pose[1])
star = empty("sparkle", (0, 0, 0)); star.parent = hp
STARM = MT("sparkM", (1, 1, 1), 0.3, (1, 1, 0.85), 40)
for a in (0, 90):
    c = cube(f"spk{a}", (0, 0, 0), (0.15, 0.012, 0.012), STARM, 0, star); c.rotation_euler = (0, 0, math.radians(a)); c.location = (0.08, 0.06, 0.03)
    c2 = cube(f"spkb{a}", (0, 0, 0), (0.07, 0.008, 0.008), STARM, 0, star); c2.rotation_euler = (0, 0, math.radians(a + 45)); c2.location = (0.08, 0.06, 0.03)
key(star, 1, scale=(0, 0, 0))
def sparkle(t, n=3):
    key(star, F(t) - 1, scale=(0, 0, 0))
    for i in range(n):
        key(star, F(t + i * 0.5) + 3, scale=(1.2, 1.2, 1.2)); key(star, F(t + i * 0.5) + 9, scale=(0.35, 0.35, 0.35))
    key(star, F(t + n * 0.5) + 2, scale=(0, 0, 0))

# chef
CHEAD = MT("chefHead", (0.72, 0.72, 0.74), 0.25)
CM = dict(body=MT("chefW", (0.95, 0.95, 0.93), 0.5), head=CHEAD, metal=MT("metalC", (0.55, 0.55, 0.58), 0.3),
          eye=MT("eyeC", (0.1, 0.1, 0.1), 0.2, (1.0, 0.55, 0.1), 10), bulb=MT("bulb"), hand=MT("chefW"))
C = Bot("Chef", CM, "CHEF", antenna=False, sc=1.22)
MTC = MT("white")
cyl("toque", (0, 0, 0.7), 0.26, 0.3, MTC, parent=C.head)
for i in range(6): sphere(f"tq{i}", (0.2 * math.cos(i * 1.047), 0.2 * math.sin(i * 1.047), 0.92), 0.17, MTC, parent=C.head)
sphere("tqTop", (0, 0, 1.0), 0.2, MTC, parent=C.head)
for sx in (-1, 1):
    mu = cube(f"mous{sx}", (0, 0, 0), (0.085, 0.02, 0.028), MT("dark"), 0.012, C.head); mu.location = (sx * 0.085, -0.31, 0.16); mu.rotation_euler = (0, math.radians(sx * 16), 0)
for i in range(4): sphere(f"cbtn{i}", (-0.1 + 0.2 * (i % 2), -0.33, 1.1 - 0.2 * (i // 2)), 0.03, MT("neonR"), parent=C.rig)
cyl("ladleH", (0, 0, -0.75), 0.018, 0.5, MT("steel"), parent=C.armR); sphere("ladleB", (0, 0, -1.02), 0.075, MT("steel"), parent=C.armR)
emis_key(MT("neonR"), 1, 0.4)

# ================= FX =================
TRACK = []   # (name, object, f0, f1) → screen positions exported for 2D overlays
def bubble(name, text, loc, w, h, t_on, t_off, ts=0.12, tail=-1, tm=None, track=False):
    e = empty(name, loc)
    cube(name + "b", (0, 0, 0), (w, 0.02, h), MT("bubW", (1, 1, 1), 0.5, (1, 1, 1), 1.6), min(h * 0.6, 0.07), e)
    tl = cube(name + "t", (0, 0, 0), (0.045, 0.018, 0.045), MT("bubW"), 0.005, e); tl.location = (tail * w * 0.5, 0, -h); tl.rotation_euler = (0, math.radians(45), 0)
    if text: txt(name + "x", text, (0, -0.03, 0), ts, tm or MT("tD", (0.03, 0.03, 0.05), 0.5), e)
    a, b = F(t_on), F(t_off)
    key(e, 1, scale=(0, 0, 0)); key(e, a - 1, scale=(0, 0, 0)); key(e, a + 3, scale=(1.18,) * 3); key(e, a + 6, scale=(1, 1, 1)); key(e, b - 3, scale=(1, 1, 1)); key(e, b, scale=(0, 0, 0))
    if track: TRACK.append((name, e, a, b))
    return e
NOTEM = [MT("nY", (1, 0.8, 0.1), 0.4, (1.0, 0.8, 0.1), 5), MT("nC", (0.2, 1, 0.9), 0.4, (0.3, 1.0, 0.9), 5), MT("nP", (1, 0.3, 0.6), 0.4, (1.0, 0.25, 0.55), 5)]
NN = [0]
def note(t, src, dx, rise=1.0, dur=1.7, size=1.0):
    i = NN[0]; NN[0] += 1; m = NOTEM[i % 3]
    e = empty(f"note{i}", src)
    sphere(f"noteH{i}", (0, 0, 0), 0.055, m, scale=(1.25, 0.6, 0.9), parent=e); cyl(f"noteS{i}", (0.06, 0, 0.11), 0.012, 0.22, m, parent=e)
    cube(f"noteF{i}", (0.1, 0, 0.2), (0.045, 0.01, 0.022), m, 0.004, e)
    a = F(t); b = F(t + dur)
    key(e, 1, scale=(0, 0, 0)); key(e, a - 1, loc=src, scale=(0, 0, 0), rot=(0, -15, 0))
    key(e, a + 5, scale=(size,) * 3); key(e, (a + b) // 2, loc=(src[0] + dx * 0.6, src[1], src[2] + rise * 0.55), rot=(0, 15, 0))
    key(e, b - 4, scale=(size * 0.9,) * 3); key(e, b, loc=(src[0] + dx, src[1], src[2] + rise), scale=(0, 0, 0), rot=(0, -10, 0))
def notes(t0, t1, origin, every=0.5, spread=0.55, rise=1.1, size=1.0):
    t = t0; k = 0
    while t < t1:
        sgn = 1 if k % 2 else -1
        note(t, (origin[0] + sgn * 0.22, origin[1], origin[2] + 0.05 * (k % 3)), sgn * spread * (0.6 + 0.4 * ((k * 7) % 5) / 4), rise, 1.7, size); t += every; k += 1
def puffs(name, loc, t, n=3, dur=1.5, r=0.14, m=None):
    for i in range(n):
        p = sphere(f"{name}{i}", (0, 0, 0), r, m or PUFF)
        a = F(t + i * 0.12); b = F(t + i * 0.12 + dur); ox = (i - (n - 1) / 2) * r * 0.9
        key(p, 1, scale=(0, 0, 0)); key(p, a - 1, loc=(loc[0] + ox, loc[1], loc[2]), scale=(0, 0, 0))
        key(p, a + 6, scale=(1, 1, 1)); key(p, b, loc=(loc[0] + ox * 1.8, loc[1], loc[2] + 0.7), scale=(0, 0, 0))
BP = (-0.05, 0.25, 0.14)          # Boulon in the kitchen (on his crate)
CP = (1.08, 0.95, 0.0); CRZ = -38  # chef
def bw(dx, dy, dz): return (BP[0] + dx, BP[1] + dy, BP[2] + dz)
QM = MT("qm", (1, 0.8, 0.1), 0.4, (1.0, 0.8, 0.1), 6)
def qmark(name, t_on, t_off, loc, size=0.34, body="?"):
    e = empty(name, loc); txt(name + "t", body, (0, 0, 0), size, QM, e, ext=0.03)
    a, b = F(t_on), F(t_off)
    key(e, 1, scale=(0, 0, 0)); key(e, a - 1, scale=(0, 0, 0), rot=(0, -20, 0)); key(e, a + 4, scale=(1.25,) * 3, rot=(0, 12, 0)); key(e, a + 8, scale=(1, 1, 1), rot=(0, 0, 0))
    key(e, b - 3, scale=(1, 1, 1), rot=(0, 8, 0)); key(e, b, scale=(0, 0, 0))
    return e
TEAR = MT("tear", (0.3, 0.7, 1.0), 0.1, (0.3, 0.7, 1.0), 2.5)
def tears(t0, t1):
    k = 0; t = t0
    while t < t1:
        sx = -1 if k % 2 else 1
        p = sphere(f"tear{t:.2f}", (0, 0, 0), 0.035, TEAR, scale=(1, 1, 1.5), parent=C.head)
        a = F(t); b = a + 13
        key(p, 1, scale=(0, 0, 0)); key(p, a - 1, loc=(sx * 0.14, -0.36, 0.24), scale=(0, 0, 0)); key(p, a + 2, scale=(1, 1, 1.5))
        key(p, b, loc=(sx * 0.2, -0.38, -0.55), scale=(1, 1, 1.5)); key(p, b + 1, scale=(0, 0, 0)); SNAP.append(p)
        t += 0.14; k += 1
def chef_red(t, v):   # v 0..1
    col_key(CHEAD, F(t), (0.72 + 0.23 * v, 0.72 - 0.62 * v, 0.74 - 0.66 * v)); lkey(rageL, F(t), 170 * v); emis_key(MT("neonR"), F(t), 0.4 + 6 * v)
def steam(t0, t1):
    t = t0; k = 0
    while t < t1:
        puffs(f"stm{t:.2f}", (CP[0] + (-0.3 if k % 2 else 0.3), CP[1], 2.75), t, 2, 0.9, 0.11); t += 0.45; k += 1

# ================= ACTING =================
# -- Boulon root / body
B.R(1, (35.6, 0.4, 0), 78); B.R(5.4, (35.6, 0.4, 0), 78)
n = 14
for i in range(n + 1):
    x = 35.6 + (39.9 - 35.6) * i / n; tt = 5.4 + 4.2 * i / n
    B.R(tt, (x, 0.4, 0.0), 78, (1.03, 1.03, 0.95));
    if i < n: B.R(tt + 0.15, (x + 0.15, 0.4, 0.09), 78, (0.97, 0.97, 1.05))
B.R(9.9, (39.9, 0.4, 0), 12); B.R(12.4, (39.9, 0.4, 0), 12); B.R(12.7, (39.9, 0.4, 0), -4); B.R(16.9, (39.9, 0.4, 0), -4)
def cutB(t, loc, rz=0):
    f = F(t); CUTF.add(f - 1); B.R(f - 1, tuple(B.root.location), math.degrees(B.root.rotation_euler[2])); B.R(f, loc, rz)
cutB(T_INT1, BP)
B.R(19.0, BP); B.R(19.25, bw(0, 0, 0.1), 0, (0.96, 0.96, 1.07)); B.R(19.5, BP, 0, (1.04, 1.04, 0.94)); B.R(19.75, BP); B.R(T_EXT2 - 0.1, BP)
cutB(T_EXT2, (39.95, 0.45, 0), 0)
B.R(25.1, (39.95, 0.45, 0), 0); B.R(25.6, (39.95, 0.45, 0), 42); B.R(26.75, (39.95, 0.45, 0), 42); B.R(26.95, (39.95, 0.45, 0.2), 30, (0.95, 0.95, 1.08)); B.R(27.2, (39.95, 0.45, 0), 20, (1.05, 1.05, 0.93)); B.R(27.4, (39.95, 0.45, 0), 14)
B.R(28.0, (39.95, 0.45, 0), 14); B.R(28.2, (39.95, 0.45, 0.14), 14, (0.96, 0.96, 1.06)); B.R(28.45, (39.95, 0.45, 0), 14); B.R(T_HANDS - 0.1, (39.95, 0.45, 0), 14)
cutB(T_HANDS, BP)
B.R(60.0, BP); B.R(60.6, BP, 16); B.R(67.0, BP, 16); B.R(67.6, BP, 0); B.R(77.2, BP, 0); B.R(77.6, BP, 14); B.R(80.6, BP, 14); B.R(80.95, BP, 0)
B.R(90.3, BP); B.R(90.5, bw(0, 0, 0.14), 0, (0.96, 0.96, 1.07)); B.R(90.75, BP, 0, (1.04, 1.04, 0.95)); B.R(90.95, BP); B.R(T_DANCE, BP)
t = T_DANCE; k = 0
while t < T_O1 - 0.6:
    B.R(t, BP, 16 * math.sin(k * 0.9), (1, 1, 1), 0); B.R(t + 0.53, bw(0, 0, 0.05), 16 * math.sin(k * 0.9 + 0.45), (0.98, 0.98, 1.03)); t += 1.06; k += 1
B.R(T_O1 - 0.2, BP, 0); B.R(153.3, BP, 0); B.R(154.6, BP, -128); B.R(NF, BP, -128)
# groove (rig sway) for both robots
for bot, ph, amp in ((B, 0.0, 2.6), (C, 1.4, 1.2)):
    t = 0.0
    while t < NF / FPS:
        key(bot.rig, F(t), rot=(0, amp * math.sin(2 * math.pi * t / 2.12 + ph), 0), loc=(0, 0, 0.012 * abs(math.sin(2 * math.pi * t / 1.06 + ph)))); t += 0.265

# -- Boulon head
HL = [
 (0.0, (0, 0, 0)), (9.6, (0, 0, 0)), (10.3, (14, 0, 14)), (11.6, (14, 0, 14)), (12.2, (8, 0, 4)), (12.7, (0, 0, 0)),
 (13.2, (4, 3, 6)), (14.0, (2, -3, -8)), (14.8, (6, 3, 4)), (15.6, (-4, 0, -22)), (16.2, (-4, 0, 20)), (16.9, (-10, 0, 0)),
 (17.0, (12, 0, -26)), (18.8, (14, 0, -28)), (19.2, (20, 0, -28)), (19.5, (4, 0, -20)), (20.3, (0, 6, 0)), (21.1, (-6, 6, 0)),
 (21.2, (0, 0, 0)), (21.7, (0, 0, 30)), (22.9, (0, 0, 30)), (23.3, (0, 14, 22)), (24.0, (0, -10, 6)), (24.6, (0, -10, 6)),
 (24.7, (0, 0, 0)), (25.3, (0, 0, 0)), (25.7, (-12, 0, 14)), (26.7, (-12, 0, 14)), (27.0, (8, 0, 0)), (27.5, (0, 0, -20)), (28.5, (4, 6, -22)), (29.5, (4, 6, -22)),
 (29.6, (-16, 0, 0)), (33.1, (-16, 0, 0)),
 (33.2, (2, 4, 0)), (34.2, (6, -5, -6)), (35.2, (6, 5, 6)), (36.2, (4, -5, -4)), (37.3, (6, 4, 4)),
 (37.4, (-14, 0, 0)), (39.3, (-14, 0, 0)), (39.9, (8, 0, -18)), (40.9, (8, 0, -18)),
 (41.0, (16, 0, -30)), (43.4, (18, 0, -30)), (44.0, (-14, 0, -10)), (44.8, (-14, 0, -10)),
 (44.9, (-12, 0, 0)), (48.2, (-12, 0, 0)),
 (52.6, (0, 0, 0)), (53.2, (4, 0, 26)), (54.0, (6, 0, -24)), (54.8, (10, 0, 10)), (55.6, (12, 0, -6)), (56.2, (0, 0, 0)),
 (56.3, (0, 0, 0)), (56.9, (10, -8, -16)), (58.6, (10, -8, -16)), (59.2, (4, 6, 0)), (60.0, (4, 6, 0)),
 (60.1, (0, 0, 0)), (60.6, (2, 0, 22)), (63.1, (2, 0, 22)),
 (67.2, (0, 0, 18)), (67.7, (0, 8, 0)), (68.9, (0, 8, 0)),
 (69.0, (0, 0, 0)), (69.4, (4, -6, -24)), (70.5, (4, -6, -24)), (70.8, (8, -10, -26)), (71.2, (-14, 0, 0)), (72.7, (-14, 0, 0)),
 (72.8, (-14, 0, 0)), (74.6, (-14, 0, 0)), (75.0, (4, 0, 24)), (76.9, (4, 0, 24)),
 (80.9, (0, 0, 0)), (81.6, (2, 4, 0)), (83.3, (2, -4, 0)), (83.8, (14, 0, 6)), (84.5, (14, 0, 6)), (85.0, (-14, 0, 0)),
 (85.1, (-14, 0, 0)), (85.8, (14, 0, 0)), (88.6, (12, 4, -6)), (89.2, (2, 0, 0)), (90.0, (4, 6, 12)), (91.0, (4, -6, -12)), (92.0, (6, 4, 8)), (93.0, (2, 0, 0)), (93.5, (-6, 0, 0)),
 (124.0, (-14, 0, 0)), (135.9, (-14, 0, 0)),
 (136.0, (8, 0, 0)), (138.0, (12, 6, 10)), (140.0, (10, -6, -10)), (142.0, (14, 6, 8)), (144.0, (10, -6, -8)), (146.0, (14, 4, 0)), (147.7, (6, 0, 0)),
 (147.8, (-14, 0, 0)), (150.2, (-14, 0, 0)), (150.8, (6, 0, 14)), (152.7, (6, 0, 14)),
 (152.8, (0, 0, 0)), (153.3, (4, 0, 0)), (154.6, (10, 0, -10)), (156.6, (10, 0, -10)), (157.4, (4, 6, 62)), (NF / FPS, (4, 6, 62)),
]
for t, r in HL: B.H(t, r)
B.nod(48.5, 9, (0, 0, 0), 0.44, 15); B.H(52.55, (0, 0, 0))
B.nod(63.3, 8, (2, 0, 22), 0.46, 14)
B.nod(77.9, 6, (2, 0, 24), 0.45, 15); B.H(77.3, (0, 0, 0)); B.H(77.7, (2, 0, 24)); B.H(80.85, (2, 0, 24))
# -- Boulon face
FA = [  # (t, eye z, brow raise, tilt)
 (0, 1, 0, 0), (10.3, 1.2, 0.03, 0), (12.6, 1, 0.01, 6), (15.5, 0.85, 0.01, 12), (16.9, 0.8, 0.01, 12),
 (17.0, 1.25, 0.04, 6), (19.2, 1.4, 0.05, 8), (20.3, 0.9, 0.0, 12), (21.1, 0.9, 0, 12),
 (21.2, 1, 0, 0), (21.8, 1.25, 0.04, 0), (23.3, 1.1, 0.03, 8), (24.6, 1.1, 0.03, 8),
 (24.7, 1, 0, 0), (25.8, 1.15, 0.03, 0), (26.9, 1.4, 0.05, 0), (27.5, 0.6, 0.04, 4), (29.5, 0.6, 0.04, 4),
 (29.6, 0.8, 0, 2), (33.1, 0.8, 0, 2), (33.2, 0.4, 0.03, 6), (37.3, 0.4, 0.03, 6),
 (37.4, 0.8, 0, 10), (40.9, 0.85, 0.01, 12), (41.0, 1.25, 0.04, 8), (43.4, 1.25, 0.04, 8), (44.0, 0.7, 0, 14), (48.2, 0.7, 0, 14),
 (48.3, 1.2, 0.045, 0), (52.5, 1.2, 0.045, 0), (52.6, 1.1, 0.03, 4), (56.2, 1.0, 0.02, 4),
 (56.3, 1, 0, 0), (56.9, 0.5, 0.04, 4), (59.2, 0.5, 0.04, 4), (60.0, 1, 0, 0),
 (60.6, 1.15, 0.04, 4), (67.2, 1.1, 0.04, 4), (67.8, 0.8, 0.03, 10), (68.9, 0.8, 0.03, 10),
 (69.0, 1, 0, 0), (69.5, 0.55, -0.01, -10), (70.5, 0.55, -0.01, -10), (70.8, 1.2, 0.04, 0), (71.3, 0.7, 0, -6), (76.9, 0.8, 0, 0),
 (77.0, 1.15, 0.04, 0), (80.8, 1.15, 0.04, 0),
 (80.9, 0.9, 0.02, 12), (83.3, 0.9, 0.03, 14), (83.8, 1.1, 0.04, 14), (85.0, 0.6, 0.01, 18),
 (85.1, 0.6, 0.01, 16), (85.9, 1.2, 0.04, 4), (88.8, 0.5, 0.04, 6), (92.6, 0.5, 0.04, 6), (93.2, 0.9, 0.02, 10), (93.5, 0.8, 0, 12),
 (124.0, 0.8, 0, 2), (135.9, 0.8, 0, 2), (136.0, 0.4, 0.035, 6), (147.7, 0.4, 0.035, 6),
 (147.8, 0.8, 0, 2), (150.3, 0.8, 0, 2), (150.8, 0.5, 0.04, 4), (152.7, 0.5, 0.04, 4),
 (152.8, 1, 0.01, 0), (154.6, 1.25, 0.04, 2), (157.0, 1.2, 0.04, 2), (157.5, 0.45, 0.04, 6), (NF / FPS, 0.45, 0.04, 6),
]
for t, ey, br, tl in FA: B.face(t, ey, br, tl)
for t in (3.0, 11.0, 14.3): B.blink(t)
# -- Boulon arms
DN = ((0, 4), (0, -4)); SHR = ((0, 45), (0, -45)); WL = (-62, -22)
def wash(t0, t1, per=1.3, big=7):
    t = t0; k = 0
    while t < t1:
        a = 2 * math.pi * (t - t0) / per
        B.A(t, WL, (-58 + big * math.sin(a), 22 + big * 1.3 * math.cos(a))); t += per / 6; k += 1
    HP(t0, WASH)
key(hp, 1, loc=WASH[0], rot=WASH[1]); vis(hp, INT_R)
AA = [
 (0, *DN), (5.3, *DN), (9.9, *DN), (10.4, (-20, 20), (0, -4)), (12.3, (-20, 20), (0, -4)), (12.7, *DN),
 (13.0, (-60, -40), (0, -4)), (14.6, (-60, -40), (0, -4)), (15.2, (0, 60), (0, -60)), (16.2, (0, 30), (0, -30)), (16.9, *DN),
]
for t, l, r in AA: B.A(t, l, r)
for i in range(n):   # arm swing while walking in
    tt = 5.4 + 4.2 * i / n; B.A(tt, (-28 if i % 2 else 24, 4), (0, -4))
B.A(T_INT1 - 0.04, *DN)
B.A(T_INT1, WL, (-58, 22)); B.A(18.9, WL, (-58, 22)); B.A(19.25, (-30, 70), (-30, -70)); B.A(19.9, (-20, 20), (-20, -20)); B.A(20.4, *SHR); B.A(21.15, *SHR)
B.A(21.2, WL, (-58, 22)); B.A(23.2, WL, (-58, 22)); B.A(23.5, (-20, 60), (-20, -60)); B.A(24.65, (-20, 60), (-20, -60))
B.A(T_EXT2, *DN); B.A(26.7, *DN); B.A(26.95, (0, 155), (0, -4)); B.A(27.3, (0, 130), (0, -4)); B.A(27.6, (0, 155), (0, -4)); B.A(27.9, (0, 130), (0, -4)); B.A(28.2, (0, 155), (0, -4)); B.A(29.55, (0, 150), (0, -4))
wash(T_HANDS, T_FACE, 1.75, 8); wash(T_FACE, T_C2, 1.6, 7)
B.A(48.3, WL, (-58, 22)); B.A(52.5, WL, (-58, 22))
wash(52.6, 56.4, 1.5, 7)
B.A(56.5, WL, (-58, 22)); B.A(56.95, (-158, -6), (0, -30)); B.A(57.6, (-152, -6), (-20, -50)); B.A(58.7, (-158, -6), (-20, -50)); B.A(59.5, WL, (-58, 22))
HP(56.5, WASH); HP(56.95, SHOW); HP(58.8, SHOW); HP(59.5, WASH); sparkle(57.2, 3)
wash(59.6, 67.2, 1.5, 7)
B.A(67.3, WL, (-58, 22)); B.A(67.8, (-40, 50), (-40, -50)); B.A(68.6, (-40, 50), (-40, -50)); B.A(68.95, WL, (-58, 22))
B.A(69.0, WL, (-58, 22)); B.A(69.45, (-122, -18), (-30, 0)); B.A(70.7, (-122, -18), (-30, 0)); B.A(71.2, WL, (-58, 22))
HP(69.0, WASH); HP(69.45, INSP); HP(70.75, INSP); HP(71.2, WASH)
wash(71.25, 77.2, 2.0, 8)
B.A(77.3, WL, (-58, 22)); B.A(80.8, WL, (-58, 22))
B.A(80.9, WL, (-58, 22)); B.A(81.5, WL, (-70, -25)); B.A(83.3, WL, (-78, -30)); B.A(84.2, WL, (-40, 5)); B.A(85.0, (-45, -10), (-40, 5))
HP(80.9, WASH); HP(85.05, WASH)
B.A(85.1, (-45, -10), (-40, 5)); B.A(85.9, (-30, 20), (-30, -20)); B.A(88.8, (-30, 20), (-30, -20))
for k, t in enumerate((89.2, 89.9, 90.6, 91.3, 92.0)):
    B.A(t, (-110, 35) if k % 2 == 0 else (-40, 60), (-40, -60) if k % 2 == 0 else (-110, -35))
B.A(92.8, (-30, 30), (-30, -30)); B.A(93.4, WL, (-58, 22))
key(hp, F(85.6) - 1, scale=(1, 1, 1)); key(hp, F(85.6), scale=(0, 0, 0)); key(hp, F(93.4), scale=(1, 1, 1))
wash(T_LAPSE, T_DANCE - 0.3, 0.34, 9)
key(hp, F(T_DANCE) - 1, scale=(1, 1, 1)); key(hp, F(T_DANCE), scale=(0, 0, 0)); key(hp, F(T_O1), scale=(1, 1, 1)); HP(T_O1, WASH)
t = T_DANCE; k = 0
while t < T_O1 - 0.5:
    B.A(t, (0, 50 + 22 * math.sin(k * 1.1)), (-118, 30)); t += 0.53; k += 1
B.A(T_O1 - 0.1, (0, 50), (-118, 30))
wash(T_O1, 150.2, 1.9, 7)
B.A(150.3, WL, (-58, 22)); B.A(150.8, (-158, -6), (-20, -40)); B.A(152.3, (-158, -6), (-20, -40)); B.A(152.75, (-60, -10), (-20, -20))
HP(150.3, WASH); HP(150.8, SHOW); HP(152.75, SHOW); sparkle(151.0, 2)
key(hp, F(T_O2) - 1, scale=(1, 1, 1)); key(hp, F(T_O2), scale=(0, 0, 0))
B.A(T_O2, *DN); B.A(154.8, *DN); B.A(156.2, (-20, 25), (-20, -25)); B.A(NF / FPS, (-10, 12), (-10, -12))
# antenna/eye glow
emis_key(BM["eye"], 1, 10); emis_key(BM["bulb"], 1, 10)

# -- Chef
def CR(t, dz=0, rz=CRZ, sc=(1, 1, 1), dx=0, tilt=0): C.R(t, (CP[0] + dx, CP[1], CP[2] + dz), rz, sc, tilt)
CR(0); C.H(0, (-8, 0, 0)); C.A(0, (-30, 10), (-45, -10)); C.face(0, 0.8, 0, -14)
def rage(t0, t1, lean=8):
    t = t0; k = 0
    while t < t1:
        CR(t, 0.0, CRZ - 4, (1.03, 1.03, 0.96), 0, -lean); CR(t + 0.14, 0.09, CRZ + 4, (0.97, 0.97, 1.05), 0, -lean)
        C.A(t, (-150 + 20 * (k % 2), 30), (-160 - 20 * (k % 2), -25)); C.A(t + 0.14, (-120, 45), (-130, -40)); C.H(t, (-6, 6 * (-1) ** k, -8)); t += 0.28; k += 1
    CR(t1, 0, CRZ)
def cry(t0, t1):
    CR(t0, 0, CRZ, (1, 1, 1), 0, -4); C.H(t0 + 0.15, (-18, 0, 0)); C.A(t0 + 0.2, (-150, -42), (-150, 42)); C.face(t0 + 0.15, 0.45, 0.03, 20)
    t = t0 + 0.3; k = 0
    while t < t1: C.H(t, (-18 + 4 * (k % 2), 0, 3 * (-1) ** k)); t += 0.2; k += 1
    tears(t0 + 0.3, t1)
def calm(t, ey=0.8): C.face(t, ey, 0, -14); C.A(t, (-30, 10), (-45, -10)); C.H(t, (-6, 0, -6)); CR(t)
# line 2: tosses one more plate
C.A(18.3, (-30, 10), (-45, -10)); C.A(18.6, (-170, 20), (-45, -10)); C.A(18.85, (-60, 10), (-45, -10)); C.A(19.6, (-30, 10), (-45, -10)); C.H(18.3, (-6, 0, -6)); C.H(18.7, (6, 0, -24)); C.H(20.5, (-6, 0, -6))
# line 3: shouts in two languages
C.face(21.3, 1.1, 0.02, -18); rage(21.4, 24.3, 6); chef_red(21.2, 0); chef_red(21.6, 0.45); chef_red(24.4, 0.45); chef_red(24.7, 0)
calm(29.6)
# chorus
chef_red(44.8, 0); cry(45.0, 46.55); chef_red(46.5, 0); chef_red(46.9, 1); C.face(46.7, 1.2, 0.02, -22); rage(46.7, 52.5, 10); steam(47.0, 52.4)
rage(52.6, 56.2, 6); chef_red(56.2, 1); chef_red(56.8, 0.35); calm(56.6, 1.0); C.H(57.2, (4, 0, -30)); C.face(57.2, 1.25, 0.04, 0); C.face(59.8, 1.25, 0.04, 0)
chef_red(60.0, 0.1); cry(60.15, 61.6); chef_red(61.5, 0.1); chef_red(61.9, 1); C.face(61.7, 1.2, 0.02, -22); rage(61.7, 63.15, 10); steam(61.9, 66.0)
t = 63.2; k = 0   # wags the ladle at Boulon
CR(63.2, 0, CRZ - 12, (1, 1, 1), 0, -8)
while t < 66.8:
    C.A(t, (-30, 20), (-95 + 22 * (k % 2), -10)); C.H(t, (-8, 0, -26)); t += 0.3; k += 1
chef_red(66.6, 1); chef_red(68.6, 0.15); calm(67.4); chef_red(72.6, 0.15)
# verse 2: points at the clock
C.H(72.8, (16, 0, -40)); C.A(72.8, (-168, 28), (-45, -10)); C.face(72.8, 1.15, 0.02, -20); CR(72.8, 0, CRZ - 6)
t = 72.9; k = 0
while t < 74.8:
    C.AL(t, (-168 + 10 * (k % 2), 28)); CR(t, 0.05 * (k % 2), CRZ - 6); t += 0.2; k += 1
chef_red(73.0, 0.5); chef_red(74.8, 0.9); rage(75.0, 76.9, 10); steam(74.9, 76.9); chef_red(77.0, 0.5)
C.face(77.0, 1.1, 0.03, -8); CR(77.1, 0, CRZ - 14, (1, 1, 1), 0, -9); C.H(77.1, (-10, 0, -28)); C.A(77.1, (-70, 40), (-70, -40)); C.A(79.0, (-80, 50), (-60, -30)); C.A(80.8, (-70, 40), (-70, -40)); chef_red(80.8, 0.3)
calm(81.2); chef_red(85.0, 0)
# time-lapse: the chef goes home
calm(124.0); CR(125.6, 0, CRZ); CR(126.0, 0, 80)
for i in range(9):
    CR(126.0 + i * 0.22, 0.0, 80, (1, 1, 1), 0.45 * i); CR(126.11 + i * 0.22, 0.08, 80, (1, 1, 1), 0.45 * i + 0.22)
CR(128.2, 0, 80, (1, 1, 1), 5.0); CR(NF / FPS, 0, 80, (1, 1, 1), 5.0)

# ================= FX timeline =================
# line 3: two languages, zero understood
bubble("bFr1", "VITE !", (0.42, 0.55, 2.62), 0.33, 0.14, 21.5, 24.5, 0.15, 1)
bubble("bAr1", "", (0.62, 0.5, 2.22), 0.3, 0.14, 22.3, 24.5, tail=1, track=True)
qmark("q1", 22.9, 24.6, bw(-0.42, -0.1, 2.5))
# line 6: the tune in his heart
notes(33.3, 37.2, bw(0, -0.45, 1.05), 0.42, 0.6, 1.2)
hrt = heart("heartB", (0, -0.4, 1.12), 0.0, MT("heart", (1.0, 0.02, 0.2), 0.3, (1.0, 0.03, 0.25), 6), B.rig)
key(hrt, 1, scale=(0, 0, 0))
def beat(t0, t1, s=0.12):
    key(hrt, F(t0) - 1, scale=(0, 0, 0)); t = t0
    while t < t1: key(hrt, F(t), scale=(s,) * 3); key(hrt, F(t) + 4, scale=(s * 1.35,) * 3); key(hrt, F(t) + 10, scale=(s,) * 3); t += 1.06
    key(hrt, F(t1), scale=(0, 0, 0))
beat(33.25, 37.35)
# chorus 1
bubble("bAr2", "", (0.45, 0.3, 2.75), 0.34, 0.15, 45.3, 46.6, tail=1, track=True)
bubble("bFr2", "PLUS VITE !", (0.4, 0.3, 2.78), 0.46, 0.15, 46.9, 48.25, 0.13, 1)
qmark("q2", 48.6, 52.5, bw(0.48, -0.1, 2.42), 0.3); qmark("q2b", 49.6, 52.5, bw(-0.5, -0.1, 2.3), 0.22)
SB = [("VITE !", (0.5, 0.2, 2.75), 0.3, 1, 52.8), ("", (-0.95, 0.0, 2.6), 0.3, -1, 53.1), ("ALLEZ !", (0.75, 0.1, 2.25), 0.33, 1, 53.4), ("BLA BLA", (-0.9, 0.0, 1.95), 0.34, -1, 53.7), ("...", (0.1, 0.4, 3.05), 0.2, 1, 54.0)]
for i, (tx, loc, w, tl, t) in enumerate(SB):
    bubble(f"bS{i}", tx, loc, w, 0.14, t, 54.5 + i * 0.12, 0.12, tl, track=(tx == ""))
    puffs(f"smk{i}", loc, 54.45 + i * 0.12, 3, 1.6, 0.15)
bubble("bAr3", "", (0.45, 0.3, 2.75), 0.34, 0.15, 60.3, 61.6, tail=1, track=True)
bubble("bFr3", "ALLEZ ! ALLEZ !", (0.25, 0.3, 2.72), 0.56, 0.15, 61.9, 63.15, 0.12, 1)
qmark("q3", 63.6, 66.9, bw(-0.42, -0.1, 2.45), 0.3)
# verse 2
qmark("ex1", 70.75, 71.3, bw(0.45, -0.1, 2.4), 0.3, "!")
bubble("bQ1", "?", (0.5, 0.3, 2.7), 0.14, 0.14, 77.3, 80.7, 0.17, 1); bubble("bQ2", "???", (0.72, 0.2, 2.3), 0.24, 0.14, 77.9, 80.7, 0.15, 1); bubble("bQ3", "C'EST PRÊT ?", (0.3, 0.2, 3.08), 0.48, 0.14, 78.6, 80.7, 0.12, 1)
# line "his own language melts into the air": 2D letters ride these empties
for i in range(5):
    e = empty(f"bn{i}", (0, 0, 0)); t0 = 81.3 + i * 0.55
    key(e, F(t0), loc=bw(0, -0.45, 1.6)); key(e, F(t0 + 2.2), loc=bw((-1) ** i * (0.25 + 0.08 * i), -0.45, 2.55)); TRACK.append((f"bn{i}", e, F(t0), F(t0 + 2.2)))
# dream: someone finally understands → stories
cl = empty("cloud", bw(0, 0.1, 2.75))
CLM = MT("cloudM", (1, 1, 1), 0.6, (1, 0.9, 0.8), 0.5)
for dx, dz, r in ((0, 0, 0.36), (-0.33, -0.03, 0.26), (0.33, -0.03, 0.26), (-0.17, 0.18, 0.24), (0.18, 0.2, 0.25), (0, -0.12, 0.3)):
    sphere("cloudS", (dx, 0.1, dz), r, CLM, scale=(1, 0.45, 1), parent=cl)
for k, (dx, dz, r) in enumerate(((-0.18, -0.5, 0.07), (-0.1, -0.68, 0.045))): sphere(f"cloudD{k}", (dx, 0, dz), r, CLM, parent=cl)
key(cl, 1, scale=(0, 0, 0)); key(cl, F(85.5) - 1, scale=(0, 0, 0)); key(cl, F(85.5) + 5, scale=(1.12,) * 3); key(cl, F(85.5) + 9, scale=(1, 1, 1)); key(cl, F(92.7), scale=(1, 1, 1)); key(cl, F(92.95), scale=(0, 0, 0))
def icon(name, t_on, t_off):
    e = empty(name, (0, -0.2, 0.02)); e.parent = cl; a, b = F(t_on), F(t_off)
    key(e, 1, scale=(0, 0, 0)); key(e, a - 1, scale=(0, 0, 0), rot=(0, 0, -25)); key(e, a + 4, scale=(1.2,) * 3, rot=(0, 0, 8)); key(e, a + 8, scale=(1, 1, 1), rot=(0, 0, 0)); key(e, b - 3, scale=(1, 1, 1), rot=(0, 0, 6)); key(e, b, scale=(0, 0, 0))
    return e
ic = icon("icHeart", 85.9, 88.9); heart("icH", (0, 0, -0.02), 0.2, MT("heart"), ic)
ic = icon("icHouse", 89.1, 90.25); cube("icHb", (0, 0, -0.08), (0.13, 0.1, 0.1), MT("b2"), 0.01, ic)
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.21, depth=0.15, location=(0, 0, 0.095), rotation=(0, 0, math.radians(45))); o = bpy.context.object; give(o, MT("b0")); o.parent = ic
cube("icHd", (0, -0.1, -0.12), (0.035, 0.01, 0.06), MT("suit"), 0, ic)
ic = icon("icBoat", 90.3, 91.45); cube("icBh", (0, 0, -0.1), (0.2, 0.07, 0.04), MT("suit"), 0.02, ic); cyl("icBm", (0, 0, 0.05), 0.01, 0.28, MT("iron"), parent=ic)
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.14, depth=0.02, location=(0.07, 0, 0.07), rotation=(math.radians(90), 0, 0)); o = bpy.context.object; give(o, MT("white")); o.parent = ic
cube("icBw", (0, 0, -0.16), (0.26, 0.05, 0.015), MT("water"), 0.01, ic)
ic = icon("icSun", 91.5, 92.75); sphere("icSs", (0, 0, 0), 0.11, MT("nY"), parent=ic)
for k in range(8):
    c = cube(f"icSr{k}", (0, 0, 0), (0.035, 0.01, 0.012), MT("nY"), 0, ic); a = k * math.pi / 4; c.location = (0.19 * math.cos(a), 0, 0.19 * math.sin(a)); c.rotation_euler = (0, -a, 0)
notes(89.2, 92.6, bw(0, -0.45, 1.3), 0.5, 0.7, 1.0, 0.8)
# instrumental + outro
notes(T_DANCE + 0.2, T_O1 - 1.2, bw(0, -0.45, 1.25), 0.53, 0.7, 1.3)
beat(T_DANCE, T_O1 - 0.3, 0.1)
notes(154.8, 158.6, bw(0, 0.5, 1.7), 0.6, 0.6, 1.0, 0.8)

# ---- light & sky timeline
def sky(t, col, es): col_key(SKY, F(t), col, "Emission Color"); emis_key(SKY, F(t), es)
NIGHT = (0.03, 0.06, 0.2)
sky(0, NIGHT, 1.0); sky(T_LAPSE, NIGHT, 1.0); sky(T_DANCE, (0.12, 0.08, 0.3), 1.6); sky(T_O1, (0.45, 0.16, 0.32), 2.6); sky(153.0, (0.95, 0.3, 0.2), 1.6); sky(157.0, (1.0, 0.42, 0.12), 1.9); sky(NF / FPS, (1.0, 0.5, 0.15), 2.1)
key(sunW, 1, loc=(WX - 0.28, 4.0, 0.9)); key(sunW, F(150.0), loc=(WX - 0.28, 4.0, 0.9)); key(sunW, F(158.5), loc=(WX - 0.28, 4.0, 2.0))
key(moonW, 1, scale=(1, 1, 1)); key(moonW, F(T_DANCE), scale=(1, 1, 1)); key(moonW, F(T_O1), scale=(0, 0, 0))
def L(t, pe=300, ke=330, fe=170, re=260, de=0, dr=0):
    for l, e in ((pend, pe), (keyI, ke), (fillI, fe), (rimI, re), (dawnL, de), (dreamL, dr)): lkey(l, F(t), e)
L(0); L(85.0); L(85.7, 110, 150, 120, 150, 0, 300); L(92.7, 110, 150, 120, 150, 0, 300); L(93.3)
L(T_LAPSE); L(T_DANCE, 240, 300, 190, 220); L(T_O1, 200, 260, 190, 150, 120); L(153.0, 150, 180, 170, 100, 900); L(157.5, 90, 120, 140, 80, 2600); L(NF / FPS, 90, 120, 140, 80, 2900)

def all_fcurves(idb):
    ad = idb.animation_data
    if ad and ad.action:
        for layer in ad.action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    for fc in cb.fcurves: yield fc
# hold the old pose until the frame before every cut (no 1-frame blends)
for o in list(bpy.data.objects):
    for fc in all_fcurves(o):
        fr = sorted((int(round(kp.co[0])), kp.co[1]) for kp in fc.keyframe_points); have = {a for a, _ in fr}
        for cf in CUTF:
            if cf + 1 in have and cf not in have:
                prev = [v for a, v in fr if a < cf]
                if prev: fc.keyframe_points.insert(cf, prev[-1])
ease_all()
for o in SNAP:
    for fc in all_fcurves(o):
        if fc.data_path == "scale":
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"
for o in (hH, hM):
    for fc in all_fcurves(o):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"

# ================= CAMERA =================
target = empty("target", (0, 0, 1.15))
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 32; cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 5.6
cam = bpy.data.objects.new("cam", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = target
WIDE = ((0.0, -5.3, 1.55), (0.0, 0.0, 1.5))
SHOTS = [  # (t0, cam0, tgt0, cam1, tgt1)
 (0.0, (39.6, -10.5, 1.5), (39.5, 0.5, 2.6), (39.65, -7.6, 1.45), (39.6, 0.5, 2.0)),
 (12.6, (39.25, -3.1, 1.3), (39.6, 0.4, 1.62), (39.3, -2.8, 1.3), (39.62, 0.4, 1.6)),
 (T_INT1, (0.0, -5.6, 1.5), (-0.1, 0.0, 1.55), (0.0, -5.2, 1.5), (-0.1, 0.0, 1.6)),
 (T_L3, (0.42, -4.3, 1.6), (0.48, 0.3, 1.72), (0.42, -4.05, 1.6), (0.48, 0.3, 1.72)),
 (T_EXT2, (40.35, -3.9, 1.25), (40.4, 0.3, 1.12), (40.35, -3.6, 1.25), (40.4, 0.3, 1.12)),
 (T_HANDS, (-0.05, -2.35, 1.8), (-0.05, -0.1, 1.3), (-0.05, -2.1, 1.78), (-0.05, -0.1, 1.3)),
 (T_FACE, (-0.05, -3.3, 1.6), (-0.05, 0.25, 1.75), (-0.05, -3.0, 1.6), (-0.05, 0.25, 1.75)),
 (T_SIDE, (1.75, -4.4, 1.9), (-0.45, 0.8, 1.62), (1.55, -4.0, 1.9), (-0.45, 0.8, 1.62)),
 (T_PILE, (-0.75, -3.4, 0.95), (-0.72, -0.4, 1.0), (-0.75, -3.4, 1.5), (-0.72, -0.4, 2.1)),
 (T_C1, (0.72, -2.7, 2.0), (0.9, 0.9, 2.2), (0.74, -2.45, 2.0), (0.9, 0.9, 2.2)),
 (T_C2, (-0.05, -3.4, 1.65), (-0.05, 0.25, 1.75), (-0.05, -3.1, 1.65), (-0.05, 0.25, 1.75)),
 (T_C3, (0.05, -5.3, 1.6), (0.0, 0.0, 1.7), (0.05, -5.0, 1.6), (0.0, 0.0, 1.7)),
 (T_C4, (-0.3, -3.3, 1.5), (-0.22, 0.0, 1.72), (-0.3, -3.05, 1.5), (-0.22, 0.0, 1.72)),
 (T_C5, (0.42, -4.3, 1.6), (0.48, 0.3, 1.75), (0.42, -4.05, 1.6), (0.48, 0.3, 1.75)),
 (T_C6, (0.3, -3.9, 1.6), (0.35, 0.3, 1.68), (0.25, -3.6, 1.6), (0.3, 0.3, 1.68)),
 (T_V1, (-0.2, -3.0, 1.6), (-0.18, 0.0, 1.62), (-0.2, -2.75, 1.6), (-0.18, 0.0, 1.62)),
 (T_V2, (0.7, -4.0, 1.9), (0.72, 1.4, 2.35), (0.7, -3.7, 1.9), (0.72, 1.4, 2.35)),
 (T_V3, (0.42, -4.3, 1.6), (0.48, 0.3, 1.9), (0.42, -4.05, 1.6), (0.48, 0.3, 1.9)),
 (T_V4, (-0.05, -2.9, 1.75), (-0.05, 0.25, 1.95), (-0.05, -2.65, 1.75), (-0.05, 0.25, 1.95)),
 (T_V5, (-0.05, -4.4, 1.9), (-0.05, 0.25, 2.2), (-0.05, -4.0, 1.9), (-0.05, 0.25, 2.2)),
 (T_REUSE, *WIDE, *WIDE),
 (T_LAPSE, (0.0, -5.5, 1.55), (-0.05, 0.0, 1.55), (0.0, -5.5, 1.55), (-0.05, 0.0, 1.55)),
 (T_DANCE, (-0.9, -3.9, 1.5), (-0.1, 0.25, 1.65), (0.7, -3.9, 1.5), (-0.05, 0.25, 1.65)),
 (T_O1, (0.3, -3.6, 1.6), (0.2, -0.1, 1.5), (0.3, -3.35, 1.6), (0.2, -0.1, 1.5)),
 (T_O2, (-0.25, -4.9, 1.8), (-0.5, 0.8, 1.8), (-0.3, -3.7, 1.8), (-0.5, 0.8, 1.8)),
]
for i, (t0, c0, g0, c1, g1) in enumerate(SHOTS):
    f0 = F(t0) if i else 1; f1 = (F(SHOTS[i + 1][0]) - 1) if i + 1 < len(SHOTS) else NF
    if i: CUTF.add(f0 - 1)
    for f, c, g in ((f0, c0, g0), (f1, c1, g1)):
        key(cam, f, loc=c); key(target, f, loc=g)
        cam_d.dof.focus_distance = (Vector(c) - Vector(g)).length; cam_d.dof.keyframe_insert("focus_distance", frame=f)
for idb in list(bpy.data.objects) + [cam_d]:
    for fc in all_fcurves(idb):
        for kp in fc.keyframe_points:
            if idb in (cam, target, cam_d): kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            if int(round(kp.co[0])) in CUTF: kp.interpolation = "CONSTANT"

world = bpy.data.worlds.new("w"); world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.035, 0.1, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4
scene.world = world
r = scene.render
r.resolution_x, r.resolution_y, r.resolution_percentage = 720, 1280, 100
r.filepath = OUT; r.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"; scene.view_settings.look = "AgX - Punchy"
if ENGINE == "CYCLES":
    r.engine = "CYCLES"; scene.cycles.device = "CPU"; scene.cycles.samples = 10; scene.cycles.use_denoising = True; scene.cycles.max_bounces = 3; scene.cycles.use_light_tree = False; scene.cycles.denoising_quality = "FAST"
    r.use_motion_blur = True; r.motion_blur_position = "START"
else:
    r.engine = "BLENDER_EEVEE"

if os.environ.get("EP6_TRACK"):
    from bpy_extras.object_utils import world_to_camera_view
    out = {}
    for name, o, a, b in TRACK:
        pts = []
        for f in range(a, b + 1):
            scene.frame_set(f); p = o.matrix_world.translation
            v = world_to_camera_view(scene, cam, p); v2 = world_to_camera_view(scene, cam, p + Vector((0, 0, 0.1)))
            pts.append([f, round(v.x * 720, 1), round((1 - v.y) * 1280, 1), round((v2.y - v.y) * 1280 * 10, 1), round(o.matrix_world.to_scale()[0], 3)])
        out[name] = pts
    json.dump(out, open(os.environ["EP6_TRACK"], "w"))
    print("TRACK", {k: len(v) for k, v in out.items()})

if os.environ.get("EP6_VIS"):
    from bpy_extras.object_utils import world_to_camera_view
    vis = []
    sgs = [(bpy.data.objects["signE"], 1.5, -0.5), (bpy.data.objects["signI"], 1.1, 0.0)]
    for f in range(1, scene.frame_end + 1):
        scene.frame_set(f); hit = False
        cx = cam.matrix_world.translation.x
        for o, hw, dz in sgs:
            if (o.matrix_world.translation.x > 20) != (cx > 20): continue
            c = o.matrix_world.translation
            for i in range(13):
                for z in (dz, 0.0, 0.25):
                    v = world_to_camera_view(scene, cam, c + Vector((hw * (i / 6 - 1), 0, z)))
                    if v.z > 0 and -0.06 < v.x < 1.06 and -0.06 < v.y < 1.06: hit = True
        if hit: vis.append(f)
    json.dump(vis, open(os.environ["EP6_VIS"], "w")); print("VIS", len(vis))
