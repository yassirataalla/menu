import sys, runpy, bpy
out, a, b = sys.argv[-3:]
sys.argv = ["x", "--", out, "CYCLES"]
runpy.run_path("toys10.py")
s = bpy.context.scene
def em(n, c):
    m = bpy.data.materials.new(n); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*c, 1); o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0]); return m
R, G = em("pR", (1, 0, 0)), em("pG", (0, 1, 0))
for o in s.objects:
    if o.type in ("MESH", "CURVE", "FONT", "SURFACE", "META"): o.is_holdout = True
for name, body, size, loc in (("signE", "LE CÈDRE", 0.4, None), ("signI", "LE CÈDRE", 0.3, (1.25, 2.5, 3.3))):
    n = bpy.data.objects[name]; n.is_holdout = False; n.data.materials.clear(); n.data.materials.append(G)
    old = n.copy(); old.data = n.data.copy(); s.collection.objects.link(old)
    old.data.body = body; old.data.size = size; old.data.materials.clear(); old.data.materials.append(R)
    if loc: old.location = loc
    n.location.y -= 0.05
for l in [o for o in s.objects if o.type == "LIGHT"]: l.hide_render = True
s.world.use_nodes = False; s.world.color = (0, 0, 0)
s.render.film_transparent = True; s.view_settings.view_transform = "Standard"; s.view_settings.look = "None"
s.cycles.samples = 12; s.cycles.use_denoising = False; s.cycles.max_bounces = 0
s.render.image_settings.color_mode = "RGBA"; s.render.image_settings.compression = 15
s.render.filepath = out; s.render.use_overwrite = False
s.frame_start, s.frame_end = int(a), min(int(b), s.frame_end)
bpy.ops.render.render(animation=True)
