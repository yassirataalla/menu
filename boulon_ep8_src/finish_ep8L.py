import json, sys, os, subprocess
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep8"
TL = json.load(open(D + "/timeline.json")); NF = TL["frames"]; DUR = NF / 24
WHITE, INK, YEL, NIGHT, RED, LIL = "&HFFFFFF&", "&H20120B&", "&H26D4FF&", "&H30140E&", "&H2D2DFF&", "&HFFB0C8&"
FD, FB = "Poppins ExtraBold", "Poppins"
def ts(x):
    x = max(0, x); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
EV = []
def ev(a, b, text, layer=1): EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},Default,,40,40,0,,{text}")
def rrect(w, h, r):
    k = r * 0.45
    return (f"m {r} 0 l {w-r} 0 b {w-k} 0 {w} {k} {w} {r} l {w} {h-r} b {w} {h-k} {w-k} {h} {w-r} {h} "
            f"l {r} {h} b {k} {h} 0 {h-k} 0 {h-r} l 0 {r} b 0 {k} {k} 0 {r} 0")
FADE = "\\fad(160,160)"
LN = TL["lines"]; CY = 968; CX = 960
for i, l in enumerate(LN):
    a, b = l["start"] - 0.1, l["end"] + 0.4
    if i + 1 < len(LN): b = min(b, LN[i + 1]["start"] - 0.1)
    ev(a, b, f"{{\\an2\\pos({CX},{CY})\\fn{FD}\\fs52\\bord5\\3c{INK}\\shad2\\4c{INK}\\4a&H70&\\1c{WHITE}\\q0\\fad(110,90)}}{l['fr']}", 8)
    ev(a, b, f"{{\\an8\\pos({CX},{CY + 10})\\fn{FB}\\b1\\fs40\\bord4\\3c{INK}\\shad1\\4c{INK}\\4a&H70&\\1c{YEL}\\q0\\fad(110,90)}}{l['en']}", 8)
def card(a, b, y, w, h, col=NIGHT, alpha="&H18&", r=22, x=960):
    ev(a, b, f"{{\\an5\\pos({x},{y})\\bord0\\shad0\\1c{col}\\1a{alpha}\\p1{FADE}}}{rrect(w, h, r)}", 2)
def text(a, b, y, s, size, col=WHITE, font=FD, extra="", layer=3, x=960):
    ev(a, b, f"{{\\an5\\pos({x},{y})\\fn{font}\\fs{size}\\bord0\\shad0\\1c{col}{FADE}{extra}}}{s}", layer)
card(0.8, 5.6, 880, 900, 300)
text(0.9, 5.6, 778, "BOULON · ÉPISODE 8", 34, YEL, extra="\\fsp3")
text(1.1, 5.6, 870, "3 HEURES DU MATIN", 84, WHITE)
text(1.3, 5.6, 968, "3 a.m. — my pillow knows everything", 38, LIL, FB, "\\b1")
card(170.0, 176.0, 130, 520, 132, RED, "&H08&", 32, x=1580)
text(170.1, 176.0, 108, "+ Abonne-toi", 44, WHITE, x=1580)
text(170.2, 176.0, 158, "@boulon.lerobot2", 30, WHITE, FB, "\\b1", x=1580)
text(170.6, 176.0, 930, "Et toi, tu penses à quoi à 3h ?", 56, WHITE, FD, "\\bord4\\3c" + INK)
text(170.8, 176.0, 1000, "What keeps YOU up at 3 a.m.?", 40, YEL, FB, "\\b1\\bord3\\3c" + INK)
HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00240F1A,&H80240F1A,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(D + "/ep8L.ass", "w", encoding="utf8").write(HEAD + "\n".join(EV) + "\n")
print("ass events", len(EV))
OFF = 1139
def src_frame(f):
    if 2050 <= f <= 2119 or 2191 <= f <= 2470: return f - OFF     # pre-chorus 2 (first half) + chorus 2 reuse chorus 1
    return f
VF = f"scale=1920:1080:flags=lanczos,ass={D}/ep8L.ass,fade=t=in:st=0:d=0.6,fade=t=out:st={DUR-0.45:.2f}:d=0.3"
if len(sys.argv) > 3 and sys.argv[1] == "still":
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", sys.argv[2], "-vf", f"scale=1920:1080:flags=lanczos,ass={D}/ep8L.ass", "-ss", sys.argv[3], "-frames:v", "1", sys.argv[4]], check=True)
elif len(sys.argv) > 2:
    FR, OUT = sys.argv[1], sys.argv[2]; SEQ = D + "/seqL"
    os.makedirs(SEQ, exist_ok=True)
    for f in range(1, NF + 1):
        dst = f"{SEQ}/f_{f:04d}.png"
        if os.path.lexists(dst): os.remove(dst)
        s = f"{FR}f_{src_frame(f):04d}.png"; assert os.path.exists(s), s
        os.symlink(s, dst)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-framerate", "24", "-i", SEQ + "/f_%04d.png", "-i", D + "/song.wav", "-vf", VF,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", "-movflags", "+faststart", OUT], check=True)
    print("done", OUT)
