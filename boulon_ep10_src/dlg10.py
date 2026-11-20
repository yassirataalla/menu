import subprocess, json, numpy as np, sys
D = "/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep10/"
V = D + "vo3/"
BOUL = [("b0.mp3", 0.2, 1.0), ("b1.mp3", 21.2, 1.0), ("c_b2.wav", 33.0, 1.0)]
MOM = [("c_m1.wav", 1.4, 1.0), ("m2.mp3", 3.8, 1.0), ("c_m3.wav", 6.55, 1.0), ("c_m4.wav", 10.65, 1.0), ("c_m5.wav", 12.4, 1.0),
       ("m6a.mp3", 16.7, 1.0), ("m6b.mp3", 22.8, 0.45), ("m7.mp3", 27.6, 1.0), ("c_m8.wav", 29.2, 1.0)]
def build(ev, out):
    args = []; fl = []
    for i, (f, t, v) in enumerate(ev):
        args += ["-i", V + f]; fl.append(f"[{i}]aresample=44100,aformat=channel_layouts=mono,volume={v},adelay={int(t*1000)}[a{i}]")
    fl.append("".join(f"[a{i}]" for i in range(len(ev))) + f"amix=inputs={len(ev)}:normalize=0,apad=whole_dur=35,atrim=0:35[o]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", ";".join(fl), "-map", "[o]", "-ar", "44100", "-ac", "1", out], check=True)
build(BOUL, D + "trkB.wav"); build(MOM, D + "trkM.wav")
def amp(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "24000", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; n = 1000
    fr = [float(np.sqrt(np.mean(a[i*n:(i+1)*n] ** 2))) if i*n < len(a) else 0.0 for i in range(840)]
    p = np.percentile([x for x in fr if x > 0.01] or [1], 90); return [round(min(1.0, x / p), 3) for x in fr]
json.dump({"frames": 840, "fps": 24, "amp": [], "lines": [], "ampB": amp(D + "trkB.wav"), "ampM": amp(D + "trkM.wav")}, open(D + "timeline.json", "w"))
print("ok")
