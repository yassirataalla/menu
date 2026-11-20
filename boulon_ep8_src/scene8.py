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

# ---------------- timing ----------------
TO = 1139 / 24.0
T1b, T1c, T2, T3, T4, T5, T5i, T6 = 9.0, 12.9, 14.0, 17.0, 20.0, 25.85, 30.6, 31.95
T7a, T7b, T7c, T7d, T8, T9, T10, T11 = 37.9, 39.4, 40.85, 42.1, 43.8, 46.85, 49.65, 55.45
T12, T12b, T13, T14, T14b = 61.5, 64.4, 67.4, 73.3, 79.25
T15a, T15c, T15d, T15e, T15f = T7a + TO, T7c + TO, 90.2, T8 + TO, T11 + TO
T16a, T16b, T16c, T16d, T17, T18, T18b, T19 = 108.9, 114.8, 120.6, 126.5, 132.4, 145.0, 147.9, 151.0
T20, T20b, T20c, T20d, T20e, TEND = 156.5, 168.0, 169.2, 176.0, 177.6, NF / 24.0

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
VT_HA = vtext("vtHa", "HA HA", 0.1); VT_DEB = vtext("vtDeb", "DÉBILE", 0.082); VT_CAVA = vtext("vtCava", "ça va :)", 0.085)
FACE = light("FACE", "POINT", (0, 0, 0), None, 6, (0.5, 0.85, 1.0), 0.15); FACE.parent = B.head; FACE.location = (0, -0.75, 0.3)
# past self, flattened inside the mirror
PM_ = dict(body=MT("robotP", (0.4, 0.3, 0.8), 0.4, (0.5, 0.35, 1.0), 0.5), head=MT("metalP", (0.7, 0.62, 0.9), 0.3, (0.6, 0.5, 1.0), 0.35), metal=MT("metalP"),
           eye=MT("eyeP", (0.1, 0.1, 0.1), 0.2, (1.0, 0.7, 1.0), 9), bulb=MT("bulbP", (0.9, 0.3, 0.9), 0.3, (1.0, 0.4, 1.0), 5), hand=MT("robotP"))
OLDPOS = (0, 0, -30)
_B = B
class Bot2(Bot): pass
Past = Bot("Past", PM_, None)

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
V(gD1, (0, T8), (T15f, T15f + 0.01)); V(gD2, (T8, None))
# nightstand, clock, glass
cube("nstand", (2.45, 2.55, 0.5), (0.5, 0.45, 0.5), WOOD, 0.04)
CLK = grp("clock", (2.3, 2.3, 1.2), (0, 0, -18))
cube("clkBody", (0, 0, 0), (0.42, 0.12, 0.2), DARK, 0.04, CLK)
CLOCKS = [("02:59", 0, 13.5), ("03:00", 13.5, T15a), ("03:47", T15a, T16b), ("04:12", T16b, T16c), ("04:38", T16c, T16d), ("05:03", T16d, T19),
          ("05:41", T19, T20c), ("06:29", T20c, 176.4), ("06:30", 176.4, None)]
for s_, a, b in CLOCKS:
    g = grp("clk" + s_, parent=CLK); txt("clkT" + s_, s_, (0, -0.125, 0), 0.2, REDE, g, ext=0.002); V(g, (a, b))
CLKL = light("CLOCKL", "POINT", (2.25, 2.0, 1.25), None, 2.5, (1.0, 0.2, 0.12), 0.08)
RING = grp("ring", parent=CLK)
for sx in (-1, 1): txt("ringT", "((" if sx < 0 else "))", (sx * 0.62, -0.1, 0.05), 0.3, REDE, RING, ext=0.002)
V(RING, *[(176.4 + i * 0.3, 176.55 + i * 0.3) for i in range(12)])
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
phA = grp("phA", parent=PH); cube("phBubA", (0.012, 0.03, 0.016), (0.1, 0.075, 0.001), BUBG, 0.004, phA)
phtext(phA, ["haha ok", "toi aussi je", "t'aime bien enfin", "pas comme ça lol"], 0.075, 0.0185)
phtext(phA, ["Vu 02:14"], -0.068, 0.014, MT("phGrey", (0.5, 0.55, 0.65), 0.5, (0.5, 0.55, 0.7), 1.0), 0.055)
phtext(phA, ["Sam"], 0.185, 0.022, WHITE)
DRAFTS = [["Désolé pour", "hier soir, je", "voulais dire..."], ["Désolé pour", "hier soi"], ["Déso"], [""]]
phB = []
for i, d in enumerate(DRAFTS):
    g = grp(f"phB{i}", parent=PH); cube("phBubB", (0.0, -0.12, 0.016), (0.108, 0.055, 0.001), BUBW, 0.004, g); phtext(g, d, -0.085, 0.0185); phB.append(g)
    cube("phBubA2", (0.012, 0.09, 0.016), (0.1, 0.05, 0.001), BUBG, 0.004, g); phtext(g, ["pas comme ça lol"], 0.09, 0.0165); phtext(g, ["Vu 02:14"], 0.03, 0.014, MT("phGrey"), 0.055)
PH_REST = ((2.1, 2.05, 1.03), (180, 0, 25)); PH_INS = ((0.1, 1.75, 2.25), (180, 0, 0)); PH_HOLD = ((0.42, 1.5, 1.9), (205, 12, 0)); PH_BED = ((0.9, 0.9, 1.75), (180, 0, 50))
def PHK(t, pose, e=None, scr=None):
    key(PH, KT(t), loc=pose[0], rot=pose[1])
    if e is not None: lkey(PHL, KT(t), e)
    if scr is not None: emis_key(PHS, KT(t), scr)

# ---------------- mini silhouettes ----------------
def mini(name, m, parent, loc=(0, 0, 0), s=1.0):
    e = grp(name, loc, parent=parent); e.scale = (s, s, s)
    cube(name + "b", (0, 0.42, 0), (0.17, 0.2, 0.012), m, 0, e); cube(name + "h", (0, 0.8, 0), (0.15, 0.12, 0.012), m, 0, e)
    cube(name + "a", (0, 1.0, 0), (0.012, 0.09, 0.012), m, 0, e); cube(name + "ab", (0, 1.1, 0), (0.03, 0.03, 0.012), m, 0, e)
    for x in (-0.09, 0.09): cube(name + "l", (x, 0.11, 0), (0.05, 0.11, 0.012), m, 0, e)
    aL = grp(name + "aL", (-0.2, 0.58, 0), parent=e); cube(name + "aLm", (0, -0.15, 0), (0.035, 0.16, 0.012), m, 0, aL)
    aR = grp(name + "aR", (0.2, 0.58, 0), parent=e); cube(name + "aRm", (0, -0.15, 0), (0.035, 0.16, 0.012), m, 0, aR)
    return e, aL, aR
def rz(o, t, a): key(o, KT(t), rot=(0, 0, a))

# S03 dossier
GD = grp("gDossier", (0, 0.55, 2.35)); V(GD, (T3, T4))
cube("dosF", (0, 0, 0), (0.62, 0.42, 0.012), PUR, 0.02, GD); cube("dosTab", (-0.38, 0.45, 0), (0.2, 0.06, 0.012), PUR, 0.02, GD)
txt("dosT1", "DOSSIER", (0, 0.12, 0.02), 0.2, WHITEE, GD, rot=(0, 0, 0)); txt("dosT2", "COMPLET", (0, -0.1, 0.02), 0.2, WHITEE, GD, rot=(0, 0, 0))
txt("dosT3", "CONFIDENTIEL", (0.18, -0.3, 0.025), 0.085, REDE, GD, rot=(0, 0, 12))
PAPER = MT("paper", (0.9, 0.86, 1.0), 0.6, (0.85, 0.78, 1.0), 0.5)
for i in range(6):
    p = cube(f"dosP{i}", (0, 0, 0.03), (0.15, 0.2, 0.004), PAPER, 0, GD); a = math.radians(-50 + i * 20)
    key(p, F(T3) + 4, loc=(0, 0, 0.03), rot=(0, 0, 0)); key(p, F(T3) + 22 + i * 3, loc=(1.15 * math.sin(a), 0.75 + 0.25 * math.cos(a) * 1.2, 0.05 + i * 0.01), rot=(0, 0, -math.degrees(a) * 0.6))
