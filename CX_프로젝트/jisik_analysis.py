import os, re, ast, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# 0. 한글 폰트
# ─────────────────────────────────────────────────────────

def set_korean_font():
    for path in ["C:/Windows/Fonts/malgun.ttf",
                 "C:/Windows/Fonts/NanumGothic.ttf",
                 "C:/Windows/Fonts/gulim.ttc"]:
        if os.path.exists(path):
            plt.rcParams["font.family"] = fm.FontProperties(fname=path).get_name()
            plt.rcParams["axes.unicode_minus"] = False
            return
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

set_korean_font()

# ─────────────────────────────────────────────────────────
# 1. 데이터 로드
# ─────────────────────────────────────────────────────────

print("=" * 60)
print(" 지식인 광파오븐 신혼부부 분석")
print("=" * 60)

df = pd.read_csv("jisik_preprocessed.csv", encoding="utf-8-sig")
print(f"로드 완료: {len(df)}행")

# tokens_full 문자열 → 리스트 변환
def parse_tokens(val):
    if not isinstance(val, str) or val.strip() == "":
        return []
    try:
        return ast.literal_eval(val)
    except Exception:
        return re.findall(r"[가-힣]{2,}", val)

df["tokens_full"]    = df["tokens_full"].apply(parse_tokens)
df["tokens_content"] = df["tokens_content"].apply(parse_tokens)
df["tokens_answer"]  = df["tokens_answer"].apply(parse_tokens)

df = df[df["tokens_full"].apply(len) >= 2].reset_index(drop=True)
print(f"유효 문서: {len(df)}개")

# ─────────────────────────────────────────────────────────
# 2. LDA 토픽모델링
# ─────────────────────────────────────────────────────────

print("\n[LDA] 토픽모델링 실행 중...")

from gensim import corpora
from gensim.models import LdaModel

NUM_TOPICS = 6

dictionary = corpora.Dictionary(df["tokens_full"].tolist())
dictionary.filter_extremes(no_below=5, no_above=0.65)
corpus = [dictionary.doc2bow(t) for t in df["tokens_full"].tolist()]

lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=NUM_TOPICS,
    passes=20,
    alpha="auto",
    eta="auto",
    random_state=42,
)
print(f"  LDA 완료 (토픽 수: {NUM_TOPICS})")

def get_dominant_topic(bow):
    topics = lda_model.get_document_topics(bow)
    return max(topics, key=lambda x: x[1])[0] if topics else -1

df["topic"] = [get_dominant_topic(bow) for bow in corpus]

# 토픽별 키워드 출력 후 실제 키워드 기반 라벨 결정
print("\n[LDA] 토픽별 실제 키워드:")
raw_keywords = {}
for i in range(NUM_TOPICS):
    words = lda_model.show_topic(i, topn=10)
    kws = [w for w, _ in words]
    raw_keywords[i] = kws
    print(f"  T{i+1}: {', '.join(kws)}")

# 실제 키워드 기반 라벨
TOPIC_LABELS = {
    0: "혼수가전 구매/브랜드 비교",
    1: "오븐 크기·설치·공간 고민",
    2: "광파오븐 vs 에어프라이어 선택",
    3: "신혼 요리 시작/레시피 활용",
    4: "스팀·기능 비교 및 청소",
    5: "출산·육아 후 오븐 활용",
}

print("\n[LDA] 토픽 라벨 (실제 키워드 기반):")
for i in range(NUM_TOPICS):
    cnt = (df["topic"] == i).sum()
    print(f"  T{i+1} [{TOPIC_LABELS[i]}] - {cnt}개 ({cnt/len(df)*100:.1f}%)")
    print(f"       핵심 키워드: {', '.join(raw_keywords[i][:7])}")

df["topic_label"] = df["topic"].map(TOPIC_LABELS)

# ─────────────────────────────────────────────────────────
# 3. 감성분석 (도메인 감성사전)
# ─────────────────────────────────────────────────────────

print("\n[감성분석] 분류 중...")

POS_WORDS = {
    "좋다","좋아","좋은","좋고","최고","편리","편하다","편해","편한","만족",
    "추천","유용","효율","간편","쉽다","쉬운","쉽게","간단","훌륭","완벽",
    "맛있다","맛있어","맛있는","신기","멋지다","깔끔","예쁘다","예쁜","실용",
    "강력","탁월","우수","저렴","가성비","착하다","합리적","다양","빠르다",
    "뛰어나다","뛰어난","딱","행복","즐거운","도움","감사","사랑","소중",
    "바삭","겉바속촉","맛집","극찬","강추","혜자","득템","꿀템","인생템",
    "필수","필수템","칭찬","감동","만능","편의","활용","효과","적합","안성맞춤",
    "성능","깔끔하다","정확","빠른","절약","특별","특화","다목적","올인원",
}

