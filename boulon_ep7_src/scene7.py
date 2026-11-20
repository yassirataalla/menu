# ================= EPISODE 7 — « মাথা নাড়ে নারায়ণ » : sets, acting, camera =================
random.seed(5)
DX, EX = 20.0, 120.0
PARK = (0, -60, 0)
# ---------------- cut times ----------------
T_DIN0 = 5.5; T_KW = 10.5; T_Y1 = 15.4; T_Y2 = 20.3; T_Y3 = 24.1; T_Y4 = 28.0
T_CA = 32.0; T_CA2 = 36.0; T_CB = 40.0; T_CB2 = 42.0; T_CC = 44.0; T_CC2 = 46.0; T_CI = 48.0; T_CD = 52.0
T_DANCE = 56.0; T_V1 = 64.0; T_V2 = 68.2; T_V3 = 72.2; T_V4 = 76.0; T_R1 = 80.0
T_M1 = 104.0; T_M2 = 106.0; T_M3 = 108.0; T_M4 = 110.0; T_R2 = 112.0
T_Z1 = 128.0; T_Z2 = 132.2; T_Z3 = 136.3; T_Z4 = 140.0; T_R3 = 144.0; T_OUT = 168.0; T_END = NF / FPS

# ================= SETS =================
bpy.ops.mesh.primitive_plane_add(size=400); give(bpy.context.object, MT("ground", (0.32, 0.32, 0.33), 0.5))
STEEL = MT("steel", (0.46, 0.48, 0.52), 0.28); STEELD = MT("steelD", (0.3, 0.31, 0.33), 0.35); IRON = MT("iron", (0.03, 0.03, 0.035), 0.4)
TILE = MT("tile", (0.36, 0.5, 0.52), 0.35); PUFF = MT("puff", (1, 1, 1), 0.9); FOAM = MT("foam", (0.95, 0.98, 1.0), 0.6)
# ---- kitchen (origin)
cube("kBack", (0.6, 2.8, 2.2), (4.4, 0.1, 2.2), TILE, 0)
for i in range(1, 7): cube(f"kJoint{i}", (0.6, 2.69, i * 0.62), (4.4, 0.005, 0.006), MT("joint", (0.25, 0.36, 0.38), 0.6), 0)
cube("kLeft", (-3.5, -4.5, 2.2), (0.1, 7.5, 2.2), TILE, 0); cube("kRight", (4.7, -4.5, 2.2), (0.1, 7.5, 2.2), TILE, 0)
cube("kCeil", (0.6, -4.5, 4.45), (4.4, 7.5, 0.05), MT("ceil", (0.85, 0.85, 0.85), 0.8), 0)
cube("kFloor", (0.6, -4.5, 0.005), (4.4, 7.5, 0.005), MT("kfloor", (0.2, 0.21, 0.23), 0.35), 0)
cube("island", (0.45, -0.2, 0.47), (2.45, 0.38, 0.47), STEEL, 0.02); cube("islandTop", (0.45, -0.2, 0.945), (2.5, 0.42, 0.02), MT("steelT", (0.58, 0.6, 0.64), 0.18), 0.01)
cube("islandKick", (0.45, -0.57, 0.08), (2.45, 0.02, 0.08), STEELD, 0)
BP = (-1.0, 0.5, 0.14); KP = (0.75, 0.5, 0.0); CP = (2.6, 1.3, 0.0); YP = (3.65, -0.25, 0.0)
cube("crate", (BP[0], BP[1], 0.07), (0.45, 0.35, 0.07), MT("crate", (0.5, 0.3, 0.14), 0.7), 0.02)
cube("sink", (-1.0, -0.2, 0.955), (0.42, 0.3, 0.012), STEELD, 0.01)
cable("faucet", [(-1.0, 0.12, 0.96), (-1.0, 0.12, 1.3), (-1.0, -0.05, 1.36), (-1.0, -0.12, 1.25)], STEEL, 0.022)
for i in range(16): sphere(f"foam{i}", (-1.0 + random.uniform(-0.36, 0.36), -0.2 + random.uniform(-0.24, 0.24), 0.98 + random.uniform(0, 0.03)), random.uniform(0.035, 0.07), FOAM)
def plate_mesh(name, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.02, vertices=28); o = bpy.context.object; smooth(o); give(o, m)
    me = o.data; me.name = name; bpy.data.objects.remove(o); return me
PD = plate_mesh("plateD", MT("plateD", (0.86, 0.8, 0.68), 0.3)); PC = plate_mesh("plateC", MT("plateC", (0.98, 0.98, 1.0), 0.12)); PK = plate_mesh("plateK", MT("plateK", (0.04, 0.04, 0.045), 0.35))
def plate(name, me, loc, parent=None, rot=(0, 0, 0), sc=1.0):
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); o.location = loc; o.scale = (sc, sc, sc)
    o.rotation_euler = [math.radians(a) for a in rot]
    if parent: o.parent = parent
    return o
for i in range(22): plate(f"dirty{i}", PD, (-1.72 + random.uniform(-0.03, 0.03), -0.2 + random.uniform(-0.03, 0.03), 0.975 + i * 0.026), rot=(random.uniform(-4, 4), random.uniform(-4, 4), 0))
for i in range(9): plate(f"clean{i}", PC, (-0.3, -0.2, 0.975 + i * 0.022))
# Kartik's station
cube("board", (0.75, -0.2, 0.975), (0.3, 0.2, 0.012), MT("board", (0.65, 0.45, 0.25), 0.6), 0.008)
for i, (x, y) in enumerate([(0.55, -0.25), (0.62, -0.1), (0.5, -0.12)]): sphere(f"tom{i}", (x, y, 1.04), 0.055, MT("tomato", (0.8, 0.08, 0.05), 0.3))
for i in range(14): sphere(f"pars{i}", (0.85 + random.uniform(-0.1, 0.12), -0.2 + random.uniform(-0.12, 0.12), 1.0), random.uniform(0.02, 0.04), MT("parsley", (0.1, 0.5, 0.12), 0.7))
sphere("lemon", (1.12, -0.3, 1.03), 0.05, MT("lemon", (0.95, 0.82, 0.1), 0.4), (1.25, 1, 1))
# stove (back right)
cube("stove", (2.3, 2.3, 0.46), (1.1, 0.42, 0.46), STEEL, 0.02); cube("stoveTop", (2.3, 2.3, 0.93), (1.1, 0.42, 0.012), IRON, 0)
cube("hood", (2.3, 2.3, 3.2), (1.15, 0.45, 0.28), STEEL, 0.05); cube("hood2", (2.3, 2.45, 3.9), (0.4, 0.25, 0.5), STEEL, 0.02)
cyl("pot", (1.75, 2.25, 1.12), 0.24, 0.36, MT("potM", (0.1, 0.1, 0.11), 0.35)); cyl("soup", (1.75, 2.25, 1.29), 0.215, 0.02, MT("soup", (0.75, 0.3, 0.1), 0.4))
pan = empty("pan", (2.75, 2.2, 0.99)); cyl("panB", (0, 0, 0), 0.24, 0.05, IRON, parent=pan); cube("panH", (0.42, 0, 0.01), (0.2, 0.025, 0.015), IRON, 0.01, pan)
FLM = MT("flame", (1, 0.5, 0.1), 0.4, (1.0, 0.42, 0.05), 14); FLM2 = MT("flame2", (1, 0.85, 0.3), 0.4, (1.0, 0.8, 0.25), 18)
flames = []
for i in range(5):
    bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=0.09, depth=0.5, location=(0, 0, 0)); o = bpy.context.object; smooth(o); give(o, FLM if i % 2 else FLM2); o.parent = pan
    o.location = ((i - 2) * 0.07, (i % 2) * 0.06 - 0.03, 0.3); flames.append(o)
flameL = light("flameL", "POINT", (2.75, 1.9, 1.6), None, 0, (1.0, 0.5, 0.15), 0.3)
# shelves + logo + clock on the back wall
cube("kShelf", (-1.3, 2.55, 2.25), (1.3, 0.16, 0.02), STEEL, 0.005)
for i in range(7): cyl(f"jar{i}", (-2.3 + i * 0.34, 2.55, 2.4), 0.09, 0.26, MT(f"jar{i % 3}", [(0.75, 0.6, 0.3), (0.5, 0.15, 0.1), (0.3, 0.45, 0.15)][i % 3], 0.3))
disc_img("kLogo", (0.5, 2.68, 3.25), 0.5, img_mat("logoE", WEB + "LIBAN-SUR-SEINE-202.png", 0.35))
clk = empty("clock", (-1.3, 2.66, 3.3)); cyl("clockB", (0, 0, 0), 0.27, 0.04, IRON, (math.radians(90), 0, 0), clk); cyl("clockF", (0, -0.015, 0), 0.24, 0.03, WHITE, (math.radians(90), 0, 0), clk)
hH = empty("hH", (0, -0.035, 0)); hH.parent = clk; cube("hHm", (0, 0, 0.06), (0.012, 0.004, 0.07), IRON, 0, hH)
hM = empty("hM", (0, -0.04, 0)); hM.parent = clk; cube("hMm", (0, 0, 0.09), (0.008, 0.004, 0.1), MT("handR", (0.85, 0.1, 0.1), 0.4), 0, hM)
def clock_at(t, hours):   # hours as float, e.g. 14.5
    key(hH, F(t), rot=(0, hours / 12 * 360, 0)); key(hM, F(t), rot=(0, (hours % 1) * 360 + int(hours) * 360, 0))