# S04 ceiling loop
G4 = grp("gLoop", (0, 0.75, 4.37), (180, 0, 0)); V(G4, (T4, T5))
ring4 = grp("ring4", parent=G4); key(ring4, F(T4), rot=(0, 0, 0)); key(ring4, F(T5), rot=(0, 0, 300)); LIN.append(ring4)
MIN4 = []
for i in range(6):
    a = math.radians(60 * i); g = grp(f"scr{i}", (1.45 * math.cos(a), 1.45 * math.sin(a), 0), (0, 0, 60 * i - 90), ring4)
    cube(f"scrP{i}", (0, 0, 0), (0.48, 0.4, 0.006), LIL, 0.02, g); MIN4.append(mini(f"m4_{i}", SIL, g, (0, -0.33, 0.02), 0.6))
for i, (e, aL, aR) in enumerate(MIN4):
    t = T4
    while t < T5:
        if i % 3 == 0: rz(aR, t, 0); rz(aR, t + 0.3, 110); rz(aR, t + 0.6, 80); rz(aR, t + 0.9, 110)
        elif i % 3 == 1: key(e, KT(t), rot=(0, 0, 0)); key(e, KT(t + 0.35), rot=(0, 0, -75)); key(e, KT(t + 0.9), rot=(0, 0, -75))
        else: rz(aL, t, 0); rz(aR, t, 0); rz(aL, t + 0.25, -150); rz(aR, t + 0.25, 150); rz(aL, t + 0.7, -150); rz(aR, t + 0.7, 150)
        t += 1.2
txt("loopT", "EN BOUCLE", (0, 0, 0.02), 0.14, PURT, G4, rot=(0, 0, 0))
# S05 wall theatre
GW = grp("gWall", (0, 3.08, 3.36), (90, 0, 0)); V(GW, (T5, T5i))
cube("wDisc", (0, 0, 0), (1.75, 0.95, 0.006), LIL, 0.3, GW)
w1 = grp("w1", parent=GW); w2 = grp("w2", parent=GW); w3 = grp("w3", parent=GW)
TA, TB, TC = T5, 27.7, 29.4
V(w1, (TA, TB)); V(w2, (TB, TC)); V(w3, (TC, T5i))
e, aL, aR = mini("w1a", SIL, w1, (-0.45, -0.8, 0.02), 1.15); rz(aR, TA, 0); rz(aR, TA + 0.5, 95); rz(aR, TB, 95)
e2, _, _ = mini("w1b", SIL, w1, (1.4, -0.8, 0.02), 1.15); key(e2, F(TA) + 6, loc=(1.4, -0.8, 0.02)); key(e2, F(TB) - 2, loc=(-1.5, -0.8, 0.03))
mini("w2a", SIL, w2, (-1.0, -0.8, 0.02), 1.0)
for i in range(3): mini(f"w2{i}", SIL, w2, (-0.2 + i * 0.6, -0.8, 0.02), 1.0)
cube("w2table", (0.1, -0.5, 0.02), (1.4, 0.035, 0.012), SIL, 0, w2)
dots = txt("w2dots", ". . .", (-1.0, 0.6, 0.03), 0.3, SIL, w2, rot=(0, 0, 0))
key(dots, F(TB) + 8, loc=(-1.0, 0.6, 0.03)); key(dots, F(TB) + 22, loc=(-1.0, 0.6, 0.03)); key(dots, F(TB) + 30, loc=(-1.0, -0.42, 0.03), rot=(0, 0, -18))
_, a3L, a3R = mini("w3a", SIL, w3, (-1.0, -0.8, 0.02), 1.0); rz(a3L, TC, -130); rz(a3R, TC, 130)
for i in range(3): mini(f"w3{i}", SIL, w3, (0.6 + i * 0.42, -0.8, 0.02), 0.7)
bub = cube("w3bub", (0, 0, 0.03), (0.5, 0.32, 0.01), SIL, 0.12, w3); bt = txt("w3t", "BLA BLA", (0, 0, 0.02), 0.2, LIL, bub, rot=(0, 0, 0))
key(bub, F(TC), loc=(-0.55, 0.45, 0.03), scale=(0.3, 0.3, 1)); key(bub, F(T5i), loc=(0.15, 0.15, 0.03), scale=(2.6, 2.3, 1))
# S06 ceiling cinema
GC = grp("gCine", (0, -0.75, 4.37), (180, 0, 0)); V(GC, (T6, T7a))
cube("cineS", (0, 0, 0), (1.5, 0.95, 0.006), LIL, 0.03, GC)
txt("cineT1", "LA HONTE", (0, 0.2, 0.02), 0.42, SIL, GC, rot=(0, 0, 0)); txt("cineT2", "un film de Mon Cerveau", (0, -0.25, 0.02), 0.15, SIL, GC, rot=(0, 0, 0))
txt("cineT3", "(encore)", (0, -0.55, 0.02), 0.11, SIL, GC, rot=(0, 0, 0))
BEAM = MT("beam", (0.6, 0.4, 1.0), 0.5, (0.6, 0.4, 1.0), 0.5, 0.07)
a_ = Vector((0, 2.5, 1.3)); b_ = Vector((0, -0.75, 4.36)); L_ = (b_ - a_).length
bpy.ops.mesh.primitive_cone_add(radius1=0.04, radius2=1.25, depth=L_, vertices=32, location=(a_ + b_) / 2)
bm_ = bpy.context.object; bm_.rotation_euler = (b_ - a_).to_track_quat("Z", "Y").to_euler(); give(bm_, BEAM); bm_.visible_shadow = False
gBm = grp("gBeam"); bm_.parent = gBm; V(gBm, (T6, T7a))
gPop = grp("gPop", (0.75, 0.75, 1.75)); V(gPop, (T6, T7a)); cube("popB", (0, 0, 0), (0.14, 0.14, 0.2), MT("popR", (0.85, 0.15, 0.15), 0.6), 0.02, gPop)
for i in range(7): sphere(f"pop{i}", (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.22 + random.uniform(0, 0.05)), 0.05, MT("popW", (1.0, 0.95, 0.8), 0.8), parent=gPop)
# S07 bubble + ?
gBu = grp("gBu"); bu = sphere("bubble", (0, 0, 0), 0.12, MT("bubM", (0.95, 0.95, 1.0), 0.4, (0.8, 0.85, 1.0), 0.8), (1.3, 1, 0.9), gBu); V(gBu, (T7a + 0.25, T7b))
key(gBu, F(T7a + 0.25), loc=(0, 1.6, 1.75)); key(gBu, F(T7a + 1.0), loc=(0.25, 1.35, 2.15)); key(gBu, F(T7b), loc=(0.6, 1.0, 2.5))
gQ = grp("gQ", (0.75, 2.2, 1.75), (30, 0, 35)); txt("qmark", "?", (0, 0, 0), 0.5, PURT, gQ, rot=(0, 0, 0), ext=0.03); V(gQ, (T7b + 0.7, T7c))
# S10 words
WORDS = ["pourquoi ?", "pfff…", "j'aurais dû", "pourquoi ?", "mardi", "j'aurais dû", "putain", "2019", "pourquoi ?", "pfff…", "hier", "j'aurais dû"]
for i, w in enumerate(WORDS):
    g = grp(f"word{i}"); t0 = T10 + 0.15 + i * 0.4; x = -0.75 + random.uniform(-0.6, 0.6)
    txt(f"wordT{i}", w, (0, 0, 0), random.uniform(0.11, 0.16), PURT, g, ext=0.002); V(g, (t0, t0 + 1.9))
    key(g, F(t0), loc=(x, 2.35, 1.75 + random.uniform(-0.2, 0.2))); key(g, F(t0 + 1.9), loc=(x + random.uniform(-0.25, 0.25), 2.0, 3.0)); LIN.append(g)
