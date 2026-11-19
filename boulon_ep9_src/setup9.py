# ================= EPISODE 8 — « 3 heures du matin » =================
import bmesh
def KT(t): return F(t) if not isinstance(t, int) else max(1, t)
def V(o, *rs): vis(o, [(F(a), (F(b) if b is not None else None)) for a, b in rs]); return o
def grp(name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    e = empty(name, loc); e.rotation_euler = [math.radians(a) for a in rot]
    if parent: e.parent = parent
    return e
def K(o, t, loc=None, rot=None, sc=None): key(o, KT(t), loc=loc, rot=rot, scale=sc)
LIN = []
WHITE = MT("white", (1, 1, 1), 0.5); DARK = MT("dark", (0.05, 0.05, 0.07), 0.4)
PUR = MT("pur", (0.3, 0.16, 0.6), 0.5, (0.4, 0.2, 0.85), 0.7)
PURT = MT("purT", (0.7, 0.5, 1.0), 0.5, (0.75, 0.55, 1.0), 5.0)
LIL = MT("lilac", (0.7, 0.55, 1.0), 0.5, (0.7, 0.55, 1.0), 0.8)
WHITEE = MT("whiteE", (1, 1, 1), 0.5, (1, 1, 1), 3.0)
SIL = MT("sil", (0.05, 0.02, 0.1), 0.8)
REDE = MT("redE", (1, 0.1, 0.05), 0.4, (1.0, 0.12, 0.06), 7.0)

# ---------------- Boulon ----------------
class Bot:
    def __init__(s, name, mats, label=None):
        s.root = empty(name, (0, 0, 0)); s.rig = empty(name + "Rig"); s.rig.parent = s.root; r = s.rig; s.m = mats
        cube(name + "body", (0, 0, 0.95), (0.42, 0.32, 0.45), mats["body"], 0.08, r)
        s.head = empty(name + "head", (0, 0, 1.4)); s.head.parent = r
        cube(name + "headbox", (0, 0, 0.3), (0.34, 0.3, 0.26), mats["head"], 0.08, s.head)
        cube(name + "visor", (0, -0.29, 0.3), (0.27, 0.03, 0.14), DARK, 0.05, s.head)
        s.eyeL = sphere(name + "eyeL", (0, 0, 0), 0.065, mats["eye"], parent=s.head); s.eyeL.location = (-0.12, -0.31, 0.3)
        s.eyeR = sphere(name + "eyeR", (0, 0, 0), 0.065, mats["eye"], parent=s.head); s.eyeR.location = (0.12, -0.31, 0.3)
        s.browL = cube(name + "browL", (0, 0, 0), (0.062, 0.012, 0.011), mats["eye"], 0.004, s.head)
        s.browR = cube(name + "browR", (0, 0, 0), (0.062, 0.012, 0.011), mats["eye"], 0.004, s.head)
        cyl(name + "ant", (0, 0, 0.7), 0.02, 0.3, mats["metal"], parent=s.head); sphere(name + "antball", (0, 0, 0.88), 0.07, mats["bulb"], parent=s.head)
        if label: txt(name + "lbl", label, (0, -0.33, 0.64), 0.13, WHITE, r, ext=0.008)
        s.armL = empty(name + "armL", (-0.47, 0, 1.25)); s.armL.parent = r
        cyl(name + "armLm", (0, 0, -0.25), 0.07, 0.5, mats["metal"], parent=s.armL); sphere(name + "handL", (0, 0, -0.52), 0.1, mats["hand"], parent=s.armL)
        s.armR = empty(name + "armR", (0.47, 0, 1.25)); s.armR.parent = r
        cyl(name + "armRm", (0, 0, -0.25), 0.07, 0.5, mats["metal"], parent=s.armR); sphere(name + "handR", (0, 0, -0.52), 0.1, mats["hand"], parent=s.armR)
        for x in (-0.22, 0.22):
            cube(f"{name}leg{x}", (x, 0, 0.3), (0.12, 0.14, 0.2), mats["metal"], 0.04, r)
            cube(f"{name}foot{x}", (x, -0.05, 0.08), (0.16, 0.22, 0.08), DARK, 0.04, r)
        s.mouth = cube(name + "mouth", (0, -0.315, 0.185), (0.1, 0.02, 0.03), mats["eye"], 0.01, s.head)
        s.ckg = grp(name + "ck", parent=s.head)
        for x in (-0.215, 0.215): sphere(name + "cheek", (x, -0.31, 0.2), 0.05, MT("cheek", (1, 0.4, 0.55), 0.4, (1.0, 0.35, 0.5), 4.0), (1, 0.3, 0.7), s.ckg)
        s.E(1, 1.0); s.BR(1); s.MO(1, 0.0)
    def R3(s, t, loc, rot, sc=(1, 1, 1)): key(s.root, KT(t), loc=loc, rot=rot, scale=sc)
    def H(s, t, rot): key(s.head, KT(t), rot=rot)
    def A(s, t, L, Rr): key(s.armL, KT(t), rot=(L[0], L[1], 0)); key(s.armR, KT(t), rot=(Rr[0], Rr[1], 0))
    def AL(s, t, L): key(s.armL, KT(t), rot=(L[0], L[1], 0))
    def AR(s, t, Rr): key(s.armR, KT(t), rot=(Rr[0], Rr[1], 0))
    def E(s, t, l, r=None, w=1.0, wr=None):
        r = l if r is None else r; wr = w if wr is None else wr
        key(s.eyeL, KT(t), scale=(w, 1, l * w)); key(s.eyeR, KT(t), scale=(wr, 1, r * wr))
    def BR(s, t, l=0.0, r=0.0, tilt=0.0):
        key(s.browL, KT(t), loc=(-0.12, -0.325, 0.395 + l), rot=(0, tilt, 0)); key(s.browR, KT(t), loc=(0.12, -0.325, 0.395 + r), rot=(0, -tilt, 0))
    def MO(s, t, op, wide=1.0): key(s.mouth, KT(t), scale=(wide * (1 + 0.25 * op), 1, 0.12 + 1.25 * op))
    def blink(s, t, back=1.0): s.E(t - 0.06, back); s.E(t, 0.08); s.E(t + 0.1, back)
    def sing(s, t0, t1, gain=1.0, wide=1.0):
        a, b = F(t0), F(t1); s.MO(a - 2, 0.0, wide)
        for f in range(a, b, 2): s.MO(f, min(1.0, TL["amp"][min(NF - 1, f - 1)] * gain), wide)
        s.MO(b + 1, 0.0, wide)
    def talk(s, t0, t1, per=0.16, op=0.6):
        t = t0; k = 0
        while t < t1: s.MO(t, op * (0.5 + 0.5 * ((k * 5) % 3) / 2) if k % 2 == 0 else 0.1); t += per; k += 1
        s.MO(t1, 0.0)
    def faceoff(s, t0, t1, back=1.0):
        s.E(t0, 0, 0, 0.001); s.MO(t0, 0, 0.001); key(s.browL, KT(t0), scale=(0, 0, 0)); key(s.browR, KT(t0), scale=(0, 0, 0))
        s.E(KT(t0) - 1, back); s.E(t1, back); s.E(KT(t1) - 1, 0, 0, 0.001); s.MO(KT(t1) - 1, 0, 0.001); s.MO(t1, 0)
        for b in (s.browL, s.browR):
            key(b, KT(t0) - 1, scale=(1, 1, 1)); key(b, KT(t1) - 1, scale=(0, 0, 0)); key(b, KT(t1), scale=(1, 1, 1))
        for f in (KT(t0) - 1, KT(t1) - 1): CUTF.add(f)
EYE = MT("eye", (0.1, 0.1, 0.1), 0.2, (0.3, 1.0, 0.9), 10)
BM = dict(body=MT("robot", (0.15, 0.45, 0.85), 0.3), head=MT("metal", (0.8, 0.8, 0.82), 0.25), metal=MT("metal"),
          eye=EYE, bulb=MT("bulb", (0.9, 0.2, 0.1), 0.3, (1.0, 0.25, 0.1), 4), hand=MT("robot"))
B = Bot("Boulon", BM, "BOULON")
cube("panel", (0, -0.33, 0.95), (0.22, 0.02, 0.16), MT("metal"), 0.03, B.rig)
for i, c in enumerate([(0.95, 0.3, 0.25), (0.3, 0.75, 0.35), (0.98, 0.78, 0.15)]): sphere(f"btn{i}", (-0.12 + 0.12 * i, -0.36, 0.98), 0.04, MT(f"b{i}", c, 0.5), parent=B.rig)
def vtext(name, body, size):
    g = grp(name + "g", parent=B.head); txt(name, body, (0, -0.335, 0.3), size, EYE, g, ext=0.002); return g
FACE = light("FACE", "POINT", (0, 0, 0), None, 6, (0.5, 0.85, 1.0), 0.15); FACE.parent = B.head; FACE.location = (0, -0.75, 0.3)
# past self, flattened inside the mirror
PM_ = dict(body=MT("robotP", (0.4, 0.3, 0.8), 0.4, (0.5, 0.35, 1.0), 0.5), head=MT("metalP", (0.7, 0.62, 0.9), 0.3, (0.6, 0.5, 1.0), 0.35), metal=MT("metalP"),
           eye=MT("eyeP", (0.1, 0.1, 0.1), 0.2, (1.0, 0.7, 1.0), 9), bulb=MT("bulbP", (0.9, 0.3, 0.9), 0.3, (1.0, 0.4, 1.0), 5), hand=MT("robotP"))
OLDPOS = (0, 0, -30)
_B = B
class Bot2(Bot): pass

# ---------------- room ----------------
WALL = MT("wall", (0.34, 0.37, 0.5), 0.9); FLOOR = MT("floor", (0.13, 0.09, 0.07), 0.6); CEIL = MT("ceil", (0.5, 0.52, 0.62), 0.9)
WOOD = MT("wood", (0.16, 0.1, 0.07), 0.5); SHEET = MT("sheet", (0.72, 0.76, 0.86), 0.8); DUV = MT("duvet", (0.2, 0.3, 0.52), 0.85)
cube("floor", (0, -1, -0.1), (3.6, 4.6, 0.1), FLOOR, 0)
cube("ceiling", (0, -1, 4.5), (3.6, 4.6, 0.1), CEIL, 0)
cube("wallB", (0, 3.2, 2.2), (3.6, 0.1, 2.3), WALL, 0); cube("wallF", (0, -5.5, 2.2), (3.6, 0.1, 2.3), WALL, 0)
cube("wallR", (3.5, -1, 2.2), (0.1, 4.6, 2.3), WALL, 0)
WY0, WY1, WZ0, WZ1 = 0.5, 2.4, 1.7, 3.6
cube("wallL1", (-3.5, (-5.5 + WY0) / 2, 2.2), (0.1, (WY0 + 5.5) / 2, 2.3), WALL, 0); cube("wallL2", (-3.5, (WY1 + 3.2) / 2, 2.2), (0.1, (3.2 - WY1) / 2, 2.3), WALL, 0)
cube("wallL3", (-3.5, (WY0 + WY1) / 2, WZ0 / 2), (0.1, (WY1 - WY0) / 2, WZ0 / 2), WALL, 0); cube("wallL4", (-3.5, (WY0 + WY1) / 2, (WZ1 + 4.5) / 2), (0.1, (WY1 - WY0) / 2, (4.5 - WZ1) / 2), WALL, 0)
FRAME = MT("frame", (0.75, 0.76, 0.8), 0.5)
for z in (WZ0, WZ1): cube("wfr", (-3.4, (WY0 + WY1) / 2, z), (0.06, (WY1 - WY0) / 2 + 0.06, 0.05), FRAME, 0.01)
for y in (WY0, WY1, (WY0 + WY1) / 2): cube("wfr", (-3.4, y, (WZ0 + WZ1) / 2), (0.05, 0.04, (WZ1 - WZ0) / 2), FRAME, 0.01)
for i in range(9):
    sl = cube("slat", (-3.44, (WY0 + WY1) / 2, WZ0 + 0.12 + i * 0.21), (0.06, (WY1 - WY0) / 2, 0.045), FRAME, 0); sl.rotation_euler = (0, math.radians(25), 0)
cube("curtain", (-3.33, WY1 - 0.1, 2.5), (0.03, 0.42, 1.3), MT("curtain", (0.2, 0.22, 0.4), 0.9), 0.02)
cube("curtRod", (-3.33, (WY0 + WY1) / 2, 3.85), (0.02, 1.3, 0.02), DARK, 0)
SKY = MT("sky", (0.02, 0.04, 0.12), 0.9, (0.1, 0.18, 0.5), 1.0); cube("skyP", (-6.5, 1.5, 3.0), (0.05, 6, 5), SKY, 0).visible_shadow = False
# bed
cube("bedframe", (0, 0.8, 0.32), (1.62, 2.18, 0.3), WOOD, 0.05); cube("mattress", (0, 0.8, 0.72), (1.52, 2.07, 0.2), SHEET, 0.1)
cube("headboard", (0, 2.98, 1.35), (1.62, 0.1, 1.05), WOOD, 0.06)
def grid(name, x0, x1, y0, y1, nx, ny, fn, m, thick=0.05):
    vs = []; fs = []
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx; y = y0 + (y1 - y0) * j / ny; vs.append((x, y, fn(x, y)))
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; fs.append((a, a + 1, a + nx + 2, a + nx + 1))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); smooth(o); give(o, m)
    so = o.modifiers.new("so", "SOLIDIFY"); so.thickness = thick
    su = o.modifiers.new("su", "SUBSURF"); su.levels = su.render_levels = 1
    return o