# the pass (right end of the island): heat lamps, ticket rail, plated dishes
cube("passRail", (2.45, -0.5, 2.95), (0.5, 0.02, 0.025), STEEL, 0.005)
for x in (2.15, 2.75):
    cyl(f"heatC{x}", (x, -0.2, 3.8), 0.01, 1.3, IRON); bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.2, radius2=0.05, depth=0.2, location=(x, -0.2, 3.05)); o = bpy.context.object; smooth(o); give(o, MT("copper", (0.75, 0.38, 0.2), 0.3))
    sphere(f"heatB{x}", (x, -0.2, 2.99), 0.05, MT("heatG", (1, 0.6, 0.3), 0.3, (1.0, 0.55, 0.2), 9))
for i in range(4): cube(f"ticket{i}", (2.1 + i * 0.22, -0.525, 2.82), (0.06, 0.003, 0.11), WHITE, 0)
PKM = MT("plateK", (0.04, 0.04, 0.045), 0.35)
def bowl(name, loc, r, food, parent=None):
    e = empty(name, loc); cyl(name + "b", (0, 0, 0.04), r, 0.08, PKM, parent=e); cyl(name + "f", (0, 0, 0.075), r * 0.86, 0.02, food, parent=e)
    if parent: e.parent = parent
    return e
HUM = MT("hummus", (0.85, 0.72, 0.45), 0.5); TAB = MT("taboule", (0.15, 0.5, 0.12), 0.7); KIB = MT("kibbeh", (0.4, 0.2, 0.08), 0.6); MOUT = MT("moutabal", (0.75, 0.25, 0.4), 0.5)
bowl("dHum", (2.2, -0.3, 0.965), 0.17, HUM); sphere("dHumOil", (2.2, -0.3, 1.06), 0.05, MT("oil", (0.7, 0.55, 0.1), 0.2), (1, 1, 0.2)); sphere("dHumP", (2.24, -0.33, 1.07), 0.02, MT("tomato"))
bowl("dTab", (2.6, -0.1, 0.965), 0.15, TAB)
for i in range(8): sphere(f"tabT{i}", (2.6 + random.uniform(-0.09, 0.09), -0.1 + random.uniform(-0.09, 0.09), 1.055), 0.018, MT("tomato"))
kp_ = plate("dKibP", PK, (2.72, -0.42, 0.975), sc=1.15)
for i in range(4): o = sphere(f"kib{i}", (2.6 + i * 0.08, -0.42, 1.03), 0.045, KIB, (1.0, 1.9, 1.0)); o.rotation_euler = (0, 0, math.radians(20))
radio = empty("radio", (1.75, 0.02, 0.965)); cube("radioB", (0, 0, 0.11), (0.2, 0.08, 0.11), MT("radioM", (0.8, 0.25, 0.15), 0.4), 0.03, radio)
for sx in (-1, 1): cyl(f"radioS{sx}", (sx * 0.1, -0.082, 0.11), 0.06, 0.01, IRON, (math.radians(90), 0, 0), radio)
cyl("radioA", (0.15, 0, 0.36), 0.008, 0.34, STEEL, (0, math.radians(18), 0), radio)

# ---- dining room (x = DX): stone-block walls, slatted bar, white tables with black lace runners
STONE = MT("stoneW", (0.74, 0.62, 0.42), 0.85); STJ = MT("stoneJ", (0.5, 0.4, 0.26), 0.9); WOODS = MT("woodSlat", (0.5, 0.33, 0.17), 0.55); WOODD = MT("woodDark", (0.16, 0.1, 0.06), 0.5)
cube("dFloor", (DX, -4, 0.006), (5.5, 8, 0.006), MT("terrazzo", (0.62, 0.58, 0.52), 0.4), 0)
for i in range(420): cyl(f"tz{i}", (DX + random.uniform(-5, 5), random.uniform(-10, 3), 0.0125), random.uniform(0.02, 0.05), 0.002, MT(f"tz{i % 3}", [(0.3, 0.27, 0.24), (0.85, 0.82, 0.76), (0.5, 0.36, 0.26)][i % 3], 0.5))
cube("dBack", (DX, 3.3, 2.3), (5.5, 0.15, 2.3), STONE, 0); cube("dLeft", (DX - 5.2, -4, 2.3), (0.15, 7.6, 2.3), STONE, 0); cube("dRight", (DX + 5.2, -4, 2.3), (0.15, 7.6, 2.3), STONE, 0)
cube("dCeil", (DX, -4, 4.62), (5.5, 7.6, 0.05), MT("ceil"), 0)
for i in range(1, 7):
    cube(f"dJh{i}", (DX, 3.148, i * 0.64), (5.5, 0.004, 0.007), STJ, 0)
    for k in range(-5, 6): cube(f"dJv{i}_{k}", (DX + k * 1.1 + (0.55 if i % 2 else 0), 3.148, i * 0.64 - 0.32), (0.007, 0.004, 0.32), STJ, 0)
# bar
BX = DX + 2.3
cube("barBody", (BX, 2.2, 0.55), (1.9, 0.35, 0.55), WOODD, 0); cube("barTop", (BX, 2.15, 1.12), (2.0, 0.45, 0.025), MT("steelT"), 0.01)
for i in range(42): cube(f"slat{i}", (BX - 1.87 + i * 0.091, 1.835, 0.55), (0.026, 0.02, 0.54), WOODS, 0.006)
for z in (2.0, 2.65): cube(f"bShelf{z}", (BX, 3.0, z), (1.9, 0.14, 0.02), WOODS, 0.005)
BOT = [(0.05, 0.2, 0.08), (0.3, 0.05, 0.05), (0.75, 0.6, 0.35), (0.1, 0.1, 0.12), (0.55, 0.3, 0.1), (0.85, 0.7, 0.75)]
for z in (2.0, 2.65):
    for i in range(15):
        c = BOT[random.randrange(6)]; x = BX - 1.75 + i * 0.25; m = MT(f"bot{BOT.index(c)}", c, 0.12)
        cyl(f"bt{z}{i}", (x, 3.0, z + 0.17), 0.048, 0.3, m); cyl(f"btn{z}{i}", (x, 3.0, z + 0.38), 0.018, 0.14, m)
cube("beam", (BX, 1.4, 3.55), (1.3, 0.06, 0.05), WOODS, 0.01)
BULB = MT("edison", (1, 0.7, 0.3), 0.3, (1.0, 0.62, 0.22), 16)
for i in range(3):
    x = BX - 0.8 + i * 0.8; cyl(f"bulbC{i}", (x, 1.4, 3.2), 0.006, 0.6, IRON); sphere(f"bulb{i}", (x, 1.4, 2.85), 0.075, BULB, (1, 1, 1.35))
for sx in (-1, 1): cyl(f"beamC{sx}", (BX + sx * 1.2, 1.4, 4.1), 0.008, 1.0, IRON)
# wall frames: banknotes + logo
fr = empty("frameNotes", (DX - 2.6, 3.13, 2.65)); cube("fnB", (0, 0, 0), (0.62, 0.02, 0.42), IRON, 0.005, fr); cube("fnW", (0, -0.012, 0), (0.58, 0.012, 0.38), MT("paper", (0.9, 0.88, 0.8), 0.7), 0, fr)
NC = [(0.6, 0.75, 0.6), (0.8, 0.5, 0.45), (0.5, 0.65, 0.8), (0.85, 0.75, 0.45), (0.7, 0.55, 0.7)]
for i in range(4):
    for j in range(5): cube(f"note_{i}{j}", (-0.42 + i * 0.28, -0.028, -0.3 + j * 0.15), (0.12, 0.004, 0.058), MT(f"bn{(i + j) % 5}", NC[(i + j) % 5], 0.6), 0, fr)
cube("fLogoB", (DX - 0.6, 3.13, 2.7), (0.5, 0.02, 0.5), MT("frameW", (0.95, 0.95, 0.93), 0.5), 0.005); disc_img("fLogo", (DX - 0.6, 3.1, 2.7), 0.45, img_mat("logoD", WEB + "LIBAN-SUR-SEINE-202.png", 0.25))
# green-framed window (left wall) with the Seine outside
GREENF = MT("greenF", (0.3, 0.5, 0.25), 0.5)
SKYM = MT("skyD", (0.5, 0.75, 1.0), 0.5, (0.45, 0.7, 1.0), 3.0)
cube("winSky", (DX - 5.04, 0.2, 2.3), (0.01, 1.5, 1.2), SKYM, 0)
for z in (1.1, 3.5): cube(f"winH{z}", (DX - 5.03, 0.2, z), (0.03, 1.56, 0.06), GREENF, 0)
for y in (-1.3, -0.3, 0.7, 1.7): cube(f"winV{y}", (DX - 5.03, y, 2.3), (0.03, 0.05, 1.2), GREENF, 0)
cube("winTrees", (DX - 5.035, 0.2, 1.45), (0.01, 1.5, 0.35), MT("treeD", (0.12, 0.35, 0.12), 0.8), 0)
# exit door (right wall) + SORTIE sign
cube("exitDoor", (DX + 5.04, -0.8, 1.25), (0.02, 0.6, 1.25), GREENF, 0.01)
EXITM = MT("exitG", (0.1, 0.9, 0.3), 0.4, (0.1, 1.0, 0.35), 4)
exitS = empty("exitSign", (DX + 5.0, -0.8, 2.85)); exitS.rotation_euler = (0, 0, math.radians(-90)); cube("exitB", (0, 0, 0), (0.42, 0.03, 0.14), EXITM, 0.01, exitS); txt("exitT", "SORTIE", (0, -0.035, 0), 0.15, WHITE, exitS, ext=0.004)
# plant
cyl("plantPot", (DX - 4.3, 2.4, 0.3), 0.26, 0.6, MT("potG", (0.35, 0.36, 0.38), 0.6))
for i in range(14):
    a = i * 0.45; o = cube(f"leaf{i}", (DX - 4.3 + 0.3 * math.cos(a), 2.4 + 0.3 * math.sin(a), 1.25 + 0.05 * (i % 4)), (0.03, 0.012, 0.75), MT("leafG", (0.12, 0.42, 0.14), 0.6), 0.01)
    o.rotation_euler = (math.radians(24 * math.sin(a)), math.radians(-24 * math.cos(a)), 0)
