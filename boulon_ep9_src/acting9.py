
# =====================================================================
#                     EPISODE 9 — « Vu »  (35 s, loops)
# =====================================================================
def sit(t, x, y, rzz, lean=0.0, dz=0.0): B.R3(t, (x, y, 0.5 + dz), (lean, 0, rzz))
tA, tB, tC, tD, tE, tF, tG, tH = 0.0, 0.9, 1.7, 4.4, 6.0, 7.2, 9.4, 10.2
tI, tJ, tK, tL, tM, tN, tO = 12.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0
tP, tQ, tR, tS, tT, tU, tV, tW, TEND = 24.0, 25.8, 26.8, 28.5, 29.8, 31.0, 32.6, 33.6, 35.0

GREY = MT("phGrey", (0.5, 0.55, 0.65), 0.5, (0.5, 0.55, 0.7), 1.0)
HDR = MT("phHdr", (0.08, 0.1, 0.16), 0.5, (0.12, 0.16, 0.26), 1.0)
INPUT = MT("phIn", (0.75, 0.77, 0.84), 0.5, (0.75, 0.78, 0.86), 0.45)
PINK = MT("pinkE", (1, 0.3, 0.5), 0.4, (1.0, 0.25, 0.45), 6.0)
TXTW = MT("phTxtW", (1, 1, 1), 0.5, (1, 1, 1), 1.2)

def chat(name, title, bubbles, extra=None):
    """bubbles: list of (side, lines, y)  side 'R' green (me) / 'L' white (them)"""
    g = grp(name, parent=PH)
    cube(name + "hdr", (0, 0.192, 0.0155), (0.118, 0.03, 0.001), HDR, 0, g)
    txt(name + "ttl", title, (0, 0.19, 0.0175), 0.026, TXTW, g, rot=(0, 0, 0), ext=0.0005)
    sphere(name + "av", (-0.085, 0.19, 0.0165), 0.017, PINK if title != "Maman" else MT("avM", (0.9, 0.7, 0.3), 0.5, (0.9, 0.7, 0.3), 1.5), (1, 1, 0.2), g)
    for side, lines, y in bubbles:
        w = max(len(l) for l in lines) * 0.0074 + 0.014; h = len(lines) * 0.019 + 0.012
        x = 0.112 - w if side == "R" else -0.112 + w
        cube(name + "bub", (x, y, 0.016), (w, h, 0.001), BUBG if side == "R" else BUBW, 0.004, g)
        phtext(g, lines, y + (len(lines) - 1) * 0.0185, 0.028, INK, x, 0.037)
    return g

def inbox(name, body):
    g = grp(name, parent=PH)
    cube(name + "box", (0, -0.192, 0.016), (0.108, 0.02, 0.001), INPUT, 0.006, g)
    if body: txt(name + "t", body, (0, -0.192, 0.0175), 0.02, INK, g, rot=(0, 0, 0), ext=0.0005)
    return g

LINA = chat("cLina", "Lina", [("R", ["tu fais quoi", "ce soir ?"], 0.088)])
gVu = grp("gVu", parent=PH); txt("vuT", "Vu 23:47", (0.07, 0.03, 0.0175), 0.019, GREY, gVu, rot=(0, 0, 0), ext=0.0005)
gDots = grp("gDots", parent=PH); cube("dotsB", (-0.065, -0.02, 0.016), (0.045, 0.02, 0.001), BUBW, 0.006, gDots)
DOTS = [sphere(f"dot{i}", (-0.085 + i * 0.02, -0.02, 0.0175), 0.0068, GREY, (1, 1, 0.3), gDots) for i in range(3)]
DRAFT = [("", tI, tI + 0.25), ("tu", tI + 0.25, tI + 0.6), ("tu dors ?", tI + 0.6, tI + 1.0), ("tu dors ? je", tI + 1.0, tI + 1.35),
         ("tu dors ? je pense", tI + 1.35, tI + 1.55), ("tu dors ? je", tI + 1.55, tI + 1.65), ("tu", tI + 1.65, tI + 1.72), ("", tI + 1.72, tK + 0.12),
         ("h", tK + 0.12, tK + 0.25), ("haha", tK + 0.25, tK + 0.8), ("ha", tK + 0.8, tK + 0.88), ("", tK + 0.88, tM + 0.15), ("?", tM + 0.15, tN)]
