import subprocess
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep9/"
DUR = 35.0
# (file, start, gain_dB, trim, fade_in, fade_out)
EV = [("room", 0.0, 22, 35.0, 0, 0), ("lofi", 0.0, -6, 6.2, 0, 0.8), ("dots", 0.9, 8, 1.0, 0, 0.2),
      ("tick", 1.7, 2, 4.3, 0.3, 0.3), ("dots", 6.0, 8, 1.2, 0, 0.2), ("romance", 7.25, 2, 2.2, 0.05, 0.05), ("scratch", 9.42, -2, 1.0, 0, 0.2),
      ("fall", 10.9, 4, 1.0, 0, 0.2), ("sigh", 11.4, 0, 1.5, 0, 0.3),
      ("keys", 12.2, 0, 1.3, 0, 0.1), ("delete", 13.5, 4, 0.5, 0, 0.1), ("keys", 15.1, 0, 0.7, 0, 0.1), ("delete", 15.82, 4, 0.3, 0, 0.1), ("keys", 17.1, 0, 0.35, 0, 0.1),
      ("whoosh", 18.72, -8, 0.6, 0, 0.1), ("nono", 20.1, -5, 0.84, 0, 0.1), ("sigh", 22.0, 0, 1.5, 0, 0.3),
      ("buzz", 24.05, -12, 0.8, 0, 0.1), ("gasp", 24.35, -3, 1.0, 0, 0.2), ("romance", 25.0, 2, 1.8, 0.05, 0.4), ("notif", 26.8, 0, 1.0, 0, 0.2),
      ("thunder", 29.8, -2, 5.0, 0, 0.6), ("rain", 30.4, -2, 4.6, 0.6, 0.3), ("keys", 31.1, 0, 0.55, 0, 0.1), ("sent", 31.75, 0, 0.62, 0, 0.1),
      ("sigh", 32.8, 0, 1.5, 0, 0.3), ("lofi", 33.4, -6, 1.6, 0.5, 0)]
args = ["ffmpeg", "-nostdin", "-v", "error", "-y"]; fl = []
for i, (f, st, g, tr, fi, fo) in enumerate(EV):
    args += ["-i", D + "sfx/" + f + ".mp3"]
    loop = ",aloop=loop=-1:size=2e9" if f == "room" else ""
    c = f"[{i}]aresample=44100,aformat=channel_layouts=stereo{loop},atrim=0:{tr},asetpts=N/SR/TB,volume={g}dB"
    if fi: c += f",afade=t=in:st=0:d={fi}"
    if fo: c += f",afade=t=out:st={max(0, tr - fo)}:d={fo}"
    c += f",adelay={int(st * 1000)}|{int(st * 1000)}[a{i}]"; fl.append(c)
fl.append("".join(f"[a{i}]" for i in range(len(EV))) + f"amix=inputs={len(EV)}:normalize=0:dropout_transition=0,atrim=0:{DUR},alimiter=limit=0.9,loudnorm=I=-15:TP=-1.5:LRA=11[out]")
args += ["-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", D + "mix9.wav"]
subprocess.run(args, check=True); print("ok")
