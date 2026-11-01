# 2026-10-31 Max 11/1用・学校と数の短い聞き取り（道案内1・数4・文法5。学校の話は2019年の過去問の公式音声）。python make_gakkou_audio.py <出力フォルダ>
import asyncio, os, subprocess, sys, tempfile
import edge_tts

OUT = sys.argv[1]
F, M = "ja-JP-NanamiNeural", "ja-JP-KeitaNeural"
RATE = "-30%"

ITEMS = {
    "d1": [(F, "学校を出て、左に行ってください。郵便局のかどを右に曲がってください。信号を渡ってください。レストランは、スーパーと本屋の間にあります。")],
    "n1": [(M, "すみません、このかばんはいくらですか。"), (F, "三千五百円です。"),
           (M, "シャツはいくらですか。"), (F, "シャツは二千八百円です。")],
    "n2": [(M, "僕の弟の誕生日は、四月八日です。おじいさんの誕生日は、九月二十日です。")],
    "n3": [(F, "木曜日の二時間目に、試験があります。試験は三十分です。")],
    "n4": [(M, "僕は日本に三週間いました。おじさんは六か月いました。")],
    "g1": [(F, "友達のエラさんが、私にチェスの本をくれました。")],
    "g2": [(M, "僕はおじいさんに、二千円もらいました。")],
    "g3": [(F, "私は弟に、赤い帽子をあげました。")],
    "g4": [(F, "数学は難しかったです。でも、今は面白くなりました。")],
    "g5": [(M, "僕はサッカーをよくしますが、野球はあまりしません。")],
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