def ss(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
def duv1(x, y):
    w = 0.03 * math.sin(6 * x + 2.5 * y) + 0.025 * math.sin(9 * y - 3 * x) + 0.02 * math.sin(14 * x)
    mound = 0.6 * math.exp(-(x / 0.62) ** 4) * ss(-0.6, -0.1, y)
    drop = -0.75 * ss(1.5, 1.72, abs(x)) - 0.6 * ss(-1.2, -1.42, y)
    return 1.03 + mound + w + drop
DV1 = grid("duvetOn", -1.75, 1.75, -1.45, 1.42, 44, 36, duv1, DUV)
def duv2(x, y):
    w = 0.08 * math.sin(5 * x + 3 * y) + 0.07 * math.sin(8 * y - 4 * x) + 0.05 * math.sin(13 * x + 1) * math.sin(7 * y)
    heap = 0.3 * math.exp(-((x - 0.9) / 0.6) ** 2 - ((y + 0.6) / 0.5) ** 2)
    drop = -0.85 * ss(1.5, 1.78, x)
    return 1.08 + w + heap + drop
DV2 = grid("duvetOff", 0.15, 2.0, -1.2, 0.55, 28, 26, duv2, DUV)
gD1 = grp("gD1"); DV1.parent = gD1; gD2 = grp("gD2"); DV2.parent = gD2
V(gD1, (0, 0.01)); V(gD2, (0, None))
# nightstand, clock, glass
cube("nstand", (2.45, 2.55, 0.5), (0.5, 0.45, 0.5), WOOD, 0.04)
CLK = grp("clock", (2.3, 2.3, 1.2), (0, 0, -18))
cube("clkBody", (0, 0, 0), (0.42, 0.12, 0.2), DARK, 0.04, CLK)
CLOCKS = [("23:47", 0, 1.7), ("23:48", 1.7, 2.6), ("23:52", 2.6, 3.5), ("00:15", 3.5, 4.4), ("00:41", 4.4, 5.2), ("01:12", 5.2, None)]
for s_, a, b in CLOCKS:
    g = grp("clk" + s_, parent=CLK); txt("clkT" + s_, s_, (0, -0.125, 0), 0.2, REDE, g, ext=0.002); V(g, (a, b))
CLKL = light("CLOCKL", "POINT", (2.25, 2.0, 1.25), None, 2.5, (1.0, 0.2, 0.12), 0.08)
RING = grp("ring", parent=CLK)
for sx in (-1, 1): txt("ringT", "((" if sx < 0 else "))", (sx * 0.62, -0.1, 0.05), 0.3, REDE, RING, ext=0.002)
V(RING, (0, 0.01))
GLASSM = MT("glass", (0.7, 0.85, 1.0), 0.05, None, 0, 0.35)
gGl = grp("gGlass", (2.7, 2.35, 1.13)); cyl("glass", (0, 0, 0), 0.08, 0.26, GLASSM, parent=gGl)
# dresser + mirror on the right wall
cube("dresser", (3.05, -2.7, 0.75), (0.35, 0.8, 0.75), WOOD, 0.04)
DRW = []
for i in range(3):
    d = cube(f"drawer{i}", (2.66, -2.7, 0.3 + i * 0.45), (0.05, 0.72, 0.19), MT("wood2", (0.22, 0.14, 0.1), 0.5), 0.02)
    cube(f"knob{i}", (-0.07, 0, 0), (0.025, 0.12, 0.025), FRAME, 0.01, d); DRW.append(d)
    cube(f"dglow{i}", (0.32, 0, 0), (0.28, 0.68, 0.16), PUR, 0, d)
txt("npo", "NE PAS OUVRIR", (-0.055, 0, 0.0), 0.085, MT("npoM", (1, 0.3, 0.3), 0.5, (1, 0.25, 0.25), 2.5), DRW[0], rot=(90, 0, -90), ext=0.002)
DRL = light("DRL", "POINT", (2.2, -2.7, 0.9), None, 0, (0.6, 0.35, 1.0), 0.2)
MIRF = cube("mirFrame", (3.37, -0.2, 1.7), (0.04, 0.95, 1.6), WOOD, 0.03)
MIRM = MT("mirror", (0.05, 0.06, 0.12), 0.15, (0.3, 0.2, 0.6), 0.0); cube("mirGlass", (3.34, -0.2, 1.7), (0.02, 0.85, 1.5), MIRM, 0)
# ceiling fan + crack
fan = grp("fan", (0, 0.6, 4.3)); cyl("fanHub", (0, 0, 0), 0.14, 0.14, FRAME, parent=fan); cyl("fanRod", (0, 0, 0.1), 0.03, 0.2, FRAME, parent=fan)
for i in range(4):
    bl = cube(f"blade{i}", (0, 0, 0), (0.55, 0.11, 0.012), WOOD, 0.01, fan); bl.rotation_euler = (0, 0, math.radians(90 * i + 20)); bl.location = (0.62 * math.cos(math.radians(90 * i + 20)), 0.62 * math.sin(math.radians(90 * i + 20)), -0.03)
CRK = MT("crack", (0.12, 0.12, 0.16), 0.9)
cp = [(-1.5, 2.2), (-1.15, 1.95), (-1.25, 1.6), (-0.85, 1.45), (-0.9, 1.1), (-0.5, 0.95)]
for (a, b), (c, d) in zip(cp, cp[1:]):
    o = cube("crk", ((a + c) / 2, (b + d) / 2, 4.395), (math.hypot(c - a, d - b) / 2 + 0.01, 0.012, 0.004), CRK, 0); o.rotation_euler = (0, 0, math.atan2(d - b, c - a))
# mess
cube("sockF", (-2.2, -0.6, 0.04), (0.2, 0.08, 0.04), MT("sock", (0.85, 0.3, 0.3), 0.9), 0.03)
cube("book", (-2.3, 0.3, 0.05), (0.22, 0.3, 0.04), MT("book", (0.7, 0.55, 0.2), 0.7), 0.01)
cube("chairS", (-2.6, -2.4, 0.8), (0.4, 0.4, 0.05), WOOD, 0.02); cube("chairB", (-2.95, -2.4, 1.4), (0.05, 0.4, 0.6), WOOD, 0.02)
for x in (-2.9, -2.3):
    for y in (-2.7, -2.1): cube("chairL", (x, y, 0.4), (0.04, 0.04, 0.4), WOOD, 0)
cube("clothes", (-2.7, -2.4, 0.95), (0.42, 0.36, 0.12), MT("cloth", (0.5, 0.25, 0.3), 0.95), 0.08)
cube("rug", (0, -2.6, 0.01), (1.4, 0.9, 0.01), MT("rug", (0.25, 0.2, 0.35), 0.95), 0)
# ---------------- pillow ----------------
PILM = MT("pillow", (0.8, 0.84, 0.95), 0.85); PEYE = MT("pilEye", (0.2, 0.24, 0.38), 0.8)
P = empty("pillow")
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=48, ring_count=24)
po = bpy.context.object; po.name = "pillowMesh"
for v in po.data.vertices:
    x, y, z = v.co; sx = (1 if x >= 0 else -1) * abs(x) ** 0.5; sz = (1 if z >= 0 else -1) * abs(z) ** 0.5
    t = (1 if y >= 0 else -1) * abs(y) ** 0.8
    pin = 1 + 0.12 * (abs(sx) * abs(sz)) ** 2
    v.co = (sx * 0.85 * pin, t * 0.21, sz * 0.55 * pin)
