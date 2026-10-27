# 2026-10-27 Numbers & dates の「聞いて選ぶ」練習の音声。docs/index.html の DATA.num から1項目1ファイル（g<種類>-<番号>.mp3）。
# python make_num_audio.py   （出力＝docs/num-audio/）
import asyncio, json, os, re, sys
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "docs")
OUT = os.path.join(DOCS, "num-audio")
VOICE, RATE = "ja-JP-NanamiNeural", "-30%"

def load_num():
    s = open(os.path.join(DOCS, "index.html"), encoding="utf-8").read()
    i = s.find('"num":[') + 6
    depth = 0
    for k in range(i, len(s)):
        if s[k] == "[": depth += 1
        elif s[k] == "]":
            depth -= 1
            if depth == 0: return json.loads(s[i:k + 1])

async def main():
    os.makedirs(OUT, exist_ok=True)
    for gi, g in enumerate(load_num()):
        for ii, it in enumerate(g["items"]):
            path = os.path.join(OUT, f"g{gi}-{ii}.mp3")
            if os.path.exists(path): continue
            text = it["r"].split("・")[0]          # 七人＝しちにん（1つ目の読み）
            if it["r"] == "half past": text = "はん"
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
            print(path, text)

asyncio.run(main())
