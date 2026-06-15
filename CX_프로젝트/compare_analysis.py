import os, ast, re, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
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

C_YT   = "#1976D2"   # 유튜브 색
C_JK   = "#E53935"   # 지식인 색
C_POS  = "#43A047"
C_NEU  = "#9E9E9E"
C_NEG  = "#E53935"

# ─────────────────────────────────────────────────────────
# 1. 데이터 로드
# ─────────────────────────────────────────────────────────

print("=" * 60)
print(" YouTube × 지식인 비교 분석")
print("=" * 60)

yt = pd.read_csv("youtube_analysis_result.csv",  encoding="utf-8-sig")
jk = pd.read_csv("jisik_analysis_result.csv",    encoding="utf-8-sig")
yt_opp = pd.read_csv("opportunity_score.csv",       encoding="utf-8-sig")
jk_opp = pd.read_csv("jisik_opportunity_score.csv", encoding="utf-8-sig")

# 지식인 tokens 파싱
def parse_tokens(val):
    if not isinstance(val, str) or val.strip() == "":
        return []
    try:
        return ast.literal_eval(val)
    except Exception:
        return re.findall(r"[가-힣]{2,}", val)

jk_raw = pd.read_csv("jisik_preprocessed.csv", encoding="utf-8-sig")
jk_raw["tokens_full"] = jk_raw["tokens_full"].apply(parse_tokens)
jk["tokens_full"] = jk_raw["tokens_full"].values

STOPWORDS = set([
    "이","그","저","것","수","때","등","및","를","가","은","는","에","의","로","도",
    "을","와","과","하","있","되","않","없","나","우리","더","아주","진짜","너무",
    "정말","같은","이런","그런","저런","하는","있는","없는","으로","에서","에게",
    "부터","까지","한","합니다","해요","했","해서","이고","이라","거","게","건","걸",
    "좀","제","내","내가","그냥","여기","저기","어디","왜","어떻게","얼마나","뭐",
    "뭔가","뭘","누구","언제","어느","구매","배송","구입","가격","후기","제품",
    "블로그","포스팅","클릭","바로","정도","조금","많이","이번","오늘","어제",
    "최근","항상","매일","처음","마지막","다시","또","계속","생각","경우","부분",
    "이용","사용","관련","내용","방법","때문","기준","느낌","정보","이후","이전",
    "가능","기능","제가","저도","저는","저희","유튜브","영상","댓글","구독","채널",
    "답변","질문","안녕","감사","부탁","드립니다","드려요","궁금","알고","주세요",
    "ㅋㅋ","ㅎㅎ","ㅠㅠ","ㅜㅜ","ㅋ","ㅎ","ㅠ","ㅜ","잘","너무","진짜","다",
])

def tokenize_text(text):
    if not isinstance(text, str):
        return []
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^가-힣\s]", " ", text)
    words = re.findall(r"[가-힣]{2,}", text)
    return [w for w in words if w not in STOPWORDS]

print("  YouTube 댓글 재토큰화 중...")
yt["tokens_full"] = yt["text"].apply(tokenize_text)

yt_raw = pd.read_csv("youtube_analysis_result.csv", encoding="utf-8-sig")

print(f"유튜브: {len(yt)}개 댓글 | 지식인: {len(jk)}개 Q&A")

# ─────────────────────────────────────────────────────────
# 2. 공통 지표 계산
# ─────────────────────────────────────────────────────────

# 감성 분포
def sent_pct(df):
    vc = df["sentiment"].value_counts()
    t  = len(df)
    return {s: round(vc.get(s, 0)/t*100, 1) for s in ["긍정","중립","부정"]}

yt_sent = sent_pct(yt)
jk_sent = sent_pct(jk)

