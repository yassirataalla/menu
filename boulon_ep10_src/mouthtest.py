import sys, runpy, bpy, os
from mathutils import Vector
OUTD = sys.argv[-1]
sys.argv = ["x", "--", "/tmp/x", "CYCLES"]
g = runpy.run_path(os.environ.get("SCRIPT", "toys15.py"))
s = bpy.context.scene; s.frame_set(int(os.environ.get("FR", "30")))
B = g["B"]; MOUTH = g["MOUTH"]
keep = set()
def _k(o):
    keep.add(o.name)
    for c in o.children: _k(c)
_k(B.root)
for o in bpy.data.objects:
    if o.type in ("MESH", "FONT", "CURVE") and o.name not in keep and not o.name.startswith(("wall", "floor", "ceiling", "bed", "mattress", "headboard")): o.hide_render = True
bpy.data.objects["PHL"].hide_render = True
hm = B.head.matrix_world
cam = s.camera; cam.animation_data_clear(); cam.data.animation_data_clear()
for c in list(cam.constraints): cam.constraints.remove(c)
cam.location = hm @ Vector((0, -1.25, 0.27)); tgt = hm @ Vector((0, -0.3, 0.26))
cam.rotation_mode = "QUATERNION"; cam.rotation_quaternion = (tgt - cam.location).to_track_quat("-Z", "Y")
cam.data.lens = 55; cam.data.dof.use_dof = False
s.render.resolution_x = s.render.resolution_y = 560; s.render.resolution_percentage = 100
MOUTH.data.shape_keys.animation_data_clear()
KS = ("talk", "shout", "O", "smile", "frown")
poses = [("neutral", {}), ("talk", {"talk": 1}), ("smile", {"smile": 1}), ("shout", {"shout": 1}), ("O", {"O": 1}), ("frown", {"frown": 1})]
for i, (nm, v) in enumerate(poses):
    for k in KS: MOUTH.data.shape_keys.key_blocks[k].value = v.get(k, 0)
    s.render.filepath = f"{OUTD}/test_{i}_{nm}.png"; bpy.ops.render.render(write_still=True); print("DONE", nm)