for i, (body, a, b) in enumerate(DRAFT): V(inbox(f"in{i}", body), (a, b))
V(inbox("inW", ""), (tA, tI), (tW, None))
MOM = chat("cMom", "Maman", [("L", ["rentre le", "linge,", "il pleut."], 0.075)])
gOk = grp("cOk", parent=PH); cube("okB", (0.08, -0.04, 0.016), (0.03, 0.02, 0.001), BUBG, 0.004, gOk); phtext(gOk, ["ok"], -0.04, 0.023, INK, 0.08); gOkIn = inbox("inOk", "ok")
V(LINA, (tA, tR), (tW, None)); V(gVu, (tA, tR), (tW, None)); V(gDots, (tE, tG)); V(MOM, (tR, tW)); V(gOkIn, (tU + 0.25, tU + 0.75)); V(gOk, (tU + 0.75, tW))
for i, d in enumerate(DOTS):
    t = tE
    while t < tG:
        K(d, t + i * 0.12, loc=(-0.085 + i * 0.02, -0.02, 0.0175)); K(d, t + i * 0.12 + 0.15, loc=(-0.085 + i * 0.02, -0.012, 0.0175)); K(d, t + i * 0.12 + 0.3, loc=(-0.085 + i * 0.02, -0.02, 0.0175)); t += 0.6

# heart eyes + floating hearts
HE = grp("heartEyes", parent=B.head)
for x in (-0.12, 0.12): heart("hEye", (x, -0.325, 0.3), 0.075, PINK, HE)
V(HE, (tF, tG), (tP + 1.0, tR))
FH = []
for i in range(5):
    hg = grp(f"fhg{i}", (0, 0, -20)); heart(f"fh{i}", (0, 0, 0), 0.09 + 0.03 * (i % 2), PINK, hg); FH.append(hg)
STAND = (0.2, 0.0, 0.92)
for i, h in enumerate(FH):
    t0 = tF + 0.15 + i * 0.35; x0 = STAND[0] + (-0.5 if i % 2 else 0.5) * (0.6 + 0.2 * (i % 3))
    V(h, (t0, t0 + 1.4))
    K(h, t0, loc=(x0, -0.3, 2.6)); K(h, t0 + 1.4, loc=(x0 + (0.25 if i % 2 else -0.25), -0.35, 3.6)); LIN.append(h)

# ---------------- poses ----------------
SITP = (0.3, -0.95)
def sitf(t): sit(t, SITP[0], SITP[1], 0)
PH_CU = ((0.3, -1.78, 1.92), (62, 0, 180))
PH_HAND = ((0.7, -1.5, 1.82), (75, 0, 180))
SIT2 = (0.45, 1.1, 0.12, 248)
def sit2(t, lean=0.0): sit(t, SIT2[0], SIT2[1], SIT2[3], lean, SIT2[2])
FRONT2 = (math.sin(math.radians(160)), -math.cos(math.radians(160)))
HEAD2 = (SIT2[0], SIT2[1], 0.5 + SIT2[2] + 1.7)
PH_UP = ((SIT2[0], SIT2[1] - 0.42, HEAD2[2] - 0.38), (70, 0, 180))
def sit3(t): sit(t, SIT2[0], SIT2[1], 360, 0, SIT2[2])
PH_SHOW = ((-0.25, 0.88, 2.12), (82, 0, 175))
PH_DOWN = ((-0.3, 0.75, 1.1), (180, 0, 25))
PIL = ((-0.45, 2.55, 1.55), (-12, 0, 32))
LIE9 = ((0.2, 0.25, 1.2), (-90, 0, 0))

def phshot(t):
    PHK(t, PH_CU, 1.2, 0.12)