# S12 timeline + old memory
g12 = grp("g12", (-0.95, 1.6, 4.37), (180, 0, 0)); V(g12, (62.9, T12b)); txt("t10", "− 10 ans", (0, 0, 0.02), 0.4, PURT, g12, rot=(0, 0, 200))
G12 = grp("gOld", (0, -0.6, 4.37), (180, 0, 0)); V(G12, (T12b, T13))
cube("oldS", (0, 0, 0), (1.5, 0.95, 0.006), LIL, 0.03, G12)
OLD = MT("oldB", (0.03, 0.12, 0.5), 0.6)
oe, oL, oR = mini("oldMe", OLD, G12, (-0.7, -0.8, 0.02), 1.2)
for i in range(4): mini(f"oldAud{i}", SIL, G12, (0.1 + i * 0.36, -0.8, 0.02), 0.75)
pap = cube("oldPaper", (0, 0, 0), (0.09, 0.12, 0.012), SIL, 0, G12)
for k in range(2):
    t = T12b + 0.2 + k * 1.35
    rz(oR, t, 0); rz(oR, t + 0.3, 100); key(pap, KT(t), loc=(-0.3, 0.05, 0.03), rot=(0, 0, 0)); key(pap, KT(t + 0.35), loc=(-0.3, 0.05, 0.03), rot=(0, 0, 0))
    key(pap, KT(t + 0.9), loc=(-0.25, -0.75, 0.03), rot=(0, 0, 120)); rz(oR, t + 0.9, 20); rz(oL, t + 0.35, 0); rz(oL, t + 0.9, -140); rz(oL, t + 1.3, 0)
txt("oldT", "2015", (1.05, 0.7, 0.02), 0.16, SIL, G12, rot=(0, 0, 0))
# S13 star, S14 spark
STAR = MT("star", (1, 0.9, 0.3), 0.4, (1.0, 0.85, 0.3), 8.0)
gSt = grp("gStar", (0.2, 1.75, 1.95)); txt("starT", "*", (0, 0, 0), 0.5, STAR, gSt, rot=(40, 0, 30), ext=0.02); V(gSt, (68.05, 68.4))
gSp = grp("gSpark", (1.9, -0.2, 2.5)); txt("sparkT", "*", (0, 0, 0), 0.45, MT("pinkE", (1, 0.4, 0.7), 0.4, (1.0, 0.35, 0.7), 10.0), gSp, rot=(90, 0, 90), ext=0.02); V(gSp, (84.3, 84.55))
# S15f scream
gAh = grp("gAh", (0, 1.0, 2.6)); txt("ahT", "AAAAH", (0, 0, 0), 0.34, PURT, gAh, ext=0.01); V(gAh, (106.75, 108.0))
key(gAh, F(106.75), loc=(0, 1.0, 2.95)); key(gAh, F(108.0), loc=(0.1, 1.0, 3.7))
# S16 sheep
SHW = MT("sheepW", (0.95, 0.95, 1.0), 0.9, (0.7, 0.8, 1.0), 0.6); SHEEP = []
for i in range(4):
    g = grp(f"sheep{i}"); sphere(f"shB{i}", (0, 0, 0), 0.2, SHW, (1.25, 0.9, 0.95), g); sphere(f"shH{i}", (0.24, 0, 0.1), 0.1, DARK, parent=g)
    for x in (-0.12, 0.12): cube(f"shL{i}{x}", (x, 0, -0.22), (0.025, 0.025, 0.08), DARK, 0, g)
    SHEEP.append(g)
gSP = grp("gShPaper"); cube("shPaper", (0, -0.05, 0), (0.14, 0.004, 0.19), PAPER, 0, gSP); txt("shPT", "2015", (0, -0.06, 0), 0.09, SIL, gSP, ext=0.001)
# S18 brain
BRN = MT("brain", (0.9, 0.5, 0.8), 0.5, (1.0, 0.45, 0.85), 2.5); GOLD = MT("gold", (1, 0.8, 0.2), 0.3, (1.0, 0.8, 0.2), 3.0)
def brain(name, m, mc, parent, flat=False):
    for x in (-0.12, 0.12): sphere(name + "lobe", (x, 0, 0), 0.2, m, (1, 1 if not flat else 0.05, 0.9), parent)
    cyl(name + "crown", (0, 0, 0.2), 0.16, 0.07, mc, parent=parent)
    for i in range(5):
        a = math.radians(72 * i + 90); bpy.ops.mesh.primitive_cone_add(radius1=0.045, depth=0.14, vertices=12, location=(0.15 * math.cos(a), 0.15 * math.sin(a) * (0 if flat else 1), 0.3))
        c = bpy.context.object; give(c, mc); c.parent = parent
    st = grp(name + "stick", (0.33, 0, -0.05), parent=parent); cyl(name + "stk", (0, 0, 0.12), 0.015, 0.4, mc, parent=st); sphere(name + "stb", (0, 0, 0.34), 0.045, mc, parent=st)
    return st
GB = grp("gBrain"); GBS = grp("gBrainS", parent=GB); GBS.scale = (1.7, 1.7, 1.7); BST = brain("br", BRN, GOLD, GBS); V(GB, (T18, T18b))
for x in (-0.09, 0.09): sphere("brEye", (x, -0.19, 0.02), 0.03, DARK, parent=GBS)
GS = grp("gBrainSh", (0.3, 3.07, 3.0)); GSS = grp("gBrainShS", parent=GS); GSS.scale = (5.5, 1, 5.5); SST = brain("brs", SIL, SIL, GSS, True); V(GS, (T18, T18b))
# S18 flying papers
FLY = []
for i in range(10):
    g = grp(f"fly{i}"); cube(f"flyP{i}", (0, 0, 0), (0.13, 0.004, 0.17), PAPER, 0, g); FLY.append(g)

# =====================================================================
#                              ACTING
# =====================================================================
LIE = ((0, 0.2, 1.2), (-90, 0, 0))
def lie(t, x=0.0, y=0.2, ry=0.0, z=1.2): B.R3(t, (x, y, z), (-90, ry, 0))
def sit(t, x, y, rzz, lean=0.0, dz=0.0): B.R3(t, (x, y, 0.5 + dz), (lean, 0, rzz))
Past.R3(1, OLDPOS, (0, 0, 0))
PHK(1, PH_REST, 0, 0)
K(gGl, 1, loc=(2.7, 2.35, 1.13))
# ---- S01 intro ----
lie(1); PL(1, *FLATP); PE(1, *NEUT)
B.A(1, (-28, 8), (-28, -8)); B.H(1, (0, 0, 0)); B.BR(1, 0, 0, 0)
B.E(1, 0, 0, 0.001); B.MO(1, 0, 0.001); lkey(FACE, 1, 0); lkey(FACE, F(6.9), 0)
B.AR(3.6, (-28, -8)); B.AR(3.9, (-40, -8)); B.AR(4.15, (-28, -8)); B.AR(4.4, (-40, -8)); B.AR(4.65, (-28, -8))
B.E(F(7.0) - 1, 0, 0, 0.001); B.E(7.0, 1.15, 1.15, 1.2); B.MO(F(7.0) - 1, 0, 0.001); B.MO(7.0, 0); lkey(FACE, F(7.0), 6); CUTF.add(F(7.0) - 1)
B.E(8.6, 1.15, 1.15, 1.2); B.E(9.0, 0.08); B.BR(9.0, -0.02, -0.02, 10); lkey(FACE, F(8.6), 6); lkey(FACE, F(9.0), 2.5)
B.E(10.9, 0.08); B.E(11.2, 0.08, 1.0); B.BR(11.2, -0.02, 0.03, 0); lkey(FACE, F(11.2), 4.5)
B.H(11.0, (0, 0, 0)); B.H(11.5, (0, 0, -14)); B.E(12.9, 0.08, 1.0); B.E(13.6, 1.1, 1.1, 1.1); B.H(13.9, (0, 0, -14))
# ---- S02 close eyes ----
B.H(T2, (0, 0, 0)); B.E(T2, 1.0); B.BR(T2, 0, 0, 0); lkey(FACE, F(T2), 6)
B.E(14.9, 1.0); B.E(15.2, 0.07); B.BR(15.2, -0.035, -0.035, 12); lkey(FACE, F(15.3), 2.2)
B.A(15.2, (-28, 8), (-28, -8)); B.A(15.6, (-45, 14), (-45, -14)); B.A(16.4, (-38, 12), (-38, -12))
K(B.rig, 15.4, sc=(1, 1, 1)); K(B.rig, 15.9, sc=(1.03, 1.06, 1)); K(B.rig, 16.6, sc=(1, 1, 1))
# ---- S03 dossier ----
memo(F(T3) - 1, 0); memo(T3, 90); B.E(T3, 0.07); PE(F(T3) - 1, *NEUT); PE(T3, *JUDGE)
B.E(17.6, 0.07, 0.07); B.E(18.0, 1.0, 0.07); B.BR(18.0, 0.035, -0.03, 0); B.MO(18.0, 0.05, 0.7); lkey(FACE, F(18.0), 5)
B.E(19.3, 1.1, 1.1); B.BR(19.3, 0.03, 0.03, -10)
# ---- S04 loop on the ceiling ----
memo(T4, 80); B.E(T4, 1.15, 1.15, 1.15); B.BR(T4, 0.03, 0.03, -12); B.A(T4, (-28, 8), (-28, -8))
for i in range(6): B.H(T4 + i * 0.9, (0, 0, -9 if i % 2 else 9))
B.A(21.6, (-28, 8), (-28, -8)); B.A(22.0, (-28, 8), (-120, -25)); B.A(22.3, (-28, 8), (-95, 20)); B.A(22.6, (-28, 8), (-120, -25)); B.A(23.2, (-28, 8), (-28, -8))
B.A(24.7, (-28, 8), (-28, -8)); B.A(25.15, (-120, 10), (-120, -10)); B.A(25.4, (-18, 10), (-18, -10)); B.E(25.4, 0.25); B.BR(25.4, -0.03, -0.03, 14)
PL(25.35, *FLATP); PL(25.5, (0, 2.3, 1.1), (-90, 0, 4)); PL(25.75, *FLATP)
K(B.root, 25.35, loc=(0, 0.2, 1.2)); K(B.root, 25.5, loc=(0, 0.2, 1.27)); K(B.root, 25.75, loc=(0, 0.2, 1.2))
# ---- S05 wall theatre ----
memo(T5, 60); sit(T5, 0, 0.75, 180, 0, 0.12); PL(T5, (-0.95, 2.72, 1.58), (-14, 0, 12)); PE(T5, *NEUT)
B.H(T5, (-12, 0, 0)); B.A(T5, (-20, 6), (-20, -6)); B.E(T5, 1.0); B.BR(T5, 0.02, 0.02, -8)
for i, t in enumerate((TA + 1.2, TB + 1.2, TC + 0.9)):
    sit(t, 0, 0.75, 180, 0, 0.12 - 0.07 * i); sit(t + 0.35, 0, 0.75, 180, 0, 0.05 - 0.07 * i); B.A(t + 0.35, (-60 - 30 * i, 10), (-60 - 30 * i, -10))