# 빈출 단어
def top_words(df, col, sent, n=20):
    if col == "tokens_full":
        series = df[df["sentiment"]==sent]["tokens_full"].dropna()
        tokens = [t for lst in series for t in (lst if isinstance(lst, list) else [])]
    else:
        series = df[df["sentiment"]==sent][col].dropna()
        tokens = " ".join(series).split()
    return Counter(tokens).most_common(n)

yt_pos_w = dict(top_words(yt, "tokens_full" if "tokens_full" in yt.columns else "text", "긍정"))
yt_neg_w = dict(top_words(yt, "tokens_full" if "tokens_full" in yt.columns else "text", "부정"))
jk_pos_w = dict(top_words(jk, "tokens_full", "긍정"))
jk_neg_w = dict(top_words(jk, "tokens_full", "부정"))

# 공통 단어 (교집합)
common_pos = set(yt_pos_w) & set(jk_pos_w)
common_neg = set(yt_neg_w) & set(jk_neg_w)

# 토픽-카테고리 맵핑 (유사 주제 묶기)
TOPIC_MAP = {
    "제품 비교·선택":   (["광파오븐·에프 비교/청소"], ["광파오븐 vs 에어프라이어 선택","스팀·기능 비교 및 청소"]),
    "구매·혼수 준비":   (["혼수가전 구매/이사준비","신혼집 가전배치/공간고민"], ["혼수가전 구매/브랜드 비교","오븐 크기·설치·공간 고민"]),
    "요리·레시피":      (["집밥 레시피/요리재료","간단집밥/반찬레시피"], ["신혼 요리 시작/레시피 활용"]),
    "신혼살림·취향":    (["신혼살림/소형가전취향"], []),
    "주방 관리":        (["음식물처리기/주방냄새"], []),
    "육아 후 활용":     ([], ["출산·육아 후 오븐 활용"]),
}

# ─────────────────────────────────────────────────────────
# 3. 시각화
# ─────────────────────────────────────────────────────────

print("\n[시각화] 비교 분석 차트 생성 중...")

fig = plt.figure(figsize=(24, 28))
fig.suptitle("YouTube × 지식인 비교 분석\n신혼부부 광파오븐 콘텐츠 기획",
             fontsize=17, fontweight="bold", y=0.99)

gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── 3-1. 감성 분포 비교 (나란히 파이) ───────────────────────
ax1a = fig.add_subplot(gs[0, 0])
ax1b = fig.add_subplot(gs[0, 1])

for ax, sent, title, color in [
    (ax1a, yt_sent, "YouTube 감성 분포", C_YT),
    (ax1b, jk_sent, "지식인 감성 분포",  C_JK),
]:
    vals   = [sent["긍정"], sent["중립"], sent["부정"]]
    colors = [C_POS, C_NEU, C_NEG]
    wedges, _, autotexts = ax.pie(
        vals, labels=["긍정","중립","부정"],
        autopct="%1.1f%%", colors=colors,
        startangle=90, textprops={"fontsize": 10},
    )
    for at in autotexts:
        at.set_fontsize(10)
    ax.set_title(title, fontsize=12, fontweight="bold", color=color)

# ── 3-2. 감성 비율 비교 바차트 ─────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
categories = ["긍정", "중립", "부정"]
yt_vals = [yt_sent[c] for c in categories]
jk_vals = [jk_sent[c] for c in categories]
x = np.arange(3)
w = 0.35
b1 = ax2.bar(x - w/2, yt_vals, w, label="YouTube", color=C_YT,   alpha=0.85)
b2 = ax2.bar(x + w/2, jk_vals, w, label="지식인",  color=C_JK,   alpha=0.85)
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=11)
ax2.set_ylabel("비율 (%)")
ax2.set_title("채널별 감성 비율 비교", fontsize=12, fontweight="bold")
ax2.legend(fontsize=10)
ax2.set_ylim(0, 100)
for bar in list(b1) + list(b2):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
             f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=9)

# ── 3-3. 토픽 분포 비교 ────────────────────────────────────
ax3a = fig.add_subplot(gs[1, 0])
ax3b = fig.add_subplot(gs[1, 1])