NEG_WORDS = {
    "불편","불편하다","불편해","어렵다","어려워","복잡","실망","후회","문제",
    "고장","비싸다","비싸","비싼","짜증","불량","부족","아쉽다","아쉬워",
    "아쉬운","아쉬움","별로","최악","힘들다","힘든","불만","단점","무겁다",
    "느리다","소음","시끄럽다","냄새","악취","귀찮다","귀찮은","번거롭다",
    "번거로운","고민","망설임","애매","낭비","거품","바가지","실패","망했다",
    "손해","헛돈","비추","안된다","오류","작동안함","무용지물","과하다",
    "과소비","불필요","한계","포기","기대이하","실용성없다","청소힘들다",
}

def analyze_sentiment(tokens):
    pos = sum(1 for t in tokens if t in POS_WORDS)
    neg = sum(1 for t in tokens if t in NEG_WORDS)
    if pos > neg:   return "긍정"
    elif neg > pos: return "부정"
    else:           return "중립"

df["sentiment"] = df["tokens_full"].apply(analyze_sentiment)

sent_counts = df["sentiment"].value_counts()
total = len(df)
print(f"  긍정: {sent_counts.get('긍정',0)}개 ({sent_counts.get('긍정',0)/total*100:.1f}%)")
print(f"  중립: {sent_counts.get('중립',0)}개 ({sent_counts.get('중립',0)/total*100:.1f}%)")
print(f"  부정: {sent_counts.get('부정',0)}개 ({sent_counts.get('부정',0)/total*100:.1f}%)")

# ─────────────────────────────────────────────────────────
# 4. Opportunity Score
# ─────────────────────────────────────────────────────────

print("\n[Opportunity Score] 계산 중...")

records = []
for label, grp in df.groupby("topic_label"):
    n   = len(grp)
    pos = (grp["sentiment"] == "긍정").sum()
    neg = (grp["sentiment"] == "부정").sum()
    pol = pos + neg

    # 지식인은 조회수 없으므로: 볼륨(70%) + 카테고리 다양성(30%)
    vol_raw  = n / total
    cat_div  = grp["category"].nunique() / df["category"].nunique()

    records.append({
        "토픽":       label,
        "문서수":     n,
        "긍정":       pos,
        "부정":       neg,
        "중립":       n - pos - neg,
        "긍정률":     round(pos / n * 100, 1),
        "부정률":     round(neg / n * 100, 1),
        "_vol":       vol_raw,
        "_cat_div":   cat_div,
        "_pol":       pol,
    })

df_opp = pd.DataFrame(records)

def minmax(s, lo=1, hi=10):
    mn, mx = s.min(), s.max()
    return lo + (s - mn) / (mx - mn) * (hi - lo) if mx != mn else pd.Series([5.0]*len(s), index=s.index)

df_opp["중요도"] = (minmax(df_opp["_vol"]) * 0.7 +
                    minmax(df_opp["_cat_div"]) * 0.3).round(2)
df_opp["만족도"] = df_opp.apply(
    lambda r: round(r["긍정"] / r["_pol"] * 10, 2) if r["_pol"] > 0 else 5.0, axis=1)
df_opp["기회점수"] = (df_opp["중요도"] +
    (df_opp["중요도"] - df_opp["만족도"]).clip(lower=0)).round(2)
df_opp = df_opp.sort_values("기회점수", ascending=False).reset_index(drop=True)

def classify_area(row):
    mid_i = df_opp["중요도"].median()
    mid_s = df_opp["만족도"].median()
    hi, hs = row["중요도"] >= mid_i, row["만족도"] >= mid_s
    if hi and not hs:   return "과소충족 기회"
    elif hi and hs:     return "충족 영역"
    elif not hi and hs: return "과잉충족 영역"
    else:               return "무관심 영역"

df_opp["Area"] = df_opp.apply(classify_area, axis=1)

AREA_COLOR = {
    "과소충족 기회":  "#E53935",
    "충족 영역":      "#43A047",
    "무관심 영역":    "#757575",
    "과잉충족 영역":  "#1E88E5",
}

# ─────────────────────────────────────────────────────────
# 5. 시각화
# ─────────────────────────────────────────────────────────

print("\n[시각화] 차트 생성 중...")

# ── 5-1. 종합 분석 차트 ────────────────────────────────────

