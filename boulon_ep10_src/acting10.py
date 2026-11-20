
# =====================================================================
#              EPISODE 10 — « Maman au téléphone »  (35 s, loops)
# =====================================================================
AB, AM = TL["ampB"], TL["ampM"]
DOORT, M1, M2, M3, M4, RINGT, SCR, M5, M6A = 1.3, 1.4, 3.8, 6.55, 10.65, 11.65, 11.7, 12.4, 16.7
SIL, TURN, B1, HOLD, HANGS, TB, M7, M8a, M8b, M8c, PLT, B2, TEND = 19.2, 20.2, 21.2, 22.8, 24.8, 26.8, 27.6, 29.2, 30.58, 31.52, 32.8, 33.0, 35.0
SITP = (0.3, -0.95); STANDP = (0.95, -1.95, 0.0)
MPOS = (-0.75, -2.65); MDOOR = (-1.6, -5.15); MHALL = (-1.6, -6.1)
YAW_TO_B = 148.3; YAW_DOOR = 155.0; YAW_CALL = -90.0
HB_MOM, HB_DOOR = -31.7, -25.0
def sit(t, lean=0.0): B.R3(t, (SITP[0], SITP[1], 0.5), (lean, 0, 0))
def MKX(obj, t, **vals):
    for k in ("talk", "shout", "O", "smile", "frown"):
        kb = obj.data.shape_keys.key_blocks[k]; kb.value = vals.get(k, 0.0); kb.keyframe_insert("value", frame=KT(t))
def lips(obj, arr, t0, t1, base, op, gain=1.0, step=2):
    for f in range(F(t0), F(t1) + 1, step):
        v = dict(base); v[op] = min(1.0, v.get(op, 0.0) + min(1.0, arr[min(len(arr) - 1, f - 1)] * gain)); MKX(obj, f, **v)
    MKX(obj, F(t1) + step, **base)
def MR(t, x, y, yaw, lean=0.0, z=0.0): M.R3(t, (x, y, z), (lean, 0, yaw))
ANGRY = dict(l=0.55, w=1.08); ANGBR = (-0.02, -0.02, 22)

# ---------------- defaults ----------------
PIL = ((-0.45, 2.55, 1.55), (-12, 0, 32))
PL(1, *PIL); PE(1, *NEUT); V(B.ckg, (0, 0.01))
PH_HAND = ((0.62, -1.5, 1.8), (75, 0, 180)); PH_HIDE = ((0.3, -1.42, 2.17), (90, 0, 180)); PH_LAP = ((0.35, -1.3, 1.45), (25, 0, 180))
sit(1); B.H(1, (0, 0, 0)); B.A(1, (-12, 6), (-80, -8)); B.E(1, 1.0); B.BR(1, 0, 0, 0); MKX(MOUTH, 1, smile=0.6); PHK(1, PH_HAND, 1.0, 0.0)
MR(1, *MHALL, YAW_DOOR); M.H(1, (0, 0, 0)); M.A(1, (0, 0), (0, 0)); M.E(1, *[ANGRY["l"]], w=ANGRY["w"]); M.BR(1, *ANGBR); MKX(MMOUTH, 1, frown=0.6)
lkey(GLOW, 1, 0); lkey(MFACE, 1, 5)
col_key(MEYE, 1, (0.3, 1.0, 0.9), "Emission Color")
V(MPH, (RINGT, TB + 0.25)); V(HALO, (M5 + 0.05, TB)); V(CARRY, (PLT, None))
for m in MESS: V(m, (0, PLT))
K(DOOR, 1, rot=(0, 0, 0)); K(DOOR, F(DOORT) - 1, rot=(0, 0, 0)); K(DOOR, DOORT + 0.08, rot=(0, 0, 112)); K(DOOR, DOORT + 0.22, rot=(0, 0, 94)); K(DOOR, DOORT + 0.36, rot=(0, 0, 101))
SHK = empty("shaker", (0, 0, 0))
def shake(t0, amp, n=6, dt=0.04):
    K(SHK, t0 - 0.01, loc=(0, 0, 0))
    for i in range(n):
        a = amp * (1 - i / n); K(SHK, t0 + i * dt, loc=(a * (1 if i % 2 else -1), 0, a * 0.6 * (1 if i % 3 else -1)))
    K(SHK, t0 + n * dt, loc=(0, 0, 0))
