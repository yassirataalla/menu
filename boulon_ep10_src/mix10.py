import subprocess
S = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/"
E9, E10, D = S + "ep9/sfx/", S + "ep10/sfx/", S + "ep10/"
DUR = 35.0
# (path, start, gain_dB, trim, fade_in, fade_out, offset)
EV = [(E9 + "room.mp3", 0.0, 18, 35.0, 0, 0, 0),
      (E9 + "lofi.mp3", 0.0, -7, 1.3, 0, 0.03, 0), (E10 + "video.mp3", 0.0, -10, 1.25, 0, 0.05, 0),
      (E9 + "scratch.mp3", 1.26, -3, 0.6, 0, 0.15, 0), (E10 + "door.mp3", 1.28, 1, 1.5, 0, 0.3, 0),
      (E10 + "whip.mp3", 1.62, -9, 0.5, 0, 0.1, 0), (E10 + "shrink.mp3", 6.1, -3, 0.6, 0, 0.1, 0),
      (E10 + "whip.mp3", 6.5, -12, 0.5, 0, 0.1, 0), (E10 + "whip.mp3", 7.7, -12, 0.5, 0, 0.1, 0), (E10 + "whip.mp3", 9.1, -12, 0.5, 0, 0.1, 0),
      (E10 + "ring.mp3", 11.62, 0, 0.72, 0, 0.04, 0),
      (E10 + "magic.mp3", 12.33, -2, 1.5, 0, 0.3, 0),
      (E10 + "angel.mp3", 12.4, -11, 6.8, 0.04, 0.12, 0),
      (E10 + "creak.mp3", 20.2, -6, 1.0, 0, 0.15, 0),
      (E10 + "angel.mp3", 22.85, -15, 3.95, 0.4, 0.04, 7.0),
      (E10 + "kiss.mp3", 26.3, -4, 0.8, 0, 0.1, 0), (E10 + "hangup.mp3", 26.8, -6, 0.6, 0, 0.1, 0),
      (E10 + "rumble.mp3", 26.85, 0, 1.5, 0, 0.3, 0),
      (E10 + "boom.mp3", 27.62, -5, 1.2, 0, 0.4, 0),
      (E10 + "boom.mp3", 29.2, 0, 1.2, 0, 0.4, 0), (E10 + "boom.mp3", 30.58, 0, 1.2, 0, 0.4, 0), (E10 + "boom.mp3", 31.52, 1, 1.2, 0, 0.4, 0),
      (E10 + "plates.mp3", 32.8, 2, 2.5, 0, 0.3, 0), (E10 + "plates.mp3", 33.9, -6, 1.1, 0, 0.3, 1.2),
      (E9 + "lofi.mp3", 34.65, -7, 0.35, 0.25, 0, 0),
      (D + "trkM.wav", 0.0, 1, 35.0, 0, 0, 0), (D + "trkB.wav", 0.0, 2, 35.0, 0, 0, 0)]
args = ["ffmpeg", "-nostdin", "-v", "error", "-y"]; fl = []
for i, (f, st, g, tr, fi, fo, off) in enumerate(EV):
    args += ["-i", f]
    loop = ",aloop=loop=-1:size=2e9" if f.endswith("room.mp3") else ""
    c = f"[{i}]aresample=44100,aformat=channel_layouts=stereo{loop},atrim={off}:{off + tr},asetpts=N/SR/TB,volume={g}dB"
    if fi: c += f",afade=t=in:st=0:d={fi}"
    if fo: c += f",afade=t=out:st={max(0, tr - fo)}:d={fo}"
    c += f",adelay={int(st * 1000)}|{int(st * 1000)}[a{i}]"; fl.append(c)
fl.append("".join(f"[a{i}]" for i in range(len(EV))) + f"amix=inputs={len(EV)}:normalize=0:dropout_transition=0,apad=whole_dur={DUR},atrim=0:{DUR},alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
args += ["-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", D + "mix10.wav"]
subprocess.run(args, check=True); print("ok")
