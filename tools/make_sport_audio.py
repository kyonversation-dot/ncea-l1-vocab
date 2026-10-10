import asyncio, os, subprocess, sys, tempfile
import edge_tts

OUT = sys.argv[1]
F, M = "ja-JP-NanamiNeural", "ja-JP-KeitaNeural"
RATE = "-30%"
RATES = {}

SECTIONS = {
    "sec1": [
        (F, "ジャックさんは、どんなスポーツが得意ですか。"),
        (M, "僕はラグビーが得意です。週末はいつもグラウンドで練習します。でも、クリケットは苦手です。"),
        (F, "そうですか。家族もスポーツが好きですか。"),
        (M, "はい。弟のルーカスは、僕よりクリケットが上手です。ルーカスは毎日学校で練習します。"),
    ],
    "sec2": [
        (M, "みおさん、昨日のバスケットボールの試合はどうでしたか。"),
        (F, "43、対、30で勝ちました。朝、グラウンドで走ってから、たいいくかんで試合をしました。試合でもたくさん走りましたから、今日は足が痛いです。"),
        (M, "大変ですね。明日も練習しますか。"),
        (F, "いいえ、明日はうちで休みます。来週の土曜日にまた試合がありますから、元気になりたいです。"),
    ],
    "sec3": [
        (M, "グレースさん、元気がありませんね。"),
        (F, "昨日風邪をひきました。喉がとても痛いです。でも、頭とお腹は痛くないです。"),
        (M, "薬を飲みましたか。"),
        (F, "はい、朝ご飯の後で、薬を飲みました。明日はネットボールの試合がありますが、今日は練習に行きません。試合に行きたいですから、うちで早く寝ます。"),
    ],
}

async def tts(voice, text, path, rate=RATE):
    await edge_tts.Communicate(text, voice, rate=rate).save(path)

async def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    gap = os.path.join(tmp, "gap.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "anullsrc=r=24000:cl=mono", "-t", "0.9", "-c:a", "libmp3lame", "-b:a", "48k", gap], check=True)
    for name, lines in SECTIONS.items():
        parts = []
        for i, (v, t) in enumerate(lines):
            p = os.path.join(tmp, f"{name}_{i}.mp3")
            await tts(v, t, p, RATES.get(name, RATE))
            parts += [p, gap]
        lst = os.path.join(tmp, f"{name}.txt")
        with open(lst, "w", encoding="utf-8") as f:
            for p in parts[:-1]:
                f.write("file '" + p.replace(chr(92), "/") + "'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-ar", "24000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "48k",
                        os.path.join(OUT, f"{name}.mp3")], check=True)
        print("ok", name)

asyncio.run(main())
