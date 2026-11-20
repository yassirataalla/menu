# ---------------- ep10 set: door + hallway, mess, plates, mom's phone, sparkles, halo ----------------
DX0, DX1, DZ = -2.15, -1.05, 2.5
_wf = bpy.data.objects["wallF"]; _wf.hide_render = True; _wf.hide_viewport = True
cube("wallF1", ((-3.6 + DX0) / 2, -5.5, 2.2), ((DX0 + 3.6) / 2, 0.1, 2.3), WALL, 0)
cube("wallF2", ((DX1 + 3.6) / 2, -5.5, 2.2), ((3.6 - DX1) / 2, 0.1, 2.3), WALL, 0)
cube("wallF3", ((DX0 + DX1) / 2, -5.5, (DZ + 4.5) / 2), ((DX1 - DX0) / 2, 0.1, (4.5 - DZ) / 2), WALL, 0)
for x in (DX0 - 0.04, DX1 + 0.04): cube("dframe", (x, -5.4, DZ / 2), (0.05, 0.06, DZ / 2), FRAME, 0.01)
cube("dframeT", ((DX0 + DX1) / 2, -5.4, DZ + 0.04), ((DX1 - DX0) / 2 + 0.09, 0.06, 0.05), FRAME, 0.01)
DOOR = empty("doorHinge", (DX0, -5.43, 0))
DOORM = MT("doorM", (0.55, 0.4, 0.3), 0.45)
cube("door", ((DX1 - DX0) / 2, 0, DZ / 2), ((DX1 - DX0) / 2 - 0.01, 0.035, DZ / 2 - 0.01), DOORM, 0.02, DOOR)
sphere("doorKnob", ((DX1 - DX0) - 0.12, 0.06, 1.1), 0.04, GOLD, parent=DOOR)
cube("doorPoster", ((DX1 - DX0) / 2, 0.04, 1.6), (0.28, 0.004, 0.36), MT("poster", (0.2, 0.6, 0.9), 0.6, (0.2, 0.55, 0.9), 0.4), 0.005, DOOR)
HALLM = MT("hall", (0.9, 0.75, 0.55), 0.8, (1.0, 0.72, 0.45), 0.6)
cube("hallBack", ((DX0 + DX1) / 2, -7.2, 2.0), (1.6, 0.05, 2.0), HALLM, 0)
for x in (DX0 - 0.6, DX1 + 0.6): cube("hallSide", (x, -6.4, 2.0), (0.05, 0.9, 2.0), HALLM, 0)
cube("hallFloor", ((DX0 + DX1) / 2, -6.4, -0.05), (1.6, 0.95, 0.05), FLOOR, 0)
HALL = light("HALL", "AREA", ((DX0 + DX1) / 2, -6.6, 2.4), ((DX0 + DX1) / 2, -4.0, 0.8), 260, (1.0, 0.72, 0.45), 1.2)
# ---- mess ----
CERA = MT("ceramic", (0.92, 0.92, 0.9), 0.15); _set(CERA, **{"Coat Weight": 0.6})
SAUCE = MT("sauce", (0.6, 0.15, 0.05), 0.5)
def plate(name, loc, parent=None, dirty=True):
    g = grp(name, loc, parent=parent)
    cyl(name + "p", (0, 0, 0), 0.16, 0.018, CERA, parent=g)
    if dirty: cyl(name + "s", (0.03, -0.02, 0.011), 0.07, 0.004, SAUCE, parent=g)
    return g
MESS = []
for i, (x, y, z) in enumerate([(1.25, -1.75, 0.01), (1.3, -1.72, 0.03), (1.22, -1.78, 0.05), (-0.55, -0.55, 1.07), (2.35, 2.45, 1.02)]):
    MESS.append(plate(f"mplate{i}", (x, y, z)))
for i, (x, y) in enumerate([(1.55, -2.05), (-1.4, -1.0)]):
    cup = grp(f"mcup{i}", (x, y, 0.0)); cyl(f"mcupB{i}", (0, 0, 0.07), 0.05, 0.14, CERA, parent=cup); MESS.append(cup)