# insert: face with blush
sit(T5i, 0, 0.75, 180, 0, 0.0); B.A(T5i, (-150, 12), (-150, -12)); B.H(T5i, (8, 0, 0)); B.E(T5i, 0.55, 1.0, 0.8, 1.15); B.BR(T5i, 0.03, 0.0, -12); B.MO(T5i, 0.05, 0.6)
V(B.ckg, (T5i, T6), (T14b + 5.0, T15a), (T17 + 6.5, T17 + 8.5)); lkey(FACE, F(T5i), 7)
# ---- S06 ceiling cinema ----
memo(T6, 80); lie(T6); PL(T6, (0, 2.3, 1.0), (-90, 0, 0)); PE(T6, *BORED)
B.A(T6, (-170, 28), (-170, -28)); B.H(T6, (0, 0, 0)); B.E(T6, 0.45); B.BR(T6, 0, 0, 0); B.MO(T6, 0)
# ---- S07 pourquoi x3 ----
memo(T7a, 0); lkey(FACE, F(T7a), 8)
B.A(T7a, (-28, 8), (-28, -8)); B.E(T7a, 1.25, 1.25, 1.25); B.BR(T7a, 0.04, 0.04, -14); B.MO(T7a, 0.5, 0.5); B.MO(38.3, 0.35, 0.5)
B.AR(38.3, (-28, -8)); B.AR(38.75, (-125, 22)); B.AR(39.1, (-80, 5)); B.MO(39.3, 0.1, 0.7)
B.A(T7b, (-28, 8), (-28, -8)); B.faceoff(T7b + 0.0, T7b + 0.75, 1.0); V(VT_HA, (T7b, T7b + 0.75), (T15a + 1.5, T15a + 2.25))
B.E(T7b + 0.75, 1.2, 1.2, 1.2); B.BR(T7b + 0.75, 0.04, 0.04, -14); B.MO(T7b + 0.75, 0.02, 1.3)
# phone
PHK(F(T7c) - 1, PH_REST, 0, 0); PHK(T7c, PH_INS, 9, 0.8); V(phA, (T7c, T8)); B.AR(T7c, (-95, -10)); B.AL(T7c, (-28, 8))
PHK(T7d, PH_HOLD, 14, 0.8); B.E(T7d, 0.45, 0.45, 0.55); B.BR(T7d, 0.05, 0.05, -16); B.MO(T7d, 0.35, 0.35); B.MO(42.7, 0.05, 0.8); PE(T7d, *JUDGE)
lkey(FACE, F(T7d), 4)
PHK(43.1, PH_HOLD, 14, 0.8); PHK(43.5, PH_BED, 0, 0.0); B.AR(43.1, (-95, -10)); B.AR(43.5, (-25, -30)); B.E(43.5, 0.2);
# ---- S08 toss & turn (jump cuts) ----
POSES = [((-0.35, 0.2, 1.3), (-90, 90, 0), (-28, 8), (-60, -8)), ((0.2, 0.3, 1.28), (90, 0, 180), (160, 30), (150, -30)), ((1.0, 1.2, 1.2), (-90, 0, 90), (-150, 25), (-28, -30)),
         ((0, 2.15, 1.2), (-90, 0, 180), (-28, 40), (-28, -40)), ((0.55, 0.2, 1.2), (-90, 0, 0), (-28, 8), (-28, -8))]
for i, (loc, rot, aL_, aR_) in enumerate(POSES):
    f = F(T8) + i * 13
    if i: CUTF.add(f - 1)
    B.R3(f, loc, rot); B.A(f, aL_, aR_)