# defaults
PHK(1, PH_CU, 1.2, 0.12); PL(1, *PIL); PE(1, *NEUT); V(B.ckg, (tL, tM), (tP + 1.0, tR))
sitf(1); B.H(1, (0, 0, 0)); B.A(1, (-12, 6), (-80, -8)); B.E(1, 1.0); B.BR(1, 0, 0, 0); B.MO(1, 0, 1.0); lkey(FACE, 1, 6)
# A: phone (Vu)
# B: face, eyes widen
PHK(tB, PH_HAND, 9, 0.12); B.E(tB, 1.0); B.E(tB + 0.12, 1.5, 1.5, 1.25); B.BR(tB + 0.12, 0.045, 0.045, -10); B.MO(tB + 0.12, 0.05, 0.6)
# C: frozen, time passes
B.E(tC, 1.35, 1.35, 1.2); B.BR(tC, 0.03, 0.03, -6)
B.blink(3.2, 1.35)
K(B.rig, tC, sc=(1, 1, 1)); K(B.rig, tD, sc=(1, 1, 0.97)); B.H(tC, (0, 0, 0)); B.H(tD, (8, 0, 0))
# D: clock insert
# E: dots!
phshot(tE)
# F: jumps on the bed
PHK(tF, ((STAND[0] + 0.4, -0.55, 2.4), (90, 0, 180)), 9, 0.12)
B.R3(tF, STAND, (0, 0, 0)); B.A(tF, (-165, 25), (-165, -25)); B.H(tF, (-12, 0, 0)); B.BR(tF, 0.05, 0.05, 0); B.MO(tF, 0.35, 1.4)
B.E(F(tF) - 1, 1.35, 1.35, 1.2); B.E(tF, 1, 1, 0.001); B.E(F(tG) - 1, 1, 1, 0.001); B.E(tG, 1.0); CUTF.update({F(tF) - 1, F(tG) - 1})
for i in range(5):
    t = tF + 0.2 + i * 0.42
    K(B.root, t, loc=STAND); K(B.root, t + 0.2, loc=(STAND[0], STAND[1], STAND[2] + 0.28)); K(B.root, t + 0.4, loc=STAND)
    B.A(t, (-165, 25), (-165, -25)); B.A(t + 0.2, (-175, 40), (-175, -40))
K(B.root, tG, loc=STAND)
# G: dots vanish (phone CU)
phshot(tG)
# H: falls back on the bed
B.R3(tH, STAND, (0, 0, 0)); B.A(tH, (-150, 25), (-150, -25)); B.E(tH, 0.55); B.BR(tH, -0.01, -0.01, -12); B.MO(tH, 0.0, 0.8); B.H(tH, (0, 0, 0))
PHK(tH, ((STAND[0] + 0.45, -0.5, 2.35), (90, 0, 180)), 6, 0.12)
B.R3(10.55, STAND, (6, 0, 0)); B.R3(10.95, (STAND[0], 0.15, 1.25), (-90, 0, 0)); B.R3(11.1, (STAND[0], 0.18, 1.33), (-90, 0, 0)); B.R3(11.3, (STAND[0], 0.2, 1.22), (-90, 0, 0))
B.A(10.95, (-170, 30), (-170, -30)); B.A(11.3, (-175, 60), (-175, -60)); B.E(11.3, 0.3); PHK(10.95, ((STAND[0] + 0.7, 0.3, 1.2), (0, 0, 30)), 6, 0.12)
# I..N: draft / face
for t in (tI, tK, tM): phshot(t); sitf(t); B.A(t, (-12, 6), (-80, -8))
for t in (tJ, tL, tN): sitf(t); PHK(t, PH_HAND, 9, 0.12); B.A(t, (-12, 6), (-80, -8))
B.E(tJ, 0.6, 0.6, 1.15); B.BR(tJ, -0.02, -0.02, 14); B.MO(tJ, 0.02, 0.8); B.H(tJ, (0, 0, 0)); B.E(tJ + 0.5, 0.45, 0.45, 1.2); B.H(tJ + 0.5, (-6, 0, 0))
B.E(tL, 0.12, 0.12, 1.25); B.BR(tL, 0.01, 0.01, 10); B.MO(tL, 0.45, 2.1); B.H(tL, (0, 4, 0)); B.H(tL + 0.4, (0, -4, 0)); B.H(tL + 0.8, (0, 3, 0))
B.E(tN, 0.6, 0.6, 1.0); B.BR(tN, 0.035, 0.035, -10); B.MO(tN, 0.08, 0.6); B.H(tN, (0, 0, 0)); B.H(tN + 0.45, (0, 0, 0)); B.H(tN + 0.75, (0, 0, 28)); B.E(tN + 0.75, 0.9)
# O: shows the pillow
sit2(tO); B.H(tO, (0, 0, 0)); B.A(tO, (-12, 6), (-70, -8)); B.E(tO, 1.0); B.BR(tO, 0.03, 0.03, -6); B.MO(tO, 0.05, 0.8); PH_O = ((-0.15, 0.84, 1.72), (70, 0, 68)); PHK(tO, PH_O, 9, 0.12)
B.AR(19.4, (-70, -8)); B.AR(19.8, (-115, -15)); PHK(19.4, PH_O, 9, 0.12); PHK(19.8, PH_SHOW, 9, 0.12); B.MO(19.8, 0.3, 1.0); B.BR(19.8, 0.05, 0.05, -8)
PE(19.9, *NEUT); PE(20.1, *JUDGE)
for i in range(8):
    t = 20.1 + i * 0.2; PL(t, PIL[0], (PIL[1][0], 0, PIL[1][2] + (16 if i % 2 else -16)))