K(SHK, 1, loc=(0, 0, 0))

# ---------------- 0–1.4  Boulon laughs at a video ----------------
lips(MOUTH, AB, 0.0, 1.25, dict(smile=0.8), "talk", 0.8)
B.E(0.05, 0.18, 0.18, 1.2); B.BR(0.05, 0.03, 0.03, -6); B.H(0.05, (-8, 4, 0))
for i in range(4):
    t = 0.1 + i * 0.26; K(B.rig, t, sc=(1, 1, 1)); K(B.rig, t + 0.13, sc=(1.01, 1.01, 0.975)); B.H(t + 0.13, (-12, 2 if i % 2 else 6, 0))
K(B.rig, 1.2, sc=(1, 1, 1)); B.E(1.2, 0.18, 0.18, 1.2)
# door slam → startle
B.E(DOORT, 0.18, 0.18, 1.2); B.E(DOORT + 0.06, 1.55, 1.55, 1.25); B.BR(DOORT + 0.06, 0.06, 0.06, -10); MKX(MOUTH, DOORT, smile=0.5); MKX(MOUTH, DOORT + 0.06, O=0.9)
K(B.rig, DOORT, sc=(1, 1, 1)); K(B.rig, DOORT + 0.06, sc=(0.96, 0.96, 1.08)); K(B.rig, DOORT + 0.25, sc=(1, 1, 1))
sit(DOORT); K(B.root, DOORT + 0.08, loc=(SITP[0], SITP[1], 0.64)); sit(DOORT + 0.3); B.H(DOORT + 0.08, (0, 0, 0))
shake(DOORT, 0.05)
# ---------------- 1.4–3.8  « Boulon ! Boulon !!! » — he hides behind the phone ----------------
MR(DOORT + 0.05, *MHALL, YAW_DOOR); MR(M1, *MDOOR, YAW_DOOR)
M.A(M1, (0, 32), (0, -32)); M.E(M1, 0.55, w=1.08); M.BR(M1, *ANGBR); M.H(M1, (-6, 0, 0))
lips(MMOUTH, AM, M1, 3.78, dict(shout=0.25), "shout", 1.0)
for t in (1.55, 2.6): M.H(t, (6, 0, 0)); K(M.rig, t, sc=(1, 1, 1.05)); M.H(t + 0.3, (-4, 0, 0)); K(M.rig, t + 0.3, sc=(1, 1, 1))
PHK(M1, PH_HAND, 1.0, 0.0); PHK(M1 + 0.25, PH_HIDE, 1.0, 0.0); B.A(M1 + 0.25, (-95, 12), (-95, -12))
B.E(M1 + 0.25, 1.4, 1.4, 1.2); MKX(MOUTH, M1 + 0.25, O=0.5, frown=0.4)
K(B.rig, M1 + 0.25, sc=(1.02, 1.02, 0.93)); K(B.rig, 3.7, sc=(1.02, 1.02, 0.93))
for i in range(6): B.H(1.7 + i * 0.3, (0, 0, -3 if i % 2 else 3))
# ---------------- 3.8–6.5  « Ça fait TROIS JOURS… » — she walks in ----------------
lips(MMOUTH, AM, M2, 6.49, dict(shout=0.3), "shout", 1.0)
steps = 8
for i in range(steps + 1):
    u = i / steps; t = M2 + u * 2.6; x = MDOOR[0] + (MPOS[0] - MDOOR[0]) * u; y = MDOOR[1] + (MPOS[1] - MDOOR[1]) * u
    yaw = YAW_DOOR + (YAW_TO_B - YAW_DOOR) * u; MR(t, x, y, yaw, 0, 0.05 if i % 2 else 0.0)
    M.A(t, (-28 if i % 2 else 22, 8), (22 if i % 2 else -28, -8))