fig = plt.figure(figsize=(22, 24))
fig.suptitle("지식인 신혼부부 광파오븐 분석 결과",
             fontsize=17, fontweight="bold", y=0.99)

# 전체 감성 파이차트
ax1 = fig.add_subplot(4, 3, 1)
ax1.pie(
    [sent_counts.get("긍정",0), sent_counts.get("중립",0), sent_counts.get("부정",0)],
    labels=["긍정","중립","부정"],
    autopct="%1.1f%%",
    colors=["#4CAF50","#9E9E9E","#F44336"],
    startangle=90,
)
ax1.set_title("전체 감성 분포", fontsize=12, fontweight="bold")

# 카테고리별 감성 비율
ax2 = fig.add_subplot(4, 3, (2, 3))
cat_sent = df.groupby(["category","sentiment"]).size().unstack(fill_value=0)
for col in ["긍정","중립","부정"]:
    if col not in cat_sent.columns: cat_sent[col] = 0
cat_sent_pct = cat_sent[["긍정","중립","부정"]].div(cat_sent.sum(axis=1), axis=0) * 100
cat_sent_pct.plot(kind="barh", stacked=True, ax=ax2,
                  color=["#4CAF50","#9E9E9E","#F44336"], width=0.7)
ax2.set_title("카테고리별 감성 비율 (%)", fontsize=12, fontweight="bold")
ax2.set_xlabel("비율 (%)")
ax2.legend(loc="lower right", fontsize=9)

# 토픽별 문서 수
ax3 = fig.add_subplot(4, 3, 4)
tc = df["topic"].value_counts().sort_index()
labels_t = [f"T{i+1}\n{TOPIC_LABELS.get(i,'')[:8]}" for i in tc.index]
bars = ax3.bar(labels_t, tc.values,
               color=plt.cm.Set2(np.linspace(0, 1, NUM_TOPICS)))
ax3.set_title("토픽별 문서 수", fontsize=12, fontweight="bold")
ax3.set_ylabel("문서 수")
ax3.tick_params(axis="x", labelsize=7)
for bar, v in zip(bars, tc.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             str(v), ha="center", va="bottom", fontsize=8)

# 상위 4개 토픽 키워드
for idx, tid in enumerate(tc.nlargest(4).index):
    ax = fig.add_subplot(4, 3, 5 + idx)
    ws = lda_model.show_topic(tid, topn=10)
    words  = [w for w, _ in ws][::-1]
    scores = [s for _, s in ws][::-1]
    ax.barh(words, scores, color=plt.cm.Set2(tid / NUM_TOPICS))
    ax.set_title(f"T{tid+1}. {TOPIC_LABELS.get(tid,'')}", fontsize=9, fontweight="bold")
    ax.set_xlabel("가중치")
    ax.tick_params(axis="y", labelsize=8)

# 카테고리별 토픽 분포 (히트맵)
ax_hm = fig.add_subplot(4, 3, (9, 10))
ct = pd.crosstab(df["category"], df["topic_label"])
ct.columns = [c[:10] for c in ct.columns]
sns.heatmap(ct, annot=True, fmt="d", cmap="YlOrRd", ax=ax_hm,
            linewidths=0.5, cbar_kws={"shrink": 0.8})
ax_hm.set_title("카테고리 × 토픽 분포", fontsize=12, fontweight="bold")
ax_hm.set_xlabel("")
ax_hm.set_ylabel("")
ax_hm.tick_params(axis="x", rotation=30, labelsize=7)
ax_hm.tick_params(axis="y", rotation=0,  labelsize=8)

# 토픽별 감성 비율
ax_ts = fig.add_subplot(4, 3, (11, 12))
topic_sent = df[df["topic"] >= 0].groupby(["topic","sentiment"]).size().unstack(fill_value=0)
for col in ["긍정","중립","부정"]:
    if col not in topic_sent.columns: topic_sent[col] = 0
topic_sent_pct = topic_sent[["긍정","중립","부정"]].div(topic_sent.sum(axis=1), axis=0) * 100
topic_sent_pct.index = [f"T{i+1}.{TOPIC_LABELS.get(i,'')[:7]}" for i in topic_sent_pct.index]
topic_sent_pct.plot(kind="bar", stacked=True, ax=ax_ts,
                    color=["#4CAF50","#9E9E9E","#F44336"], width=0.7)