PL(21.75, *PIL)
B.E(21.6, 1.0); B.E(21.9, 0.45, 0.45, 1.1); B.BR(21.9, -0.015, -0.015, -14); B.MO(21.9, 0.0, 0.7); B.H(21.9, (18, 0, 0))
B.AR(21.9, (-115, -15)); B.AR(22.5, (-40, -15)); PHK(21.9, PH_SHOW, 9, 0.12); PHK(22.5, PH_DOWN, 0, 0.0)
K(B.rig, 21.9, sc=(1, 1, 1)); K(B.rig, 22.4, sc=(1.02, 1.02, 0.95)); K(B.rig, 23.4, sc=(1, 1, 0.97)); sit2(22.7); sit3(23.3); B.H(23.3, (16, 0, 0))
PE(22.6, *JUDGE); PE(22.9, *KIND); PL(22.9, *PIL); PL(23.2, PIL[0], (PIL[1][0] - 10, 0, PIL[1][2])); PL(23.5, *PIL); PL(23.8, PIL[0], (PIL[1][0] - 10, 0, PIL[1][2])); PL(24.1, *PIL)
# P: buzz!
for i in range(8):
    t = tP + 0.05 + i * 0.07; d = 0.025 if i % 2 else -0.025
    PHK(t, ((PH_DOWN[0][0] + d, PH_DOWN[0][1], PH_DOWN[0][2] + abs(d) * 0.5), PH_DOWN[1]), 3.0, 0.0)
PHK(tP + 0.65, PH_DOWN, 3.0, 0.0); PHK(tP + 0.75, PH_DOWN, 0, 0.0)
B.H(tP, (18, 0, 0)); B.E(tP, 0.45, 0.45, 1.1)
B.H(tP + 0.3, (14, 0, -30)); B.E(tP + 0.3, 1.45, 1.45, 1.2); B.BR(tP + 0.3, 0.05, 0.05, -10); B.MO(tP + 0.3, 0.3, 0.8); K(B.rig, tP + 0.3, sc=(1, 1, 1.04))
B.AR(tP + 0.55, (-40, -15)); B.AR(tP + 0.8, (-30, 25)); PHK(tP + 0.8, PH_DOWN, 0, 0.0); PHK(tP + 1.0, PH_UP, 9, 0.12)
B.A(tP + 1.0, (-95, 30), (-95, -30)); B.H(tP + 1.0, (0, 0, 0)); B.MO(tP + 1.0, 0.5, 1.2); B.BR(tP + 1.0, 0.06, 0.06, 0)
B.E(F(tP + 1.0) - 1, 1.45, 1.45, 1.2); B.E(tP + 1.0, 1, 1, 0.001); B.E(F(tR) - 1, 1, 1, 0.001); CUTF.update({F(tP + 1.0) - 1})
for i in range(4): K(B.root, tP + 1.1 + i * 0.4, loc=(SIT2[0], SIT2[1], 0.62)); K(B.root, tP + 1.3 + i * 0.4, loc=(SIT2[0], SIT2[1], 0.69))
# R: mom
phshot(tR)
# S: blank
sit3(tS); PHK(tS, PH_UP, 9, 0.12); B.A(tS, (-95, 30), (-95, -30)); B.E(tS, 0.1, 0.1, 1.25); B.BR(tS, 0.0, 0.0, 0); B.MO(tS, 0.0, 0.9); B.H(tS, (0, 0, 0))
B.E(tS + 0.9, 0.1, 0.1, 1.25); B.E(tS + 1.1, 0.1, 0.1, 1.25)
# T: thunder
for t, e in ((tT, 3.2), (tT + 0.08, 60), (tT + 0.2, 6), (tT + 0.3, 45), (tT + 0.55, 3.2)): lkey(MOON, F(t), e)
lkey(MOON, 1, 3.2); lkey(MOON, F(tT) - 1, 3.2)
for t, s_ in ((tT, 1.0), (tT + 0.08, 12.0), (tT + 0.2, 2.0), (tT + 0.3, 9.0), (tT + 0.55, 1.0)): emis_key(SKY, F(t), s_)
emis_key(SKY, 1, 1.0); emis_key(SKY, F(tT) - 1, 1.0)
PE(tT, *BORED); B.E(tT + 0.1, 0.1, 0.1, 1.25); B.H(tT + 0.4, (8, 0, 0))
# U: ok
phshot(tU)
# V: sigh, looks down
sit3(tV); PHK(tV, PH_UP, 9, 0.12); B.A(tV, (-95, 30), (-95, -30)); B.E(tV, 0.35, 0.35, 1.15); B.BR(tV, -0.01, -0.01, -14); B.MO(tV, 0.02, 0.8)
K(B.rig, tV, sc=(1, 1, 1)); K(B.rig, tV + 0.4, sc=(1.02, 1.02, 0.95)); B.H(tV, (0, 0, 0)); B.H(tV + 0.6, (16, 0, 0)); B.E(tV + 0.6, 0.6, 0.6, 1.1)
# W: back to Lina (loops to A)
phshot(tW)