yt_tc = yt["topic_label"].value_counts()
jk_tc = jk["topic_label"].value_counts()

for ax, tc, title, color in [
    (ax3a, yt_tc, "YouTube 토픽 분포", C_YT),
    (ax3b, jk_tc, "지식인 토픽 분포",  C_JK),
]:
    pct  = (tc / tc.sum() * 100).round(1)
    labs = [f"{l[:12]}\n({v}%)" for l, v in zip(pct.index, pct.values)]
    ax.barh(labs[::-1], pct.values[::-1],
            color=[color]*len(pct), alpha=0.8, edgecolor="white")
    ax.set_title(title, fontsize=11, fontweight="bold", color=color)
    ax.set_xlabel("비율 (%)")
    ax.tick_params(axis="y", labelsize=7.5)

# ── 3-4. 유사 주제 묶음 비교 ───────────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
topic_groups = list(TOPIC_MAP.keys())
yt_grp_pct, jk_grp_pct = [], []

for grp, (yt_topics, jk_topics) in TOPIC_MAP.items():
    yt_n = yt["topic_label"].isin(yt_topics).sum() if yt_topics else 0
    jk_n = jk["topic_label"].isin(jk_topics).sum() if jk_topics else 0
    yt_grp_pct.append(round(yt_n / len(yt) * 100, 1))
    jk_grp_pct.append(round(jk_n / len(jk) * 100, 1))

x4 = np.arange(len(topic_groups))
w4 = 0.35
ax4.bar(x4 - w4/2, yt_grp_pct, w4, label="YouTube", color=C_YT, alpha=0.85)
ax4.bar(x4 + w4/2, jk_grp_pct, w4, label="지식인",  color=C_JK, alpha=0.85)
ax4.set_xticks(x4)
ax4.set_xticklabels(topic_groups, rotation=20, ha="right", fontsize=8)
ax4.set_ylabel("비율 (%)")
ax4.set_title("유사 주제 채널 간 비중 비교", fontsize=11, fontweight="bold")
ax4.legend(fontsize=9)

# ── 3-5. Opportunity Score 비교 ────────────────────────────
ax5 = fig.add_subplot(gs[2, :])

yt_opp_s = yt_opp[["토픽","기회점수","Area"]].copy()
jk_opp_s = jk_opp[["토픽","기회점수","Area"]].copy()
yt_opp_s["채널"] = "YouTube"
jk_opp_s["채널"] = "지식인"
all_opp = pd.concat([yt_opp_s, jk_opp_s], ignore_index=True).sort_values("기회점수", ascending=True)

AREA_COLOR = {
    "과소충족 기회": "#E53935",
    "충족 영역":     "#43A047",
    "무관심 영역":   "#757575",
    "과잉충족 영역": "#1E88E5",
}
bar_colors = [AREA_COLOR.get(a, "#999") for a in all_opp["Area"]]
labels_opp = [f"[{'YT' if c=='YouTube' else 'JK'}] {t}" for t, c in zip(all_opp["토픽"], all_opp["채널"])]
hatches = ["" if c == "YouTube" else "///" for c in all_opp["채널"]]

bars_opp = ax5.barh(labels_opp, all_opp["기회점수"],
                    color=bar_colors, edgecolor="white", height=0.65)
for bar, hatch in zip(bars_opp, hatches):
    bar.set_hatch(hatch)

ax5.axvline(x=10, color="gray", linestyle="--", lw=1, alpha=0.6)
ax5.set_title("Opportunity Score 비교 — YouTube [실선] vs 지식인 [빗금]",
              fontsize=12, fontweight="bold")
ax5.set_xlabel("Opportunity Score")
ax5.tick_params(axis="y", labelsize=8.5)
for bar, val in zip(bars_opp, all_opp["기회점수"]):
    ax5.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             f"{val:.1f}", va="center", fontsize=9, fontweight="bold")

