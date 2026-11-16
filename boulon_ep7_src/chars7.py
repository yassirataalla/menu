# ================= EPISODE 7 — characters =================
import bmesh
WEB = '/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep7/web/'
def KT(t): return F(t) if not isinstance(t, int) else max(1, t)

def shell(name, r, m, pred, parent, loc=(0, 0, 0), scale=(1, 1, 1), seg=112, rings=72):
    """part of a sphere (hair cap / beard): keeps faces whose centre satisfies pred(x,y,z) on the unit sphere"""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    dead = [f for f in bm.faces if not pred(*f.calc_center_median().normalized())]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    for v in bm.verts: v.co = v.co * r
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); o.location = loc; o.scale = scale
    smooth(o); give(o, m); o.parent = parent
    so = o.modifiers.new("so", "SOLIDIFY"); so.thickness = 0.012; so.offset = 1
    return o

def img_mat(name, path, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(path); t.extension = "CLIP"
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.6
    if emit:
        nt.links.new(t.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emit
    return m
def disc_img(name, loc, r, m, parent=None, rot=(90, 0, 0)):
    bpy.ops.mesh.primitive_circle_add(radius=r, vertices=48, fill_type="NGON", location=loc, rotation=[math.radians(a) for a in rot])
    o = bpy.context.object; o.name = name
    o.data.uv_layers.new(name="uv")
    for poly in o.data.polygons:
        for li in poly.loop_indices:
            v = o.data.vertices[o.data.loops[li].vertex_index].co
            o.data.uv_layers.active.data[li].uv = (0.5 + v.x / (2 * r), 0.5 + v.y / (2 * r))
    give(o, m)
    if parent: o.parent = parent
    return o
LOGO = img_mat("logo", WEB + "LIBAN-SUR-SEINE-202.png")
WHITE = MT("white", (1, 1, 1), 0.5); DARK = MT("dark", (0.05, 0.05, 0.07), 0.4)
EYEW = MT("eyeW", (0.95, 0.95, 0.95), 0.25); TEETH = MT("teeth", (0.95, 0.93, 0.88), 0.3); MOUTHM = MT("mouthM", (0.25, 0.04, 0.05), 0.5)

class Human:
    def __init__(s, name, skin, jacket, pants, hair, iris=(0.12, 0.07, 0.04), sc=(1, 1, 1), sleeve=0.5, shoes=None):
        s.name = name; s.amp_ranges = []
        s.root = empty(name, (0, 0, 0)); s.rig = empty(name + "Rig"); s.rig.parent = s.root; s.rig.scale = sc; r = s.rig
        s.skin = MT(name + "skin", skin, 0.55); s.jk = jacket; s.hairM = hair
        SK = s.skin; shoes = shoes or MT("shoe", (0.03, 0.03, 0.035), 0.4)
        # legs
        s.legs = []
        for sx in (-1, 1):
            hip = empty(f"{name}hip{sx}", (sx * 0.15, 0, 0.74)); hip.parent = r; s.legs.append(hip)
            cyl(f"{name}leg{sx}", (0, 0, -0.33), 0.115, 0.66, pants, parent=hip)
            cube(f"{name}shoe{sx}", (0, -0.06, -0.68), (0.12, 0.2, 0.065), shoes, 0.05, hip)
        # torso
        s.torso = cube(name + "torso", (0, 0, 1.1), (0.36, 0.23, 0.39), jacket, 0.13, r); s.torso.modifiers["bev"].segments = 8; smooth(s.torso)
        cube(name + "hipband", (0, 0, 0.75), (0.3, 0.19, 0.07), pants, 0.06, r)
        cyl(name + "collar", (0, 0, 1.5), 0.125, 0.09, jacket, parent=r)
        cyl(name + "neck", (0, 0, 1.55), 0.085, 0.14, SK, parent=r)
        # arms
        s.armL = empty(name + "armL", (-0.44, 0, 1.38)); s.armL.parent = r
        s.armR = empty(name + "armR", (0.44, 0, 1.38)); s.armR.parent = r
        for a, sx in ((s.armL, -1), (s.armR, 1)):
            sphere(f"{name}sh{sx}", (0, 0, 0), 0.115, jacket, parent=a)
            cyl(f"{name}slv{sx}", (0, 0, -sleeve / 2), 0.095, sleeve, jacket, parent=a)
            if sleeve < 0.45: cyl(f"{name}fore{sx}", (0, 0, -(sleeve + 0.5) / 2), 0.07, 0.5 - sleeve, SK, parent=a)
            sphere(f"{name}hand{sx}", (0, 0, -0.55), 0.1, SK, parent=a)
        # head
        s.head = empty(name + "head", (0, 0, 1.6)); s.head.parent = r; h = s.head
        s.HC = (0, 0, 0.3); s.HS = (0.29, 0.3, 0.33)
        sphere(name + "skull", s.HC, 1.0, SK, s.HS, h)
        for sx in (-1, 1): sphere(f"{name}ear{sx}", (sx * 0.29, 0.02, 0.3), 0.06, SK, (0.5, 0.8, 1.0), h)
        sphere(name + "nose", (0, -0.3, 0.27), 0.05, SK, (0.85, 1.0, 1.15), h)
        s.eyes = []; s.brows = []
        IR = MT(name + "iris", iris, 0.2)
        for sx in (-1, 1):
            e = empty(f"{name}eye{sx}", (sx * 0.105, -0.255, 0.36)); e.parent = h; s.eyes.append(e)
            sphere(f"{name}eyeW{sx}", (0, 0, 0), 0.058, EYEW, (1.0, 0.55, 1.0), e)
            sphere(f"{name}eyeI{sx}", (0, -0.027, 0.0), 0.032, IR, (1.0, 0.5, 1.0), e)
            sphere(f"{name}eyeP{sx}", (0, -0.04, 0.0), 0.016, DARK, (1.0, 0.5, 1.0), e)
            b = cube(f"{name}brow{sx}", (0, 0, 0), (0.062, 0.016, 0.014), hair, 0.008, h); s.brows.append(b)
        s.mouth = empty(name + "mouth", (0, -0.283, 0.135)); s.mouth.parent = h
        sphere(name + "mouthD", (0, 0, 0), 0.07, MOUTHM, (1.0, 0.35, 0.62), s.mouth)
        s.teeth = cube(name + "teethU", (0, -0.012, 0.022), (0.05, 0.012, 0.012), TEETH, 0.006, s.mouth)
        s.face(1, 1.0, 0.0, 0.0); s.MO(1, 0.0)
    # ---- hair / beard builders (coordinates on the unit sphere: -y = face, +z = up)
    def cap(s, pred, m=None, grow=1.045, name="hair", up=0.0):
        return shell(s.name + name, 1.0, m or s.hairM, pred, s.head, (s.HC[0], s.HC[1], s.HC[2] + up), tuple(k * grow for k in s.HS))
    def beard(s, pred, m=None, grow=1.03): return s.cap(pred, m, grow, "beard")
    def stache(s, m=None, w=0.085, drop=0.0):
        m = m or s.hairM
        for sx in (-1, 1):
            o = cube(f"{s.name}st{sx}", (sx * w * 0.55, -0.292, 0.193 + drop), (w * 0.62, 0.014, 0.016), m, 0.008, s.head); o.rotation_euler = (0, math.radians(sx * 14), math.radians(-sx * 12))
    # ---- animation
    def R(s, t, loc, rz=0, sc=(1, 1, 1), tilt=0): key(s.root, KT(t), loc=loc, rot=(tilt, 0, rz), scale=sc)
    def H(s, t, rot): key(s.head, KT(t), rot=rot)
    def A(s, t, L, Rr): key(s.armL, KT(t), rot=(L[0], L[1], 0)); key(s.armR, KT(t), rot=(Rr[0], Rr[1], 0))
    def AL(s, t, L): key(s.armL, KT(t), rot=(L[0], L[1], 0))
    def AR(s, t, Rr): key(s.armR, KT(t), rot=(Rr[0], Rr[1], 0))
    def LG(s, t, l=0, r=0): key(s.legs[0], KT(t), rot=(l, 0, 0)); key(s.legs[1], KT(t), rot=(r, 0, 0))
    def EY(s, t, z):
        for e in s.eyes: key(e, KT(t), scale=(1, 1, z))
    def BR(s, t, l=0.0, r=0.0, tilt=0.0):
        key(s.brows[0], KT(t), loc=(-0.105, -0.283, 0.455 + l), rot=(0, -tilt, 12)); key(s.brows[1], KT(t), loc=(0.105, -0.283, 0.455 + r), rot=(0, tilt, -12))
    def face(s, t, ey=1.0, br=0.0, tilt=0.0): s.EY(t, ey); s.BR(t, br, br, tilt)
    def MO(s, t, op, wide=1.0): key(s.mouth, KT(t), scale=(wide * (1 + 0.1 * op), 1, 0.2 + 1.15 * op))
    def nod(s, t0, n, base=(0, 0, 0), per=0.42, amp=15):
        for i in range(n):
            s.H(t0 + i * per, (base[0] + 3, base[1], base[2])); s.H(t0 + i * per + per * 0.5, (base[0] - amp, base[1], base[2]))
        s.H(t0 + n * per, base)
    def blink(s, t, back=1.0): s.EY(t - 0.06, back); s.EY(t, 0.08); s.EY(t + 0.1, back)
    def sing(s, t0, t1, gain=1.0, wide=1.0):
        a, b = F(t0), F(t1)
        s.MO(a - 2, 0.0, wide)
        for f in range(a, b, 2): s.MO(f, min(1.0, TL["amp"][min(NF - 1, f - 1)] * gain), wide)
        s.MO(b + 1, 0.0, wide)
    def talk(s, t0, t1, per=0.16, op=0.75):
        t = t0; k = 0
        while t < t1: s.MO(t, op * (0.5 + 0.5 * ((k * 5) % 3) / 2) if k % 2 == 0 else 0.1); t += per; k += 1
        s.MO(t1, 0.0)
    def walk(s, t0, t1, p0, p1, rz=0, step=0.3, bob=0.035, swing=24):
        n = max(2, int(round((t1 - t0) / step)));
        for i in range(n + 1):
            u = i / n; t = t0 + (t1 - t0) * u
            s.R(t, (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u, p0[2] + (bob if i % 2 else 0)), rz)
            sg = swing if i % 2 else -swing
            if i in (0, n): sg = 0
            s.LG(t, sg, -sg)

# ---------------- cast ----------------
BLACKJ = MT("blackJ", (0.022, 0.022, 0.026), 0.62); PANTSB = MT("pantsB", (0.03, 0.03, 0.036), 0.7)
WHITEJ = MT("whiteJ", (0.93, 0.94, 0.96), 0.55)
HAIRK = MT("hairBlack", (0.02, 0.017, 0.015), 0.55); HAIRB = MT("hairBrown", (0.045, 0.03, 0.022), 0.6)
STUB = MT("stubble", (0.03, 0.022, 0.018), 0.8)

# ---- the Chef: white jacket, short dark hair with a quiff, goatee, green-grey eyes
CH = Human("Chef", (0.62, 0.36, 0.22), WHITEJ, PANTSB, HAIRK, iris=(0.3, 0.42, 0.3), sc=(1.06, 1.06, 1.0))
CHEAD = CH.skin
CH.cap(lambda x, y, z: z > (0.42 + 0.42 * max(0.0, -y) if y < 0 else 0.42 - 0.75 * y))
CH.cap(lambda x, y, z: z > (0.2 + 0.62 * max(0.0, -y) if y < 0 else 0.2 - 0.8 * y), MT("fade", (0.16, 0.12, 0.1), 0.7), 1.02, "fade")
random.seed(3)
for i in range(26):   # spiky quiff
    a = random.uniform(-1, 1); b = random.uniform(-0.75, 0.25)
    o = sphere(f"chq{i}", (a * 0.16, b * 0.24, 0.585 + 0.04 * (1 - a * a) - 0.05 * max(0, b)), 0.05, HAIRK, (0.75, 0.75, 1.5 + 0.5 * random.random()), CH.head)
    o.rotation_euler = (math.radians(-22 + 30 * b), math.radians(a * 22), 0)
CH.beard(lambda x, y, z: y < 0 and ((abs(x) < 0.34 and z < -0.5) or (-0.9 < z < -0.62 and y < 0.2) or (abs(x) > 0.5 and y < -0.2 and z < -0.45)), HAIRK)
CH.stache(HAIRK)
for sx in (-1, 1):   # goatee sides joining the moustache
    o = cube(f"chg{sx}", (sx * 0.085, -0.268, 0.115), (0.014, 0.016, 0.06), HAIRK, 0.008, CH.head); o.rotation_euler = (math.radians(-18), 0, 0)
# jacket details: mandarin collar flags, placket, logo, name
cube("chPlacket", (0.06, -0.232, 1.08), (0.012, 0.01, 0.36), MT("whiteJ2", (0.82, 0.84, 0.88), 0.5), 0.004, CH.rig)
def flag_lb(name, loc, parent, w=0.05, h=0.034, rot=(90, 0, 0)):
    e = empty(name, loc); e.parent = parent; e.rotation_euler = [math.radians(a) for a in rot]
    RED = MT("flagR", (0.85, 0.05, 0.07), 0.5); GRN = MT("flagG", (0.0, 0.45, 0.2), 0.5)
    cube(name + "w", (0, 0, 0), (w, h, 0.004), WHITE, 0, e)
    for sy in (-1, 1): cube(name + f"r{sy}", (0, sy * h * 0.75, 0.002), (w, h * 0.25, 0.004), RED, 0, e)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=h * 0.48, depth=0.004, location=(0, 0, 0)); c = bpy.context.object; c.name = name + "cedar"; give(c, GRN); c.parent = e; c.location = (0, 0, 0.004); c.rotation_euler = (0, 0, math.radians(90))
    return e
def flag_fr(name, loc, parent, w=0.05, h=0.034, rot=(90, 0, 0)):
    e = empty(name, loc); e.parent = parent; e.rotation_euler = [math.radians(a) for a in rot]
    for i, c in enumerate([MT("frB", (0.0, 0.12, 0.6), 0.5), WHITE, MT("flagR", (0.85, 0.05, 0.07), 0.5)]):
        cube(f"{name}{i}", ((i - 1) * w * 0.667, 0, 0), (w / 3, h, 0.004), c, 0, e)
    return e
def flag_bd(name, loc, parent, w=0.05, h=0.034, rot=(90, 0, 0)):
    e = empty(name, loc); e.parent = parent; e.rotation_euler = [math.radians(a) for a in rot]
    cube(name + "g", (0, 0, 0), (w, h, 0.004), MT("bdG", (0.0, 0.32, 0.2), 0.5), 0, e)
    cyl(name + "r", (-w * 0.1, 0, 0.003), h * 0.6, 0.004, MT("flagR", (0.85, 0.05, 0.07), 0.5), parent=e)
    return e
flag_lb("chFlagL", (-0.105, -0.118, 1.52), CH.rig, 0.03, 0.02, (78, 0, 28))
flag_fr("chFlagF", (0.105, -0.118, 1.52), CH.rig, 0.03, 0.02, (78, 0, -28))
disc_img("chLogo", (0.2, -0.236, 1.22), 0.075, LOGO, CH.rig)
txt("chName", "Bachar Nahas", (0.2, -0.238, 1.105), 0.028, MT("nameR", (0.75, 0.05, 0.08), 0.5), CH.rig, ext=0.001)

# ---- Kartik: black jacket, white hair net, short beard, big smile
KA = Human("Kartik", (0.27, 0.13, 0.07), BLACKJ, PANTSB, HAIRK, sc=(1.0, 1.0, 0.97))
NETM = MT("net", (0.9, 0.92, 0.95), 0.9)
net = KA.cap(lambda x, y, z: z > (0.3 + 0.38 * max(0.0, -y) if y < 0 else 0.3 - 0.95 * y), NETM, 1.11, "net", 0.02)
dm = net.modifiers.new("d", "DISPLACE"); tx = bpy.data.textures.new("netT", "CLOUDS"); tx.noise_scale = 0.07; dm.texture = tx; dm.strength = 0.035
KA.cap(lambda x, y, z: z > (0.36 + 0.42 * max(0.0, -y) if y < 0 else 0.3 - 0.9 * y), HAIRK, 1.03, "hairIn")
KA.beard(lambda x, y, z: y < 0.28 and z < (-0.47 + 0.5 * abs(x)) and not (abs(x) < 0.3 and -0.6 < z < -0.3 and y < 0), STUB)
KA.stache(HAIRK, 0.09)
for i in range(6): sphere(f"kaBtn{i}", (0.1, -0.235, 0.86 + i * 0.105), 0.016, MT("btnK", (0.06, 0.06, 0.07), 0.3), parent=KA.rig)
cube("kaFlap", (0.1, -0.228, 1.1), (0.14, 0.008, 0.36), MT("blackJ2", (0.035, 0.035, 0.04), 0.55), 0.004, KA.rig)

# ---- Yasser: tall, slim, curly dark hair, short beard, black jacket with wooden buttons, bracelet
YA = Human("Yasser", (0.52, 0.29, 0.17), BLACKJ, PANTSB, HAIRB, sc=(0.93, 0.93, 1.09), sleeve=0.3)
YA.cap(lambda x, y, z: z > (0.36 + 0.4 * max(0.0, -y) if y < 0 else 0.26 - 0.85 * y), MT("yaSide", (0.06, 0.04, 0.03), 0.7), 1.03, "sides")
random.seed(11)
for i in range(95):   # curls
    th = random.uniform(0, 2 * math.pi); ph = random.uniform(0.0, 0.95)
    x = math.sin(ph) * math.cos(th); y = math.sin(ph) * math.sin(th); z = math.cos(ph)
    if y < -0.62 and z < 0.75: continue
    k = 1.08 + 0.1 * random.random() + 0.1 * max(0, z - 0.6)
    sphere(f"yaC{i}", (x * 0.29 * k, y * 0.3 * k - 0.01, 0.3 + z * 0.33 * k), random.uniform(0.05, 0.075), HAIRB, parent=YA.head)
YA.beard(lambda x, y, z: y < 0.3 and z < (-0.5 + 0.52 * abs(x)) and not (abs(x) < 0.28 and -0.62 < z < -0.3 and y < 0), STUB)
YA.stache(STUB, 0.08)
WOOD = MT("woodBtn", (0.5, 0.3, 0.12), 0.5)
for i in range(5): sphere(f"yaBtn{i}", (0.06, -0.235, 0.9 + i * 0.12), 0.02, WOOD, parent=YA.rig)
cyl("yaBrace", (0, 0, -0.44), 0.078, 0.03, MT("silver", (0.8, 0.8, 0.82), 0.25), parent=YA.armL)

# ---- Boulon (plays Narayan, the dishwasher)
class Bot:
    def __init__(s, name, mats, label=None, antenna=True, sc=1.0):
        s.root = empty(name, (0, 0, 0)); s.rig = empty(name + "Rig"); s.rig.parent = s.root; s.rig.scale = (sc, sc, sc); r = s.rig; s.m = mats
        cube(name + "body", (0, 0, 0.95), (0.42, 0.32, 0.45), mats["body"], 0.08, r)
        s.head = empty(name + "head", (0, 0, 1.4)); s.head.parent = r
        cube(name + "headbox", (0, 0, 0.3), (0.34, 0.3, 0.26), mats["head"], 0.08, s.head)
        cube(name + "visor", (0, -0.29, 0.3), (0.27, 0.03, 0.14), DARK, 0.05, s.head)
        s.eyeL = sphere(name + "eyeL", (0, 0, 0), 0.065, mats["eye"], parent=s.head); s.eyeL.location = (-0.12, -0.31, 0.3)
        s.eyeR = sphere(name + "eyeR", (0, 0, 0), 0.065, mats["eye"], parent=s.head); s.eyeR.location = (0.12, -0.31, 0.3)
        s.browL = cube(name + "browL", (0, 0, 0), (0.062, 0.012, 0.011), mats["eye"], 0.004, s.head)
        s.browR = cube(name + "browR", (0, 0, 0), (0.062, 0.012, 0.011), mats["eye"], 0.004, s.head)
        cyl(name + "ant", (0, 0, 0.7), 0.02, 0.3, mats["metal"], parent=s.head); sphere(name + "antball", (0, 0, 0.88), 0.07, mats["bulb"], parent=s.head)
        txt(name + "lbl", label, (0, -0.33, 0.64), 0.13, WHITE, r, ext=0.008)
        s.armL = empty(name + "armL", (-0.47, 0, 1.25)); s.armL.parent = r
        cyl(name + "armLm", (0, 0, -0.25), 0.07, 0.5, mats["metal"], parent=s.armL); sphere(name + "handL", (0, 0, -0.52), 0.1, mats["hand"], parent=s.armL)
        s.armR = empty(name + "armR", (0.47, 0, 1.25)); s.armR.parent = r
        cyl(name + "armRm", (0, 0, -0.25), 0.07, 0.5, mats["metal"], parent=s.armR); sphere(name + "handR", (0, 0, -0.52), 0.1, mats["hand"], parent=s.armR)
        for x in (-0.22, 0.22):
            cube(f"{name}leg{x}", (x, 0, 0.3), (0.12, 0.14, 0.2), mats["metal"], 0.04, r)
            cube(f"{name}foot{x}", (x, -0.05, 0.08), (0.16, 0.22, 0.08), DARK, 0.04, r)
        s.mouth = cube(name + "mouth", (0, -0.315, 0.185), (0.1, 0.02, 0.03), mats["eye"], 0.01, s.head)
        s.face(1, 1.0, 0.0, 0.0); s.MO(1, 0.0)
    def R(s, t, loc, rz=0, sc=(1, 1, 1), tilt=0): key(s.root, KT(t), loc=loc, rot=(tilt, 0, rz), scale=sc)
    def H(s, t, rot): key(s.head, KT(t), rot=rot)
    def A(s, t, L, Rr): key(s.armL, KT(t), rot=(L[0], L[1], 0)); key(s.armR, KT(t), rot=(Rr[0], Rr[1], 0))
    def AL(s, t, L): key(s.armL, KT(t), rot=(L[0], L[1], 0))
    def AR(s, t, Rr): key(s.armR, KT(t), rot=(Rr[0], Rr[1], 0))
    def LG(s, t, l=0, r=0): pass
    def EY(s, t, z):
        for e in (s.eyeL, s.eyeR): key(e, KT(t), scale=(1, 1, z))
    def BR(s, t, l=0.0, r=0.0, tilt=0.0):
        key(s.browL, KT(t), loc=(-0.12, -0.325, 0.395 + l), rot=(0, -tilt, 0)); key(s.browR, KT(t), loc=(0.12, -0.325, 0.395 + r), rot=(0, tilt, 0))
    def face(s, t, ey=1.0, br=0.0, tilt=0.0): s.EY(t, ey); s.BR(t, br, br, tilt)
    def MO(s, t, op, wide=1.0): key(s.mouth, KT(t), scale=(wide * (1 + 0.25 * op), 1, 0.12 + 1.25 * op))
    def nod(s, t0, n, base=(0, 0, 0), per=0.42, amp=15):
        for i in range(n):
            s.H(t0 + i * per, (base[0] + 3, base[1], base[2])); s.H(t0 + i * per + per * 0.5, (base[0] - amp, base[1], base[2]))
        s.H(t0 + n * per, base)
    def blink(s, t, back=1.0): s.EY(t - 0.06, back); s.EY(t, 0.08); s.EY(t + 0.1, back)
Bot.sing = Human.sing; Bot.talk = Human.talk; Bot.walk = Human.walk
BM = dict(body=MT("robot", (0.15, 0.45, 0.85), 0.3), head=MT("metal", (0.8, 0.8, 0.82), 0.25), metal=MT("metal"),
          eye=MT("eye", (0.1, 0.1, 0.1), 0.2, (0.3, 1.0, 0.9), 10), bulb=MT("bulb", (0.9, 0.2, 0.1), 0.3, (1.0, 0.25, 0.1), 10), hand=MT("robot"))
B = Bot("Boulon", BM, "BOULON")
cube("panel", (0, -0.33, 0.95), (0.22, 0.02, 0.16), MT("metal"), 0.03, B.rig)
for i, c in enumerate([(0.95, 0.3, 0.25), (0.3, 0.75, 0.35), (0.98, 0.78, 0.15)]): sphere(f"btn{i}", (-0.12 + 0.12 * i, -0.36, 0.98), 0.04, MT(f"b{i}", c, 0.5), parent=B.rig)
GLOVE = MT("glove", (1.0, 0.8, 0.1), 0.45)
for arm in (B.armL, B.armR):
    g = sphere("glove", (0, 0, 0), 0.118, GLOVE, parent=arm); g.location = (0, 0, -0.52)
    c = cyl("cuff", (0, 0, 0), 0.085, 0.1, GLOVE, parent=arm); c.location = (0, 0, -0.4)
sponge = cube("sponge", (0, 0, 0), (0.07, 0.045, 0.03), MT("sponge", (0.2, 0.85, 0.35), 0.8), 0.015, B.armR); sponge.location = (-0.03, -0.08, -0.6)
CAST = [YA, KA, CH, B]
