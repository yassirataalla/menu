# ---- look upgrade: glossy toy plastic, chrome, reflective floor, rim lights, shallow DOF ----
def _set(m, **kw):
    b = BS(m)
    for k, v in kw.items():
        if k in b.inputs: b.inputs[k].default_value = v
def _M_(n): return bpy.data.materials.get(n)
for n in ("robot",):
    m = _M_(n)
    if m: _set(m, **{"Roughness": 0.28, "Coat Weight": 1.0, "Coat Roughness": 0.04, "Specular IOR Level": 0.6})
for n in ("metal",):
    m = _M_(n)
    if m: _set(m, **{"Metallic": 0.95, "Roughness": 0.16, "Base Color": (0.85, 0.86, 0.9, 1)})
m = _M_("dark")
if m: _set(m, **{"Roughness": 0.08, "Coat Weight": 1.0, "Coat Roughness": 0.0})
for n in ("b0", "b1", "b2", "bulb"):
    m = _M_(n)
    if m: _set(m, **{"Roughness": 0.15, "Coat Weight": 1.0, "Coat Roughness": 0.02})
m = _M_("floor")
if m: _set(m, **{"Roughness": 0.12, "Coat Weight": 0.8, "Coat Roughness": 0.03})
for n in ("wood", "wood2"):
    m = _M_(n)
    if m: _set(m, **{"Roughness": 0.3, "Coat Weight": 0.6, "Coat Roughness": 0.08})
for n in ("sheet", "duvet", "pillow", "curtain", "rug", "cloth"):
    m = _M_(n)
    if m: _set(m, **{"Sheen Weight": 1.0, "Sheen Roughness": 0.4, "Sheen Tint": (0.75, 0.85, 1.0, 1)})
_rc = bpy.data.collections.new("BotRecv"); scene.collection.children.link(_rc)
def _kids(o):
    for c in o.children:
        yield c; yield from _kids(c)
for o in _kids(B.root):
    if o.type in ("MESH", "FONT", "CURVE"): _rc.objects.link(o)
_fl = bpy.data.objects.get("FACE")
if _fl: _fl.visible_glossy = False
# rim lights that follow Boulon (he faces -Y), so his silhouette always pops from the dark room
for nm, x, col, e in (("RIMc", 0.95, (0.35, 0.8, 1.0), 70), ("RIMm", -0.95, (1.0, 0.4, 0.75), 50)):
    rl = light(nm, "AREA", (0, 0, 0), None, e, col, 0.6); rl.parent = B.root; rl.location = (x, 1.1, 2.1)
    rl.rotation_euler = (Vector((0, 0, 1.55)) - Vector((x, 1.1, 2.1))).to_track_quat("-Z", "Y").to_euler()
    rl.data.spread = math.radians(60); rl.light_linking.receiver_collection = _rc; rl.visible_glossy = False
cam_d.dof.aperture_fstop = float(os.environ.get("FSTOP", "1.8")); cam_d.dof.aperture_blades = 7
scene.cycles.samples = int(os.environ.get("SAMPLES", "12")); scene.cycles.max_bounces = 4
scene.cycles.glossy_bounces = 3; scene.cycles.use_denoising = True; scene.cycles.denoising_quality = "HIGH"