M.A(6.5, (-90, 0), (-20, -25)); M.E(M2, 0.5, w=1.08); M.BR(M2, *ANGBR)
PHK(M2, PH_HIDE, 1.0, 0.0); PHK(M2 + 0.35, PH_LAP, 1.0, 0.0); B.A(M2 + 0.35, (-30, 6), (-35, -6)); K(B.rig, M2 + 0.35, sc=(1, 1, 1))
B.H(M2 + 0.35, (4, 0, HB_DOOR)); B.E(M2 + 0.35, 1.25, 1.25, 1.15); B.BR(M2 + 0.35, 0.035, 0.035, -12); MKX(MOUTH, M2 + 0.35, frown=0.6)
B.H(4.9, (6, 0, -8)); B.H(5.4, (4, 0, HB_DOOR)); B.H(6.0, (8, 0, 10)); B.H(6.45, (4, 0, HB_MOM))   # eyes dart: mom → mess → mom
B.E(5.0, 1.2, 1.2, 1.1); B.blink(5.7, 1.2); MKX(MOUTH, 6.1, frown=0.7, O=0.15); MKX(MOUTH, 6.3, frown=0.6)   # gulp
# ---------------- 6.55–10.6  « Regarde-moi ce BORDEL… hôtel… » ----------------
lips(MMOUTH, AM, M3, 10.63, dict(shout=0.3), "shout", 1.05)
MR(M3, *MPOS, YAW_TO_B); M.A(M3, (-85, 0), (-20, -25)); M.H(M3, (0, 0, 40)); M.E(M3, 0.6, 0.45, 1.1)    # points at the mess
M.H(7.75, (-4, 0, 0)); M.A(7.75, (-100, 10), (-100, -10)); M.BR(7.75, -0.025, -0.025, 24)
for i in range(4): M.A(7.95 + i * 0.3, (-110 if i % 2 else -90, 10), (-90 if i % 2 else -110, -10))
M.A(9.2, (0, 34), (0, -34)); M.H(9.2, (0, -12, 0)); M.BR(9.2, -0.005, -0.03, 18)          # hands on hips, one brow up
M.blink(9.0, 0.6)
B.E(6.55, 1.2, 1.2, 1.1); B.H(6.9, (10, 0, 12)); B.H(7.6, (4, 0, HB_MOM))
B.E(9.15, 0.9, 0.9, 1.05); B.BR(9.15, -0.015, -0.015, -16); MKX(MOUTH, 9.15, frown=0.9); B.H(9.15, (10, 0, HB_MOM))
K(B.rig, 9.15, sc=(1, 1, 1)); K(B.rig, 9.6, sc=(1.02, 1.02, 0.94)); B.blink(9.9, 0.9)
# 10.65 « Tu te crois à l'hôtel ou— »
lips(MMOUTH, AM, M4, 11.6, dict(shout=0.35), "shout", 1.1, 1)
MR(M4, *MPOS, YAW_TO_B, 10); M.A(M4, (0, 34), (-90, -8)); M.H(M4, (-6, 0, 0)); M.E(M4, 0.42, w=1.12); M.BR(M4, -0.03, -0.03, 26)
# ---------------- 11.65 RING — frozen mid-word ----------------
MKX(MMOUTH, RINGT, shout=0.6); MKX(MMOUTH, 12.2, shout=0.6)
M.E(RINGT, 0.42, w=1.12); M.E(RINGT + 0.08, 1.2, w=1.0); M.BR(RINGT + 0.08, 0.02, 0.02, 0); M.H(RINGT + 0.08, (14, 0, 0))
M.A(RINGT, (0, 34), (-90, -8)); M.A(11.95, (0, 34), (-110, 0))
B.E(RINGT, 0.9, 0.9, 1.05); B.E(RINGT + 0.15, 1.25, 1.25, 1.1); B.BR(RINGT + 0.15, 0.04, 0.04, -6); MKX(MOUTH, RINGT + 0.15, smile=0.25)
MR(12.0, *MPOS, YAW_TO_B); MR(12.3, *MPOS, YAW_CALL)
# ---------------- 12.4–19.2  the angel voice ----------------
M.A(12.3, (0, 10), (-155, 0)); MKX(MMOUTH, 12.3, smile=1.0)
M.E(12.35, 1.2); M.E(M5, 0.14, w=1.22); M.BR(M5, 0.045, 0.045, -10); M.H(M5, (-4, 16, 0))
lips(MMOUTH, AM, M5 + 0.05, 16.6, dict(smile=0.85), "talk", 0.55)
col_key(MEYE, F(M5) - 1, (0.3, 1.0, 0.9), "Emission Color"); col_key(MEYE, F(M5), (1.0, 0.55, 0.85), "Emission Color")
lkey(GLOW, F(M5) - 1, 0); lkey(GLOW, F(M5), 160); lkey(MFACE, F(M5), 9)
for i, sg in enumerate(SPARKS):
    rs = []; t = M5 + 0.05 + (i % 5) * 0.11
    while t < TB - 0.1: rs.append((t, t + 0.35 + (i % 3) * 0.1)); t += 0.75 + (i % 4) * 0.13
    V(sg, *rs)