ax_ts.set_title("토픽별 감성 비율 (%)", fontsize=12, fontweight="bold")
ax_ts.set_ylabel("비율 (%)")
ax_ts.legend(loc="upper right", fontsize=9)
ax_ts.tick_params(axis="x", rotation=25, labelsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("jisik_analysis_result.png", dpi=150, bbox_inches="tight")
plt.close()
print("  저장: jisik_analysis_result.png")

# ── 5-2. Opportunity Score 차트 ────────────────────────────

fig2 = plt.figure(figsize=(20, 14))
fig2.suptitle("Opportunity Score & Area - 지식인 신혼부부 광파오븐",
              fontsize=15, fontweight="bold", y=0.99)

# Opportunity Score 바차트
ax_b = fig2.add_subplot(2, 2, 1)
colors_bar = [AREA_COLOR[a] for a in df_opp["Area"]]
bars2 = ax_b.barh(df_opp["토픽"][::-1], df_opp["기회점수"][::-1],
                  color=colors_bar[::-1], edgecolor="white", height=0.6)
ax_b.axvline(x=10, color="gray", linestyle="--", linewidth=1, alpha=0.6)
ax_b.set_title("Opportunity Score (토픽별)", fontsize=12, fontweight="bold")
ax_b.set_xlabel("Opportunity Score")
ax_b.tick_params(axis="y", labelsize=8)
for bar, val in zip(bars2, df_opp["기회점수"][::-1]):
    ax_b.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=9, fontweight="bold")
patches = [mpatches.Patch(color=c, label=l) for l, c in AREA_COLOR.items()]
ax_b.legend(handles=patches, fontsize=8, loc="lower right")

# Opportunity Matrix
ax_m = fig2.add_subplot(2, 2, 2)
mid_i = df_opp["중요도"].median()
mid_s = df_opp["만족도"].median()
ax_m.axhspan(mid_i, df_opp["중요도"].max()+0.5, xmin=0,   xmax=0.5,
             facecolor="#FFEBEE", alpha=0.45)
ax_m.axhspan(mid_i, df_opp["중요도"].max()+0.5, xmin=0.5, xmax=1,
             facecolor="#E8F5E9", alpha=0.45)
ax_m.axhspan(0,     mid_i,                       xmin=0,   xmax=0.5,
             facecolor="#F5F5F5", alpha=0.45)
ax_m.axhspan(0,     mid_i,                       xmin=0.5, xmax=1,
             facecolor="#E3F2FD", alpha=0.45)
ax_m.axhline(y=mid_i, color="gray", linestyle="--", lw=1, alpha=0.7)
ax_m.axvline(x=mid_s, color="gray", linestyle="--", lw=1, alpha=0.7)

x_min = df_opp["만족도"].min() - 0.3
x_max = df_opp["만족도"].max() + 0.3
y_max = df_opp["중요도"].max() + 0.5

ax_m.text(mid_s-0.1, y_max-0.1, "과소충족 기회\n(최우선)", ha="right", va="top",
          fontsize=8.5, color="#C62828", fontweight="bold")
ax_m.text(mid_s+0.1, y_max-0.1, "충족 영역\n(유지·강화)", ha="left", va="top",
          fontsize=8.5, color="#2E7D32", fontweight="bold")
ax_m.text(mid_s-0.1, 0.1, "무관심 영역\n(후순위)", ha="right", va="bottom",
          fontsize=8.5, color="#424242")
ax_m.text(mid_s+0.1, 0.1, "과잉충족\n(투자 축소)", ha="left", va="bottom",
          fontsize=8.5, color="#1565C0")

for _, row in df_opp.iterrows():
    color = AREA_COLOR[row["Area"]]
    ax_m.scatter(row["만족도"], row["중요도"], s=150+row["문서수"]/3,
                 color=color, alpha=0.85, edgecolors="white", lw=1.2, zorder=5)
    ax_m.annotate(row["토픽"][:12], (row["만족도"], row["중요도"]),
                  textcoords="offset points", xytext=(6, 4),
                  fontsize=7.5, color=color, fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="none"))

ax_m.set_xlabel("만족도 (Satisfaction)", fontsize=9)
ax_m.set_ylabel("중요도 (Importance)", fontsize=9)
ax_m.set_title("Opportunity Matrix", fontsize=12, fontweight="bold")
ax_m.set_xlim(x_min, x_max)
ax_m.set_ylim(0, y_max)