PL(T8, *FLATP); PE(T8, *NEUT); PHK(T8, PH_BED, 0, 0); lkey(FACE, F(T8), 6)
B.E(T8, 0.3); B.BR(T8, -0.03, -0.03, 14); B.MO(T8, 0.1, 0.8); B.H(T8, (0, 0, 0))
f = F(T8) + 4 * 13; B.AR(f + 3, (-28, -8)); B.AR(f + 7, (-110, -15)); B.AR(f + 10, (-95, -15)); B.AR(f + 13, (-115, -15)); B.AR(f + 16, (-95, -15))
# ---- S09 the pillow knows ----
PA = ((-0.7, 2.62, 1.58), (-12, 0, 24))
sit(T9, 0.65, 1.35, -58); PL(T9, *PA); PE(T9, *JUDGE); B.H(T9, (0, 0, 0)); B.A(T9, (-15, 6), (-15, -6))
B.E(T9, 0.5); B.BR(T9, 0.0, 0.045, 0); B.MO(T9, 0)
B.AR(47.3, (-15, -6)); B.AR(47.9, (-82, 10)); B.AR(49.4, (-82, 10)); B.H(47.3, (0, 0, 0)); B.H(47.9, (4, 6, -8)); lkey(FACE, F(T9), 12)
# ---- S10 it has heard everything ----
sit(T10, 0.65, 1.35, -58); PL(T10, *PA); K(P, T10, sc=(1, 1, 1))
for i in range(5): K(P, T10 + 0.6 + i * 1.1, sc=(1.02, 1.05, 1.02)); K(P, T10 + 1.15 + i * 1.1, sc=(1, 1, 1))
B.AR(T10, (-15, -6)); B.E(T10, 0.45); B.BR(T10, 0.0, 0.0, 0); B.H(T10, (6, 0, 0))
K(B.rig, 52.9, sc=(1, 1, 1)); K(B.rig, 53.5, sc=(1.04, 1.04, 1.05)); K(B.rig, 54.4, sc=(1, 1, 0.97)); K(B.rig, 55.2, sc=(1, 1, 1)); B.H(53.5, (-6, 0, 0)); B.H(54.4, (14, 0, 0))
# ---- S11 I whisper to it ----
PB = ((-0.72, 2.3, 1.56), (-9, 0, 40))
sit(T11, 0.7, 1.55, -72); PL(T11, *PB); PE(T11, *NEUT); K(B.rig, T11, sc=(1, 1, 1))
B.E(T11, 1.0); B.BR(T11, 0.02, 0.02, -6); B.H(T11, (0, 0, 0)); B.A(T11, (-15, 6), (-15, -6))
sit(56.0, 0.55, 1.6, -72, 10); B.AL(56.0, (-120, -20)); B.H(56.0, (8, 0, -6))
for i in range(4): B.AR(56.3 + i * 0.55, (-60, 10)); B.AR(56.58 + i * 0.55, (-85, -10))
B.H(57.8, (8, 0, -6)); B.H(58.0, (16, 0, -6)); B.H(58.2, (8, 0, -6)); B.H(58.4, (16, 0, -6))
sit(58.6, 0.55, 1.6, -72, 10); sit(59.0, 0.7, 1.55, -72, 0); B.A(59.0, (-15, 6), (-15, -6)); B.H(59.0, (0, 0, 0)); B.E(58.6, 1.0); B.E(59.0, 0.12); B.BR(59.0, 0, 0, 0); B.MO(59.0, 0, 1.0)
B.H(59.5, (0, 8, 0)); B.AR(59.7, (-15, -6)); B.AR(60.0, (-88, 0)); B.AR(60.2, (-80, 0)); B.AR(60.6, (-15, -6))
PL(60.0, *PB); PL(60.15, (-0.8, 2.36, 1.56), (-16, 0, 40)); PL(60.4, (-0.7, 2.29, 1.56), (-6, 0, 40)); PL(60.65, *PB)
sit(61.2, 0.7, 1.55, -72, 0);
# ---- S12 ceiling / ten years ago ----
lie(T12); PL(T12, *FLATP); PE(T12, *NEUT); B.H(T12, (0, 0, 0)); B.A(T12, (-28, 8), (-28, -8)); B.E(T12, 0.8); B.BR(T12, 0, 0, 0); memo(T12, 0); memo(62.8, 0); memo(63.2, 90)
memo(T12b, 80); B.E(T12b, 1.0); B.A(T12b, (-28, 8), (-28, -8)); B.A(T12b + 0.5, (-105, -22), (-105, 22)); B.A(66.3, (-105, -22), (-105, 22)); B.A(66.9, (-28, 8), (-28, -8)); B.BR(66.3, 0.02, 0.02, 0); B.BR(66.9, -0.01, -0.01, -14)
# ---- S13 débile / laugh / hurts ----
memo(T13, 0); lie(T13); B.A(T13, (-28, 8), (-28, -8)); B.E(T13, 0.8); B.BR(T13, -0.02, -0.02, 12); lkey(FACE, F(T13), 7)
B.AR(67.7, (-28, -8)); B.AR(68.05, (-165, 22)); B.AR(69.3, (-165, 22)); B.AR(69.7, (-28, -8))
B.faceoff(68.1, 69.5, 0.8); V(VT_DEB, (68.1, 69.5))
B.E(69.6, 0.22, 0.22, 1.1); B.BR(69.6, 0.03, 0.03, 8); B.MO(69.6, 0.7, 1.3); lkey(FACE, F(69.6), 10)
for i in range(8):
    K(B.root, 69.6 + i * 0.22, loc=(0, 0.2, 1.2)); K(B.root, 69.71 + i * 0.22, loc=(0, 0.2, 1.26)); B.MO(69.6 + i * 0.22, 0.75, 1.3); B.MO(69.71 + i * 0.22, 0.45, 1.3)
K(B.root, 71.4, loc=(0, 0.2, 1.2)); B.MO(71.5, 0.5, 1.2); B.MO(72.0, 0.15, 0.9); B.MO(72.5, 0.0, 0.7)
B.E(71.5, 0.22, 0.22, 1.1); B.E(72.1, 0.9); B.BR(71.6, 0.03, 0.03, 8); B.BR(72.3, 0.02, 0.02, 0); B.BR(72.8, 0.02, -0.03, -8); lkey(FACE, F(71.5), 10); lkey(FACE, F(72.9), 3.5)
B.AL(72.0, (-28, 8)); B.AL(72.7, (-60, -42)); PE(T13, *NEUT); PE(72.2, *NEUT); PE(72.9, 6, 0.9, 0.1)
# ---- S14 mirror ----
B.R3(T14, (1.95, -0.2, 0), (0, 0, 90)); B.A(T14, (0, 4), (0, -4)); B.H(T14, (0, 0, 0)); B.E(T14, 0.5); B.BR(T14, -0.01, -0.01, -10); B.MO(T14, 0.03, 0.7)
PL(T14, *PROP); PE(T14, *NEUT); lkey(FACE, F(T14), 5); memo(T14, 0); emis_key(MIRM, F(T14) - 1, 0); emis_key(MIRM, F(T14), 0.5); emis_key(MIRM, F(T14b) - 1, 0.5); emis_key(MIRM, F(T14b), 0)
Past.R3(F(T14) - 1, OLDPOS, (0, 0, 0)); Past.R3(T14, (3.27, -0.2, 0.2), (0, 0, -90), (1, 0.1, 1)); Past.R3(F(T14b) - 1, (3.27, -0.2, 0.2), (0, 0, -90), (1, 0.1, 1)); Past.R3(T14b, OLDPOS, (0, 0, 0))
Past.E(T14, 1.2, 1.2, 1.2); Past.BR(T14, 0.04, 0.04, -12); Past.MO(T14, 0.3, 2.0)
t = T14
while t < T14b - 0.3:
    Past.A(t, (0, 60), (0, -60)); Past.A(t + 0.16, (0, 120), (0, -120)); Past.MO(t, 0.6, 2.0); Past.MO(t + 0.16, 0.2, 2.0); Past.H(t, (0, 10, 0)); Past.H(t + 0.16, (0, -10, 0)); t += 0.32
B.H(76.0, (0, 0, 0)); B.H(76.6, (10, 0, 0)); B.E(76.6, 0.35)
# 14b: realisation
B.H(T14b, (0, 0, 0)); B.E(T14b, 0.6); B.BR(T14b, 0, 0, -10); B.A(T14b, (0, 4), (0, -4)); lkey(FACE, F(T14b), 3)
B.A(80.3, (0, 4), (0, -4)); B.A(81.0, (-55, -12), (-55, 12)); B.H(80.6, (0, 0, 0)); B.H(81.2, (22, 0, 0)); B.H(82.3, (22, 0, 0)); B.H(82.9, (4, 0, 0))
B.E(82.4, 0.6); B.E(82.9, 0.08); B.A(83.6, (-55, -12), (-55, 12)); B.A(84.2, (0, 4), (0, -4))
K(B.root, 84.2, loc=(1.95, -0.2, 0)); K(B.root, 84.33, loc=(1.95, -0.2, 0.16)); K(B.root, 84.5, loc=(1.95, -0.2, 0)); B.E(84.33, 0.3, 0.3, 1.3); B.BR(84.33, 0.05, 0.05, 14); B.E(84.9, 0.5); B.BR(84.9, 0.0, 0.0, -14)
lkey(MOON, 1, 3.2); lkey(MOON, F(T14b) - 1, 3.2); lkey(MOON, F(T14b), 1.6); lkey(MOON, F(T15a) - 1, 1.6); lkey(MOON, F(T15a), 3.2)
# ---- S15c typing and deleting ----
lie(T15c); PL(T15c, *FLATP); PE(T15c, *JUDGE); B.H(T15c, (0, 0, 0)); B.A(T15c, (-28, 8), (-95, -10)); PHK(F(T15c) - 1, PH_BED, 0, 0); PHK(T15c, PH_INS, 9, 0.8)
for i, (a, b) in enumerate(((T15c, 89.0), (89.0, 89.45), (89.45, 89.85), (89.85, T15e))): V(phB[i], (a, b))
PHK(T15d, PH_HOLD, 14, 0.8); B.E(T15c, 0.5, 0.5, 0.6); B.BR(T15c, 0.05, 0.05, -16); B.MO(T15c, 0.05, 0.7); lkey(FACE, F(T15c), 4)
PHK(90.7, PH_HOLD, 14, 0.8); PHK(91.2, PH_BED, 0, 0); B.AR(90.7, (-95, -10)); B.AR(91.2, (-25, -30)); B.E(90.6, 0.5, 0.5, 0.6); B.E(91.1, 0.1)
# ---- S15f hug & scream ----
PH2 = ((0, 1.02, 1.5), (0, 0, 0))
sit(T15f, 0, 1.45, 0); PL(T15f, *PH2); PE(T15f, *NEUT); B.A(T15f, (-52, -30), (-52, 30)); B.H(T15f, (0, 0, 0)); B.E(T15f, 0.9); B.BR(T15f, 0.02, 0.02, -8); lkey(FACE, F(T15f), 7)
B.H(103.4, (0, 0, 0)); B.H(103.9, (20, 0, 10)); B.H(105.6, (20, 0, 10)); B.H(106.0, (0, 0, 0)); B.E(105.9, 0.9); B.E(106.1, 0.12); B.BR(106.1, 0, 0, 0)
PL(105.9, *PH2); PL(106.4, (0, 1.05, 2.05), (0, 0, 0)); B.A(105.9, (-52, -30), (-52, 30)); B.A(106.4, (-110, -30), (-110, 30)); PL(106.7, (0, 1.05, 2.05), (0, 0, 0))
for i in range(6):
    sit(106.7 + i * 0.2, 0.03, 1.45, 0); sit(106.8 + i * 0.2, -0.03, 1.45, 0); PL(106.7 + i * 0.2, (0.03, 1.05, 2.05), (0, 0, 3)); PL(106.8 + i * 0.2, (-0.03, 1.05, 2.05), (0, 0, -3))
