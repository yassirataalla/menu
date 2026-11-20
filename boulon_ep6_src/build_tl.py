import json, wave, numpy as np
D = '/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep6/'
FPS = 24
# (key, start, end, bengali, french, emphasis words fr)
L = [
 ("l1", 12.98, 16.10, "প্যারিসের রাতে একলা নারায়ণ শিকদার", "Dans la nuit de Paris, seul : Narayan Shikdar"),
 ("l2", 17.24, 20.22, "লেবানিজ হেঁশেলে চলে থালার পাহাড়", "Dans une cuisine libanaise, une montagne d'assiettes"),
 ("l3", 21.44, 24.44, "ফরাসি কি আরবি কিছুই বোঝে না সে", "Français ou arabe : il ne comprend rien"),
 ("l4", 24.96, 28.48, "তবু এই অচেনা শহরে কাজের খোঁজে আসে", "Pourtant, dans cette ville inconnue, il vient chercher du travail"),
 ("l5", 29.90, 33.36, "হাত তার চলে শান্ত আর ধীর লয়ে", "Ses mains avancent, calmes, à un rythme lent"),
 ("l6", 33.44, 36.94, "নিজেরই এক অদ্ভুত সুর হৃদয়ে বয়ে", "Avec, dans le cœur, une étrange mélodie à lui"),
 ("l7", 37.68, 41.14, "প্যারিসের রাতে একলা নারায়ণ শিকদার", "Dans la nuit de Paris, seul : Narayan Shikdar"),
 ("l8", 41.18, 44.44, "লেবানিজ হেঁশেলে চলে থালার পাহাড়", "Dans une cuisine libanaise, une montagne d'assiettes"),
 ("c1", 45.38, 48.22, "শেফ কাঁদে আরবিতে ফরাসিতে রেগে লাল", "Le chef pleure en arabe, rouge de colère en français"),
 ("c2", 48.46, 52.64, "কিছুই বোঝে না নারায়ণ শুধু মাথা নাড়ে চাল", "Narayan ne comprend rien, il hoche juste la tête"),
 ("c3", 52.74, 56.22, "সবাই বলে কতো কথা ভাষা শুধু এক ধোঁয়া", "Tout le monde parle tant… la langue n'est que fumée"),
 ("c4", 56.42, 60.14, "নারায়ণ একা শুধু বোঝে থালা পরিষ্কার ধোয়া", "Narayan, lui, ne comprend qu'une chose : laver les assiettes"),
 ("c5", 60.24, 63.24, "শেফ কাঁদে আরবিতে ফরাসিতে রেগে লাল", "Le chef pleure en arabe, rouge de colère en français"),
 ("c6", 63.28, 67.22, "কিছুই বোঝে না নারায়ণ শুধু মাথা নাড়ে চাল", "Narayan ne comprend rien, il hoche juste la tête"),
 ("v1", 69.42, 72.18, "কাজে তার দেরি হোক নিখুঁত সে চায়", "Tant pis si c'est lent : il veut que ce soit parfait"),
 ("v2", 72.96, 76.16, "শেফ শুধু রাগে ফোঁসে সময়ের ইশারায়", "Le chef fulmine en montrant l'heure"),
 ("v3", 77.12, 80.64, "কেউ কিছু জিজ্ঞেস করলে শুধু মাথা নাড়ে সে", "Si on lui pose une question, il hoche juste la tête"),
 ("v4", 81.06, 85.24, "তার নিজেরই ভাষা যেন মিলিয়ে যায় বাতাসে", "Sa propre langue semble se dissoudre dans l'air"),
 ("v5", 85.32, 88.90, "যদি কেউ বুঝতো তার মনের ওই ভাষা", "Si quelqu'un comprenait la langue de son cœur…"),
 ("v6", 89.00, 92.84, "বলতো সে কত গল্প মেটাতো সেই আশা", "…il raconterait tant d'histoires, comblerait cet espoir"),
 ("w1", 94.04, 97.04, "কাজে তার দেরি হোক নিখুঁত সে চায়", "Tant pis si c'est lent : il veut que ce soit parfait"),
 ("w2", 97.56, 101.12, "শেফ শুধু রাগে ফোঁসে সময়ের ইশারায়", "Le chef fulmine en montrant l'heure"),
 ("d1", 101.80, 104.62, "শেফ কাঁদে আরবিতে ফরাসিতে রেগে লাল", "Le chef pleure en arabe, rouge de colère en français"),
 ("d2", 104.88, 108.84, "কিছুই বোঝে না নারায়ণ শুধু মাথা নাড়ে চাল", "Narayan ne comprend rien, il hoche juste la tête"),
 ("d3", 109.16, 112.22, "সবাই বলে কতো কথা ভাষা শুধু এক ধোঁয়া", "Tout le monde parle tant… la langue n'est que fumée"),
 ("d4", 112.84, 116.56, "নারায়ণ একা শুধু বোঝে থালা পরিষ্কার ধোয়া", "Narayan, lui, ne comprend qu'une chose : laver les assiettes"),
 ("d5", 116.66, 119.64, "শেফ কাঁদে আরবিতে ফরাসিতে রেগে লাল", "Le chef pleure en arabe, rouge de colère en français"),
 ("d6", 119.80, 124.32, "কিছুই বোঝে না নারায়ণ শুধু মাথা নাড়ে চাল", "Narayan ne comprend rien, il hoche juste la tête"),
 ("o1", 148.02, 152.04, "রাত শেষ হয়ে আসে থালা শুধু চলে হাত", "La nuit s'achève ; les assiettes, les mains continuent"),
 ("o2", 153.04, 157.46, "নারায়ণের মনে তার নিজেরই এক প্রভাত", "Dans le cœur de Narayan, une aube rien qu'à lui"),
]
w = wave.open(D + 'song.wav'); sr = w.getframerate(); n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, 2).mean(1) / 32768.0
dur = n / sr; NF = int(dur * FPS)
X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr); X[(fr < 350) | (fr > 3200)] = 0
v = np.fft.irfft(X, len(x))
hop = sr // FPS
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) for i in range(NF)])
words = [w_ for w_ in json.load(open(D + 'stt_full.json'))['words'] if w_.get('type') == 'word']
gate = np.zeros(NF)
for w_ in words:
    a, b = int((w_['start'] - 0.04) * FPS), int((w_['end'] + 0.08) * FPS)
    gate[max(0, a):min(NF, b)] = 1
amp = np.zeros(NF)
for (k, a, b, *_r) in L:
    i0, i1 = int(a * FPS), min(NF, int((b + 0.3) * FPS)); seg = env[i0:i1]
    amp[i0:i1] = np.clip(seg / (np.percentile(seg, 90) + 1e-9), 0, 1) ** 0.7
amp *= gate
# syllable-ish flutter so held notes keep the mouth alive
amp = np.clip(amp * (0.75 + 0.25 * np.sin(np.arange(NF) * 1.9)), 0, 1)
json.dump({"frames": NF, "duration": dur, "fps": FPS, "amp": [round(float(a), 3) for a in amp],
           "lines": [dict(key=k, start=a, end=b, bn=bn, fr=f) for (k, a, b, bn, f) in L]},
          open(D + 'timeline.json', 'w'), ensure_ascii=False)
print(NF, dur, round(float(amp.mean()), 3))