# tables + chairs
CLOTH = MT("cloth", (0.93, 0.93, 0.92), 0.75); LACE = MT("lace", (0.03, 0.03, 0.035), 0.8); GLASS = MT("glass", (0.85, 0.92, 0.95), 0.05, None, 0, 0.35); CHAIRM = MT("chairB", (0.03, 0.03, 0.035), 0.5)
PAMPA = MT("pampa", (0.85, 0.75, 0.6), 0.9)
def table(name, x, y, chairs=((0, 1),)):
    e = empty(name, (x, y, 0))
    cube(name + "c", (0, 0, 0.42), (0.52, 0.52, 0.42), CLOTH, 0.03, e); cube(name + "top", (0, 0, 0.845), (0.56, 0.56, 0.012), CLOTH, 0.01, e)
    cube(name + "lace", (0, 0, 0.86), (0.58, 0.14, 0.004), LACE, 0, e)
    for gx, gy in ((-0.3, -0.28), (0.3, 0.28)):
        cyl(f"{name}gs{gx}", (gx, gy, 0.95), 0.008, 0.16, GLASS, parent=e); sphere(f"{name}gb{gx}", (gx, gy, 1.09), 0.07, GLASS, (1, 1, 1.25), e); cyl(f"{name}gf{gx}", (gx, gy, 0.87), 0.05, 0.008, GLASS, parent=e)
    sphere(name + "vase", (0, 0, 0.93), 0.06, GLASS, (1, 1, 1.1), e); cyl(name + "stem", (0.01, 0, 1.12), 0.005, 0.34, PAMPA, (0, math.radians(8), 0), e)
    o = sphere(name + "pampa", (0.05, 0, 1.38), 0.06, PAMPA, (0.6, 0.6, 2.6), e); o.rotation_euler = (0, math.radians(14), 0)
    for (cx, cy) in chairs:
        c = empty(f"{name}ch{cx}{cy}", (cx * 0.95, cy * 0.95, 0)); c.parent = e; c.rotation_euler = (0, 0, math.atan2(-cx, cy) if (cx or cy) else 0)
        cube(c.name + "s", (0, 0, 0.5), (0.24, 0.24, 0.03), CHAIRM, 0.02, c); cube(c.name + "b", (0, 0.23, 0.85), (0.24, 0.025, 0.36), CHAIRM, 0.03, c)
        for lx in (-0.2, 0.2):
            for ly in (-0.2, 0.2): cyl(f"{c.name}l{lx}{ly}", (lx, ly, 0.25), 0.015, 0.5, IRON, parent=c)
    return e
table("tA", DX - 3.2, 1.3, ((0, 1), (-1, 0))); table("tB", DX - 0.4, 1.6, ((0, 1), (1, 0))); table("tC", DX - 3.5, -1.6, ((-1, 0),)); table("tD", DX + 3.3, -0.3, ((1, 0), (0, 1)))

# ---- exterior (x = EX): the restaurant on the bank of the Seine, by day
cube("eSky", (EX, 30, 12), (45, 0.1, 14), MT("eSkyM", (0.3, 0.55, 1.0), 0.5, (0.25, 0.5, 1.0), 1.3), 0)
for i in range(7): sphere(f"cloud{i}", (EX - 14 + i * 4.6 + random.uniform(-1, 1), 28, 9 + random.uniform(-2, 3)), 1.3, MT("cloud", (1, 1, 1), 0.9, (1, 1, 1), 0.9), (2.2 + random.random(), 0.5, 0.7))
cube("eGrass", (EX, 6, 0.02), (30, 9, 0.02), MT("grass", (0.2, 0.42, 0.14), 0.9), 0)
cube("eRiver", (EX, -9, 0.0), (40, 6, 0.01), MT("river", (0.1, 0.3, 0.42), 0.06), 0)
cube("eQuay", (EX, -2.6, 0.12), (30, 0.6, 0.12), MT("quay", (0.6, 0.57, 0.5), 0.8), 0)
cube("eBuild", (EX, 5, 2.4), (4.2, 2.2, 2.4), MT("eWall", (0.82, 0.74, 0.58), 0.85), 0.03)
cube("eRoof", (EX, 5, 5.0), (4.5, 2.5, 0.22), MT("roof", (0.3, 0.2, 0.16), 0.7), 0.05)
MT("eGlass", (0.2, 0.3, 0.35), 0.08)
for x in (-2.7, -0.9, 0.9, 2.7):
    if abs(x) < 1: cube(f"eDoor{x}", (EX + x, 2.78, 1.2), (0.6, 0.03, 1.2), GREENF, 0.01) if x > 0 else cube(f"eWinB{x}", (EX + x, 2.78, 1.7), (0.65, 0.03, 0.75), MT("eGlass", (0.2, 0.3, 0.35), 0.08), 0)
    else: cube(f"eWin{x}", (EX + x, 2.78, 1.7), (0.65, 0.03, 0.75), MT("eGlass"), 0)
    if not (abs(x) < 1 and x > 0):
        for dz in (-0.78, 0.78): cube(f"eWf{x}{dz}", (EX + x, 2.76, 1.7 + dz), (0.7, 0.04, 0.05), GREENF, 0)
        for dx in (-0.68, 0, 0.68): cube(f"eWv{x}{dx}", (EX + x + dx, 2.76, 1.7), (0.04, 0.04, 0.78), GREENF, 0)
disc_img("eLogo", (EX, 2.76, 3.75), 0.72, img_mat("logoX", WEB + "LIBAN-SUR-SEINE-202.png", 0.2)); cyl("eLogoB", (EX, 2.79, 3.75), 0.78, 0.03, WHITE, (math.radians(90), 0, 0))
txt("eSign", "LIBAN SUR SEINE", (EX, 2.74, 2.78), 0.3, MT("signG", (0.1, 0.4, 0.15), 0.5), ext=0.02)
for i, x in enumerate((-8.5, -6, 6, 8.5, -11.5, 11.5)):   # lime trees (promenade des Tilleuls)
    cyl(f"trunk{i}", (EX + x, 2.2 + (i % 2), 1.2), 0.16, 2.4, MT("trunk", (0.3, 0.2, 0.12), 0.8))
    for k in range(5): sphere(f"crown{i}{k}", (EX + x + random.uniform(-0.6, 0.6), 2.2 + (i % 2) + random.uniform(-0.5, 0.5), 3.0 + random.uniform(0, 1.2)), random.uniform(0.9, 1.3), MT("lime", (0.22, 0.5, 0.15), 0.8))

# ================= LIGHTS (each set only burns while it is on screen) =================
KL = [(light("kKey", "AREA", (-2.5, -5.5, 4.0), (0.6, 0.3, 1.4), 1, (1.0, 0.96, 0.9), 5), 520), (light("kFill", "AREA", (4.2, -5, 2.4), (0.6, 0.3, 1.4), 1, (0.8, 0.88, 1.0), 5), 180),
      (light("kTop", "AREA", (0.6, 0.8, 4.2), (0.6, 0.6, 0), 1, (1, 1, 1), 5), 230), (light("kRim", "AREA", (0.6, 2.4, 3.6), (0.6, 0.3, 1.6), 1, (1.0, 0.9, 0.8), 3), 150)]
DL = [(light("dKey", "AREA", (DX - 3, -6, 4.0), (DX, 0, 1.4), 1, (1.0, 0.9, 0.76), 6), 600), (light("dFill", "AREA", (DX + 4, -5.5, 2.4), (DX, 0, 1.4), 1, (0.85, 0.9, 1.0), 5), 190),
      (light("dTop", "AREA", (DX, 0.5, 4.4), (DX, 0.5, 0), 1, (1.0, 0.92, 0.8), 6), 230), (light("dBar", "POINT", (BX, 1.2, 2.7), None, 1, (1.0, 0.65, 0.3), 0.3), 120),
      (light("dWin", "AREA", (DX - 4.8, 0.2, 2.4), (DX, 0, 1.2), 1, (0.6, 0.8, 1.0), 2.5), 200)]
EL = [(light("eSun", "SUN", (EX - 10, -12, 14), (EX, 3, 1), 1, (1.0, 0.95, 0.85), 0.05), 2.4), (light("eFill", "AREA", (EX + 6, -9, 4), (EX, 3, 2), 1, (0.7, 0.85, 1.0), 10), 500)]
rageL = light("rageL", "POINT", (CP[0], CP[1] - 0.8, 2.5), None, 0, (1.0, 0.15, 0.08), 0.4)

# ================= FX =================
TRACK = []
def bubble(name, text, loc, w, h, t_on, t_off, ts=0.12, tail=-1, tm=None, track=False):
    e = empty(name, loc)
    cube(name + "b", (0, 0, 0), (w, 0.02, h), MT("bubW", (1, 1, 1), 0.5, (1, 1, 1), 0.35), min(h * 0.6, 0.07), e)
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
    while t < t1 - 0.2:
        sgn = 1 if k % 2 else -1
        note(t, (origin[0] + sgn * 0.22, origin[1], origin[2] + 0.05 * (k % 3)), sgn * spread * (0.6 + 0.4 * ((k * 7) % 5) / 4), rise, min(1.7, t1 - t), size); t += every; k += 1
def puffs(name, loc, t, n=3, dur=1.5, r=0.14, m=None):
    for i in range(n):
        p = sphere(f"{name}{i}", (0, 0, 0), r, m or PUFF)
        a = F(t + i * 0.12); b = F(t + i * 0.12 + dur); ox = (i - (n - 1) / 2) * r * 0.9
        key(p, 1, scale=(0, 0, 0)); key(p, a - 1, loc=(loc[0] + ox, loc[1], loc[2]), scale=(0, 0, 0))
        key(p, a + 6, scale=(1, 1, 1)); key(p, b, loc=(loc[0] + ox * 1.8, loc[1], loc[2] + 0.7), scale=(0, 0, 0))