M.H(14.2, (-4, 10, 0)); M.H(15.4, (-6, 18, 0)); MR(13.5, *MPOS, YAW_CALL + 6); MR(15.0, *MPOS, YAW_CALL - 6)
lips(MMOUTH, AM, M6A, 19.2, dict(smile=0.9), "talk", 0.6)
M.A(M6A, (-165, -28), (-155, 0)); M.A(17.4, (-172, -20), (-155, 0)); M.A(18.1, (-165, -28), (-155, 0))   # plays with her curlers
M.H(M6A, (-8, 18, 0)); MR(M6A, *MPOS, YAW_CALL + 5); MR(18.6, *MPOS, YAW_CALL - 4)
B.E(M5, 1.5, 1.5, 1.2); B.BR(M5, 0.06, 0.06, -10); MKX(MOUTH, M5, O=0.7); B.H(M5, (0, 0, HB_MOM))
# ---------------- 19.2–24.8  « …des anges ?? » — the look to camera ----------------
MKX(MMOUTH, 19.25, smile=0.9)
B.E(SIL, 1.1, 1.1, 1.05); B.BR(SIL, 0.02, 0.02, 0); MKX(MOUTH, SIL, O=0.25); B.H(SIL, (0, 0, HB_MOM))
B.E(19.75, 1.1, 1.1, 1.05); B.E(19.85, 0.08, 0.08, 1.05); B.E(20.05, 1.0, 1.0, 1.05)           # one slow blink
B.H(TURN, (0, 0, HB_MOM)); B.H(TURN + 0.8, (0, 0, 0)); B.E(TURN + 0.8, 0.55, 0.55, 1.12); B.BR(TURN + 0.8, 0.05, -0.012, 0)
MKX(MOUTH, TURN, O=0.2); MKX(MOUTH, TURN + 0.8, frown=0.45)
lips(MOUTH, AB, B1, 22.8, dict(frown=0.4), "O", 0.7)
B.E(23.75, 0.55, 0.55, 1.12); B.E(23.85, 0.08, 0.08, 1.12); B.E(24.0, 0.55, 0.55, 1.12)
PE(B1, *JUDGE)
lips(MMOUTH, AM, HOLD, 26.8, dict(smile=0.9), "talk", 0.6)
# ---------------- 24.8–26.8  bisous + hang up ----------------
M.H(HANGS, (-6, 14, 0)); M.A(HANGS, (0, 10), (-155, 0))
M.A(26.0, (-140, -35), (-155, 0)); MKX(MMOUTH, 26.05, O=0.9); MKX(MMOUTH, 26.3, O=0.9); MKX(MMOUTH, 26.45, smile=0.9)
M.A(26.45, (-95, 10), (-155, 0)); M.A(TB, (0, 10), (-150, 0))
# ---------------- 26.8–27.6  the slow turn back ----------------
M.A(TB + 0.2, (0, 20), (-40, 0)); M.A(27.4, (0, 34), (0, -34))
MR(TB, *MPOS, YAW_CALL); MR(27.45, *MPOS, YAW_TO_B - 360)
M.E(TB, 0.14, w=1.22); M.E(TB + 0.25, 1.0, w=1.0); M.E(27.35, 0.42, w=1.12); M.BR(TB + 0.25, 0.0, 0.0, 0); M.BR(27.35, -0.03, -0.03, 26); M.H(TB + 0.25, (0, 0, 0))
MKX(MMOUTH, TB, smile=0.9); MKX(MMOUTH, TB + 0.35, smile=0.0); MKX(MMOUTH, 27.35, frown=0.8)
col_key(MEYE, F(TB) - 1, (1.0, 0.55, 0.85), "Emission Color"); col_key(MEYE, F(TB) + 2, (0.3, 1.0, 0.9), "Emission Color"); col_key(MEYE, F(27.3), (1.0, 0.02, 0.0), "Emission Color")
lkey(GLOW, F(TB) - 1, 160); lkey(GLOW, F(TB), 0); lkey(MFACE, F(TB), 5)
B.E(TB, 1.0, 1.0, 1.0); B.H(TB, (0, 0, HB_MOM)); MKX(MOUTH, TB, smile=0.5); MKX(MOUTH, TB + 0.6, smile=0.0, frown=0.2); B.E(27.3, 1.2, 1.2, 1.1)
# ---------------- 27.6–32.7  « Et les assiettes ?!!! TOUT. DE. SUITE. » ----------------
lips(MMOUTH, AM, M7, 29.0, dict(shout=0.4), "shout", 1.1, 1)
MR(M7, *MPOS, YAW_TO_B - 360, 12); M.A(M7, (-90, 0), (0, -34)); M.H(M7, (-8, 0, 0)); M.E(M7, 0.38, w=1.15); M.BR(M7, -0.035, -0.035, 28)
shake(M7, 0.02, 5)
for tw in (M8a, M8b, M8c):
    MR(tw - 0.06, *MPOS, YAW_TO_B - 360, 4); MR(tw, *MPOS, YAW_TO_B - 360, 16); MR(tw + 0.3, *MPOS, YAW_TO_B - 360, 8)
    M.H(tw - 0.06, (4, 0, 0)); M.H(tw, (-12, 0, 0)); MKX(MMOUTH, tw - 0.06, frown=0.6); shake(tw, 0.035, 6)
    M.A(tw, (-100, 0), (-100, 0)); M.A(tw + 0.3, (-80, 10), (-80, -10))