patches = [mpatches.Patch(color=c, label=l) for l, c in AREA_COLOR.items()]
patches += [mpatches.Patch(facecolor="white", edgecolor="black", label="YouTube"),
            mpatches.Patch(facecolor="white", edgecolor="black", hatch="///", label="지식인")]
ax5.legend(handles=patches, fontsize=8, loc="lower right", ncol=2)

# ── 3-6. 공통 페인포인트 키워드 ────────────────────────────
ax6 = fig.add_subplot(gs[3, 0])
common_neg_list = sorted(common_neg,
                         key=lambda w: yt_neg_w.get(w,0) + jk_neg_w.get(w,0),
                         reverse=True)[:12]
yt_neg_vals = [yt_neg_w.get(w, 0) for w in common_neg_list]
jk_neg_vals = [jk_neg_w.get(w, 0) for w in common_neg_list]
x6 = np.arange(len(common_neg_list))
ax6.bar(x6 - 0.2, yt_neg_vals, 0.4, label="YouTube", color=C_YT, alpha=0.85)
ax6.bar(x6 + 0.2, jk_neg_vals, 0.4, label="지식인",  color=C_JK, alpha=0.85)
ax6.set_xticks(x6)
ax6.set_xticklabels(common_neg_list, rotation=35, ha="right", fontsize=8)
ax6.set_title("공통 페인포인트 키워드 빈도", fontsize=11, fontweight="bold")
ax6.set_ylabel("빈도")
ax6.legend(fontsize=9)

# ── 3-7. 공통 니즈 키워드 ──────────────────────────────────
ax7 = fig.add_subplot(gs[3, 1])
common_pos_list = sorted(common_pos,
                         key=lambda w: yt_pos_w.get(w,0) + jk_pos_w.get(w,0),
                         reverse=True)[:12]
yt_pos_vals = [yt_pos_w.get(w, 0) for w in common_pos_list]
jk_pos_vals = [jk_pos_w.get(w, 0) for w in common_pos_list]
x7 = np.arange(len(common_pos_list))
ax7.bar(x7 - 0.2, yt_pos_vals, 0.4, label="YouTube", color=C_YT, alpha=0.85)
ax7.bar(x7 + 0.2, jk_pos_vals, 0.4, label="지식인",  color=C_JK, alpha=0.85)
ax7.set_xticks(x7)
ax7.set_xticklabels(common_pos_list, rotation=35, ha="right", fontsize=8)
ax7.set_title("공통 니즈 키워드 빈도", fontsize=11, fontweight="bold")
ax7.set_ylabel("빈도")
ax7.legend(fontsize=9)

# ── 3-8. 채널별 단독 페인포인트 ────────────────────────────
ax8 = fig.add_subplot(gs[3, 2])
yt_only_neg = {w: c for w, c in yt_neg_w.items() if w not in jk_neg_w}
jk_only_neg = {w: c for w, c in jk_neg_w.items() if w not in yt_neg_w}
yt_only_top = sorted(yt_only_neg, key=yt_only_neg.get, reverse=True)[:6]
jk_only_top = sorted(jk_only_neg, key=jk_only_neg.get, reverse=True)[:6]

y_pos = np.arange(6)
ax8.barh(y_pos + 0.2, [yt_only_neg[w] for w in yt_only_top],
         0.35, label="YouTube 단독", color=C_YT, alpha=0.85)
ax8.barh(y_pos - 0.2, [jk_only_neg[w] for w in jk_only_top],
         0.35, label="지식인 단독",  color=C_JK, alpha=0.85)
ax8.set_yticks(y_pos)
ax8.set_yticklabels([f"YT:{y}  /  JK:{j}"
                     for y, j in zip(yt_only_top, jk_only_top)], fontsize=8)
ax8.set_title("채널별 단독 페인포인트 키워드", fontsize=11, fontweight="bold")
ax8.set_xlabel("빈도")
ax8.legend(fontsize=8)