QM = MT("qm", (1, 0.8, 0.1), 0.4, (1.0, 0.8, 0.1), 6)
def qmark(name, t_on, t_off, loc, size=0.34, body="?", m=None):
    e = empty(name, loc); txt(name + "t", body, (0, 0, 0), size, m or QM, e, ext=0.03)
    a, b = F(t_on), F(t_off)
    key(e, 1, scale=(0, 0, 0)); key(e, a - 1, scale=(0, 0, 0), rot=(0, -20, 0)); key(e, a + 4, scale=(1.25,) * 3, rot=(0, 12, 0)); key(e, a + 8, scale=(1, 1, 1), rot=(0, 0, 0))
    key(e, b - 3, scale=(1, 1, 1), rot=(0, 8, 0)); key(e, b, scale=(0, 0, 0))
    return e
def steam(t0, t1, at, every=0.4):
    t = t0; k = 0
    while t < t1 - 0.5:
        puffs(f"stm{at[0]:.1f}{t:.2f}", (at[0] + (-0.25 if k % 2 else 0.25), at[1], at[2]), t, 2, min(0.9, t1 - t), 0.1); t += every; k += 1
STARM = MT("starY", (1, 0.85, 0.2), 0.4, (1.0, 0.82, 0.15), 8)
def dizzy(name, head, t0, t1, n=4, r=0.42, z=0.78):
    piv = empty(name, (0, 0, z)); piv.parent = head
    for i in range(n):
        a = 2 * math.pi * i / n; bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.07, depth=0.03, location=(0, 0, 0)); o = bpy.context.object; give(o, STARM); o.parent = piv
        o.location = (r * math.cos(a), r * math.sin(a), 0); o.rotation_euler = (math.radians(70), 0, a)
    a, b = F(t0), F(t1)
    key(piv, 1, scale=(0, 0, 0)); key(piv, a - 1, scale=(0, 0, 0)); key(piv, a + 3, scale=(1, 1, 1)); key(piv, b - 2, scale=(1, 1, 1)); key(piv, b, scale=(0, 0, 0))
    piv.rotation_euler = (0, 0, 0); piv.keyframe_insert("rotation_euler", frame=a); piv.rotation_euler = (0, 0, math.radians(360 * (t1 - t0) * 1.2)); piv.keyframe_insert("rotation_euler", frame=b); LIN.append(piv)
LIN = [hH, hM]
def chef_red(t, v):
    col_key(CHEAD, F(t), (0.62 + 0.3 * v, 0.36 - 0.3 * v, 0.22 - 0.18 * v)); lkey(rageL, F(t), 150 * v)

# ---- props carried by the cast
tray = empty("tray", (0, -0.12, -0.6)); tray.parent = YA.armL; tray.rotation_euler = (math.radians(79), 0, 0); cyl("trayD", (0, 0, 0), 0.3, 0.02, IRON, parent=tray); bowl("trH", (-0.1, 0.05, 0.01), 0.11, HUM, tray); bowl("trT", (0.12, -0.06, 0.01), 0.1, TAB, tray)
ticket = cube("ordTicket", (0, -0.1, -0.68), (0.07, 0.004, 0.11), WHITE, 0, YA.armR)
rag = cube("rag", (0, -0.05, -0.66), (0.11, 0.09, 0.02), MT("rag", (0.3, 0.6, 0.85), 0.9), 0.015, YA.armR)
stackY = empty("stackY", (0, -0.14, -0.6)); stackY.parent = YA.armL; stackY.rotation_euler = (math.radians(78), 0, 0)
for i in range(7): plate(f"sy{i}", PK, (0, 0, i * 0.022), stackY)
knife = empty("knife", (0, -0.1, -0.62)); knife.parent = KA.armR; cube("knifeB", (0, -0.14, 0), (0.02, 0.13, 0.004), STEEL, 0, knife); cube("knifeH", (0, 0.04, 0), (0.018, 0.06, 0.012), IRON, 0.005, knife)
ladle = empty("ladle", (0, -0.05, -0.6)); ladle.parent = CH.armR; cyl("ladleS", (0, 0, -0.2), 0.012, 0.5, STEEL, parent=ladle); sphere("ladleB", (0, 0, -0.47), 0.07, STEEL, (1, 1, 0.6), ladle)
duck = empty("duck", (0, -0.06, -0.72)); duck.parent = B.armR; DUK = MT("duckY", (1.0, 0.82, 0.1), 0.35)
sphere("duckB", (0, 0, 0), 0.13, DUK, (1.0, 1.25, 0.85), duck); sphere("duckH", (0, -0.1, 0.14), 0.09, DUK, parent=duck)
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.04, depth=0.09, location=(0, 0, 0)); o = bpy.context.object; give(o, MT("beak", (1.0, 0.4, 0.05), 0.4)); o.parent = duck; o.location = (0, -0.2, 0.13); o.rotation_euler = (math.radians(90), 0, 0)
for sx in (-1, 1): sphere(f"duckE{sx}", (sx * 0.045, -0.165, 0.18), 0.016, DARK, parent=duck)
duck.rotation_euler = (math.radians(180), 0, 0)
egg = empty("egg", (0, -0.02, 0.66)); egg.parent = CH.head; sphere("eggW", (0, 0, 0), 0.16, WHITE, (1.1, 0.95, 0.16), egg); sphere("eggY", (0.02, -0.01, 0.025), 0.055, MT("yolk", (1.0, 0.65, 0.05), 0.3), (1, 1, 0.6), egg)
vis(tray, [(F(T_DIN0), F(T_KW)), (F(T_Y1), F(T_Y2))]); vis(ticket, [(F(T_KW), F(T_Y1)), (F(T_Y2), F(T_Y4))]); vis(rag, [(F(T_V2), F(T_V3))]); vis(stackY, [(F(T_M4), F(T_R2))])
vis(duck, [(F(T_Z1 + 2.0), F(T_Z2))]); vis(egg, [(F(T_V1 + 0.8), F(T_V2))]); vis(sponge, [(1, F(T_Z1 + 1.2)), (F(T_Z2), None)])
# globe (z3)
globe = empty("globe", (DX, -0.7, 1.55)); sphere("globeS", (0, 0, 0), 0.5, MT("ocean", (0.1, 0.35, 0.75), 0.3), parent=globe)
for i in range(16):
    th = random.uniform(0, 6.28); ph = random.uniform(0.5, 2.5); sphere(f"land{i}", (0.47 * math.sin(ph) * math.cos(th), 0.47 * math.sin(ph) * math.sin(th), 0.47 * math.cos(ph)), random.uniform(0.09, 0.17), MT("land", (0.2, 0.55, 0.2), 0.7), (1, 1, 0.6), globe)
cyl("globeSt", (0, 0, -0.75), 0.03, 0.5, IRON, parent=globe); cyl("globeBs", (0, 0, -1.0), 0.22, 0.04, IRON, parent=globe); cube("globeTb", (0, 0, -1.29), (0.3, 0.3, 0.27), CLOTH, 0.03, globe)
PINL = (-0.2, -0.44, 0.14); PINB = (0.24, -0.43, 0.06)
for nm, p, fl in (("pinL", PINL, flag_lb), ("pinB", PINB, flag_bd)):
    pe = empty(nm, p); pe.parent = globe; cyl(nm + "s", (0, 0, 0.22), 0.008, 0.44, IRON, parent=pe); sphere(nm + "d", (0, 0, 0), 0.03, MT("flagR"), parent=pe)
    f_ = fl(nm + "f", (0.11 if nm == "pinB" else -0.11, -0.005, 0.37), pe, 0.11, 0.075)
    a = F(T_Z3 + (0.5 if nm == "pinL" else 1.9)); key(pe, 1, scale=(0, 0, 0)); key(pe, a - 1, scale=(0, 0, 0)); key(pe, a + 4, scale=(1.3,) * 3); key(pe, a + 8, scale=(1, 1, 1))
for i in range(9):
    u = (i + 1) / 10; p = [PINL[k] + (PINB[k] - PINL[k]) * u for k in range(3)]; p[1] -= 0.05; p[2] += 0.16 * math.sin(u * math.pi)
    d = sphere(f"arc{i}", tuple(p), 0.014, WHITE, parent=globe); a = F(T_Z3 + 2.2 + i * 0.06); key(d, 1, scale=(0, 0, 0)); key(d, a - 1, scale=(0, 0, 0)); key(d, a + 2, scale=(1, 1, 1)); SNAP.append(d)
vis(globe, [(F(T_Z3), F(T_Z4))])

# ================= ACTING =================
def P(c, t, loc, rz=0, head=(0, 0, 0), L=(0, 6), Rr=(0, -6), ey=1.0, br=0.0, tilt=0.0, sc=(1, 1, 1), lean=0):
    c.R(t, loc, rz, sc, lean); c.H(t, head); c.A(t, L, Rr); c.face(t, ey, br, tilt); c.LG(t, 0, 0)
def off(c, t): c.R(t, PARK, 0)
def bob(c, t0, t1, loc, rz=0, per=0.5, amp=0.035, sway=0.0, lean=0):
    n = int(round((t1 - t0) / per))
    for i in range(n + 1):
        t = t0 + i * per; sg = 1 if i % 2 else -1
        c.R(t, (loc[0] + sway * sg, loc[1], loc[2]), rz, tilt=lean); c.R(t + per * 0.5, (loc[0], loc[1], loc[2] + amp), rz, tilt=lean) if i < n else None
