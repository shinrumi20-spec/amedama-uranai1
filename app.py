import streamlit as st
import datetime as dt
import random
from textwrap import dedent

st.set_page_config(page_title="飴玉占い🍬", page_icon="🍬")

st.title("飴玉占い（栄養素で吉凶）🍬")
st.caption("Python × Streamlit でつくった無料の占いアプリ")

# --- データ定義（お好みで増減OK） ---
CANDIES = [
    {"name": "みかんビタミンC飴", "nutrient": "ビタミンC", "desc": "免疫サポート＆美容に◎"},
    {"name": "緑茶カテキン飴",   "nutrient": "カテキン",   "desc": "リフレッシュ＆気分すっきり"},
    {"name": "こんぶ食物繊維飴", "nutrient": "食物繊維", "desc": "整える・ため込まない"},
    {"name": "はちみつプロポリス飴", "nutrient": "プロポリス", "desc": "のど守って会話もスムーズ"},
    {"name": "ヨーグルト乳酸菌飴", "nutrient": "乳酸菌",   "desc": "ごきげんバランスUP"},
    {"name": "レモンクエン酸飴",  "nutrient": "クエン酸",  "desc": "疲れにサッと効く回復系"},
]

# 栄養素→運勢候補（重み付き）
FORTUNES = {
    "ビタミンC": [
        ("大吉", "チャンスに光。新しい連絡には即レスで◎", 3),
        ("中吉", "整う日。5分の深呼吸で集中UP", 2),
        ("小吉", "整える日。机回りの片付けから", 1),
    ],
    "カテキン": [
        ("大吉", "直感ズバリ。迷ったら最初の案で", 2),
        ("中吉", "人間関係スムーズ。挨拶多めで吉", 2),
        ("小吉", "無理は禁物。15分の散歩が開運", 1),
    ],
    "食物繊維": [
        ("大吉", "積み上げが実る。習慣タスクを先に", 2),
        ("中吉", "情報整理◎。メモ→1行要約で進む", 2),
        ("小吉", "小休憩で流れ良く。白湯タイム吉", 1),
    ],
    "プロポリス": [
        ("大吉", "発信力UP。短い言葉が刺さる日", 2),
        ("中吉", "交渉◎。相手の“目的”を先に確認", 2),
        ("小吉", "喉ケア吉。のど飴＆加湿で運気安定", 1),
    ],
    "乳酸菌": [
        ("大吉", "チーム運◎。ありがとうを3回言う", 2),
        ("中吉", "学習効率UP。午前中に1学び", 2),
        ("小吉", "寝不足注意。早寝宣言で回復", 1),
    ],
    "クエン酸": [
        ("大吉", "スピード決断吉。先送りは1つだけ", 2),
        ("中吉", "やり切り運。25分タイマーで集中", 2),
        ("小吉", "エネルギーチャージ。ストレッチ吉", 1),
    ],
}

def weighted_choice(rng, items):
    # items: [(fortune, advice, weight)]
    population = []
    for (f, a, w) in items:
        population += [(f, a)] * int(w)
    return rng.choice(population)

def daily_result(name: str):
    """名前(任意) + 今日の日付で毎日固定の結果にする"""
    today = dt.date.today().isoformat()
    seed_str = f"{name}|{today}"
    rng = random.Random(seed_str)
    candy = rng.choice(CANDIES)
    (fortune, advice) = weighted_choice(rng, FORTUNES[candy["nutrient"]])
    return today, candy, fortune, advice

def random_result():
    rng = random.Random()
    candy = rng.choice(CANDIES)
    (fortune, advice) = weighted_choice(rng, FORTUNES[candy["nutrient"]])
    return candy, fortune, advice

# --- UI ---
st.subheader("1) ニックネーム（任意）")
name = st.text_input("占い結果を“今日の運勢”として毎日固定化したい場合は記入（未記入でもOK）", value="")

col1, col2 = st.columns(2)
with col1:
    if st.button("今日の飴をひく（毎日固定）", use_container_width=True):
        today, candy, fortune, advice = daily_result(name.strip())
        st.success(f"📅 {today} の運勢 / {name or 'あなた'} さん")
        st.markdown(f"### 🍬 {candy['name']}（栄養素：{candy['nutrient']}）")
        st.caption(candy["desc"])
        st.markdown(f"## 結果：**{fortune}**")
        st.write(f"🔑 アドバイス：{advice}")
        share = dedent(f"""
        【飴玉占い🍬】{today}
        今日の私は「{candy['name']}（{candy['nutrient']}）」で **{fortune}**
        メモ：{advice}
        """).strip()
        st.code(share, language="markdown")

with col2:
    if st.button("シャッフル（完全ランダム）", type="secondary", use_container_width=True):
        candy, fortune, advice = random_result()
        st.info("結果は毎回変わります（シェア用は上の“今日の飴”がおすすめ）")
        st.markdown(f"### 🍬 {candy['name']}（栄養素：{candy['nutrient']}）")
        st.caption(candy["desc"])
        st.markdown(f"## 結果：**{fortune}**")
        st.write(f"🔑 アドバイス：{advice}")

st.divider()
with st.expander("▼ 使い方・メモ"):
    st.markdown(
        "- 「今日の飴」は、ニックネーム＋日付で結果が毎日固定になります。\n"
        "- ニックネーム未入力でもOK（その場合は“あなた”で固定されます）。\n"
        "- “シャッフル”はその場のランダム結果です。"
    )
