# ---- human-like robot mouth: glowing lips on the visor screen, teeth + tongue inside, shape keys ----
MOUTH_Z = 0.175
_vis = [o for o in B.head.children if o.name.endswith("visor")][0]
print("VISLOC", tuple(_vis.location), tuple(_vis.scale)); _vis.scale = (1, 1, 0.17 / 0.14); _vis.location.z = 0.27 - 0.3 * (0.17 / 0.14)
B.mouth.hide_render = True; B.mouth.hide_viewport = True
MPOSE = {  # w, upper-open, lower-open, smile-curve, cupid bow
    "Basis": (0.058, 0.000, 0.000, 0.010, 0.000),
    "talk":  (0.050, 0.016, 0.034, 0.004, 0.000),
    "shout": (0.078, 0.026, 0.046, -0.008, 0.000),
    "O":     (0.030, 0.022, 0.030, 0.000, 0.000),
    "smile": (0.070, -0.004, 0.028, 0.022, 0.000),
    "frown": (0.056, 0.000, 0.000, -0.020, 0.000),
}
NX = 44
def _cols(w, hu, hl, s, bow):
    out = []
    for i in range(NX + 1):
        u = -1 + 2 * i / NX; x = u * w; e = math.sqrt(max(0.0, 1 - u * u)); c = s * u * u
        zu = c + hu * e - bow * math.exp(-(x / 0.014) ** 2) * (1 if hu > 0.002 else 0.3)
        zl = c - hl * e
        tu = 0.0025 + 0.0045 * e; tl = 0.003 + 0.0065 * e
        out.append([(x, zl - tl), (x, zl), (x, zu), (x, zu + tu)])
    return out
def _verts(p): return [(x, 0.0, z) for col in _cols(*p) for (x, z) in col]
me = bpy.data.meshes.new("mouthM"); vs = _verts(MPOSE["Basis"]); fs = []; fm = []
for i in range(NX):
    for r in range(3):
        a = i * 4 + r; fs.append((a, a + 4, a + 5, a + 1)); fm.append(0)
me.from_pydata(vs, [], fs); me.update()
uv = me.uv_layers.new(name="UVMap")
for poly in me.polygons:
    for li in poly.loop_indices:
        vi = me.loops[li].vertex_index; uv.data[li].uv = ((vi // 4) / NX, [0.0, 0.0, 1.0, 1.0][vi % 4])
MOUTH = bpy.data.objects.new("mouth2", me); scene.collection.objects.link(MOUTH)
MOUTH.parent = B.head; MOUTH.location = (0, -0.324, MOUTH_Z); MOUTH.scale = (1.4, 1, 1.4)
for p in me.polygons: p.material_index = fm[p.index]; p.use_smooth = True
LIPM = EYE  # same sky-blue glow as the eyes
INM = bpy.data.materials.new("mouthIn"); INM.use_nodes = True; nt = INM.node_tree; nt.nodes.clear()
o_ = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission"); tc = nt.nodes.new("ShaderNodeTexCoord")
sx = nt.nodes.new("ShaderNodeSeparateXYZ"); cr = nt.nodes.new("ShaderNodeValToRGB"); em.inputs["Strength"].default_value = 2.2
els = cr.color_ramp.elements; cr.color_ramp.interpolation = "CONSTANT"
els[0].position = 0.0; els[0].color = (0.9, 0.25, 0.4, 1)          # tongue
els[1].position = 0.28; els[1].color = (0.02, 0.03, 0.06, 1)       # dark inside
e3 = els.new(0.68); e3.color = (1.0, 1.0, 1.0, 1)                # teeth
nt.links.new(tc.outputs["UV"], sx.inputs[0]); nt.links.new(sx.outputs["Y"], cr.inputs[0])
nt.links.new(cr.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs[0], o_.inputs["Surface"])
me.materials.append(LIPM); me.materials.append(INM)
MOUTH.shape_key_add(name="Basis")
for k, p in MPOSE.items():
    if k == "Basis": continue
    sk = MOUTH.shape_key_add(name=k, from_mix=False)
    for i, v in enumerate(_verts(p)): sk.data[i].co = v
def MK(t, **vals):
    for k in ("talk", "shout", "O", "smile", "frown"):
        kb = MOUTH.data.shape_keys.key_blocks[k]; kb.value = vals.get(k, 0.0); kb.keyframe_insert("value", frame=KT(t))
_dk = bpy.data.materials.get("dark")
VISM = MT("visorM", (0.004, 0.005, 0.008), 0.12)
_set(VISM, **{"Coat Weight": 1.0, "Coat Roughness": 0.03})
_vis.data.materials.clear(); _vis.data.materials.append(VISM)
MOUTH.visible_diffuse = False; MOUTH.visible_glossy = False
for _o in bpy.data.objects:
    if _o.type == "LIGHT": _o.visible_camera = False; _o.visible_glossy = False if _o.name in ("FACE", "RIMc", "RIMm") else _o.visible_glossy
_fc = bpy.data.objects["FACE"]; _fc.data.shadow_soft_size = 0.04; _fc.location = (0, -0.7, 0.62)
