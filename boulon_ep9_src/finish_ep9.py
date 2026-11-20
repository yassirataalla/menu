import sys, os, subprocess
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep9"
MODE, FR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]   # MODE v|l
NF, DUR = 840, 35.0
W, H = (720, 1280) if MODE == "v" else (1920, 1080)
INK, YEL = "&H20120B&", "&H26D4FF&"
def ts(x): return f"0:{int(x//60):02d}:{x%60:05.2f}"
if MODE == "v": X, y, y2, s1, s2, T1, T2 = 360, 760, 870, 50, 34, "POV : ton crush\\Na vu ton message", "POV: your crush\\Nleft you on read"
else: X, y, y2, s1, s2, T1, T2 = 380, 470, 610, 66, 42, "POV : ton crush\\Na vu ton message", "POV: your crush\\Nleft you on read"
EV = [f"Dialogue: 5,{ts(0.15)},{ts(1.65)},Default,,0,0,0,,{{\\an5\\pos({X},{y})\\fnPoppins ExtraBold\\fs{s1}\\bord5\\3c{INK}\\shad2\\4c{INK}\\1c&HFFFFFF&\\fad(80,120)}}{T1}",
      f"Dialogue: 5,{ts(0.25)},{ts(1.65)},Default,,0,0,0,,{{\\an5\\pos({X},{y2})\\fnPoppins\\b1\\fs{s2}\\bord4\\3c{INK}\\1c{YEL}\\fad(80,120)}}{T2}"]
open(D + f"/ep9{MODE}.ass", "w", encoding="utf8").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00240F1A,&H80240F1A,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(EV) + "\n")
pre = "" if MODE == "v" else "scale=1920:1080:flags=lanczos,"
VF = f"{pre}ass={D}/ep9{MODE}.ass"
if FR == "still":
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", OUT, "-vf", VF, "-ss", "0.6", "-frames:v", "1", sys.argv[4]], check=True); sys.exit()
for f in range(1, NF + 1): assert os.path.exists(f"{FR}f_{f:04d}.png"), f
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-framerate", "24", "-i", FR + "f_%04d.png", "-i", D + "/mix9.wav", "-vf", VF,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", "-movflags", "+faststart", OUT], check=True)
print("done", OUT)