def wash(t0, t1, per=0.8):
    t = t0; k = 0
    while t < t1: B.A(t, (-58 + (8 if k % 2 else -8), -16), (-58 + (-8 if k % 2 else 8), 16)); t += per / 2; k += 1
def chop(t0, t1, per=0.3):
    t = t0; k = 0
    while t < t1: KA.A(t, (-42, -14), (-50 if k % 2 else -78, 12)); t += per / 2; k += 1
def stir(t0, t1, per=0.9):
    t = t0; k = 0
    while t < t1: CH.A(t, (-10, 8), (-62 + (10 if k % 2 else -10), 14 if k % 2 else -8)); t += per / 2; k += 1
def dance(c, t0, t1, loc, rz=0, ph=0, big=1.0, hand=True):
    """seamless 2 s loop: step-touch + arm pumps"""
    n = int(round((t1 - t0) / 0.5))
    for i in range(n + 1):
        t = t0 + i * 0.5; k = (i + ph) % 4; sg = 1 if k in (0, 1) else -1; up = k % 2
        c.R(t, (loc[0] + 0.12 * sg * big, loc[1], loc[2]), rz + 8 * sg, tilt=0)
        if i < n: c.R(t + 0.25, (loc[0] + 0.12 * sg * big, loc[1], loc[2] + 0.07 * big), rz + 8 * sg)
        c.H(t, (-4 if up else 4, 10 * sg, 0))
        if hand: c.A(t, (-150 * big, 20) if up else (-40, 25), (-40, -25) if up else (-150 * big, -20))
        c.LG(t, 14 * sg, -14 * sg)
YRZ = -62
# ---------- park everyone, opening ----------
for c in CAST: P(c, 1, PARK)
clock_at(0, 12.0); clock_at(T_V1 - 0.1, 14.5); clock_at(T_V1, 22.4); clock_at(T_Z2 - 0.1, 22.6); clock_at(T_Z2, 22.6); clock_at(T_Z3, 25.6); clock_at(T_END, 25.6)
# 5.5 dining: Yasser crosses with a tray
YA.walk(T_DIN0, T_KW - 0.1, (DX - 3.4, -0.6, 0), (DX + 1.6, -1.1, 0), rz=58, step=0.28)
YA.A(T_DIN0, (-78, -30), (10, -8)); YA.H(T_DIN0, (0, 0, -40)); YA.H(T_DIN0 + 2.5, (0, 0, -55)); YA.face(T_DIN0, 1, 0.01)
# 10.5 kitchen wide: everyone at work, Yasser arrives at the pass with a ticket
P(B, T_KW, BP, 0, (-8, 0, 0)); wash(T_KW, T_Y1)
P(KA, T_KW, KP, 0, (-14, 0, 0)); chop(T_KW, T_Y1)
P(CH, T_KW, CP, -160, (0, 0, 0)); stir(T_KW, T_Y1); CH.R(T_KW + 3.0, CP, -160); CH.R(T_KW + 3.6, CP, -25); CH.H(T_KW + 3.6, (0, 0, -20)); CH.face(T_KW + 3.6, 0.8, -0.012, 10)
YA.walk(T_KW, T_KW + 2.4, (5.6, -1.6, 0), YP, rz=YRZ, step=0.3); YA.A(T_KW, (0, 6), (-60, 0)); YA.H(T_KW, (0, 0, 0)); YA.A(T_KW + 2.6, (0, 6), (-100, 0)); YA.A(T_KW + 3.2, (0, 6), (-80, 0)); YA.A(T_KW + 3.8, (0, 6), (-100, 0)); YA.A(T_KW + 4.6, (0, 6), (-85, 0))
YA.talk(T_KW + 2.5, T_KW + 4.6)
# 15.4 y1: Yasser runs through the dining room, singing
P(YA, T_Y1, (DX - 2.2, -1.6, 0), 0)
YA.walk(T_Y1, T_Y1 + 2.3, (DX - 2.2, -1.6, 0), (DX + 1.0, -1.8, 0), rz=28, step=0.2, bob=0.06, swing=34)
YA.walk(T_Y1 + 2.3, T_Y2 - 0.05, (DX + 1.0, -1.8, 0), (DX - 1.6, -2.2, 0), rz=-30, step=0.2, bob=0.06, swing=34)
YA.A(T_Y1, (-80, -28), (-30, -10)); YA.A(T_Y1 + 1.2, (-80, -28), (-120, -30)); YA.A(T_Y1 + 2.3, (-80, -28), (-40, -10)); YA.A(T_Y1 + 3.6, (-80, -28), (-125, -30)); YA.A(T_Y2 - 0.1, (-80, -28), (-40, -10))
YA.H(T_Y1, (0, 0, -22)); YA.H(T_Y1 + 2.3, (0, 0, 24)); YA.face(T_Y1, 1, 0.012)
# 20.3 y2: at the pass, the order -> Kartik
P(YA, T_Y2, YP, YRZ, (0, 0, 8), (0, 6), (-95, 0), br=0.01)
for i in range(7): YA.AR(T_Y2 + 0.4 + i * 0.5, (-105 if i % 2 else -85, 0))
bob(YA, T_Y2, T_Y4, YP, YRZ, 0.5, 0.03)
P(KA, T_Y2, KP, 42, (0, 0, 0), (-20, 4), (-20, -4), br=0.015); KA.H(T_Y2 + 1.2, (0, 0, 14)); KA.H(T_Y2 + 2.2, (0, 0, -8)); KA.H(T_Y2 + 3.0, (0, 0, 10)); KA.face(T_Y2 + 1.5, 1, 0.03, -8)
P(B, T_Y2, BP, 0, (-8, 0, 0)); wash(T_Y2, T_Y4)
P(CH, T_Y2, CP, -160); stir(T_Y2, T_CA)
bubble("bY2", "2 MEZZÉS !\n1 CHICH TAOUK !", (2.9, -0.6, 3.35), 0.86, 0.3, T_Y2 + 0.5, T_Y3 - 0.1, 0.15, 1)
# 24.1 y3: Kartik answers in English
P(KA, T_Y3, KP, 30, (0, 0, 0), (-20, 4), (-20, -4), br=0.03)
for i in range(3): KA.A(T_Y3 + 0.5 + i * 1.1, (-55, 55), (-55, -55)); KA.A(T_Y3 + 1.0 + i * 1.1, (-35, 35), (-35, -35))
KA.H(T_Y3 + 0.5, (4, 0, 12)); KA.H(T_Y3 + 1.6, (4, 0, -10)); KA.H(T_Y3 + 2.7, (4, 0, 10)); KA.talk(T_Y3 + 1.6, T_Y4 - 0.2); KA.R(T_Y3 + 0.5, (KP[0], KP[1], 0.05), 30); KA.R(T_Y3 + 1.0, KP, 30)
P(YA, T_Y3, YP, YRZ, (0, 0, 8), (0, 6), (-60, 0)); YA.AR(T_Y3 + 2.0, (-60, 0)); YA.AR(T_Y3 + 2.5, (-150, 42)); YA.H(T_Y3 + 2.5, (-14, 0, 8)); YA.EY(T_Y3 + 2.5, 0.1)
bubble("bY3", "SORRY…\nNO FRENCH !", (0.2, 0.2, 2.95), 0.62, 0.3, T_Y3 + 1.4, T_Y4 - 0.1, 0.15, 1)
# 28.0 y4: Narayan (Boulon) only understands Bengali
P(B, T_Y4, BP, 0, (0, 0, 0), (-20, -10), (-20, 10), br=0.02); B.A(T_Y4 + 0.6, (-70, -62), (-70, 62)); B.H(T_Y4 + 0.6, (6, 0, 0)); B.nod(T_Y4 + 2.0, 3, (6, 0, 0), 0.5, 10)
bubble("bBn1", None, (BP[0] + 0.72, 0.2, 3.02), 0.62, 0.24, T_Y4 + 0.7, T_CA - 0.1, tail=-1, track=True)
P(KA, T_Y4, KP, -38, (0, 0, 0), (-20, 4), (-20, -4), br=0.02)
# ---------- chorus (32–56, reused twice) ----------
P(B, T_CA, BP, 0, (0, 0, 0), (-25, -12), (-25, 12), br=0.03); B.nod(T_CA + 0.1, 8, (0, 0, 0), 0.5, 22)
for i, (t, x, z) in enumerate([(T_CA + 0.6, -0.75, 2.6), (T_CA + 1.4, 0.75, 2.75), (T_CA + 2.2, -0.2, 3.05)]): qmark(f"q{i}", t, T_CA2 - 0.1, (BP[0] + x, BP[1] - 0.4, z), 0.36)
P(KA, T_CA, KP, -40, (0, 0, 0), (-20, 4), (-20, -4))
# 36: Yasser + Kartik explain, Boulon nods at everything
P(YA, T_CA2, (1.7, 0.55, 0), -48, (0, 0, 0), (-70, 20), (-95, 0), br=0.01); P(KA, T_CA2, KP, -42, (0, 0, 0), (-80, 10), (-40, -10), br=0.01)
for i in range(4):
    YA.A(T_CA2 + i, (-70, 20), (-95, 0)); YA.A(T_CA2 + i + 0.5, (-110, 10), (-60, -10)); KA.A(T_CA2 + i, (-85, 10), (-40, -10)); KA.A(T_CA2 + i + 0.5, (-50, 10), (-95, -10))
