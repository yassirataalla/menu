import sys, runpy, bpy
script, out, a, b = sys.argv[-4:]
sys.argv = ["x", "--", out, "CYCLES"]
runpy.run_path(script)
s = bpy.context.scene
s.render.filepath = out
s.render.use_overwrite = False
s.frame_start, s.frame_end = int(a), min(int(b), s.frame_end)
bpy.ops.render.render(animation=True)