# 중요도/만족도/기회점수 비교
ax_c = fig2.add_subplot(2, 2, (3, 4))
x = np.arange(len(df_opp))
w = 0.28
ax_c.bar(x - w, df_opp["중요도"],  w, label="중요도",  color="#1976D2", alpha=0.85)
ax_c.bar(x,     df_opp["만족도"],  w, label="만족도",  color="#FF7043", alpha=0.85)
ax_c.bar(x + w, df_opp["기회점수"], w, label="기회점수", color="#6A1B9A", alpha=0.85)
ax_c.set_xticks(x)
ax_c.set_xticklabels(df_opp["토픽"], rotation=18, ha="right", fontsize=8.5)
ax_c.set_ylabel("점수 (0~10)", fontsize=9)
ax_c.set_title("토픽별 중요도 / 만족도 / 기회점수 비교", fontsize=12, fontweight="bold")
ax_c.legend(fontsize=9)
ax_c.set_ylim(0, 13)
for i, col in enumerate(["중요도","만족도","기회점수"]):
    for j, val in enumerate(df_opp[col]):
        ax_c.text(j + (i-1)*w, val + 0.1, f"{val:.1f}",
                  ha="center", va="bottom", fontsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("jisik_opportunity_score.png", dpi=150, bbox_inches="tight")
plt.close()
print("  저장: jisik_opportunity_score.png")

# ── 5-3. pyLDAvis ──────────────────────────────────────────
try:
    import pyLDAvis
    import pyLDAvis.gensim_models as gensimvis
    vis = gensimvis.prepare(lda_model, corpus, dictionary, mds="mmds")
    pyLDAvis.save_html(vis, "jisik_lda_visualization.html")
    print("  저장: jisik_lda_visualization.html")
except Exception as e:
    print(f"  pyLDAvis 건너뜀: {e}")

# ─────────────────────────────────────────────────────────
# 6. 결과 저장
# ─────────────────────────────────────────────────────────

df["topic_label"] = df["topic"].map(TOPIC_LABELS)
out = df[["category","keyword","title","content_clean","answer_clean",
          "sentiment","topic","topic_label","url"]]
out.to_csv("jisik_analysis_result.csv", index=False, encoding="utf-8-sig")
print("  저장: jisik_analysis_result.csv")

df_opp[["토픽","문서수","긍정률","부정률","중요도","만족도","기회점수","Area"]]\
    .to_csv("jisik_opportunity_score.csv", index=False, encoding="utf-8-sig")
print("  저장: jisik_opportunity_score.csv")

# ─────────────────────────────────────────────────────────
# 7. 최종 결과 요약
# ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(" 최종 분석 결과 요약")
print("=" * 60)

print(f"\n[데이터] 총 {len(df)}개 Q&A 문서 분석\n")

print("[감성분석]")
for s, c in sent_counts.items():
    print(f"  {s}: {c}개 ({c/total*100:.1f}%)")

print("\n[LDA 토픽]")
for i in range(NUM_TOPICS):
    cnt = (df["topic"] == i).sum()
    print(f"  T{i+1} [{TOPIC_LABELS[i]}] - {cnt}개 ({cnt/len(df)*100:.1f}%)")
    print(f"       {', '.join(raw_keywords[i][:6])}")

print("\n[Opportunity Score]")
print(f"  {'토픽':<24} {'중요도':>5} {'만족도':>5} {'기회점수':>6}  Area")
print("  " + "-" * 58)
for _, row in df_opp.iterrows():
    print(f"  {row['토픽']:<24} {row['중요도']:>5.2f} {row['만족도']:>5.2f} "
          f"{row['기회점수']:>6.2f}  {row['Area']}")

print("\n[최우선 콘텐츠 기회 - 과소충족 기회 영역]")
top = df_opp[df_opp["Area"] == "과소충족 기회"]
for _, row in top.iterrows():
    print(f"  >> {row['토픽']}  (기회점수: {row['기회점수']:.1f} | 부정률: {row['부정률']}%)")

print("\n[페인포인트 - 부정 댓글 빈출 단어]")
neg_tok = df[df["sentiment"]=="부정"]["tokens_full"].explode()
print("  " + " / ".join(f"{w}({c})" for w, c in Counter(neg_tok).most_common(15)))

print("\n[니즈 - 긍정 댓글 빈출 단어]")
pos_tok = df[df["sentiment"]=="긍정"]["tokens_full"].explode()
print("  " + " / ".join(f"{w}({c})" for w, c in Counter(pos_tok).most_common(15)))

print("\n" + "=" * 60)
print(" 완료! 생성 파일:")
print("  - jisik_analysis_result.png")
print("  - jisik_opportunity_score.png")
print("  - jisik_lda_visualization.html")
print("  - jisik_analysis_result.csv")
print("  - jisik_opportunity_score.csv")
print("=" * 60)
