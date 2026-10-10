# 2026-10-10 Max 10/11用・日付の短い聞き取り（1問1文〜2文）。python make_hizuke_audio.py <出力フォルダ>
import asyncio, os, sys
import edge_tts

OUT = sys.argv[1]
F, M = "ja-JP-NanamiNeural", "ja-JP-KeitaNeural"
RATE = "-30%"
# 日付と「まち」はかなで書く＝読みを固定（Whisperは数字で書き出すので読みを検算できないため）

ITEMS = [
    (F, "ごがつ、いつかは、こどもの日です。家族と海に泳ぎに行きます。"),
    (F, "はつかに、まちに新しい靴を買いに行きます。"),
    (M, "じゅうがつ、じゅうににちは、スポーツの日でした。ラグビーをしすぎましたから、足が痛いです。"),
    (F, "くがつ、ついたちは私の誕生日でした。ケーキを食べすぎましたから、夜、お腹が痛かったです。"),
    (F, "じゅういちがつ、みっかは、文化の日です。図書館で音楽を聞きながら、宿題をします。"),
    (M, "しちがつ、ようかに、友達と話しながら、公園を歩きました。"),
]

async def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (v, t) in enumerate(ITEMS, 1):
        await edge_tts.Communicate(t, v, rate=RATE).save(os.path.join(OUT, f"h{i}.mp3"))
        print("ok", i)

asyncio.run(main())