YA.talk(T_CA2 + 0.2, T_CB - 0.3); KA.talk(T_CA2 + 0.4, T_CB - 0.3)
P(B, T_CA2, BP, 30, (0, 0, 0), (-25, -12), (-25, 12), br=0.03); B.nod(T_CA2 + 0.1, 8, (0, 0, 0), 0.5, 22)
bubble("bCa1", "VITE !", (1.7, 0.1, 3.3), 0.42, 0.19, T_CA2 + 0.4, T_CB - 0.2, 0.17, -1); bubble("bCa2", "QUICK !", (0.55, 0.1, 2.95), 0.5, 0.19, T_CA2 + 1.2, T_CB - 0.2, 0.17, -1)
qmark("q4", T_CA2 + 1.8, T_CB - 0.1, (BP[0] - 0.45, BP[1] - 0.4, 2.75), 0.36)
# 40: the chef explodes
P(CH, T_CB, CP, -12, (0, 0, 0), (-20, 10), (-150, -15), 0.75, -0.025, 16); chef_red(T_CB, 0.0); chef_red(T_CB + 0.9, 1.0); chef_red(T_CC - 0.1, 1.0); chef_red(T_CC, 0.0)
for i in range(8): CH.AR(T_CB + 0.25 + i * 0.5, (-165 if i % 2 else -120, -15)); CH.H(T_CB + 0.25 + i * 0.5, (-6, 6 if i % 2 else -6, 0)); CH.R(T_CB + 0.25 + i * 0.5, (CP[0] + (0.04 if i % 2 else -0.04), CP[1], 0), -12)
CH.talk(T_CB + 0.2, T_CC - 0.2, 0.14, 1.0); steam(T_CB + 0.6, T_CC, (CP[0], CP[1], 2.45))
bubble("bAr1", None, (CP[0] - 0.75, CP[1] - 0.5, 3.0), 0.46, 0.2, T_CB + 0.7, T_CB2 - 0.05, tail=1, track=True)
P(YA, T_CB, YP, YRZ, (0, 0, 20)); P(KA, T_CB, KP, 0, (0, 0, -30)); P(B, T_CB, BP, 0, (0, 0, 0), (-25, -12), (-25, 12), br=0.03)
# 42: wide — Yasser and Kartik duck, Boulon keeps nodding
P(YA, T_CB2, YP, YRZ, (0, 0, 30), (-150, -30), (-150, 30), 1, 0.04); YA.R(T_CB2 + 0.5, (YP[0], YP[1], -0.55), YRZ); YA.R(T_CC - 0.1, (YP[0], YP[1], -0.55), YRZ)
P(KA, T_CB2, KP, 0, (0, 0, -30), (-150, -30), (-150, 30), 1, 0.04); KA.R(T_CB2 + 0.4, (KP[0], KP[1], -0.7), 0); KA.R(T_CC - 0.1, (KP[0], KP[1], -0.7), 0)
B.nod(T_CB2, 4, (0, 0, 0), 0.5, 22)
# 44: Lebanese dishes on the pass, Bengali song on the radio
notes(T_CC + 0.1, T_CC2, (1.75, -0.1, 1.45), 0.33, 0.5, 0.9, 0.9)
for i in range(8): key(radio, F(T_CC + i * 0.25), scale=(1, 1, 1.08 if i % 2 else 0.95))
key(radio, F(T_CC2), scale=(1, 1, 1))
# 46: Boulon dances at the sink
dance(B, T_CC2, T_CI, BP, 0, 0, 0.8); notes(T_CC2, T_CI, (BP[0], BP[1] - 0.3, 2.5), 0.4, 0.7, 0.9)
B.face(T_CC2, 0.5, 0.03)
# 48: instrumental — the whole kitchen grooves (the chef refuses)
dance(B, T_CI, T_CD, BP, 0, 0, 0.8); P(KA, T_CI, KP, 0); dance(KA, T_CI, T_CD, KP, 0, 1); P(YA, T_CI, YP, YRZ); dance(YA, T_CI, T_CD, YP, YRZ + 20, 2)
P(CH, T_CI, CP, -12, (0, 0, 0), (-62, -52), (-62, 52), 0.7, -0.02, 14)
for i in range(8): CH.H(T_CI + i * 0.5, (0, 0, 16 if i % 2 else -16))
KA.face(T_CI, 1, 0.01); YA.face(T_CI, 1, 0.01); B.face(T_CI, 1, 0.02)
notes(T_CI, T_CD, (0.6, 0.3, 2.9), 0.4, 1.2, 0.9)
# 52: "we'll go crazy"
P(YA, T_CD, (1.45, -1.5, 0), -14, (0, 0, 0), (-150, -32), (-150, 32), 0.6, 0.04, -10); P(KA, T_CD, (0.3, -1.5, 0), 14, (0, 0, 0), (-150, -32), (-150, 32), 0.6, 0.04, -10)
for i in range(8):
    for c, s_ in ((YA, 1), (KA, -1)): c.H(T_CD + i * 0.5, (0, 14 * s_ * (1 if i % 2 else -1), 12 * (1 if i % 2 else -1)))
dizzy("dzY", YA.head, T_CD + 0.2, T_DANCE - 0.05); dizzy("dzK", KA.head, T_CD + 0.2, T_DANCE - 0.05)
P(B, T_CD, BP, 0, (0, 0, 0), (-25, -12), (-25, 12)); B.nod(T_CD, 8, (0, 0, 0), 0.5, 20)
# ---------- 56–64 dance break in the dining room (seamless loop, reused) ----------
DY, DK, DB = (DX - 1.1, -1.4, 0), (DX, -1.0, 0), (DX + 1.15, -1.4, 0)
for c, p, ph in ((YA, DY, 0), (KA, DK, 2), (B, DB, 0)):
    P(c, T_DANCE, p, 0); dance(c, T_DANCE, T_V1, p, 0, ph); c.face(T_DANCE, 1, 0.02)
P(CH, T_DANCE, (DX + 2.6, 0.9, 0), -30, (0, 0, 0), (-62, -52), (-62, 52), 0.7, -0.02, 14)
for i in range(17): CH.H(T_DANCE + i * 0.5, (-6 if i % 2 else 2, 0, 0))
notes(T_DANCE, T_V1 - 0.05, (DX, -1.2, 2.7), 0.5, 1.4, 0.9)
# ---------- verse 2 ----------
# 64: end of the day, the chef's head is boiling
P(CH, T_V1, CP, -8, (0, 0, 0), (-62, -52), (-62, 52), 0.7, -0.025, 16); chef_red(T_V1, 0.2); chef_red(T_V1 + 1.2, 1.0); chef_red(T_V2 - 0.1, 1.0); chef_red(T_V2, 0)
steam(T_V1 + 0.3, T_V2, (CP[0], CP[1], 2.5), 0.3)
for i in range(8): CH.R(T_V1 + i * 0.5, (CP[0] + (0.02 if i % 2 else -0.02), CP[1], 0), -8)
key(egg, F(T_V1 + 0.8), rot=(0, 0, 0));
for i in range(10): key(egg, F(T_V1 + 1.0 + i * 0.3), rot=(0, 0, 8 if i % 2 else -8))
for c in (YA, KA): off(c, T_V1)
P(B, T_V1, BP, 0, (-8, 0, 0)); wash(T_V1, T_V2)
# 68.2: finish fast and run — Yasser wipes a table, eyes on the exit
YW = (DX + 2.2, -0.35, 0)
P(YA, T_V2, YW, 55, (0, 0, 0), (0, 6), (-62, 0), 1, 0.02);
for i in range(16): YA.AR(T_V2 + i * 0.22, (-62, 32 if i % 2 else -24))
YA.H(T_V2, (-10, 0, 0)); YA.H(T_V2 + 1.3, (-10, 0, 0)); YA.H(T_V2 + 1.6, (0, 0, -70)); YA.H(T_V2 + 2.5, (0, 0, -70)); YA.H(T_V2 + 2.8, (-10, 0, 0)); YA.H(T_V2 + 3.3, (0, 0, -70))
for i in range(9): emis_key(EXITM, F(T_V2 + i * 0.45), 9 if i % 2 else 3)
for c in (KA, CH, B): off(c, T_V2)
# 72.2: the chain — Yasser tells Kartik, Kartik tells Narayan
YC = (1.7, 0.55, 0)
P(YA, T_V3, YC, -48, (0, 0, 0), (0, 6), (-95, 10)); YA.talk(T_V3 + 0.2, T_V3 + 1.8); YA.AR(T_V3 + 0.6, (-105, 10)); YA.AR(T_V3 + 1.0, (-90, 30)); YA.AR(T_V3 + 1.5, (-100, 40)); YA.AR(T_V3 + 2.2, (-20, -6))
P(KA, T_V3, KP, 40, (0, 0, 0), (-20, 4), (-20, -4)); KA.nod(T_V3 + 0.8, 2, (0, 0, 0), 0.4, 10); KA.R(T_V3 + 1.7, KP, 40); KA.R(T_V3 + 2.1, KP, -42); KA.A(T_V3 + 2.1, (-20, 4), (-20, -4)); KA.A(T_V3 + 2.4, (-95, 10), (-30, -8)); KA.talk(T_V3 + 2.2, T_V4 - 0.3)
P(B, T_V3, BP, 0, (-8, 0, 0)); wash(T_V3, T_V3 + 2.3); B.R(T_V3 + 2.2, BP, 0); B.R(T_V3 + 2.6, BP, 30); B.H(T_V3 + 2.6, (0, 0, 0)); B.A(T_V3 + 2.6, (-25, -12), (-25, 12)); B.H(T_V3 + 3.0, (0, 12, 0)); B.face(T_V3 + 2.8, 1, 0.03)
P(CH, T_V3, CP, -160); stir(T_V3, T_R1)
bubble("bV3a", "DIS-LUI !", (1.7, 0.1, 3.3), 0.56, 0.19, T_V3 + 0.3, T_V3 + 2.0, 0.17, -1); bubble("bV3b", "HURRY UP !", (0.5, 0.1, 2.95), 0.66, 0.19, T_V3 + 2.3, T_V4 - 0.1, 0.17, -1)
qmark("q5", T_V3 + 2.9, T_V4 - 0.1, (BP[0] - 0.5, BP[1] - 0.4, 2.75), 0.36)
# 76: "finish fast, get ready" — Kartik taps his wrist, Boulon says yes yes and keeps his pace
P(KA, T_V4, KP, -42, (0, 0, 0), (-95, -30), (-80, 30))
for i in range(7): KA.AR(T_V4 + 0.3 + i * 0.5, (-92 if i % 2 else -75, 40))
KA.talk(T_V4 + 0.2, T_V4 + 2.0)
P(B, T_V4, BP, 30, (0, 0, 0), (-25, -12), (-25, 12), br=0.03); B.nod(T_V4 + 0.6, 4, (0, 0, 0), 0.45, 20); B.R(T_V4 + 2.4, BP, 30); B.R(T_V4 + 2.8, BP, 0); B.H(T_V4 + 2.8, (-8, 0, 0)); wash(T_V4 + 2.8, T_R1, 1.6)
bubble("bBn2", None, (BP[0] - 0.7, 0.2, 2.95), 0.5, 0.2, T_V4 + 0.7, T_V4 + 2.7, tail=1, track=True)
off(YA, T_V4)
# ---------- 104–112 service montage ----------
P(CH, T_M1, (2.75, 1.45, 0), -180, (0, 0, 0), (-10, 8), (-70, 0));
for i in range(5): key(pan, F(T_M1 + i * 0.4), loc=(2.75, 2.2, 0.99 + (0.14 if i % 2 else 0)), rot=(0, -14 if i % 2 else 0, 0)); CH.AR(T_M1 + i * 0.4, (-80 if i % 2 else -62, 0))
key(pan, F(T_M2), loc=(2.75, 2.2, 0.99), rot=(0, 0, 0))
for i, fl in enumerate(flames):
    key(fl, 1, scale=(0, 0, 0)); key(fl, F(T_M1) - 1, scale=(0, 0, 0))
    for k in range(9): key(fl, F(T_M1 + k * 0.22), scale=(1, 1, (1.2 + 1.3 * (((k + i) * 7) % 5) / 4) if k else 0.2))
    key(fl, F(T_M2), scale=(0, 0, 0))
