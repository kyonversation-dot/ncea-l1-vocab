# 2026-10-20 Max 10/25用・旅行と町の短い聞き取り（文法8・道案内2・セクション1）。python make_ryokou_audio.py <出力フォルダ>
import asyncio, os, subprocess, sys, tempfile
import edge_tts

OUT = sys.argv[1]
F, M = "ja-JP-NanamiNeural", "ja-JP-KeitaNeural"
RATE = "-30%"
# 北島・角・町は読みを固定するため、かなで書く（町は「ちょう」と読まれた）

ITEMS = {
    "g1": [(M, "僕は土曜日に、ラグビーの試合に出ます。")],
    "g2": [(F, "私は夏休みに、よくビーチに行きます。")],
    "g3": [(F, "私は飛行機に乗りました。映画を見ながら、ご飯を食べました。")],
    "g4": [(F, "私は昨日、お寺だけ見物しました。")],
    "g5": [(M, "地下鉄は、バスより速いです。")],
    "g6": [(F, "この湖で、キャンプができます。")],
    "g7": [(F, "神社で写真を撮ってもいいですか。"), (M, "はい、いいですよ。")],
    "g8": [(M, "ここで泳いでもいいですか。"), (F, "だめです。泳いではいけません。")],
    "d1": [(F, "駅を出て、まっすぐ行ってください。信号を右に曲がってください。ホテルは公園の隣です。")],
    "d2": [(F, "デパートのかどを左に曲がってください。図書館はスーパーの前にあります。")],
    "s1": [(M, "ゾーイさん、休みにどこに行きましたか。"),
           (F, "おじさんと、タウポに行きました。タウポは、きたじまの大きい湖です。キャンプをしました。"),
           (M, "いいですね。火曜日はどうでしたか。"),
           (F, "火曜日は雨でしたから、まちに行きました。映画を見て、帽子を買いました。")],
}

async def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    gap = os.path.join(tmp, "gap.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "anullsrc=r=24000:cl=mono", "-t", "0.9", "-c:a", "libmp3lame", "-b:a", "48k", gap], check=True)
    for name, lines in ITEMS.items():
        parts = []
        for i, (v, t) in enumerate(lines):
            p = os.path.join(tmp, f"{name}_{i}.mp3")
            await edge_tts.Communicate(t, v, rate=RATE).save(p)
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