pz = grp("pizza", (-1.5, -1.6, 0.0), (0, 0, 20)); cube("pizzaBox", (0, 0, 0.03), (0.3, 0.3, 0.03), MT("cardboard", (0.65, 0.45, 0.25), 0.8), 0.01, pz)
cube("pizzaLid", (0, 0.32, 0.25), (0.3, 0.02, 0.25), MT("cardboard"), 0.01, pz)
for i, (x, y, r, c) in enumerate([(-0.5, -3.7, 30, (0.3, 0.5, 0.8)), (0.9, -3.3, -20, (0.8, 0.75, 0.2)), (-1.1, -2.9, 60, (0.3, 0.6, 0.35)), (1.8, -2.7, 10, (0.85, 0.3, 0.3))]):
    cl = cube(f"cloth{i}", (x, y, 0.06), (0.32, 0.22, 0.05), MT(f"clothM{i}", c, 0.95), 0.05); cl.rotation_euler = (0, 0, math.radians(r))
cube("sock2", (0.4, -2.2, 0.04), (0.18, 0.07, 0.04), MT("sock"), 0.03).rotation_euler = (0, 0, math.radians(40))
cube("tshirtBed", (-0.9, 0.2, 1.1), (0.35, 0.3, 0.05), MT("clothM0"), 0.06)
# plates Boulon carries at the end
CARRY = grp("carry", (0, -0.5, 1.02), parent=B.rig)
for i in range(5): plate(f"cplate{i}", ((i % 2) * 0.02 - 0.01, 0, i * 0.03), CARRY, dirty=(i == 4))
cg = grp("ccup", (0.03, 0, 0.21), parent=CARRY); cyl("ccupB", (0, 0, 0.0), 0.05, 0.14, CERA, parent=cg)
# ---- Boulon's phone: a funny video on screen ----
VIDM = bpy.data.materials.new("vidM"); VIDM.use_nodes = True; nt = VIDM.node_tree; nt.nodes.clear()
_o = nt.nodes.new("ShaderNodeOutputMaterial"); _e = nt.nodes.new("ShaderNodeEmission"); _n = nt.nodes.new("ShaderNodeTexNoise"); _mp = nt.nodes.new("ShaderNodeMapping")
_tc = nt.nodes.new("ShaderNodeTexCoord"); _cr = nt.nodes.new("ShaderNodeValToRGB"); _e.inputs["Strength"].default_value = 1.6; _n.inputs["Scale"].default_value = 3.0
_cr.color_ramp.elements[0].color = (1.0, 0.45, 0.2, 1); _cr.color_ramp.elements[1].color = (0.25, 0.6, 1.0, 1); _cr.color_ramp.elements.new(0.5).color = (1.0, 0.9, 0.3, 1)
nt.links.new(_tc.outputs["Object"], _mp.inputs[0]); nt.links.new(_mp.outputs[0], _n.inputs["Vector"]); nt.links.new(_n.outputs["Fac"], _cr.inputs[0])
nt.links.new(_cr.outputs["Color"], _e.inputs["Color"]); nt.links.new(_e.outputs[0], _o.inputs["Surface"])
_loc = _mp.inputs["Location"]; _loc.default_value = (0, 0, 0); _loc.keyframe_insert("default_value", frame=1); _loc.default_value = (4, 2, 3); _loc.keyframe_insert("default_value", frame=NF)
VID = cube("phVid", (0, 0.0, 0.0155), (0.112, 0.2, 0.001), VIDM, 0, PH)
# ---- mom's phone ----
MPH = grp("momPhone", (0, -0.13, -0.7), (0, 180, 0), parent=M.armR)
cube("mphBody", (0, 0, 0), (0.07, 0.012, 0.13), DARK, 0.008, MPH)
MPHS = MT("mphScr", (0.05, 0.06, 0.1), 0.3, (0.12, 0.16, 0.26), 1.4); cube("mphScr", (0, -0.013, 0), (0.063, 0.002, 0.12), MPHS, 0, MPH)
TXTW = MT("phTxtW", (1, 1, 1), 0.5, (1, 1, 1), 1.2)
txt("mphName", "Tata Samira", (0, -0.016, 0.06), 0.022, TXTW, MPH, rot=(90, 0, 0), ext=0.0005)
sphere("mphAv", (0, -0.016, 0.0), 0.028, MT("avS", (0.9, 0.6, 0.4), 0.5, (1.0, 0.65, 0.4), 1.5), (1, 0.2, 1), MPH)
sphere("mphOk", (0.035, -0.016, -0.085), 0.016, MT("okG", (0.2, 0.9, 0.4), 0.5, (0.2, 0.9, 0.4), 3.0), (1, 0.2, 1), MPH)
sphere("mphNo", (-0.035, -0.016, -0.085), 0.016, MT("noR", (1.0, 0.2, 0.2), 0.5, (1.0, 0.2, 0.2), 3.0), (1, 0.2, 1), MPH)
# ---- angelic halo + sparkles + glow around mom ----
TXTW = MT("phTxtW", (1, 1, 1), 0.5, (1, 1, 1), 1.2)
HALOM = MT("haloM", (1, 0.85, 0.4), 0.3, (1.0, 0.85, 0.45), 6.0)
HALO = grp("haloG", (0, 0, 0.82), parent=M.head)
bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.022, location=(0, 0, 0))
_h = bpy.context.object; _h.name = "halo"; give(_h, HALOM); smooth(_h); _h.parent = HALO
SPKM = MT("spark", (1, 0.9, 0.95), 0.3, (1.0, 0.8, 0.9), 8.0)
SPARKS = []
random.seed(11)
for i in range(14):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(0.42, 0.62); z = random.uniform(-0.1, 0.75)
    sg = grp(f"spkg{i}", (r * math.cos(a), -0.15 + r * 0.4 * math.sin(a), z), parent=M.head)
    for ax in ((1, 0.12, 0.12), (0.12, 0.12, 1)):
        sphere(f"spk{i}", (0, 0, 0), 0.035, SPKM, ax, sg)
    SPARKS.append(sg)
