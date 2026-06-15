import os, re, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from collections import Counter

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# 0. 한글 폰트 설정
# ─────────────────────────────────────────────────────────

def set_korean_font():
    for path in ["C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/NanumGothic.ttf",
                 "C:/Windows/Fonts/gulim.ttc"]:
        if os.path.exists(path):
            plt.rcParams["font.family"] = fm.FontProperties(fname=path).get_name()
            plt.rcParams["axes.unicode_minus"] = False
            return path
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False
    return None

FONT_PATH = set_korean_font()

# ─────────────────────────────────────────────────────────
# 1. 데이터 로드
# ─────────────────────────────────────────────────────────

print("=" * 60)
print(" 신혼부부 광파오븐 콘텐츠 분석")
print("=" * 60)

df_v = pd.read_csv("youtube_videos.csv",   encoding="utf-8-sig")
df_c = pd.read_csv("youtube_comments.csv", encoding="utf-8-sig")

# 영상-키워드 매핑
vid2kw = df_v.set_index("video_id")["keyword"].to_dict()
df_c["keyword"] = df_c["video_id"].map(vid2kw)

print(f"영상: {len(df_v)}개 | 댓글: {len(df_c)}개")

# ─────────────────────────────────────────────────────────
# 2. 텍스트 전처리
# ─────────────────────────────────────────────────────────

STOPWORDS = set([
    "이","그","저","것","수","때","등","및","를","가","은","는","에","의","로","도",
    "을","와","과","하","있","되","않","없","나","우리","더","아주","진짜","너무",
    "정말","같은","이런","그런","저런","하는","있는","없는","으로","에서","에게",
    "부터","까지","한","합니다","해요","했","했어요","해서","이고","이라","거","게",
    "건","걸","좀","제","내","내가","그냥","여기","저기","어디","왜","어떻게",
    "얼마나","뭐","뭔가","뭘","누구","언제","어느","구매","배송","구입","가격",
    "후기","제품","블로그","포스팅","클릭","바로","정도","조금","많이","이번",
    "오늘","어제","최근","항상","매일","처음","마지막","다시","또","계속","진짜",
    "유튜브","영상","댓글","구독","채널","소개","추천","영상","보고","좋아",
    "ㅋㅋ","ㅎㅎ","ㅠㅠ","ㅜㅜ","ㄱㄱ","ㄷㄷ","ㅠ","ㅜ","ㅋ","ㅎ",
    "생각","경우","부분","이용","사용","관련","내용","방법","때문","기준",
    "느낌","정보","이후","이전","가능","기능","제가","저도","저는","저희",
])

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_nouns(texts, min_len=2):
    try:
        from konlpy.tag import Okt
        okt = Okt()
        result = []
        for text in texts:
            nouns = okt.nouns(text)
            filtered = [n for n in nouns if len(n) >= min_len and n not in STOPWORDS]
            result.append(filtered)
        print("  KoNLPy Okt 사용")
        return result
    except Exception as e:
        print(f"  KoNLPy 오류({e}) -> 정규식 대체")
        result = []
        for text in texts:
            words = re.findall(r"[가-힣]{2,}", text)
            filtered = [w for w in words if w not in STOPWORDS]
            result.append(filtered)
        return result

print("\n[전처리] 텍스트 정제 중...")
df_c["clean"] = df_c["text"].apply(clean_text)
df_c = df_c[df_c["clean"].str.len() >= 5].reset_index(drop=True)
print(f"  유효 댓글: {len(df_c)}개")

print("[전처리] 명사 추출 중... (시간이 걸릴 수 있습니다)")
texts_list = df_c["clean"].tolist()
tokenized = extract_nouns(texts_list)
df_c["tokens"] = tokenized
df_c = df_c[df_c["tokens"].apply(len) >= 2].reset_index(drop=True)
print(f"  토큰 추출 완료: {len(df_c)}개 댓글")


# ─────────────────────────────────────────────────────────
# 3. LDA 토픽모델링
# ─────────────────────────────────────────────────────────

print("\n[LDA] 토픽 모델링 실행 중...")

from gensim import corpora
from gensim.models import LdaModel

NUM_TOPICS = 7

dictionary = corpora.Dictionary(df_c["tokens"].tolist())
dictionary.filter_extremes(no_below=5, no_above=0.6)
corpus = [dictionary.doc2bow(tokens) for tokens in df_c["tokens"].tolist()]

lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=NUM_TOPICS,
    passes=15,
    alpha="auto",
    eta="auto",
    random_state=42,
)
print(f"  LDA 완료 (토픽 수: {NUM_TOPICS})")

# 각 댓글에 주요 토픽 할당
def get_dominant_topic(bow):
    topics = lda_model.get_document_topics(bow)
    if not topics:
        return -1
    return max(topics, key=lambda x: x[1])[0]

df_c["topic"] = [get_dominant_topic(bow) for bow in corpus]

# 토픽별 상위 키워드
topic_keywords = {}
TOPIC_LABELS = {}
TOPIC_NAME_MAP = {
    0: "신혼집 가전배치/공간고민",
    1: "음식물처리기/주방냄새",
    2: "혼수가전 구매/이사준비",
    3: "신혼살림/소형가전취향",
    4: "집밥 레시피/요리재료",
    5: "광파오븐·에프 비교/청소",
    6: "간단집밥/반찬레시피",
}

print("\n[LDA] 토픽별 주요 키워드:")
for i in range(NUM_TOPICS):
    words = lda_model.show_topic(i, topn=10)
    kws = [w for w, _ in words]
    topic_keywords[i] = kws
    label = TOPIC_NAME_MAP.get(i, f"토픽{i+1}")
    TOPIC_LABELS[i] = label
    print(f"  토픽{i+1} [{label}]: {', '.join(kws)}")


# ─────────────────────────────────────────────────────────
# 4. 감성분석 (감성사전 기반)
# ─────────────────────────────────────────────────────────

print("\n[감성분석] 감성 분류 중...")

POS_WORDS = {
    "좋다", "좋아", "좋은", "최고", "편리", "편하다", "편해", "편한", "만족",
    "추천", "유용", "효율", "간편", "쉽다", "쉬운", "쉽게", "간단", "훌륭",
    "완벽", "맛있다", "맛있어", "맛있는", "맛있게", "신기", "멋지다", "멋진",
    "깔끔", "예쁘다", "예뻐", "예쁜", "실용", "강력", "탁월", "우수",
    "저렴", "가성비", "착하다", "합리적", "다양", "빠르다", "빠른", "빠르게",
    "성능", "뛰어나다", "뛰어난", "적합", "딱", "안성맞춤", "행복", "즐거운",
    "도움", "잘되다", "잘되", "잘됨", "잘나온다", "기대이상", "고마워",
    "감사", "사랑", "소중", "따뜻", "부드럽다", "촉촉", "바삭", "겉바속촉",
    "촉촉하다", "맛집", "극찬", "강추", "완벽", "혜자", "득템", "꿀템",
    "인생템", "필수", "필수템", "효도", "칭찬", "감동",
}

NEG_WORDS = {
    "불편", "불편하다", "불편해", "어렵다", "어려워", "복잡", "실망",
    "후회", "문제", "고장", "비싸다", "비싸", "비싼", "짜증", "불량",
    "부족", "아쉽다", "아쉬워", "아쉬운", "아쉬움", "별로", "최악",
    "힘들다", "힘들어", "힘든", "불만", "단점", "무겁다", "무거운",
    "느리다", "느린", "소음", "시끄럽다", "시끄러운", "냄새", "악취",
    "귀찮다", "귀찮아", "귀찮은", "번거롭다", "번거로운", "번거로워",
    "고민", "망설임", "모르겠다", "애매", "낭비", "거품", "바가지",
    "후기나쁨", "실패", "망했다", "망했어", "손해", "헛돈", "비추",
    "안되다", "안됨", "안나온다", "오류", "버그", "작동안함",
}

def analyze_sentiment(tokens):
    pos = sum(1 for t in tokens if t in POS_WORDS)
    neg = sum(1 for t in tokens if t in NEG_WORDS)
    if pos > neg:
        return "긍정"
    elif neg > pos:
        return "부정"
    else:
        return "중립"

df_c["sentiment"] = df_c["tokens"].apply(analyze_sentiment)

sent_counts = df_c["sentiment"].value_counts()
total = len(df_c)
print(f"  긍정: {sent_counts.get('긍정',0)}개 ({sent_counts.get('긍정',0)/total*100:.1f}%)")
print(f"  중립: {sent_counts.get('중립',0)}개 ({sent_counts.get('중립',0)/total*100:.1f}%)")
print(f"  부정: {sent_counts.get('부정',0)}개 ({sent_counts.get('부정',0)/total*100:.1f}%)")


# ─────────────────────────────────────────────────────────
# 5. 시각화
# ─────────────────────────────────────────────────────────

