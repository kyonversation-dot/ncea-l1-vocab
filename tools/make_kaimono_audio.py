# 2026-10-17 Max 10/18用・買い物と食べ物の短い聞き取り（1問2〜3文）。python make_kaimono_audio.py <出力フォルダ>
import asyncio, os, sys
import edge_tts

OUT = sys.argv[1]
F, M = "ja-JP-NanamiNeural", "ja-JP-KeitaNeural"
RATE = "-30%"
# 値段はかなで書く＝読みを固定（Whisperは数字で書き出すので読みを検算できないため）

ITEMS = [
    (F, "この店のパンは、ひとつ、にひゃくえんです。でも、今日だけ、ひゃくごじゅうえんです。"),
    (F, "スーパーに行きました。卵とミルクを買いたかったです。でも、卵は高かったですから、ミルクだけ買いました。"),
    (M, "土曜日に、おばあさんのうちで、ハーンギを食べました。肉と野菜がありました。肉がいちばん、おいしかったです。"),
    (F, "この肉は、せんにひゃくえんです。魚は、肉より安いです。はっぴゃくえんです。"),
    (M, "明日、デパートに、家族のおみやげを買いに行きます。お金は、さんぜんえんだけあります。"),
    (M, "サンドイッチは、よんひゃくごじゅうえんで、ジュースは、ひゃくごじゅうえんです。ぼくは、サンドイッチをひとつと、ジュースをふたつ買いました。"),
    (F, "この店のケーキは、おいしいですが、小さいです。ひとつ、ろっぴゃくえんです。"),
]

async def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (v, t) in enumerate(ITEMS, 1):
        await edge_tts.Communicate(t, v, rate=RATE).save(os.path.join(OUT, f"k{i}.mp3"))
        print("ok", i)

asyncio.run(main())
