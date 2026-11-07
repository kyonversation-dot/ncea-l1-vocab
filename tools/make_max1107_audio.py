# 2026-11-06 Max 11/7用・短い聴解7つ（形容詞・ペット・食べ物・道案内・値段・日付）。台本＝_work/AI_Lab_ncea_listening_proto/items/max-1107/max-1107.txt。python make_max1107_audio.py <出力フォルダ>
import asyncio, os, subprocess, sys, tempfile
import edge_tts

OUT = sys.argv[1]
F, M = "ja-JP-NanamiNeural", "ja-JP-KeitaNeural"
RATE = "-30%"

ITEMS = {
    "m0": [(F, "昨日、お母さんとマーラータンを食べに行きました。マーラータンは中国の料理です。新しい店です。野菜や肉や麺がたくさんありました。好きなものを取ります。百グラム、三百九十円です。とても美味しかったです。でも、ちょっと辛かったです。また行きたいです。")],
    "l1": [(F, "ハミッシュさんは、ペットを飼っていますか。"),
           (M, "はい、犬を三匹飼っています。一匹はとても大きいですから、友達は怖いと言います。でも、優しい犬です。二匹は小さくて、いつも一緒に遊んでいます。")],
    "l2": [(M, "ちひろさん、週末にどこに行きましたか。"),
           (F, "おじさんの農場に行きました。農場には、牛と羊がたくさんいます。馬もいます。私は馬に乗りました。その馬は小さかったですから、怖くなかったです。")],
    "l3": [(F, "ノアさん、昼ご飯に何を食べますか。"),
           (M, "僕はハンバーガーが一番好きです。でも、ハンバーガーは体に悪いと思います。だから、今日は野菜のサンドイッチを食べます。サンドイッチは六百円です。")],
    "l4": [(F, "こうたさん、動物園に行きましたか。"),
           (M, "はい、十一月三日に家族と行きました。いろいろな動物がいました。僕は鳥が一番好きです。鳥は小さくて、きれいでしたから。でも、弟は鳥が怖いと言いました。")],
    "l5": [(M, "すみません、公園はどこですか。"),
           (F, "まっすぐ行ってください。スーパーのかどを左に曲がってください。公園は図書館の隣です。公園では犬と遊んでもいいですよ。")],
    "l6": [(M, "ひなたさんの数学の先生は、どんな人ですか。"),
           (F, "スミス先生はとても厳しいです。でも、真面目で、頭がいい先生です。授業は長いですが、全然つまらなくないです。でも、宿題がたくさんありますから、私は毎日暇がありません。")],
    "l7": [(M, "アロハさんのおばあさんのうちは、どうですか。"),
           (F, "おばあさんのうちは、とても古いです。伝統的なうちです。山の中にありますから、夏も涼しいです。でも、近くに店がありません。ちょっと不便です。")],
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
