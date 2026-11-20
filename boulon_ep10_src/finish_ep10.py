import sys, os, subprocess
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep10"
MODE, FR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]   # MODE v|l
NF, DUR = 840, 35.0
W, H = (720, 1280) if MODE == "v" else (1920, 1080)
INK, YEL, WHT, CYA = "&H20120B&", "&H26D4FF&", "&HFFFFFF&", "&HFFE070&"
def ts(x): return f"0:{int(x//60):02d}:{x%60:05.2f}"
if MODE == "v": X, CY, FS, PY, PFS = 360, 830, 50, 240, 46
else: X, CY, FS, PY, PFS = 960, 925, 72, 130, 64
# chunks: (speaker, end, [(word, start), ...], size_mult)
CH = [("M", 2.7, [("BOULON !", 1.56)], 1.25), ("M", 3.9, [("BOULON !!!", 2.82)], 1.35),
      ("M", 5.1, [("Ça", 3.96), ("fait", 4.12), ("TROIS", 4.32), ("JOURS", 4.78)], 1.0),
      ("M", 6.6, [("que", 5.1), ("je", 5.22), ("te", 5.36), ("dis", 5.5), ("de", 5.68), ("ranger !!", 5.92)], 1.0),
      ("M", 8.5, [("Regarde-moi", 6.7), ("ce", 7.36), ("BORDEL !!", 7.66)], 1.1),
      ("M", 9.56, [("On", 8.62), ("dirait", 8.74), ("qu'une", 9.0), ("bombe", 9.3)], 1.0),
      ("M", 10.75, [("a", 9.58), ("explosé", 9.68), ("ici !!", 10.2)], 1.0),
      ("M", 11.72, [("Tu", 10.8), ("te", 10.92), ("crois", 11.06), ("à", 11.24), ("l'hôtel", 11.32), ("ou—", 11.6)], 1.0),
      ("M", 14.45, [("Allôôô", 12.48), ("ma", 13.2), ("chérieéé !", 13.38)], 1.0),
      ("M", 16.8, [("Oui", 14.56), ("oui,", 14.74), ("tout", 15.32), ("va", 15.48), ("super", 15.8), ("bien…", 16.26)], 1.0),
      ("M", 19.2, [("Les", 16.94), ("enfants", 17.22), ("sont", 17.98), ("des", 18.2), ("ANGES !", 18.58)], 1.0),
      ("B", 22.95, [("…des", 21.48), ("anges ??", 22.14)], 1.15),
      ("m", 24.85, [("Ils", 23.0), ("sont", 23.32), ("trop", 23.64), ("sages !", 24.08)], 0.8),
      ("m", 26.8, [("Bisous", 26.12), ("bisous !", 26.42)], 0.8),
      ("M", 29.15, [("Et", 27.8), ("les", 27.98), ("ASSIETTES ?!!!", 28.2)], 1.15),
      ("M", 30.62, [("TOUT.", 29.44)], 1.5), ("M", 31.88, [("TOUT.", 29.44), ("DE.", 30.66)], 1.5),
      ("M", 32.8, [("TOUT.", 29.44), ("DE.", 30.66), ("SUITE. !!!", 31.92)], 1.5),
      ("B", 34.9, [("Oui", 33.06), ("maman…", 33.24), ("j'arrive…", 34.14)], 1.0)]
EV = []
for sp, end, words, mult in CH:
    base = CYA if sp == "B" else WHT; fs = int(FS * mult)
    for i, (w, st) in enumerate(words):
        e = words[i + 1][1] if i + 1 < len(words) else end
        if words[0][0] == "TOUT." and i < len(words) - 1: continue  # accumulating punch chunks: only the newest word
        parts = []
        for j, (w2, _) in enumerate(words):
            col = YEL if j == i else base
            parts.append(f"{{\\1c{col}}}{w2}")
        pop = "\\t(0,90,\\fscx112\\fscy112)\\t(90,180,\\fscx100\\fscy100)" if i == 0 else ""
        EV.append(f"Dialogue: 4,{ts(st)},{ts(e)},Default,,0,0,0,,{{\\an5\\pos({X},{CY})\\fnPoppins ExtraBold\\fs{fs}\\bord6\\3c{INK}\\shad3\\4c{INK}{pop}}}" + " ".join(parts))
EV.append(f"Dialogue: 5,{ts(0.1)},{ts(1.32)},Default,,0,0,0,,{{\\an5\\pos({X},{PY})\\fnPoppins ExtraBold\\fs{PFS}\\bord5\\3c{INK}\\shad2\\4c{INK}\\1c&HFFFFFF&\\fad(80,60)}}POV : t'as pas rangé\\Nta chambre")
open(D + f"/ep10{MODE}.ass", "w", encoding="utf8").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00240F1A,&H80240F1A,0,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(EV) + "\n")
pre = "" if MODE == "v" else "scale=1920:1080:flags=lanczos,"
VF = f"{pre}ass={D}/ep10{MODE}.ass"
if FR == "still":
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", OUT, "-vf", VF, "-ss", sys.argv[5] if len(sys.argv) > 5 else "0.6", "-frames:v", "1", sys.argv[4]], check=True); sys.exit()
for f in range(1, NF + 1): assert os.path.exists(f"{FR}f_{f:04d}.png"), f
if not os.path.exists(D + "/mix10.wav"): subprocess.run([sys.executable, D + "/mix10.py"], check=True)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-framerate", "24", "-i", FR + "f_%04d.png", "-i", D + "/mix10.wav", "-vf", VF,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", "-movflags", "+faststart", OUT], check=True)
print("done", OUT)