lips(MMOUTH, AM, M8a, 32.75, dict(shout=0.3), "shout", 1.2, 1)
B.E(M7, 1.6, 1.6, 1.25); B.BR(M7, 0.07, 0.07, -10); MKX(MOUTH, M7, O=1.0); K(B.root, M7 + 0.08, loc=(SITP[0], SITP[1], 0.68)); sit(M7 + 0.3)
# ---------------- 32.8–35  « Oui maman… j'arrive… » ----------------
CUTF.update({F(PLT) - 1}); sit(F(PLT) - 1); B.R3(PLT, STANDP, (0, 0, 0)); B.H(PLT, (6, 6, 0)); B.A(PLT, (-68, 22), (-68, -22))
B.E(PLT, 0.75, 0.75, 1.08); B.BR(PLT, -0.012, -0.012, -16); MKX(MOUTH, PLT, smile=0.95)
PHK(PLT, ((2.1, 2.05, 1.03), (180, 0, 25)), 0, 0.0)
lips(MOUTH, AB, B2, 34.7, dict(smile=0.85), "talk", 0.4)
for i in range(10):
    t = PLT + 0.05 + i * 0.2; K(CARRY, t, rot=(3 if i % 2 else -3, 4 if i % 3 else -4, 0)); B.H(t, (6, 6 if i % 2 else 3, 0))
B.blink(33.9, 0.75); MR(PLT, *MPOS, YAW_TO_B - 360); M.A(PLT, (0, 34), (0, -34)); M.E(PLT, 0.5, w=1.1)