smooth(po); give(po, PILM); po.parent = P
def arc(name, w, d, m, parent, r=0.017):
    return cable(name, [(-w, 0, 0), (0, 0, -d), (w, 0, 0)], m, r, parent)
peL = grp("peL", (-0.3, -0.2, 0.12), parent=P); peR = grp("peR", (0.3, -0.2, 0.12), parent=P); pmo = grp("pmo", (0, -0.21, -0.14), parent=P)
arc("peLc", 0.13, 0.045, PEYE, peL); arc("peRc", 0.13, 0.045, PEYE, peR); arc("pmoc", 0.09, 0.03, PEYE, pmo, 0.014)
def PE(t, tilt=0.0, curve=1.0, smile=0.15):
    key(peL, KT(t), rot=(0, tilt, 0), scale=(1, 1, curve)); key(peR, KT(t), rot=(0, -tilt, 0), scale=(1, 1, curve)); key(pmo, KT(t), scale=(1, 1, smile))
def PL(t, loc, rot, sc=(1, 1, 1)): key(P, KT(t), loc=loc, rot=rot, scale=sc)
FLATP = ((0, 2.3, 1.0), (-90, 0, 0)); PROP = ((0, 2.72, 1.58), (-14, 0, 0))
NEUT, JUDGE, BORED, KIND = (0, 1.0, 0.15), (14, 0.7, 0.05), (-6, 1.3, -0.5), (0, -1.6, 1.6)

