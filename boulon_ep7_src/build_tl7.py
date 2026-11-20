import json, wave, numpy as np
D = '/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad/ep7/'
FPS = 24
A = "মাথা নাড়ে নারায়ণ, কিছুই বোঝে না"; Af = "Narayan hoche la tête, il ne comprend rien"; Aa = "نارايان يهزّ رأسه، ولا يفهم شيئًا"
Bb = "শেফের রাগে কিচেনেতে আর থাকা যায় না"; Bf = "Avec la colère du chef, impossible de rester en cuisine"; Ba = "من غضب الشيف لم يعد البقاء في المطبخ ممكنًا"
Cb = "লেবানিজ খাবারেতে শুধু বাংলা গান বাজে"; Cf = "Sur la cuisine libanaise, que des chansons bengalies"; Ca = "مع الأكل اللبناني لا تُسمع إلا الأغاني البنغالية"
Db = "পাগল হয়ে যাব মোরা কাজের মাঝে মাঝে"; Df = "On va devenir fous, en plein travail"; Da = "سنُجنّ ونحن في وسط الشغل"
def chorus(p, o, dend=55.9):
    return [(p + "A", 32.0 + o, 35.7 + o, A, Af, Aa), (p + "A2", 36.0 + o, 39.7 + o, A, Af, Aa), (p + "B", 40.0 + o, 43.7 + o, Bb, Bf, Ba),
            (p + "C", 44.0 + o, 47.7 + o, Cb, Cf, Ca), (p + "D", 52.0 + o, dend + o, Db, Df, Da)]
L = [
 ("y1", 15.55, 20.2, "আমি ইয়াসার, সার্ভিসে ছুটি ছুটি করছি ভাই", "Moi, Yasser, je cours partout en salle, mon frère", "أنا ياسر، أجري وأجري في الخدمة يا أخي"),
 ("y2", 20.35, 23.7, "অর্ডার নিয়ে কার্তিককে শুধু বোঝাতে চাই", "La commande en main, je veux juste que Kartik me comprenne", "معي الطلب، وأريد فقط أن يفهمني كارتيك"),
 ("y3", 24.2, 28.0, "কার্তিক কয় ইংরেজিতে: আমি তো ফ্রেঞ্চ জানি না", "Kartik répond en anglais : « Je ne parle pas français »", "كارتيك يردّ بالإنجليزية: «أنا لا أعرف الفرنسية»"),
 ("y4", 28.1, 31.85, "নারায়ণ শুধু বাংলা বোঝে, অন্য কিছু মানে না", "Narayan ne comprend que le bengali, rien d'autre", "ونارايان لا يفهم إلا البنغالية ولا يقبل غيرها"),
 *chorus("c", 0),
 ("v1", 64.3, 67.7, "দিনের শেষে শেফের মাথা ভীষণ গরম ভাই", "En fin de journée, la tête du chef est brûlante, mon frère", "آخر النهار رأس الشيف يغلي يا أخي"),
 ("v2", 68.4, 71.8, "তাড়াতাড়ি কাজ সেরে এবার পালাতে চাই", "Vite, finir le travail… et filer d'ici", "ننهي الشغل بسرعة… ونهرب"),
 ("v3", 72.35, 75.7, "কার্তিককে বলি আমি: তুমি নারায়ণকে কও", "Je dis à Kartik : « Toi, dis-le à Narayan »", "أقول لكارتيك: «قل أنت لنارايان»"),
 ("v4", 76.05, 79.7, "জলদি কাজ শেষ করে রেডি এবার হও", "Finis vite le travail et tiens-toi prêt", "أنهِ شغلك بسرعة واستعدّ"),
 *chorus("d", 48),
 ("z1", 128.3, 131.3, "আমরা বলি এক, তো ও শোনে আরেকটা", "Nous, on dit une chose… lui en entend une autre", "نقول شيئًا… فيسمع شيئًا آخر"),
 ("z2", 132.3, 135.7, "এইভাবে কাটে রে ভাই আমাদের এই দিনটা", "Voilà comment passe notre journée, mon frère", "هكذا يمضي يومنا يا أخي"),
 ("z3", 136.4, 139.7, "কোথায় লেবানন আর কোথায় যে বাংলাদেশ", "Où est le Liban… et où est le Bangladesh !", "أين لبنان… وأين بنغلاديش!"),
 ("z4", 140.0, 143.8, "সবাই মিলে মিশে মোদের দিন হল যে শেষ", "Tous ensemble, et voilà notre journée finie", "كلنا معًا… وانتهى يومنا"),
 *chorus("e", 112, 57.0),
]
w = wave.open(D + 'song.wav'); sr = w.getframerate(); n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, 2).mean(1) / 32768.0
dur = n / sr; NF = int(dur * FPS)
X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr); X[(fr < 350) | (fr > 3200)] = 0
v = np.fft.irfft(X, len(x)); hop = sr // FPS
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) for i in range(NF)])
words = [w_ for w_ in json.load(open(D + 'stt_full.json'))['words'] if w_.get('type') == 'word']
gate = np.zeros(NF)
for w_ in words:
    a, b = int((w_['start'] - 0.04) * FPS), int((w_['end'] + 0.08) * FPS); gate[max(0, a):min(NF, b)] = 1
amp = np.zeros(NF)
for (k, a, b, *_r) in L:
    i0, i1 = int(a * FPS), min(NF, int((b + 0.3) * FPS)); seg = env[i0:i1]
    amp[i0:i1] = np.clip(seg / (np.percentile(seg, 90) + 1e-9), 0, 1) ** 0.7
amp *= gate
amp = np.clip(amp * (0.75 + 0.25 * np.sin(np.arange(NF) * 1.9)), 0, 1)
# chorus 2/3 reuse chorus 1 frames -> copy its amp so reused frames stay consistent
json.dump({"frames": NF, "duration": dur, "fps": FPS, "amp": [round(float(a), 3) for a in amp],
           "lines": [dict(key=k, start=a, end=b, bn=bn, fr=f, ar=ar) for (k, a, b, bn, f, ar) in L]}, open(D + 'timeline.json', 'w'), ensure_ascii=False)
print(NF, dur, round(float(amp.mean()), 3))