print("\n[시각화] 차트 생성 중...")

fig = plt.figure(figsize=(22, 26))
fig.suptitle("신혼부부 광파오븐 콘텐츠 기획 - YouTube 분석 결과",
             fontsize=17, fontweight="bold", y=0.98)

# ── 5-1. 전체 감성 분포 (파이차트) ──────────────────────────
ax1 = fig.add_subplot(4, 3, 1)
colors_sent = ["#4CAF50", "#9E9E9E", "#F44336"]
wedges, texts, autotexts = ax1.pie(
    [sent_counts.get("긍정", 0), sent_counts.get("중립", 0), sent_counts.get("부정", 0)],
    labels=["긍정", "중립", "부정"],
    autopct="%1.1f%%",
    colors=colors_sent,
    startangle=90,
)
for at in autotexts:
    at.set_fontsize(11)
ax1.set_title("전체 감성 분포", fontsize=12, fontweight="bold")

# ── 5-2. 키워드별 감성 비율 ────────────────────────────────
ax2 = fig.add_subplot(4, 3, (2, 3))
kw_sent = df_c.groupby(["keyword", "sentiment"]).size().unstack(fill_value=0)
for col in ["긍정", "중립", "부정"]:
    if col not in kw_sent.columns:
        kw_sent[col] = 0
kw_sent = kw_sent[["긍정", "중립", "부정"]]
kw_sent_pct = kw_sent.div(kw_sent.sum(axis=1), axis=0) * 100
kw_sent_pct.plot(kind="barh", stacked=True, ax=ax2,
                 color=["#4CAF50", "#9E9E9E", "#F44336"], width=0.7)
ax2.set_title("키워드별 감성 비율 (%)", fontsize=12, fontweight="bold")
ax2.set_xlabel("비율 (%)")
ax2.legend(loc="lower right", fontsize=9)
ax2.tick_params(axis="y", labelsize=8)

# ── 5-3. LDA 토픽 분포 ────────────────────────────────────
ax3 = fig.add_subplot(4, 3, 4)
topic_counts = df_c["topic"].value_counts().sort_index()
labels_t = [f"T{i+1}\n{TOPIC_LABELS.get(i,'')}" for i in topic_counts.index]
bars = ax3.bar(labels_t, topic_counts.values,
               color=plt.cm.Set2(np.linspace(0, 1, NUM_TOPICS)))
ax3.set_title("토픽별 댓글 수", fontsize=12, fontweight="bold")
ax3.set_ylabel("댓글 수")
ax3.tick_params(axis="x", labelsize=7)
for bar, v in zip(bars, topic_counts.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             str(v), ha="center", va="bottom", fontsize=8)

# ── 5-4. 토픽별 상위 키워드 (상위 4개 토픽) ──────────────────
for idx, topic_id in enumerate(topic_counts.nlargest(4).index):
    ax = fig.add_subplot(4, 3, 5 + idx)
    words_scores = lda_model.show_topic(topic_id, topn=10)
    words  = [w for w, _ in words_scores][::-1]
    scores = [s for _, s in words_scores][::-1]
    color = plt.cm.Set2(topic_id / NUM_TOPICS)
    bars2 = ax.barh(words, scores, color=color)
    ax.set_title(f"T{topic_id+1}. {TOPIC_LABELS.get(topic_id,'')}", fontsize=10, fontweight="bold")
    ax.set_xlabel("가중치")
    ax.tick_params(axis="y", labelsize=9)

# ── 5-5. 영상 조회수 TOP 10 ───────────────────────────────
ax_top = fig.add_subplot(4, 3, (9, 10))
top10 = df_v.nlargest(10, "view_count")[["title", "view_count"]].copy()
top10["title_short"] = top10["title"].str[:22] + "..."
bars3 = ax_top.barh(top10["title_short"][::-1], top10["view_count"][::-1] / 10000,
                    color="#1976D2")
ax_top.set_title("조회수 TOP 10 영상", fontsize=12, fontweight="bold")
ax_top.set_xlabel("조회수 (만)")
ax_top.tick_params(axis="y", labelsize=8)

# ── 5-6. 토픽별 감성 비율 ────────────────────────────────
ax_ts = fig.add_subplot(4, 3, (11, 12))
topic_sent = df_c[df_c["topic"] >= 0].groupby(["topic", "sentiment"]).size().unstack(fill_value=0)
for col in ["긍정", "중립", "부정"]:
    if col not in topic_sent.columns:
        topic_sent[col] = 0