sit(108.0, 0, 1.45, 0); PL(108.0, (0, 1.05, 2.05), (0, 0, 0)); B.R3(108.6, (0, 0.2, 1.2), (-90, 0, 0)); PL(108.6, (0, 1.9, 1.75), (-90, 0, 0)); B.A(108.0, (-110, -30), (-110, 30)); B.A(108.6, (-28, 30), (-28, -30))
# ---- S16 the night goes by ----
lkey(MOON, F(T16a), 3.2); lkey(MOON, F(T17), 2.0); K(MOON, T16a, rot=None)
lie(T16a); PL(T16a, *FLATP); PE(T16a, *NEUT); B.A(T16a, (-28, 8), (-28, -8)); B.E(T16a, 0.9); B.BR(T16a, 0, 0, 0); B.H(T16a, (0, 0, 0)); lkey(FACE, F(T16a), 6)
for i, g in enumerate(SHEEP):
    t0 = T16a + 0.4 + i * 0.9; stop = (i == 3)
    V(g, (t0, 114.0 if stop else t0 + 1.7))
    key(g, F(t0), loc=(-1.9, 1.0, 2.2)); key(g, F(t0 + 0.45), loc=(-0.9, 1.0, 3.0)); key(g, F(t0 + 0.85), loc=(0, 1.0, 2.5))
    if not stop: key(g, F(t0 + 1.3), loc=(0.9, 1.0, 3.0)); key(g, F(t0 + 1.7), loc=(1.9, 1.0, 2.2))
    else: key(g, F(113.5), loc=(0, 1.0, 2.5)); key(g, F(113.9), loc=(0.6, 1.0, 3.6))
V(gSP, (112.6, 113.7)); K(gSP, 112.6, loc=(0.1, 0.9, 2.2)); K(gSP, 113.7, loc=(0.1, 0.9, 2.2))
B.E(112.5, 0.9); B.E(112.8, 1.2, 1.2, 1.15); B.BR(112.8, 0.03, 0.03, -10); B.AR(113.1, (-28, -8)); B.AR(113.45, (-125, 20)); B.AR(113.75, (-90, -25)); B.AR(114.3, (-28, -8)); B.E(114.3, 0.4)
# b: glass of water
sit(T16b, 0, -0.75, 0); PL(T16b, *PROP); B.A(T16b, (-12, 6), (-70, -8)); B.H(T16b, (0, 0, 0)); B.E(T16b, 0.6); B.BR(T16b, 0, 0, -8)
K(gGl, F(T16b) - 1, loc=(2.7, 2.35, 1.13)); gl = [(T16b, (0.47, -1.24, 1.6), -70), (116.0, (0.47, -1.24, 1.6), -70), (116.6, (0.3, -1.12, 1.95), -118), (117.6, (0.3, -1.12, 1.95), -118), (118.2, (0.47, -1.24, 1.6), -70), (120.5, (0.47, -1.24, 1.6), -70)]
for t, loc, ar in gl: K(gGl, t, loc=loc); B.AR(t, (ar, -8 if ar > -100 else 16))
K(gGl, T16c, loc=(2.7, 2.35, 1.13))
B.H(116.6, (-14, 0, 0)); B.H(117.6, (-14, 0, 0)); B.H(118.3, (22, 0, 0)); B.H(119.0, (22, 0, 12)); B.H(119.4, (22, 0, -12)); B.H(119.8, (22, 0, 12)); B.H(120.2, (22, 0, -12)); B.E(118.3, 0.5)
# c: upside down
B.R3(T16c, (0, 0.45, 1.2), (-90, 0, 180)); PL(T16c, (1.0, 2.6, 1.55), (-22, 0, -18)); PE(T16c, *BORED); B.A(T16c, (-28, 55), (-28, -55)); B.H(T16c, (0, 0, 0)); B.E(T16c, 1.0); B.BR(T16c, 0, 0, 0)
for i in range(5): B.A(T16c + 0.8 + i * 1.0, (-28, 55), (-28, -55)); B.A(T16c + 1.3 + i * 1.0, (-170, 25), (-170, -25))
# d: gives up, hugging the pillow
lie(T16d); PL(T16d, (0, 1.15, 1.66), (-90, 0, 0)); PE(T16d, *NEUT); B.A(T16d, (-48, -26), (-48, 26)); B.H(T16d, (0, 0, 0)); B.E(T16d, 1.1, 1.1, 1.1); B.BR(T16d, 0, 0, 0)
B.blink(129.0, 1.1); B.blink(131.0, 1.1)
# ---- S17 tomorrow I'll smile ----
sit(T17, 0, 1.0, 0); PL(T17, (0.62, 2.72, 1.62), (-14, 0, -10)); PE(T17, *JUDGE); B.A(T17, (-10, 5), (-10, -5)); B.H(T17, (0, 0, 0)); lkey(FACE, F(T17), 7)
B.E(T17, 0.55); B.BR(T17, 0, 0, -8); B.MO(T17, 0, 1.0)
def smile(t): B.MO(t, 0.22, 2.3); B.BR(t, 0.035, 0.035, 6); B.E(t, 1.0)
def real(t): B.MO(t, 0.0, 0.8); B.BR(t, -0.005, -0.005, -12); B.E(t, 0.5)
B.MO(132.9, 0, 1.0); smile(133.5); B.E(135.2, 1.0)
B.AR(135.6, (-10, -5)); B.AR(136.1, (-100, -22)); B.AR(138.3, (-100, -22)); B.AR(138.8, (-10, -5))
B.faceoff(136.4, 138.3, 1.0); V(VT_CAVA, (136.4, 138.3)); smile(138.3)
lkey(WARM, F(T17), 0); lkey(WARM, F(133.5), 130); lkey(WARM, F(139.0), 130); lkey(WARM, F(144.3), 0)
for t, fn in ((139.1, smile), (140.2, smile), (140.45, real), (141.0, real), (141.2, smile), (141.9, smile), (142.15, real), (142.6, real), (142.8, smile), (143.3, smile), (143.6, real)): fn(t)
B.H(143.6, (0, 0, 0)); B.H(144.4, (14, 0, 0)); B.E(144.4, 0.3)
# ---- S18 dictator ----
sit(T18, 0, 0.9, 0); PL(T18, (0.9, 2.72, 1.58), (-14, 0, -12)); PE(T18, *NEUT); B.H(T18, (-10, 0, 0)); B.A(T18, (-10, 5), (-10, -5)); B.E(T18, 1.2, 1.2, 1.15); B.BR(T18, 0.04, 0.04, -12); B.MO(T18, 0.05, 0.6)
memo(F(T18) - 1, 0); memo(T18, 200); lkey(FACE, F(T18), 6)
for i in range(8):
    t = T18 + i * 0.4; K(GB, t, loc=(0, 0.9, 3.45 + (0.08 if i % 2 else 0)), rot=(0, 0, 0)); K(BST, t, rot=(0, 35 if i % 2 else -25, 0)); K(SST, t, rot=(0, 35 if i % 2 else -25, 0))
    K(GS, t, loc=(0.3, 3.07, 3.0 + (0.12 if i % 2 else 0)))