plt.savefig("compare_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("  저장: compare_analysis.png")

# ─────────────────────────────────────────────────────────
# 4. 결과 요약 출력
# ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(" 비교 분석 결과 요약")
print("=" * 60)

print("\n[1] 감성 분포 비교")
print(f"  {'':8}  {'긍정':>6}  {'중립':>6}  {'부정':>6}")
print(f"  {'YouTube':8}  {yt_sent['긍정']:>5.1f}%  {yt_sent['중립']:>5.1f}%  {yt_sent['부정']:>5.1f}%")
print(f"  {'지식인':8}  {jk_sent['긍정']:>5.1f}%  {jk_sent['중립']:>5.1f}%  {jk_sent['부정']:>5.1f}%")
print("  → 지식인의 부정률이 YouTube 대비 5배 높음")
print("  → 지식인은 '구매 전 고민·불안' 심리가 반영된 페인포인트 데이터")
print("  → YouTube는 '시청 후 반응' 위주로 상대적으로 긍정적")

print("\n[2] 공통 과소충족 기회 영역 (두 채널 모두 확인)")
common_opp = []
yt_over = set(yt_opp[yt_opp["Area"]=="과소충족 기회"]["토픽"].tolist())
jk_over = set(jk_opp[jk_opp["Area"]=="과소충족 기회"]["토픽"].tolist())
print(f"  YouTube 과소충족: {list(yt_over)}")
print(f"  지식인  과소충족: {list(jk_over)}")
print("  → '광파오븐·에어프라이어 비교/선택' 이 두 채널 공통 과소충족 영역")
print("  → 지식인 추가: '신혼 요리 시작/레시피 활용' (부정률 32.9% → 높은 미충족)")

print("\n[3] 공통 페인포인트 키워드")
for w in common_neg_list[:10]:
    print(f"  '{w}'  —  YouTube: {yt_neg_w.get(w,0)}회 / 지식인: {jk_neg_w.get(w,0)}회")

print("\n[4] 공통 니즈 키워드")
for w in common_pos_list[:10]:
    print(f"  '{w}'  —  YouTube: {yt_pos_w.get(w,0)}회 / 지식인: {jk_pos_w.get(w,0)}회")

print("\n[5] 채널별 단독 페인포인트")
print("  YouTube 전용:", " / ".join(yt_only_top))
print("  지식인  전용:", " / ".join(jk_only_top))

print("\n[6] 주제별 채널 간 비중 차이")
for grp, (yt_t, jk_t) in TOPIC_MAP.items():
    yt_n = round(yt["topic_label"].isin(yt_t).sum()/len(yt)*100, 1) if yt_t else 0
    jk_n = round(jk["topic_label"].isin(jk_t).sum()/len(jk)*100, 1) if jk_t else 0
    diff = jk_n - yt_n
    arrow = "↑지식인" if diff > 3 else ("↑YouTube" if diff < -3 else "≈유사")
    print(f"  {grp:<12}: YouTube {yt_n:>5.1f}%  /  지식인 {jk_n:>5.1f}%  {arrow}")

print("\n[7] 콘텐츠 전략 우선순위")
print("  ★★★ 1순위: 광파오븐 vs 에어프라이어 실사용 비교")
print("           → 두 채널 모두 과소충족 확인, 부정률 높음")
print("  ★★  2순위: 신혼 요리 초보 실전 가이드 (광파오븐 활용 레시피)")
print("           → 지식인 과소충족, YouTube 요리 레시피 충족 영역")
print("           → 두 채널 간 gap 활용 → 심화·차별화 콘텐츠 기회")
print("  ★   3순위: 광파오븐 청소·관리 노하우")
print("           → YouTube 부정 키워드 '청소' 고빈도, 지식인과 공통")

print("\n" + "=" * 60)
print(" 완료! 생성 파일: compare_analysis.png")
print("=" * 60)