topic_sent = topic_sent[["긍정", "중립", "부정"]]
topic_sent_pct = topic_sent.div(topic_sent.sum(axis=1), axis=0) * 100
topic_sent_pct.index = [f"T{i+1}.{TOPIC_LABELS.get(i,'')[:6]}" for i in topic_sent_pct.index]
topic_sent_pct.plot(kind="bar", stacked=True, ax=ax_ts,
                    color=["#4CAF50", "#9E9E9E", "#F44336"], width=0.7)
ax_ts.set_title("토픽별 감성 비율 (%)", fontsize=12, fontweight="bold")
ax_ts.set_xlabel("")
ax_ts.set_ylabel("비율 (%)")
ax_ts.legend(loc="upper right", fontsize=9)
ax_ts.tick_params(axis="x", rotation=30, labelsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("analysis_result.png", dpi=150, bbox_inches="tight")
plt.close()
print("  저장: analysis_result.png")


# ─────────────────────────────────────────────────────────
# 6. pyLDAvis 인터랙티브 시각화
# ─────────────────────────────────────────────────────────

try:
    import pyLDAvis
    import pyLDAvis.gensim_models as gensimvis
    vis = gensimvis.prepare(lda_model, corpus, dictionary, mds="mmds")
    pyLDAvis.save_html(vis, "lda_visualization.html")
    print("  저장: lda_visualization.html (브라우저로 열어보세요)")
except Exception as e:
    print(f"  pyLDAvis 오류 (건너뜀): {e}")


# ─────────────────────────────────────────────────────────
# 7. 결과 저장
# ─────────────────────────────────────────────────────────

df_c["topic_label"] = df_c["topic"].map(TOPIC_LABELS)
out_cols = ["video_id", "keyword", "text", "sentiment", "topic", "topic_label"]
df_c[out_cols].to_csv("youtube_analysis_result.csv", index=False, encoding="utf-8-sig")
print("  저장: youtube_analysis_result.csv")


# ─────────────────────────────────────────────────────────
# 8. 분석 결과 요약 출력
# ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(" 분석 결과 요약")
print("=" * 60)

print(f"\n[데이터] 영상 {len(df_v)}개 | 분석 댓글 {len(df_c)}개\n")

print("[감성분석 결과]")
for sent, cnt in sent_counts.items():
    print(f"  {sent}: {cnt}개 ({cnt/total*100:.1f}%)")

print("\n[LDA 토픽 분석 결과]")
for i in range(NUM_TOPICS):
    cnt = (df_c["topic"] == i).sum()
    kws = ", ".join(topic_keywords[i][:6])
    label = TOPIC_LABELS.get(i, "")
    print(f"  T{i+1} [{label}] - {cnt}개 ({cnt/len(df_c)*100:.1f}%)")
    print(f"       핵심 키워드: {kws}")

print("\n[키워드별 긍정률 TOP 5]")
kw_pos_rate = (kw_sent_pct["긍정"].sort_values(ascending=False))
for kw, rate in kw_pos_rate.head(5).items():
    print(f"  '{kw}' - 긍정 {rate:.1f}%")

print("\n[키워드별 부정률 TOP 5]")
kw_neg_rate = (kw_sent_pct["부정"].sort_values(ascending=False))
for kw, rate in kw_neg_rate.head(5).items():
    print(f"  '{kw}' - 부정 {rate:.1f}%")

print("\n[조회수 TOP 5 영상]")
for _, row in df_v.nlargest(5, "view_count").iterrows():
    print(f"  {row['view_count']//10000}만회 | {row['title'][:40]}")

print("\n[페인포인트 추정 - 부정 댓글 빈출 단어]")
neg_comments = df_c[df_c["sentiment"] == "부정"]["tokens"].explode()
neg_top = Counter(neg_comments).most_common(15)
print("  " + " / ".join([f"{w}({c})" for w, c in neg_top]))

print("\n[니즈 추정 - 긍정 댓글 빈출 단어]")
pos_comments = df_c[df_c["sentiment"] == "긍정"]["tokens"].explode()
pos_top = Counter(pos_comments).most_common(15)
print("  " + " / ".join([f"{w}({c})" for w, c in pos_top]))

print("\n" + "=" * 60)
print(" 완료! 생성 파일:")
print("  - analysis_result.png     (종합 시각화)")
print("  - lda_visualization.html  (인터랙티브 LDA)")
print("  - youtube_analysis_result.csv (댓글+토픽+감성 통합)")
print("=" * 60)
