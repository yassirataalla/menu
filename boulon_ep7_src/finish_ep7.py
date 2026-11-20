import json, sys, os, subprocess
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep7"
TL = json.load(open(D + "/timeline.json")); NF = TL["frames"]; DUR = NF / 24
TRK = json.load(open(D + "/track.json"))
WHITE, INK, YEL, NIGHT, RED, MINT = "&HFFFFFF&", "&H20120B&", "&H26D4FF&", "&H26160E&", "&H2D2DFF&", "&HB8FFC8&"
BN, AR, FD, FB = "Noto Sans Bengali", "Noto Sans Arabic", "Poppins ExtraBold", "Poppins"
def ts(x):
    x = max(0, x); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
EV = []
def ev(a, b, text, layer=1): EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},Default,,40,40,0,,{text}")
def rrect(w, h, r):
    k = r * 0.45
    return (f"m {r} 0 l {w-r} 0 b {w-k} 0 {w} {k} {w} {r} l {w} {h-r} b {w} {h-k} {w-k} {h} {w-r} {h} "
            f"l {r} {h} b {k} {h} 0 {h-k} 0 {h-r} l 0 {r} b 0 {k} {k} 0 {r} 0")
FADE = "\\fad(160,160)"; RLM = "‏"
# ---------- lyrics: Bengali (sung) + Arabic + French ----------
LN = TL["lines"]; CY = 985
for i, l in enumerate(LN):
    a, b = l["start"] - 0.1, l["end"] + 0.4
    if i + 1 < len(LN): b = min(b, LN[i + 1]["start"] - 0.12)
    ev(a, b, f"{{\\an2\\pos(360,{CY})\\fn{BN}\\b1\\fs41\\bord4\\3c{INK}\\shad2\\4c{INK}\\4a&H70&\\1c{WHITE}\\q0\\fad(110,90)}}{l['bn']}", 8)
    ev(a, b, f"{{\\an8\\pos(360,{CY + 4})\\fn{AR}\\b1\\fs43\\bord3.5\\3c{INK}\\shad1\\4c{INK}\\4a&H70&\\1c{MINT}\\q2\\fad(110,90)}}{RLM}{l['ar']}{RLM}", 8)
    ev(a, b, f"{{\\an8\\pos(360,{CY + 72})\\fn{FB}\\b1\\fs27\\bord3.5\\3c{INK}\\shad1\\4c{INK}\\4a&H70&\\1c{YEL}\\q0\\fad(110,90)}}{l['fr']}", 8)
def card(a, b, y, w, h, col=NIGHT, alpha="&H18&", r=22):
    ev(a, b, f"{{\\an5\\pos(360,{y})\\bord0\\shad0\\1c{col}\\1a{alpha}\\p1{FADE}}}{rrect(w, h, r)}", 2)
def text(a, b, y, s, size, col=WHITE, font=FD, extra="", layer=3):
    ev(a, b, f"{{\\an5\\pos(360,{y})\\fn{font}\\fs{size}\\bord0\\shad0\\1c{col}{FADE}{extra}}}{s}", layer)
card(0.8, 5.3, 1010, 600, 250)
text(0.9, 5.3, 930, "LIBAN SUR SEINE · LA CHANSON", 24, YEL, extra="\\fsp3")
text(1.1, 5.3, 1005, "মাথা নাড়ে নারায়ণ", 62, WHITE, BN, "\\b1")
text(1.3, 5.3, 1082, "« Narayan hoche la tête »", 30, WHITE, FB, "\\b1")
card(6.0, 10.2, 1060, 560, 84)
text(6.1, 10.2, 1046, "UNE JOURNÉE EN CUISINE", 27, WHITE, extra="\\fsp2")
text(6.2, 10.2, 1078, "avec Yasser, Kartik, le Chef… et Boulon dans le rôle de Narayan", 17, YEL, FB, "\\b1")
card(172.8, 180.2, 190, 440, 112, RED, "&H08&", 28)
text(172.9, 180.2, 172, "+ Abonne-toi", 34, WHITE)
text(173.0, 180.2, 212, "@boulon.lerobot2", 22, WHITE, FB, "\\b1")
text(176.6, 180.4, 640, "À demain !", 60, WHITE, FD, "\\bord4\\3c" + INK)
# ---------- tracked 2D text ----------
def tracked(name, s, font, col, k=0.17, bord=0, shifts=(0,), tag=False):
    for off in shifts:
        for (f, x, y, ppm, sc) in TRK[name]:
            if sc < 0.05: continue
            size = max(1, ppm * k * (1.0 if tag else sc)); t0 = (f - 1 + off) / 24
            ev(t0, t0 + 1 / 24 + 0.001, f"{{\\an5\\pos({x:.1f},{y:.1f})\\fn{font}\\b1\\fs{size:.1f}\\bord{bord}\\3c{INK}\\shad0\\1c{col}}}{s}", 6)
CH = (0, 1152, 2688)
tracked("bBn1", "শুধু বাংলা!", BN, INK, 0.2)
tracked("bAr1", RLM + "يلا يلا!!" + RLM, AR, INK, 0.2, shifts=CH)
tracked("bBn2", "হ্যাঁ হ্যাঁ!", BN, INK, 0.19)
tracked("bBn3", "হাঁস?", BN, INK, 0.2)
for nm, s in (("tagY", "YASSER"), ("tagK", "KARTIK"), ("tagC", "LE CHEF"), ("tagB", "NARAYAN")):
    tracked(nm, s, FD, YEL, 0.13, bord=3, tag=True)
HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00240F1A,&H80240F1A,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(D + "/ep7.ass", "w", encoding="utf8").write(HEAD + "\n".join(EV) + "\n")
print("ass events", len(EV))
def src_frame(f):
    if 1921 <= f <= 2496: return f - 1152     # chorus 2 = chorus 1
    if 3457 <= f <= 4032: return f - 2688     # chorus 3 = chorus 1
    if 2689 <= f <= 2880: return f - 1344     # dance break, twice
    if 2881 <= f <= 3072: return f - 1536
    return f
VF = f"ass={D}/ep7.ass,fade=t=in:st=0:d=0.5,fade=t=out:st={DUR-1.2:.2f}:d=1.1"
if len(sys.argv) > 3 and sys.argv[1] == "still":
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", sys.argv[2], "-vf", f"ass={D}/ep7.ass", "-ss", sys.argv[3], "-frames:v", "1", sys.argv[4]], check=True)
elif len(sys.argv) > 2:
    FR, OUT = sys.argv[1], sys.argv[2]; SEQ = D + "/seq"
    os.makedirs(SEQ, exist_ok=True)
    for f in range(1, NF + 1):
        dst = f"{SEQ}/f_{f:04d}.png"
        if os.path.lexists(dst): os.remove(dst)
        s = f"{FR}f_{src_frame(f):04d}.png"; assert os.path.exists(s), s
        os.symlink(s, dst)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-framerate", "24", "-i", SEQ + "/f_%04d.png", "-i", D + "/song.wav", "-vf", VF,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", "-movflags", "+faststart", OUT], check=True)
    print("done", OUT)
