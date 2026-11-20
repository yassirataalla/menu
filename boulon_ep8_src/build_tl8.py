import json, wave, numpy as np
D = '/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep8/'
FPS = 24
L = [
 (14.08,16.50,"Il est trois heures, je ferme les yeux.","It's 3 a.m., I close my eyes."),
 (17.12,19.54,"Mon cerveau sort le dossier complet.","My brain pulls out the full file."),
 (20.06,22.75,"Chaque connerie, chaque mot de trop,","Every screw-up, every word too many,"),
 (22.80,25.54,"il me les balance en boucle, putain.","it throws them at me on loop, damn."),
 (25.86,28.45,"Les moments gênants, les silences lourds,","The awkward moments, the heavy silences,"),
 (28.50,31.36,"les fois où j'ai parlé trop fort en auto.","the times I talked too loud on autopilot."),
 (31.98,34.55,"Tout revient net, sans pitié, sans filtre,","It all comes back sharp, no mercy, no filter,"),
 (34.60,37.34,"comme un film de merde que je connais par cœur.","like a crappy movie I know by heart."),
 (37.92,39.36,"Pourquoi j'ai dit ça ?","Why did I say that?"),
 (39.42,40.50,"Pourquoi j'ai ri ?","Why did I laugh?"),
 (40.86,43.38,"Pourquoi j'ai envoyé ce message pourri ?","Why did I send that awful text?"),
 (43.84,46.44,"Je me retourne, je maudis mon lit.","I toss and turn, I curse my bed."),
 (46.88,49.42,"Mon oreiller sait déjà tout de ma vie.","My pillow already knows everything about my life."),
 (49.68,52.36,"Il a entendu tous mes « putain, pourquoi ? »,","It's heard all my “damn, why?”,"),
 (52.72,54.96,"tous mes soupirs, tous mes « j'aurais dû ».","all my sighs, all my “I should have”."),
 (55.52,58.45,"Je lui parle bas comme à un vieux pote,","I whisper to it like an old friend,"),
 (58.50,61.40,"mais lui, il se fiche de moi, il est juste là.","but it couldn't care less — it's just there."),
 (61.50,64.00,"Je regarde le plafond comme un con.","I stare at the ceiling like an idiot."),
 (64.48,67.04,"Je refais des scènes vieilles de dix ans.","I replay scenes from ten years ago."),
 (67.42,70.05,"Je me traite de débile à voix haute,","I call myself stupid out loud,"),
 (70.10,73.08,"puis je ris tout seul et ça fait un peu mal.","then I laugh alone — and it kind of hurts."),
 (73.34,76.05,"Je me vois encore maladroit, trop nerveux,","I still see myself clumsy, too nervous,"),
 (76.10,79.04,"en train de dire n'importe quoi pour plaire.","saying anything just to be liked."),
 (79.28,82.05,"Et là, dans le noir, je réalise enfin","And here in the dark, I finally realise"),
 (82.10,84.92,"à quel point j'étais ridicule et ça pique.","how ridiculous I was — and it stings."),
 (85.40,86.86,"Pourquoi j'ai dit ça ?","Why did I say that?"),
 (86.92,88.00,"Pourquoi j'ai ri ?","Why did I laugh?"),
 (88.38,90.90,"Pourquoi j'ai envoyé ce message pourri ?","Why did I send that awful text?"),
 (91.34,93.86,"Je me retourne, je maudis mon lit.","I toss and turn, I curse my bed."),
 (94.30,96.68,"Mon oreiller sait déjà tout de ma vie.","My pillow already knows everything about my life."),
 (97.10,99.78,"Il a entendu tous mes « putain, pourquoi ? »,","It's heard all my “damn, why?”,"),
 (100.14,102.58,"tous mes soupirs, tous mes « j'aurais dû ».","all my sighs, all my “I should have”."),
 (102.94,105.85,"Je lui parle bas comme à un vieux pote,","I whisper to it like an old friend,"),
 (105.90,108.80,"mais lui, il se fiche de moi, il est juste là.","but it couldn't care less — it's just there."),
 (132.50,135.28,"Et demain, je sourirai comme d'habitude.","And tomorrow I'll smile like always."),
 (135.58,138.64,"Je dirai « ça va » avec mon plus beau mensonge.","I'll say “I'm fine” with my prettiest lie."),
 (139.14,141.65,"Je ferai comme si rien n'existait,","I'll act like nothing happened,"),
 (141.70,144.48,"comme si mon cerveau n'avait pas fait le con.","like my brain didn't act up."),
 (145.10,147.46,"Mais ce soir, il règne en dictateur.","But tonight it rules like a dictator."),
 (148.16,150.58,"Il ouvre tous les tiroirs que j'ai fermés.","It opens every drawer I ever closed."),
 (151.04,153.65,"Et moi, je suis juste là, dans le noir,","And me, I'm just here, in the dark,"),
 (153.70,156.46,"à en chier tout seul, là, jusqu'au jour.","struggling alone, here, till daylight."),
 (160.48,162.12,"Et à en chier tout seul.","Struggling all alone."),
 (168.08,169.40,"Jusqu'au jour.","Till daylight."),
]
w = wave.open(D + 'song.wav'); sr = w.getframerate(); n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, 2).mean(1) / 32768.0
dur = n / sr; NF = int(dur * FPS)
X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr); X[(fr < 350) | (fr > 3200)] = 0
v = np.fft.irfft(X, len(x)); hop = sr // FPS
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) for i in range(NF)])
words = [w_ for w_ in json.load(open(D + 'stt.json'))['words'] if w_.get('type') == 'word']
gate = np.zeros(NF)
for w_ in words:
    a, b = int((w_['start'] - 0.04) * FPS), int((w_['end'] + 0.08) * FPS); gate[max(0, a):min(NF, b)] = 1
amp = np.zeros(NF)
for (a, b, *_r) in L:
    i0, i1 = int(a * FPS), min(NF, int((b + 0.3) * FPS)); seg = env[i0:i1]
    amp[i0:i1] = np.clip(seg / (np.percentile(seg, 90) + 1e-9), 0, 1) ** 0.7
amp *= gate
amp = np.clip(amp * (0.75 + 0.25 * np.sin(np.arange(NF) * 1.9)), 0, 1)
json.dump({"frames": NF, "duration": dur, "fps": FPS, "amp": [round(float(a), 3) for a in amp],
           "lines": [dict(start=a, end=b, fr=f, en=e) for (a, b, f, e) in L]}, open(D + 'timeline.json', 'w'), ensure_ascii=False)
print(NF, dur)
