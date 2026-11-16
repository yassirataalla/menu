import json, sys, os, subprocess
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep6"
TL = json.load(open(D + "/timeline.json")); NF = TL["frames"]; DUR = NF / 24
TRK = json.load(open(D + "/track.json"))
WHITE, INK, YEL, NIGHT, GREEN, RED = "&HFFFFFF&", "&H20120B&", "&H26D4FF&", "&H26160E&", "&H73FF19&", "&H2D2DFF&"
BN, AR, FD, FB = "Noto Sans Bengali", "Noto Sans Arabic", "Poppins ExtraBold", "Poppins"
def ts(x):
    x = max(0, x); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
EV = []
def ev(a, b, text, layer=1): EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},Default,,40,40,0,,{text}")
def rrect(w, h, r):
    k = r * 0.45
    return (f"m {r} 0 l {w-r} 0 b {w-k} 0 {w} {k} {w} {r} l {w} {h-r} b {w} {h-k} {w-k} {h} {w-r} {h} "
            f"l {r} {h} b {k} {h} 0 {h-k} 0 {h-r} l 0 {r} b 0 {k} {k} 0 {r} 0")
FADE = "\\fad(160,160)"

# ---------- lyrics: Bengali (sung) + French ----------
LN = TL["lines"]; CY = 1012
for i, l in enumerate(LN):
    a, b = l["start"] - 0.12, l["end"] + 0.45
    if i + 1 < len(LN): b = min(b, LN[i + 1]["start"] - 0.14)
    ev(a, b, f"{{\\an2\\pos(360,{CY})\\fn{BN}\\b1\\fs44\\bord4\\3c{INK}\\shad2\\4c{INK}\\4a&H70&\\1c{WHITE}\\q0\\fad(110,90)}}{l['bn']}", 8)
    ev(a, b, f"{{\\an8\\pos(360,{CY + 10})\\fn{FB}\\b1\\fs31\\bord3.5\\3c{INK}\\shad1\\4c{INK}\\4a&H70&\\1c{YEL}\\q0\\fad(110,90)}}{l['fr']}", 8)

# ---------- title ----------
def card(a, b, y, w, h, col=NIGHT, alpha="&H18&", r=22):
    ev(a, b, f"{{\\an5\\pos(360,{y})\\bord0\\shad0\\1c{col}\\1a{alpha}\\p1{FADE}}}{rrect(w, h, r)}", 2)
def text(a, b, y, s, size, col=WHITE, font=FD, extra="", layer=3):
    ev(a, b, f"{{\\an5\\pos(360,{y})\\fn{font}\\fs{size}\\bord0\\shad0\\1c{col}{FADE}{extra}}}{s}", layer)
card(1.0, 6.2, 250, 560, 230)
text(1.1, 6.2, 178, "BOULON CHANTE", 26, YEL, extra="\\fsp4")
text(1.3, 6.2, 248, "ভাষার আড়ালে", 64, WHITE, BN, "\\b1")
text(1.5, 6.2, 322, "« Derrière la langue »", 32, WHITE, FB, "\\b1")
card(7.0, 12.2, 1090, 520, 84)
text(7.1, 12.2, 1076, "BOULON", 30, WHITE, extra="\\fsp2")
text(7.2, 12.2, 1108, "dans le rôle de Narayan, plongeur à Paris", 23, YEL, FB, "\\b1")
# time-lapse stamp
card(124.6, 135.6, 190, 360, 70)
text(124.7, 135.6, 190, "…toute la nuit", 28, WHITE, FB, "\\b1")
# outro
card(155.2, 159.6, 190, 440, 112, RED, "&H08&", 28)
text(155.3, 159.6, 172, "+ Abonne-toi", 34, WHITE)
text(155.4, 159.6, 212, "@boulon.lerobot2", 22, WHITE, FB, "\\b1")

# ---------- tracked 2D text on the 3D speech bubbles ----------
SHIFT_C = 1354   # chorus 2 reuses the chorus 1 frames
def tracked(name, s, font, col, k=0.17, fade=False, bord=0, dup=False):
    pts = TRK[name]; n = len(pts)
    for off in ((0, SHIFT_C) if dup else (0,)):
        for j, (f, x, y, ppm, sc) in enumerate(pts):
            size = max(1, ppm * k * (sc if not fade else 1.0))
            if sc < 0.05 and not fade: continue
            al = ""
            if fade:
                u = j / max(1, n - 1); a = int(255 * max(0.0, min(1.0, (u - 0.25) / 0.75))) if u > 0.25 else int(255 * (1 - u / 0.25) * 0.0)
                al = f"\\alpha&H{a:02X}&"; size *= 0.45 + 1.0 * u
            t0 = (f - 1 + off) / 24
            ev(t0, t0 + 1 / 24 + 0.001, f"{{\\an5\\pos({x:.1f},{y:.1f})\\fn{font}\\b1\\fs{size:.1f}\\bord{bord}\\3c{INK}\\shad0\\1c{col}{al}}}{s}", 6)
R = "\u200f"
tracked("bAr1", R + "يلا يلا!" + R, AR, INK); tracked("bAr2", R + "بسرعة!" + R, AR, INK, dup=True); tracked("bAr3", R + "خلّصنا!" + R, AR, INK, dup=True); tracked("bS1", R + "يلا!" + R, AR, INK, dup=True)
for i, w in enumerate(["আমি", "কথা", "গল্প", "ঘর", "মা"]):
    tracked(f"bn{i}", w, BN, "&HE6FF4D&", 0.2, fade=True, bord=2)

HEAD = f"""[Script Info]
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
open(D + "/ep6.ass", "w", encoding="utf8").write(HEAD + "\n".join(EV) + "\n")
print("ass events", len(EV))

def src_frame(f):
    if f <= 2246: return f
    if f == 2247: return 2246
    if f < 2435: return f - 591      # verse-2 couplet repeated (w1, w2)
    if f < 2977: return f - 1354     # chorus 2 = chorus 1
    return f
VF = f"ass={D}/ep6.ass,fade=t=in:st=0:d=0.5,fade=t=out:st={DUR-1.5:.2f}:d=1.4"
if len(sys.argv) > 3 and sys.argv[1] == "still":
    t = float(sys.argv[3])
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", sys.argv[2], "-vf", f"ass={D}/ep6.ass", "-ss", f"{t}", "-frames:v", "1", sys.argv[4]], check=True)
elif len(sys.argv) > 2:
    FR, OUT = sys.argv[1], sys.argv[2]; SEQ = D + "/seq"
    os.makedirs(SEQ, exist_ok=True)
    for f in range(1, NF + 1):
        dst = f"{SEQ}/f_{f:04d}.png"
        if os.path.lexists(dst): os.remove(dst)
        s = f"{FR}f_{src_frame(f):04d}.png"; assert os.path.exists(s), s
        os.symlink(s, dst)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-framerate", "24", "-i", SEQ + "/f_%04d.png", "-i", D + "/song.wav", "-vf", VF,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", "-movflags", "+faststart", OUT], check=True)
    print("done", OUT)