lkey(flameL, 1, 0); lkey(flameL, F(T_M1) - 1, 0); lkey(flameL, F(T_M1 + 0.2), 500); lkey(flameL, F(T_M2) - 1, 420); lkey(flameL, F(T_M2), 0)
for c in (YA, KA, B): off(c, T_M1)
P(KA, T_M2, KP, 0, (-14, 0, 0)); chop(T_M2, T_M3, 0.2); P(CH, T_M2, CP, -160); stir(T_M2, T_M4)
P(B, T_M3, BP, 0, (-8, 0, 0)); wash(T_M3, T_M4, 0.4)
for i in range(6): puffs(f"mf{i}", (BP[0] + random.uniform(-0.3, 0.3), -0.25, 1.1), T_M3 + 0.2 + i * 0.28, 1, 0.8, 0.07, FOAM)
P(YA, T_M4, (DX - 3, -1.2, 0), 60, (0, 0, -45), (-78, -30), (10, -8)); YA.walk(T_M4, T_R2 - 0.05, (DX - 3, -1.2, 0), (DX + 2.5, -1.6, 0), rz=62, step=0.2, bob=0.05, swing=32)
for c in (KA, CH, B): off(c, T_M4)
# ---------- verse 3 ----------
# 128: we say one thing, he hears another (a plate → a rubber duck)
YZ = (0.35, 0.55, 0)
P(YA, T_Z1, YZ, -50, (0, 0, 0), (0, 6), (-95, 10)); YA.talk(T_Z1 + 0.2, T_Z1 + 1.5); YA.AR(T_Z1 + 0.6, (-105, 0)); YA.AR(T_Z1 + 1.0, (-90, 10)); YA.AR(T_Z1 + 2.4, (-90, 10)); YA.AR(T_Z1 + 2.9, (-150, 42)); YA.H(T_Z1 + 2.9, (-14, 0, 0)); YA.EY(T_Z1 + 2.9, 0.1)
P(B, T_Z1, BP, 34, (0, 0, 0), (-25, -12), (-25, 12), br=0.03); B.nod(T_Z1 + 0.5, 2, (0, 0, 0), 0.4, 20)
B.R(T_Z1 + 1.3, BP, 34); B.R(T_Z1 + 1.6, (BP[0], BP[1], -0.9), 34); B.R(T_Z1 + 2.05, (BP[0], BP[1], -0.9), 34); B.R(T_Z1 + 2.4, BP, 34); B.AR(T_Z1 + 2.05, (-25, 12)); B.AR(T_Z1 + 2.5, (-165, -10)); B.face(T_Z1 + 2.5, 1, 0.04)
for i in range(4): B.AR(T_Z1 + 2.8 + i * 0.3, (-165, -22 if i % 2 else 2))
bubble("bZ1", "UNE ASSIETTE !", (0.45, 0.1, 3.3), 0.8, 0.19, T_Z1 + 0.3, T_Z1 + 2.3, 0.15, -1)
bubble("bBn3", None, (BP[0] - 0.75, 0.2, 2.2), 0.42, 0.2, T_Z1 + 2.7, T_Z2 - 0.1, tail=1, track=True)
for c in (KA, CH): off(c, T_Z1)
# 132.2: that's how our day goes — everybody flat out, the clock races
P(B, T_Z2, BP, 0, (-8, 0, 0)); wash(T_Z2, T_Z3, 0.3); P(KA, T_Z2, KP, 0, (-14, 0, 0)); chop(T_Z2, T_Z3, 0.18); P(CH, T_Z2, CP, -160); stir(T_Z2, T_Z3, 0.35)
YA.walk(T_Z2, T_Z2 + 1.3, (5.6, -1.6, 0), YP, rz=YRZ, step=0.18); YA.A(T_Z2, (0, 6), (-60, 0)); YA.H(T_Z2, (0, 0, 0)); YA.walk(T_Z2 + 1.7, T_Z2 + 2.8, YP, (5.8, -1.6, 0), rz=100, step=0.18); YA.walk(T_Z2 + 2.9, T_Z3 - 0.05, (5.8, -1.6, 0), YP, rz=YRZ, step=0.18)
# 136.3: where is Lebanon, where is Bangladesh
P(CH, T_Z3, (DX - 1.15, -0.5, 0), 30, (0, 0, 0), (0, 6), (-20, -6), 1, 0.0, 0); CH.AR(T_Z3 + 0.5, (-100, 30)); CH.face(T_Z3 + 0.5, 1, 0.02); CH.MO(T_Z3 + 0.6, 0.3, 1.2)
P(KA, T_Z3, (DX + 1.2, -0.5, 0), -30, (0, 0, 0), (-20, 6), (0, -6)); KA.AL(T_Z3 + 1.9, (-100, -30)); KA.MO(T_Z3 + 2.0, 0.5, 1.2); KA.face(T_Z3 + 1.9, 1, 0.02)
key(globe, F(T_Z3), rot=(0, 0, -25)); key(globe, F(T_Z4), rot=(0, 0, 25))
for c in (YA, B): off(c, T_Z3)
# 140: all together, the day is done
LINE = [(YA, DX - 1.65), (KA, DX - 0.55), (CH, DX + 0.55), (B, DX + 1.65)]
for c, x in LINE:
    P(c, T_Z4, (x, -1.2, 0), 0, (0, 0, 0), (0, 40), (0, -40), 1, 0.02); c.A(T_Z4 + 0.8, (0, 62), (0, -62))
    for i in range(6): c.R(T_Z4 + 0.9 + i * 0.5, (x, -1.2, 0.09 if i % 2 == 0 else 0), 0); c.A(T_Z4 + 0.9 + i * 0.5, (-160, 25) if i % 2 == 0 else (0, 62), (-160, -25) if i % 2 == 0 else (0, -62))
CH.face(T_Z4, 1, 0.02); CH.MO(T_Z4, 0.4, 1.25)
# ---------- 168 outro: goodnight ----------
for i, (c, x) in enumerate(LINE):
    P(c, T_OUT, (x, -1.2, 0), 0, (0, 0, 0), (0, 6), (-160, -20), 1, 0.02)
    for k in range(13): c.AR(T_OUT + k * 0.4, (-160, -38 if k % 2 else -4))
    c.AR(T_OUT + 5.6, (0, -6)); c.H(T_OUT + 5.6, (0, 0, 0)); c.H(T_OUT + 6.4, (18, 0, 0)); c.H(T_OUT + 7.4, (18, 0, 0)); c.H(T_OUT + 8.0, (0, 0, 0))
    if c is not B: c.MO(T_OUT, 0.35, 1.25)
# ---------- singing ----------
VERSE = [k for k in TL["lines"] if k["key"][0] in "yvz"]
for l in VERSE: YA.sing(l["start"], l["end"] + 0.2, 1.0, 1.1)
for l in TL["lines"]:
    if l["key"] in ("cA", "cA2", "cC", "cD"):
        for c in (YA, KA, B): c.sing(l["start"], l["end"] + 0.2, 0.9, 1.1)
    if l["key"] == "eD":
        for c in (YA, KA, B): c.sing(T_OUT, l["end"] + 0.2, 0.9, 1.1)
# blinks
for c in CAST:
    t = 3.0 + random.random()
    while t < T_END - 1: c.blink(t); t += random.uniform(2.4, 4.6)

# ---- name tags (2D, tracked) for the kitchen wide shot
for nm, c, z in (("tagY", YA, 2.75), ("tagK", KA, 2.55), ("tagC", CH, 2.6), ("tagB", B, 2.6)):
    e = empty(nm, (0, 0, z)); e.parent = c.root; TRACK.append((nm, e, F(T_KW + 2.6), F(T_Y1) - 1))
