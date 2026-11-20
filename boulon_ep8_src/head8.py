import bpy, math, sys
from mathutils import Vector

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/frames/f_"
ENGINE = sys.argv[sys.argv.index("--") + 2] if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 2 else "CYCLES"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
import json as _j
TIMELINE = '/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep8/timeline.json'
FPS = 24
END = _j.load(open(TIMELINE))['frames']
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, END


# ---------- helpers ----------
def mat(name, color, rough=0.5, emit=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = 0.0
    return m


def give(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj


def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True


def bevel(obj, w=0.05, seg=4):
    mod = obj.modifiers.new("bev", "BEVEL")
    mod.width, mod.segments = w, seg


def cube(name, loc, scale, m, bev=0.05, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name, o.scale = name, scale
    bpy.ops.object.transform_apply(scale=True)
    if bev:
        bevel(o, bev)
    give(o, m)
    if parent:
        o.parent = parent
    return o


def sphere(name, loc, r, m, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    o = bpy.context.object
    o.name, o.scale = name, scale
    smooth(o)
    give(o, m)
    if parent:
        o.parent = parent
    return o


def cyl(name, loc, r, d, m, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=24)
    o = bpy.context.object
    o.name = name
    smooth(o)
    give(o, m)
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
    o.location = loc
    return o


def key(obj, frame, loc=None, rot=None, scale=None):
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert("location", frame=frame)
    if rot is not None:
        obj.rotation_euler = [math.radians(a) for a in rot]
        obj.keyframe_insert("rotation_euler", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert("scale", frame=frame)


def ease_all():
    for o in bpy.data.objects:
        ad = o.animation_data
        if ad and ad.action:
            for layer in getattr(ad.action, "layers", []):
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        for fc in cb.fcurves:
                            for kp in fc.keyframe_points:
                                kp.interpolation = "BEZIER"
                                kp.easing = "AUTO"