# =====================================================================
#                              CAMERA
# =====================================================================
target = empty("target", (0, 0, 1.15))
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 32; cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 4.0
cam = bpy.data.objects.new("cam", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = target
PCU = PH_CU[0]
CU = ((0.3, -1.29, 2.21), PCU, (0.3, -1.33, 2.19), PCU)
HD1 = (SITP[0], SITP[1], 2.18)
FACE1 = ((0.3, -2.6, 2.1), (0.3, -0.95, 2.05), (0.3, -2.4, 2.1), (0.3, -0.95, 2.05))
HDQ = (HEAD2[0], HEAD2[1], HEAD2[2] - 0.12)
FACE2 = ((HEAD2[0], HEAD2[1] - 1.75, HEAD2[2] - 0.05), HDQ, (HEAD2[0], HEAD2[1] - 1.55, HEAD2[2] - 0.05), HDQ)
WIDE = ((0.3, -3.9, 2.5), (0.2, 0.4, 1.75), (0.3, -3.6, 2.45), (0.2, 0.4, 1.75))
SHOTS = [  # (t0, lens, cam0, tgt0, cam1, tgt1)
 (tA, 30, *CU),
 (tB, 32, *FACE1),
 (tC, 26, (-1.3, -3.7, 1.95), (0.75, 0.6, 1.55), (-1.15, -3.45, 1.95), (0.75, 0.6, 1.55)),
 (tD, 40, (1.75, 1.5, 1.45), (2.3, 2.3, 1.22), (1.8, 1.6, 1.42), (2.3, 2.3, 1.22)),
 (tE, 30, *CU),
 (tF, 24, *WIDE),
 (tG, 30, *CU),
 (tH, 24, *WIDE),
 (tI, 30, *CU), (tJ, 32, *FACE1), (tK, 30, *CU), (tL, 32, *FACE1), (tM, 30, *CU), (tN, 32, *FACE1),
 (tO, 24, (-2.95, 0.35, 2.2), (0.0, 1.8, 1.6), (-2.8, 0.45, 2.18), (0.0, 1.8, 1.6)),
 (tP, 28, (0.3, -1.9, 2.15), (0.2, 1.0, 1.55), (0.3, -1.7, 2.15), (0.25, 1.0, 1.6)),
 (tQ, 32, *FACE2),
 (tR, 30, *CU),
 (tS, 32, *FACE2),
 (tT, 24, *WIDE),
 (tU, 30, *CU),
 (tV, 32, *FACE2),
 (tW, 30, *CU),
]