GLOW = light("MOMGLOW", "AREA", (0, -1.1, 0.35), None, 0, (1.0, 0.7, 0.85), 0.8); GLOW.parent = M.head
GLOW.rotation_euler = (math.radians(90), 0, 0)
MFACE = light("MOMFACE", "POINT", (0, -0.75, 0.3), None, 5, (1.0, 0.75, 0.9), 0.15); MFACE.parent = M.head
_mrc = bpy.data.collections.new("MomRecv"); scene.collection.children.link(_mrc)
for o in _kids(M.root):
    if o.type in ("MESH", "FONT", "CURVE"): _mrc.objects.link(o)
for nm, x, col, e in (("MRIMc", 0.95, (0.35, 0.8, 1.0), 60), ("MRIMm", -0.95, (1.0, 0.45, 0.75), 70)):
    rl = light(nm, "AREA", (0, 0, 0), None, e, col, 0.6); rl.parent = M.root; rl.location = (x, 1.1, 2.0)
    rl.rotation_euler = (Vector((0, 0, 1.45)) - Vector((x, 1.1, 2.0))).to_track_quat("-Z", "Y").to_euler()
    rl.data.spread = math.radians(60); rl.light_linking.receiver_collection = _mrc; rl.visible_glossy = False
for _o in bpy.data.objects:
    if _o.type == "LIGHT": _o.visible_camera = False
for nm in ("FACE", "MOMFACE", "PHL", "MOMGLOW"): bpy.data.objects[nm].visible_glossy = False
_fc = bpy.data.objects["FACE"]; _fc.data.shadow_soft_size = 0.04; _fc.location = (0, -0.7, 0.62)