# drawers
sit(T18b, 0, 0.9, 60); B.H(T18b, (0, 0, 0)); B.A(T18b, (-10, 5), (-10, -5)); B.E(T18b, 1.25, 1.25, 1.2)
for i, d in enumerate(DRW):
    z = 0.3 + i * 0.45; t = 148.2 + (2 - i) * 0.55
    K(d, T18b, loc=(2.66, -2.7, z)); K(d, t, loc=(2.66, -2.7, z)); K(d, t + 0.25, loc=(2.1, -2.7, z)); K(d, 150.3, loc=(2.1, -2.7, z)); K(d, 150.55, loc=(2.66, -2.7, z))
lkey(DRL, F(148.2), 0); lkey(DRL, F(148.5), 140); lkey(DRL, F(150.3), 220); lkey(DRL, F(150.6), 0)
for i, g in enumerate(FLY):
    t0 = 148.4 + (i % 3) * 0.5 + i * 0.05; z0 = 0.5 + ((9 - i) % 3) * 0.45
    V(g, (t0, 150.55)); x1 = random.uniform(-0.6, 1.6); y1 = random.uniform(-2.6, -0.2); z1 = random.uniform(1.6, 3.4)
    key(g, F(t0), loc=(2.2, -2.7 + random.uniform(-0.4, 0.4), z0), rot=(0, 0, 60)); key(g, F(t0 + 0.9), loc=(x1, y1, z1), rot=(random.uniform(-80, 80), random.uniform(-80, 80), random.uniform(0, 300)))
    key(g, F(150.2), loc=(x1 - 0.2, y1, z1 - 0.25), rot=(random.uniform(-80, 80), random.uniform(-80, 80), random.uniform(0, 300))); key(g, F(150.5), loc=(2.3, -2.7, 0.8), rot=(0, 0, 60))
B.AL(149.2, (-10, 5)); B.AL(149.6, (-85, 0)); B.AR(149.6, (-85, 0)); B.AR(149.2, (-10, -5)); B.A(150.3, (-85, 0), (-85, 0)); B.A(150.8, (-10, 5), (-10, -5)); memo(150.3, 200); memo(150.7, 0)
# ---- S19 just here in the dark ----
lie(T19); PP = ((-1.15, 1.72, 1.03), (-90, 0, -90)); PL(T19, *PP); PE(T19, *NEUT); B.H(T19, (0, 0, 0)); B.A(T19, (-22, 62), (-28, -8)); B.E(T19, 0.5); B.BR(T19, 0, 0, 0); B.MO(T19, 0, 1.0)
lkey(FACE, F(T19), 4.5); lkey(MOON, F(T19), 1.7); B.blink(154.2, 0.5)
# ---- S20 dawn ----
lie(T20); PL(T20, *PP); B.H(T20, (0, 0, 0)); B.A(T20, (-22, 62), (-28, -8)); B.E(T20, 0.5)
B.R3(157.6, (0, 0.2, 1.2), (-90, 0, 0)); B.R3(158.6, (-0.1, 0.2, 1.3), (-90, -62, 0)); B.A(158.6, (-30, 20), (-70, -10)); B.E(158.6, 0.75); B.BR(158.6, 0.02, 0.02, -10)
B.talk(160.5, 162.1, 0.17, 0.4); B.AR(162.3, (-70, -10)); B.AR(162.6, (-95, -10)); B.AR(162.85, (-75, -10)); B.AR(163.1, (-95, -10)); B.AR(163.4, (-75, -10))
PL(162.6, *PP); PL(162.72, PP[0], PP[1], (1, 0.9, 1)); PL(162.85, *PP); PL(163.1, PP[0], PP[1], (1, 0.9, 1)); PL(163.4, *PP)
B.R3(164.0, (-0.1, 0.2, 1.3), (-90, -62, 0)); B.R3(165.0, (-0.42, 0.22, 1.36), (-90, -62, 0)); PL(164.6, *PP); PL(165.1, PP[0], PP[1], (1.04, 0.85, 1.03)); PE(164.6, *NEUT); PE(165.4, *KIND)
B.E(165.2, 0.75); B.E(166.2, 0.4); B.BR(166.2, 0.01, 0.01, 0)
# sky / dawn
def sky(t, c, s):
    col_key(SKY, KT(t), c, "Emission Color"); emis_key(SKY, KT(t), s)
sky(1, (0.1, 0.18, 0.5), 1.0); sky(T19, (0.1, 0.18, 0.5), 1.0); sky(T20b, (1.0, 0.45, 0.25), 2.2); sky(175.0, (1.0, 0.7, 0.45), 4.0)
lkey(DAWN, F(T20b) - 1, 0); lkey(DAWN, F(T20b), 0.6); lkey(DAWN, F(175.5), 5.5); lkey(MOON, F(T20), 1.7); lkey(MOON, F(T20b), 0.8); lkey(MOON, F(173.0), 0.0)
lkey(FILL, 1, 55); lkey(FILL, F(T20b), 55); lkey(FILL, F(175.0), 90)
for l_ in (FILL,):
    l_.data.color = (0.3, 0.4, 0.9); l_.data.keyframe_insert("color", frame=F(T20b)); l_.data.color = (0.9, 0.6, 0.5); l_.data.keyframe_insert("color", frame=F(175.5))
B.E(T20c, 0.4); B.E(172.0, 0.3); B.E(173.0, 0.07); B.MO(T20c, 0, 1.0); lkey(FACE, F(T20c), 4.5); lkey(FACE, F(174.5), 1.5)
# alarm
for i in range(14): K(CLK, 176.4 + i * 0.12, rot=(0, 6 if i % 2 else -6, -18))
K(CLK, 176.3, rot=(0, 0, -18))
B.E(T20e, 0.07); B.E(177.9, 0.07, 0.07); B.E(178.1, 0.07, 0.75); B.BR(178.1, 0, 0.01, 0); lkey(FACE, F(178.1), 4)
B.AL(178.3, (-30, 20)); B.AL(178.7, (-30, 75)); B.AL(179.3, (-120, 30))
PL(178.7, PP[0], PP[1], (1.04, 0.85, 1.03)); PL(179.35, (-0.55, 1.95, 1.95), (-90, 25, -90)); PE(178.6, *KIND); PE(179.3, *NEUT)

# sing along with every line (except the hand-acted mouth bits)
NOSING = [(T7a, 40.6), (T13, T14), (T14, T14b), (T15a, T15a + 2.7), (T17, T18), (160.0, 163.0), (T20b, TEND), (T5, T6), (T10, T11), (T18b, T19)]
for l in TL["lines"]:
    if any(a - 0.2 <= l["start"] < b for a, b in NOSING): continue
    B.sing(l["start"], l["end"], 0.75)