# ---------------- lights ----------------
MOON = light("MOON", "SUN", (-9, 1.4, 6.0), (0, 1.25, 1.6), 3.2, (0.5, 0.65, 1.0), 0.02); MOON.data.angle = math.radians(1.2)
FILL = light("FILL", "AREA", (0, -1.5, 4.3), (0, -1.0, 0), 55, (0.3, 0.4, 0.9), 5.0)
FRONT = light("FRONT", "AREA", (0.5, -5.0, 2.6), (0, 0.8, 1.3), 40, (0.35, 0.45, 0.95), 3.0)
MEMO = light("MEMO", "AREA", (0, 0.4, 4.2), (0, 0.8, 0), 0, (0.62, 0.38, 1.0), 2.0)
WARM = light("WARM", "AREA", (2.6, -1.2, 2.6), (0, 1.0, 1.9), 0, (1.0, 0.75, 0.45), 1.5)
DAWN = light("DAWN", "SUN", (-9, 1.2, 4.6), (0, 0.9, 1.1), 0, (1.0, 0.62, 0.35), 0.02); DAWN.data.angle = math.radians(2.0)
PHL = light("PHL", "POINT", (0, 0, 0), None, 0, (0.85, 0.92, 1.0), 0.1)
def memo(t, e): lkey(MEMO, KT(t), e)
memo(1, 0)
# dust in the moonbeam
for i in range(34):
    y = random.uniform(0.3, 2.3); x = random.uniform(-2.8, 1.2); z = 2.65 - (x + 3.4) * 0.5 + random.uniform(-0.75, 0.75)
    d = sphere(f"dust{i}", (x, y, z), random.uniform(0.006, 0.012), MT("dustM", (1, 1, 1), 0.5, (0.7, 0.8, 1.0), 2.0))
    key(d, 1, loc=(x, y, z)); key(d, NF, loc=(x + random.uniform(-0.5, 0.5), y + random.uniform(-0.4, 0.4), z + random.uniform(-0.45, 0.45))); LIN.append(d)