# =====================================================================
#                              CAMERA
# =====================================================================
target = empty("target", (0, 0, 1.15))
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 32; cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 2.0
cam = bpy.data.objects.new("cam", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = target
cam.parent = SHK; target.parent = SHK
def rv(bot, t, dist, dz=0.0, dx=0.0, hz=1.67):
    scene.frame_set(F(t)); rm = bot.root.matrix_world
    return tuple(rm @ Vector((dx, -dist, hz + dz))), tuple(rm @ Vector((0, -0.3, hz + dz * 0.3)))
def phonev(t, d=0.36):
    scene.frame_set(F(t)); mw = MPH.matrix_world; p = mw.translation.copy(); n = (mw.to_3x3() @ Vector((0, -1, 0))).normalized()
    return tuple(p + n * d), tuple(p)
scene.frame_set(F(3.8)); _mh0 = tuple(M.root.matrix_world @ Vector((0, 0, 1.6)))
scene.frame_set(F(6.45)); _mh1 = tuple(M.root.matrix_world @ Vector((0, 0, 1.6)))
cE0, gE0 = rv(M, 7.75, 1.25, 0.0, 0.12); cE1, gE1 = rv(M, 9.1, 1.12, 0.0, 0.12)
cF0, gF0 = rv(B, 9.15, 1.3, 0.0, -0.3); cF1, gF1 = rv(B, 10.6, 1.2, 0.0, -0.3)
cG0, gG0 = rv(M, M4, 1.05, 0.02); cG1, gG1 = rv(M, 11.6, 0.95, 0.02)
cH0, gH0 = phonev(11.78, 0.36); cH1, gH1 = phonev(11.95, 0.31)
cI0, gI0 = rv(M, M5, 1.7, 0.05); cI1, gI1 = rv(M, 13.1, 0.95, 0.05); cI2, gI2 = rv(M, 16.6, 0.88, 0.05)
cJ0, gJ0 = rv(M, M6A, 2.1, -0.35, 0.2); cJ1, gJ1 = rv(M, 19.1, 1.9, -0.3, 0.2)
cL0, gL0 = rv(M, HANGS, 1.05, 0.03); cL1, gL1 = rv(M, 26.7, 0.98, 0.03)
cN1, gN1 = rv(M, 27.9, 1.35, 0.02)
cO, gO = rv(M, M8a - 0.1, 1.5, 0.02); cP, gP = rv(M, M8b - 0.1, 1.45, 0.02); cQ, gQ = rv(M, M8c - 0.1, 1.4, 0.02)
cR0, gR0 = rv(B, PLT, 1.75, -0.45); cR1, gR1 = rv(B, 34.9, 1.55, -0.42)
BOUL = (0.3, -0.95, 2.12); MHEAD = (MPOS[0], MPOS[1], 1.62)
SHOTS = [  # (t0, lens, cam0, tgt0, cam1, tgt1)
 (0.0, 32, (0.3, -2.55, 2.14), BOUL, (0.3, -2.4, 2.14), BOUL),
 (M1, 24, (1.65, 0.15, 2.55), (-1.6, -5.0, 1.35), (1.55, -0.05, 2.5), (-1.6, -5.0, 1.35)),
 (M2, 26, (0.85, -1.3, 1.95), _mh0, (0.8, -1.45, 1.95), _mh1),
 (M3, 28, (2.3, -3.3, 1.05), (1.15, -1.9, 0.2), (2.2, -3.1, 1.0), (1.15, -1.9, 0.2)),
 (7.75, 35, cE0, gE0, cE1, gE1),
 (9.15, 35, cF0, gF0, cF1, gF1),
 (M4, 35, cG0, gG0, cG1, gG1),
 (SCR, 40, cH0, gH0, cH1, gH1),
 (12.0, 30, cI0, gI0, cI1, gI1),
 (13.1, 30, cI1, gI1, cI2, gI2),
 (M6A, 30, cJ0, gJ0, cJ1, gJ1),
 (SIL, 34, (0.42, -2.45, 2.15), BOUL, (0.4, -2.22, 2.15), BOUL),
 (HANGS, 34, cL0, gL0, cL1, gL1),
 (TB, 30, (0.55, -1.35, 1.95), MHEAD, (0.47, -1.48, 1.93), MHEAD),
 (M7, 30, (0.47, -1.48, 1.93), MHEAD, cN1, gN1),
 (27.9, 34, cN1, gN1, cN1, gN1),
 (M8a, 38, cO, gO, cO, gO),
 (M8b, 46, cP, gP, cP, gP),
 (M8c, 56, cQ, gQ, cQ, gQ),
 (PLT, 34, cR0, gR0, cR1, gR1),
]
scene.frame_set(1)