# =====================================================================
#                              CAMERA
# =====================================================================
target = empty("target", (0, 0, 1.15))
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 32; cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 4.0
cam = bpy.data.objects.new("cam", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = target
TOPW = ((0, 0.3, 4.3), (0, 0.85, 1.0))
SHOTS = [  # (t0, lens, cam0, tgt0, cam1, tgt1)
 (0, 24, (2.7, -4.9, 4.0), (0, 0.9, 1.0), (2.0, -3.7, 3.5), (0, 1.0, 1.1)),
 (T1b, 35, (2.9, 0.3, 2.9), (0, 1.6, 1.35), (2.7, 0.4, 2.8), (0, 1.6, 1.35)),
 (T1c, 50, (0.9, 0.9, 1.75), (2.25, 2.3, 1.22), (1.0, 1.0, 1.7), (2.25, 2.3, 1.22)),
 (T2, 40, (0, 1.3, 3.7), (0, 1.95, 1.3), (0, 1.35, 3.4), (0, 1.95, 1.3)),
 (T3, 26, (0, 0.2, 4.25), (0, 1.15, 1.2), (0, 0.25, 4.1), (0, 1.15, 1.2)),
 (T4, 21, (0.5, -2.7, 1.55), (0, 1.1, 3.5), (0.3, -2.5, 1.55), (0, 1.1, 3.5)),
 (T5, 28, (1.0, -1.9, 2.5), (0, 3.1, 3.05), (0.8, -1.6, 2.5), (0, 3.1, 3.05)),
 (T5i, 45, (0.35, 2.55, 2.25), (0, 0.75, 2.2), (0.3, 2.5, 2.25), (0, 0.75, 2.2)),
 (T6, 21, (-0.6, -2.8, 1.6), (0, 0.9, 3.6), (-0.4, -2.6, 1.6), (0, 0.9, 3.6)),
 (T7a, 50, (0, 1.55, 3.0), (0, 1.9, 1.45), (0, 1.6, 2.8), (0, 1.9, 1.45)),
 (T7b, 45, (1.5, 0.9, 3.3), (0.05, 1.95, 1.45), (1.4, 1.0, 3.2), (0.05, 1.95, 1.45)),
 (T7c, 45, (0.1, 1.62, 1.6), (0.1, 1.75, 2.25), (0.1, 1.62, 1.66), (0.1, 1.75, 2.25)),
 (T7d, 35, (0, 1.2, 3.5), (0, 2.0, 1.3), (0, 1.25, 3.3), (0, 2.0, 1.3)),
 (T8, 21, *TOPW, *TOPW),
 (T9, 30, (0.25, -2.6, 2.0), (0, 1.9, 1.7), (0.2, -2.2, 2.0), (0, 1.9, 1.7)),
 (T10, 50, (-0.2, 0.3, 1.9), (-0.8, 2.6, 1.7), (-0.1, 0.3, 2.0), (-0.75, 2.6, 2.1)),
 (52.8, 30, (0.3, -2.4, 2.0), (0, 1.9, 1.7), (0.3, -2.3, 2.0), (0, 1.9, 1.7)),
 (T11, 28, (0, -2.5, 2.0), (0, 1.8, 1.65), (0, -2.2, 2.0), (0, 1.8, 1.65)),
 (T12, 22, (0, 1.9, 1.75), (-0.3, 1.3, 4.4), (0, 1.9, 1.75), (-0.5, 1.35, 4.4)),
 (T12b, 21, (0.5, -2.9, 1.5), (0, 1.0, 3.9), (0.4, -2.8, 1.5), (0, 1.0, 3.9)),
 (T13, 50, (1.3, 0.8, 3.0), (0, 1.85, 1.4), (1.2, 0.9, 2.8), (0, 1.85, 1.4)),
 (T14, 32, (0.2, -2.3, 2.4), (3.3, -0.2, 1.45), (0.5, -2.1, 2.3), (3.3, -0.2, 1.45)),
 (T14b, 30, (3.25, -0.7, 1.9), (1.95, -0.2, 1.6), (3.05, -0.6, 1.85), (1.95, -0.2, 1.6)),
 (T15a, 50, (0, 1.55, 3.0), (0, 1.9, 1.45), (0, 1.6, 2.8), (0, 1.9, 1.45)),   # (reused frames, never rendered)
 (T15c, 45, (0.1, 1.62, 1.6), (0.1, 1.75, 2.25), (0.1, 1.62, 1.66), (0.1, 1.75, 2.25)),
 (T15d, 35, (0, 1.2, 3.5), (0, 2.0, 1.3), (0, 1.25, 3.3), (0, 2.0, 1.3)),
 (T15e, 21, *TOPW, *TOPW),                                                    # (reused)
 (T15f, 35, (0, -2.3, 2.05), (0, 1.5, 1.8), (0, -2.0, 2.05), (0, 1.5, 1.8)),
 (T16a, 38, (0, -4.8, 2.5), (0.2, 1.0, 1.75), (0, -4.6, 2.5), (0.2, 1.0, 1.75)),
 (T16b, 38, (0, -4.8, 2.5), (0.2, 1.0, 1.75), (0, -4.6, 2.5), (0.2, 1.0, 1.75)),
 (T16c, 38, (0, -4.8, 2.5), (0.2, 1.0, 1.75), (0, -4.6, 2.5), (0.2, 1.0, 1.75)),
 (T16d, 38, (0, -4.8, 2.5), (0.2, 1.0, 1.75), (0, -4.6, 2.5), (0.2, 1.0, 1.75)),
 (T17, 50, (0, -1.9, 2.1), (0.1, 1.0, 1.95), (0, -1.9, 2.1), (0.1, 1.0, 1.95)),
 (T18, 21, (0.4, -3.4, 0.9), (0, 1.6, 2.75), (0.3, -3.2, 0.9), (0, 1.6, 2.75)),
 (T18b, 26, (0.3, -0.7, 2.7), (2.3, -2.6, 1.1), (0.4, -0.8, 2.6), (2.3, -2.6, 1.1)),
 (T19, 24, (0, 0.4, 3.3), (0, 0.9, 1.0), (0, 0.3, 4.3), (0, 0.85, 1.0)),
 (T20, 35, (-2.9, 1.2, 3.0), (-0.35, 1.7, 1.25), (-2.6, 1.3, 2.8), (-0.35, 1.7, 1.25)),
 (T20b, 50, (1.4, 0.4, 2.3), (-3.4, 1.45, 2.65), (1.2, 0.5, 2.3), (-3.4, 1.45, 2.65)),
 (T20c, 26, (1.3, -4.6, 2.5), (0, 1.0, 1.4), (1.0, -4.2, 2.4), (0, 1.0, 1.4)),
 (T20d, 45, (1.0, 0.8, 1.75), (2.25, 2.3, 1.25), (1.0, 0.8, 1.75), (2.25, 2.3, 1.25)),
 (T20e, 35, (-2.6, 1.3, 2.8), (-0.35, 1.7, 1.3), (-2.5, 1.3, 2.7), (-0.35, 1.7, 1.3)),
]
for i, (t0, ln, c0, g0, c1, g1) in enumerate(SHOTS):
    f0 = F(t0) if i else 1; f1 = (F(SHOTS[i + 1][0]) - 1) if i + 1 < len(SHOTS) else NF
    if i: CUTF.add(f0 - 1)
    for f, c, g in ((f0, c0, g0), (f1, c1, g1)):
        key(cam, f, loc=c); key(target, f, loc=g)
        cam_d.dof.focus_distance = (Vector(c) - Vector(g)).length; cam_d.dof.keyframe_insert("focus_distance", frame=f)
        cam_d.lens = ln; cam_d.keyframe_insert("lens", frame=f)
# S10: pan from the pillow to Boulon sighing; S13: rack focus to the pillow

def all_fcurves(idb):
    ad = idb.animation_data
    if ad and ad.action:
        for layer in ad.action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    for fc in cb.fcurves: yield fc
ANIM = list(bpy.data.objects) + list(bpy.data.lights) + list(bpy.data.materials) + [m.node_tree for m in bpy.data.materials if m.node_tree] + [cam_d]
for o in ANIM:
    for fc in all_fcurves(o):
        frs = sorted((int(round(kp.co[0])), kp.co[1]) for kp in fc.keyframe_points); have = {a for a, _ in frs}
        for cf in CUTF:
            if cf + 1 in have and cf not in have:
                prev = [v for a, v in frs if a < cf]
                if prev: fc.keyframe_points.insert(cf, prev[-1])
ease_all()
for o in SNAP:
    for fc in all_fcurves(o):
        if fc.data_path == "scale":
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"
for o in LIN:
    for fc in all_fcurves(o):
        for kp in fc.keyframe_points:
            if kp.interpolation != "CONSTANT": kp.interpolation = "LINEAR"
for idb in ANIM:
    for fc in all_fcurves(idb):
        for kp in fc.keyframe_points:
            if idb in (cam, target, cam_d): kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            if int(round(kp.co[0])) in CUTF: kp.interpolation = "CONSTANT"

world = bpy.data.worlds.new("w"); world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.03, 0.08, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.3
scene.world = world
r = scene.render
r.resolution_x, r.resolution_y, r.resolution_percentage = 720, 1280, 100
r.filepath = OUT; r.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"; scene.view_settings.look = "AgX - Punchy"
if ENGINE == "CYCLES":
    r.engine = "CYCLES"; scene.cycles.device = "CPU"; scene.cycles.samples = 8; scene.cycles.use_denoising = True; scene.cycles.max_bounces = 3; scene.cycles.use_light_tree = False; scene.cycles.denoising_quality = "FAST"
    scene.cycles.transparent_max_bounces = 6
    r.use_motion_blur = True; r.motion_blur_position = "START"
else:
    r.engine = "BLENDER_EEVEE"
print("OBJECTS", len(bpy.data.objects), "FRAMES", NF)
