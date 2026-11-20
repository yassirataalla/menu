for i, (t0, ln, c0, g0, c1, g1) in enumerate(SHOTS):
    f0 = F(t0) if i else 1; f1 = (F(SHOTS[i + 1][0]) - 1) if i + 1 < len(SHOTS) else NF
    if i: CUTF.add(f0 - 1)
    for f, c, g in ((f0, c0, g0), (f1, c1, g1)):
        key(cam, f, loc=c); key(target, f, loc=g)
        cam_d.dof.focus_distance = (Vector(c) - Vector(g)).length; cam_d.dof.keyframe_insert("focus_distance", frame=f)
        cam_d.lens = ln; cam_d.keyframe_insert("lens", frame=f)

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