# ---- sky through the dining-room window: day → sunset → night
def sky(t, col, es, win): col_key(SKYM, F(t), col, "Emission Color"); emis_key(SKYM, F(t), es); WIN.append((F(t), win))
WIN = []
sky(0, (0.45, 0.7, 1.0), 3.0, 1.0); sky(T_V1, (0.45, 0.7, 1.0), 3.0, 1.0); sky(T_V2, (1.0, 0.5, 0.2), 3.0, 0.9); sky(T_R2, (1.0, 0.5, 0.2), 3.0, 0.9); sky(T_Z3, (0.25, 0.2, 0.55), 1.2, 0.3); sky(T_OUT, (0.03, 0.05, 0.2), 0.6, 0.1); sky(T_END, (0.03, 0.05, 0.2), 0.6, 0.1)

# ================= CAMERA =================
target = empty("target", (0, 0, 1.15))
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 32; cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 5.6
cam = bpy.data.objects.new("cam", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = target
DWIDE = ((DX, -8.2, 1.7), (DX, -1.0, 1.35))
SHOTS = [  # (t0, set, cam0, tgt0, cam1, tgt1)
 (0.0, "E", (EX, -13.5, 6.5), (EX, 3, 3.6), (EX, -9.5, 2.2), (EX, 3, 2.9)),
 (T_DIN0, "D", (DX - 1.5, -7.6, 1.7), (DX - 0.8, 0, 1.5), (DX + 0.6, -6.6, 1.7), (DX + 0.6, 0, 1.5)),
 (T_KW, "K", (1.0, -9.0, 1.9), (1.0, 0.3, 1.45), (1.0, -7.9, 1.85), (1.0, 0.3, 1.45)),
 (T_Y1, "D", (DX - 0.4, -7.2, 1.6), (DX - 0.4, -1.8, 1.45), (DX - 0.4, -6.6, 1.6), (DX - 0.4, -1.8, 1.45)),
 (T_Y2, "K", (2.2, -6.2, 1.9), (2.2, 0.1, 1.7), (2.2, -5.7, 1.9), (2.2, 0.1, 1.7)),
 (T_Y3, "K", (1.0, -3.9, 1.8), (0.8, 0.4, 1.85), (1.0, -3.6, 1.8), (0.8, 0.4, 1.85)),
 (T_Y4, "K", (-0.75, -4.4, 1.8), (-0.75, 0.4, 1.95), (-0.75, -4.0, 1.8), (-0.75, 0.4, 1.95)),
 (T_CA, "K", (-1.0, -3.6, 1.75), (-1.0, 0.4, 2.0), (-1.0, -3.2, 1.75), (-1.0, 0.4, 2.0)),
 (T_CA2, "K", (0.45, -6.3, 1.9), (0.45, 0.4, 1.85), (0.45, -5.8, 1.9), (0.45, 0.4, 1.85)),
 (T_CB, "K", (2.3, -3.3, 1.9), (2.5, 1.2, 2.1), (2.35, -2.7, 1.9), (2.55, 1.2, 2.1)),
 (T_CB2, "K", (0.9, -9.0, 2.1), (0.9, 0.3, 1.5), (0.9, -8.6, 2.1), (0.9, 0.3, 1.5)),
 (T_CC, "K", (2.25, -2.6, 1.9), (2.2, -0.1, 1.1), (2.25, -2.5, 1.75), (2.15, -0.1, 1.15)),
 (T_CC2, "K", (-1.0, -4.6, 1.7), (-1.0, 0.4, 1.75), (-1.0, -4.2, 1.7), (-1.0, 0.4, 1.75)),
 (T_CI, "K", (0.9, -9.4, 2.0), (0.9, 0.3, 1.55), (0.9, -8.6, 2.0), (0.9, 0.3, 1.55)),
 (T_CD, "K", (0.88, -5.6, 1.8), (0.88, -1.5, 1.85), (0.88, -5.1, 1.8), (0.88, -1.5, 1.85)),
 (T_DANCE, "D", (DX, -7.3, 1.55), (DX, -1.2, 1.4), (DX, -7.3, 1.55), (DX, -1.2, 1.4)),
 (T_V1, "K", (2.45, -3.2, 1.9), (2.6, 1.3, 2.15), (2.5, -2.5, 1.95), (2.6, 1.3, 2.15)),
 (T_V2, "D", (DX + 1.3, -5.2, 1.7), (DX + 2.6, -0.5, 1.5), (DX + 1.6, -4.7, 1.7), (DX + 2.9, -0.5, 1.5)),
 (T_V3, "K", (0.45, -6.6, 1.9), (0.45, 0.4, 1.85), (0.45, -6.2, 1.9), (0.45, 0.4, 1.85)),
 (T_V4, "K", (-0.15, -5.0, 1.8), (-0.15, 0.4, 1.8), (-0.15, -4.6, 1.8), (-0.15, 0.4, 1.8)),
 (T_R1, "K", (0, -6, 1.8), (0, 0, 1.6), (0, -6, 1.8), (0, 0, 1.6)),
 (T_M1, "K", (4.35, -0.6, 2.0), (2.8, 1.9, 1.5), (4.35, -0.2, 2.0), (2.8, 1.9, 1.5)),
 (T_M2, "K", (0.75, -3.0, 1.75), (0.75, 0.2, 1.45), (0.75, -2.7, 1.75), (0.75, 0.2, 1.45)),
 (T_M3, "K", (-1.0, -3.0, 1.75), (-1.0, 0.2, 1.5), (-1.0, -2.7, 1.75), (-1.0, 0.2, 1.5)),
 (T_M4, "D", (DX - 0.3, -7.2, 1.6), (DX - 0.3, -1.4, 1.45), (DX - 0.3, -6.8, 1.6), (DX - 0.3, -1.4, 1.45)),
 (T_R2, *(("D",) + DWIDE + DWIDE)),
 (T_Z1, "K", (-0.3, -5.4, 1.85), (-0.3, 0.4, 1.85), (-0.3, -5.0, 1.85), (-0.3, 0.4, 1.85)),
 (T_Z2, "K", (0.75, -9.6, 2.2), (0.6, 0.6, 2.0), (0.75, -8.8, 2.2), (0.3, 0.6, 2.1)),
 (T_Z3, "D", (DX, -6.0, 1.8), (DX, -0.7, 1.75), (DX, -5.5, 1.8), (DX, -0.7, 1.75)),
 (T_Z4, "D", (DX, -9.2, 1.7), (DX, -1.2, 1.5), (DX, -8.4, 1.7), (DX, -1.2, 1.5)),
 (T_R3, "K", (0, -6, 1.8), (0, 0, 1.6), (0, -6, 1.8), (0, 0, 1.6)),
 (T_OUT, "D", (DX, -8.4, 1.7), (DX, -1.2, 1.5), (DX, -9.4, 1.8), (DX, -1.2, 1.6)),
]
for i, (t0, st, c0, g0, c1, g1) in enumerate(SHOTS):
    f0 = F(t0) if i else 1; f1 = (F(SHOTS[i + 1][0]) - 1) if i + 1 < len(SHOTS) else NF
    if i: CUTF.add(f0 - 1)
    for f, c, g in ((f0, c0, g0), (f1, c1, g1)):
        key(cam, f, loc=c); key(target, f, loc=g)
        cam_d.dof.focus_distance = (Vector(c) - Vector(g)).length; cam_d.dof.keyframe_insert("focus_distance", frame=f)
    for S_, LS in (("K", KL), ("D", DL), ("E", EL)):
        for l, e in LS: lkey(l, f0, e if st == S_ else 0)
# dining lights follow the day; the last seconds go dark
def dl_scale(t, k, kwin=None):
    for l, e in DL: lkey(l, F(t), e * (kwin if (l.name == "dWin" and kwin is not None) else k))
dl_scale(T_V2, 0.85, 0.8); dl_scale(T_Z3, 0.8, 0.25); dl_scale(T_Z4, 0.8, 0.25); dl_scale(T_OUT, 0.75, 0.05); dl_scale(T_OUT + 7.2, 0.75, 0.05); dl_scale(T_OUT + 9.0, 0.06, 0.02); dl_scale(T_END, 0.06, 0.02)
for l, c in ((DL[4][0], None),):
    for t, col in ((0, (0.6, 0.8, 1.0)), (T_V1, (0.6, 0.8, 1.0)), (T_V2, (1.0, 0.55, 0.25)), (T_Z3, (0.4, 0.35, 0.8))):
        l.data.color = col; l.data.keyframe_insert("color", frame=F(t))
emis_key(BULB, F(T_OUT + 7.2), 16); emis_key(BULB, F(T_OUT + 9.0), 3)

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
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
for idb in ANIM:
    for fc in all_fcurves(idb):
        for kp in fc.keyframe_points:
            if idb in (cam, target, cam_d): kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            if int(round(kp.co[0])) in CUTF: kp.interpolation = "CONSTANT"

world = bpy.data.worlds.new("w"); world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.3, 0.4, 0.55, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.25
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
print("OBJECTS", len(bpy.data.objects), "FRAMES", NF)

if os.environ.get("EP7_TRACK"):
    from bpy_extras.object_utils import world_to_camera_view
    out = {}
    for name, o, a, b in TRACK:
        pts = []
        for f in range(a, b + 1):
            scene.frame_set(f); p = o.matrix_world.translation
            v = world_to_camera_view(scene, cam, p); v2 = world_to_camera_view(scene, cam, p + Vector((0, 0, 0.1)))
            pts.append([f, round(v.x * 720, 1), round((1 - v.y) * 1280, 1), round((v2.y - v.y) * 1280 * 10, 1), round(o.matrix_world.to_scale()[0], 3)])
        out[name] = pts
    json.dump(out, open(os.environ["EP7_TRACK"], "w"))
    print("TRACK", {k: len(v) for k, v in out.items()})
