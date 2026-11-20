# ---- Maman: Boulon's mother (same robot family, pink, apron, hair curlers, lashes, earrings) ----
MOMB = MT("momBody", (0.78, 0.3, 0.55), 0.3); _set(MOMB, **{"Coat Weight": 1.0, "Coat Roughness": 0.04})
MOMH = MT("momHead", (0.93, 0.8, 0.86), 0.18); _set(MOMH, **{"Metallic": 0.9})
MEYE = MT("momEye", (0.1, 0.1, 0.1), 0.2, (0.3, 1.0, 0.9), 10)
MM = dict(body=MOMB, head=MOMH, metal=MOMH, eye=MEYE, bulb=MT("bulb"), hand=MOMB)
M = Bot("Maman", MM)
for o in list(M.head.children):
    if o.name in ("Mamanant", "Mamanantball"): o.hide_render = True; o.hide_viewport = True
M.mouth.hide_render = True; M.mouth.hide_viewport = True
_mv = [o for o in M.head.children if o.name.endswith("visor")][0]
_mv.scale = (1, 1, 0.17 / 0.14); _mv.location.z = 0.27 - 0.3 * (0.17 / 0.14)
_mv.data.materials.clear(); _mv.data.materials.append(VISM)
MMOUTH = MOUTH.copy(); MMOUTH.data = MOUTH.data.copy(); MMOUTH.name = "momMouth"; scene.collection.objects.link(MMOUTH)
MMOUTH.parent = M.head; MMOUTH.location = (0, -0.324, MOUTH_Z)
MMOUTH.data.materials.clear(); MMOUTH.data.materials.append(MEYE)
if MMOUTH.data.shape_keys and MMOUTH.data.shape_keys.animation_data: MMOUTH.data.shape_keys.animation_data_clear()
# eyelashes (children of the eyes so they blink with them)
for eye, sx in ((M.eyeL, -1), (M.eyeR, 1)):
    for k, ang in enumerate((25, 52, 80)):
        a = math.radians(ang); r0 = 0.068
        lb = cube(f"lash{sx}{k}", (0, 0, 0), (0.016, 0.004, 0.0045), MEYE, 0.002, eye)
        lb.location = (sx * r0 * math.cos(a) * 1.05, -0.02, r0 * math.sin(a) * 1.05); lb.rotation_euler = (0, -sx * a, 0)
# hair curlers on top of the head
CURL = [MT("curl1", (1.0, 0.45, 0.7), 0.35), MT("curl2", (0.65, 0.5, 1.0), 0.35), MT("curl3", (1.0, 0.85, 0.3), 0.35)]
for i, (x, y, z) in enumerate([(-0.19, -0.1, 0.6), (0.0, -0.1, 0.62), (0.19, -0.1, 0.6), (-0.1, 0.12, 0.61), (0.1, 0.12, 0.61)]):
    c = cyl(f"curler{i}", (0, 0, 0), 0.055, 0.15, CURL[i % 3], rot=(0, math.pi / 2, 0), parent=M.head); c.location = (x, y, z)
    for e in (-1, 1): ring = cyl(f"curlEnd{i}{e}", (0, 0, 0), 0.062, 0.012, MOMH, rot=(0, math.pi / 2, 0), parent=c); ring.location = (0, 0, e * 0.07)
# earrings
GOLD = MT("gold", (1.0, 0.75, 0.3), 0.15); _set(GOLD, **{"Metallic": 1.0})
for sx in (-1, 1):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.009, location=(0, 0, 0), rotation=(0, math.pi / 2, 0))
    er = bpy.context.object; er.name = f"earring{sx}"; give(er, GOLD); smooth(er); er.parent = M.head; er.location = (sx * 0.355, -0.02, 0.1)
# apron with pocket + heart
APR = MT("apron", (0.97, 0.93, 0.95), 0.6); _set(APR, **{"Sheen Weight": 0.6})
cube("apron", (0, 0, 0), (0.34, 0.012, 0.36), APR, 0.03, M.rig).location = (0, -0.335, 0.86)
cube("aprStrapL", (0, 0, 0), (0.025, 0.012, 0.09), APR, 0.005, M.rig).location = (-0.2, -0.335, 1.3)
cube("aprStrapR", (0, 0, 0), (0.025, 0.012, 0.09), APR, 0.005, M.rig).location = (0.2, -0.335, 1.3)
cube("aprPocket", (0, 0, 0), (0.15, 0.008, 0.09), MT("apronP", (1.0, 0.55, 0.72), 0.6), 0.02, M.rig).location = (0, -0.35, 0.7)
heart("aprHeart", (0, -0.36, 0.72), 0.05, MT("heartR", (0.95, 0.15, 0.3), 0.4), M.rig)
# fluffy slippers
SLIP = MT("slipper", (1.0, 0.6, 0.78), 0.9); _set(SLIP, **{"Sheen Weight": 1.0, "Sheen Roughness": 0.5})
for o in M.rig.children:
    if "foot" in o.name: o.data.materials.clear(); o.data.materials.append(SLIP)

