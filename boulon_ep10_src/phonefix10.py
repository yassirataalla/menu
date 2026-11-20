from mathutils import Euler
# re-aim the phone insert per frame on the final (eased) animation; deeper focus for that shot
_fa, _fb = F(SCR), F(12.0) - 1
_pk = []
for _f in range(_fa, _fb + 1):
    scene.frame_set(_f); _mw = MPH.matrix_world; _p = _mw.translation.copy()
    _n = (_mw.to_3x3() @ Vector((0, -1, 0))).normalized(); _u = (_mw.to_3x3() @ Vector((0, 0, 1))).normalized()
    _d = 0.40 - 0.06 * (_f - _fa) / max(1, _fb - _fa)
    _q = (_mw.to_3x3().normalized() @ Euler((math.radians(90), 0, 0)).to_matrix()).to_euler()
    _pk.append((_f, tuple(_p + _n * _d + _u * 0.02), tuple(_p), _d, _q))
_tc = cam.constraints[0]
for _f, _v in ((1, 1.0), (_fa - 1, 1.0), (_fa, 0.0), (_fb, 0.0), (_fb + 1, 1.0)):
    _tc.influence = _v; _tc.keyframe_insert("influence", frame=_f)
for _f, _c, _g, _d, _q in _pk:
    key(cam, _f, loc=_c); key(target, _f, loc=_g); cam.rotation_euler = _q; cam.keyframe_insert("rotation_euler", frame=_f)
    cam_d.dof.focus_distance = _d; cam_d.dof.keyframe_insert("focus_distance", frame=_f)
for _f, _v in ((1, 2.0), (_fa - 1, 2.0), (_fa, 5.6), (_fb, 5.6), (_fb + 1, 2.0)):
    cam_d.dof.aperture_fstop = _v; cam_d.dof.keyframe_insert("aperture_fstop", frame=_f)
for _o in (cam, target, cam_d):
    for _fc in all_fcurves(_o):
        for _kp in _fc.keyframe_points:
            if _fa - 1 <= int(round(_kp.co[0])) <= _fb + 1: _kp.interpolation = "CONSTANT"
cam.rotation_euler = (0, 0, 0); cam.keyframe_insert("rotation_euler", frame=_fa - 1); cam.keyframe_insert("rotation_euler", frame=_fb + 1)
for _fc in all_fcurves(cam):
    if _fc.data_path == "rotation_euler":
        for _kp in _fc.keyframe_points: _kp.interpolation = "CONSTANT"