# ---------------- phone ----------------
PH = empty("phone")
cube("phBody", (0, 0, 0), (0.13, 0.24, 0.012), DARK, 0.01, PH)
PHS = MT("phScreen", (0.05, 0.06, 0.1), 0.2, (0.75, 0.85, 1.0), 0.0); cube("phScr", (0, 0, 0.013), (0.118, 0.222, 0.002), PHS, 0, PH)
PHL.parent = PH; PHL.location = (0, 0, 0.22)
INK = MT("ink", (0.02, 0.02, 0.05), 0.6); BUBG = MT("bubG", (0.2, 0.8, 0.45), 0.5, (0.2, 0.85, 0.45), 1.4); BUBW = MT("bubW", (0.9, 0.9, 0.95), 0.5, (0.9, 0.9, 1.0), 1.2)
def phtext(parent, lines, y0, size=0.021, m=INK, x=0.0, dy=None):
    dy = dy or size * 1.35
    for i, l in enumerate(lines): txt("pht", l, (x, y0 - i * dy, 0.021), size, m, parent, rot=(0, 0, 0), ext=0.0005)
PH_REST = ((2.1, 2.05, 1.03), (180, 0, 25)); PH_INS = ((0.1, 1.75, 2.25), (180, 0, 0)); PH_HOLD = ((0.42, 1.5, 1.9), (205, 12, 0)); PH_BED = ((0.9, 0.9, 1.75), (180, 0, 50))
def PHK(t, pose, e=None, scr=None):
    key(PH, KT(t), loc=pose[0], rot=pose[1])
    if e is not None: lkey(PHL, KT(t), e)
    if scr is not None: emis_key(PHS, KT(t), scr)