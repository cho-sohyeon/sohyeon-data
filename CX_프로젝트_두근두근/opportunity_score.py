import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# 0. 한글 폰트
# ─────────────────────────────────────────────────────────

def set_korean_font():
    for path in ["C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/NanumGothic.ttf",
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

df   = pd.read_csv("youtube_analysis_result.csv",  encoding="utf-8-sig")
df_v = pd.read_csv("youtube_videos.csv",            encoding="utf-8-sig")

# video_id → view_count 매핑
vid2view = df_v.set_index("video_id")["view_count"].to_dict()
df["view_count"] = df["video_id"].map(vid2view).fillna(0)

df = df[df["topic"] >= 0].copy()
total_comments = len(df)

# ─────────────────────────────────────────────────────────
# 2. 토픽별 지표 계산
# ─────────────────────────────────────────────────────────

records = []
for label, grp in df.groupby("topic_label"):
    n       = len(grp)
    pos     = (grp["sentiment"] == "긍정").sum()
    neg     = (grp["sentiment"] == "부정").sum()
    neu     = (grp["sentiment"] == "중립").sum()
    pol     = pos + neg

    vol_raw   = n / total_comments                    # 댓글 비중
    view_avg  = grp["view_count"].mean()              # 평균 조회수

    records.append({
        "토픽":       label,
        "댓글수":     n,
        "긍정":       pos,
        "부정":       neg,
        "중립":       neu,
        "긍정률":     round(pos / n * 100, 1),
        "부정률":     round(neg / n * 100, 1),
        "평균조회수": int(view_avg),
        "_vol_raw":   vol_raw,
        "_view_raw":  view_avg,
        "_pol":       pol,
    })

df_opp = pd.DataFrame(records)

# ── Min-Max 정규화로 1~10 스케일 조정 ──────────────────────
def minmax(s, lo=1, hi=10):
    mn, mx = s.min(), s.max()
    if mx == mn:
        return pd.Series([5.0] * len(s), index=s.index)
    return lo + (s - mn) / (mx - mn) * (hi - lo)

df_opp["vol_score"]  = minmax(df_opp["_vol_raw"])
df_opp["view_score"] = minmax(df_opp["_view_raw"])

# Importance = 댓글 볼륨(70%) + 평균 조회수(30%)
df_opp["중요도"] = (df_opp["vol_score"] * 0.7 + df_opp["view_score"] * 0.3).round(2)

# Satisfaction = 긍정/(긍정+부정) × 10, 중립만 있으면 5점
def sat_score(row):
    pol = row["_pol"]
    return round((row["긍정"] / pol * 10) if pol > 0 else 5.0, 2)

df_opp["만족도"] = df_opp.apply(sat_score, axis=1)

# ── Opportunity Score (Ulwick) ─────────────────────────────
df_opp["기회점수"] = (df_opp["중요도"] +
    (df_opp["중요도"] - df_opp["만족도"]).clip(lower=0)).round(2)

df_opp = df_opp.sort_values("기회점수", ascending=False).reset_index(drop=True)

# ── Area 분류 ────────────────────────────────────────────
def classify_area(row):
    imp  = row["중요도"]
    sat  = row["만족도"]
    mid_i = df_opp["중요도"].median()
    mid_s = df_opp["만족도"].median()
    if imp >= mid_i and sat < mid_s:
        return "과소충족 기회"       # HIGH imp / LOW sat  → 최우선
    elif imp >= mid_i and sat >= mid_s:
        return "충족 영역"           # HIGH imp / HIGH sat → 유지강화
    elif imp < mid_i and sat < mid_s:
        return "무관심 영역"         # LOW imp  / LOW sat  → 후순위
    else:
        return "과잉충족 영역"       # LOW imp  / HIGH sat → 투자축소

df_opp["Area"] = df_opp.apply(classify_area, axis=1)

AREA_COLOR = {
    "과소충족 기회":  "#E53935",
    "충족 영역":      "#43A047",
    "무관심 영역":    "#757575",
    "과잉충족 영역":  "#1E88E5",
}

# ─────────────────────────────────────────────────────────
# 3. 시각화
# ─────────────────────────────────────────────────────────

fig = plt.figure(figsize=(20, 14))
fig.suptitle("Opportunity Score & Area 분석\n신혼부부 광파오븐 콘텐츠 기획",
             fontsize=16, fontweight="bold", y=0.99)

# ── 3-1. Opportunity Score 바차트 ─────────────────────────
ax1 = fig.add_subplot(2, 2, 1)
colors_bar = [AREA_COLOR[a] for a in df_opp["Area"]]
bars = ax1.barh(df_opp["토픽"][::-1], df_opp["기회점수"][::-1],
                color=colors_bar[::-1], edgecolor="white", height=0.6)
ax1.axvline(x=10, color="gray", linestyle="--", linewidth=1, alpha=0.6)
ax1.set_title("Opportunity Score (토픽별)", fontsize=12, fontweight="bold")
ax1.set_xlabel("Opportunity Score  (Importance + max(Importance - Satisfaction, 0))")
ax1.tick_params(axis="y", labelsize=8.5)
for bar, val in zip(bars, df_opp["기회점수"][::-1]):
    ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f}", va="center", fontsize=9, fontweight="bold")

# 범례
legend_patches = [mpatches.Patch(color=c, label=l) for l, c in AREA_COLOR.items()]
ax1.legend(handles=legend_patches, fontsize=8, loc="lower right")

# ── 3-2. Opportunity Matrix (중요도 × 만족도 산점도) ─────
ax2 = fig.add_subplot(2, 2, 2)

mid_i = df_opp["중요도"].median()
mid_s = df_opp["만족도"].median()

# 사분면 배경
ax2.axhspan(mid_i, df_opp["중요도"].max() + 0.5, xmin=0,   xmax=0.5,
            facecolor="#FFEBEE", alpha=0.5, zorder=0)
ax2.axhspan(mid_i, df_opp["중요도"].max() + 0.5, xmin=0.5, xmax=1,
            facecolor="#E8F5E9", alpha=0.5, zorder=0)
ax2.axhspan(0,     mid_i,                         xmin=0,   xmax=0.5,
            facecolor="#F5F5F5", alpha=0.5, zorder=0)
ax2.axhspan(0,     mid_i,                         xmin=0.5, xmax=1,
            facecolor="#E3F2FD", alpha=0.5, zorder=0)

ax2.axhline(y=mid_i, color="gray", linestyle="--", linewidth=1, alpha=0.7)
ax2.axvline(x=mid_s, color="gray", linestyle="--", linewidth=1, alpha=0.7)

# 사분면 라벨
pad = 0.15
x_max = df_opp["만족도"].max() + 0.5
x_min = df_opp["만족도"].min() - 0.5
y_max = df_opp["중요도"].max() + 0.5
y_min = 0

ax2.text(mid_s - pad, y_max - pad, "과소충족 기회\n(최우선 콘텐츠)",
         ha="right", va="top", fontsize=8.5, color="#C62828", fontweight="bold")
ax2.text(mid_s + pad, y_max - pad, "충족 영역\n(유지·강화)",
         ha="left",  va="top", fontsize=8.5, color="#2E7D32", fontweight="bold")
ax2.text(mid_s - pad, y_min + pad, "무관심 영역\n(후순위)",
         ha="right", va="bottom", fontsize=8.5, color="#424242")
ax2.text(mid_s + pad, y_min + pad, "과잉충족 영역\n(투자 축소)",
         ha="left",  va="bottom", fontsize=8.5, color="#1565C0")

for _, row in df_opp.iterrows():
    color = AREA_COLOR[row["Area"]]
    size  = 120 + row["댓글수"] / 8
    ax2.scatter(row["만족도"], row["중요도"], s=size, color=color,
                alpha=0.85, edgecolors="white", linewidth=1.2, zorder=5)

    short = row["토픽"].replace("/", "/\n")
    ax2.annotate(short, (row["만족도"], row["중요도"]),
                 textcoords="offset points", xytext=(6, 4),
                 fontsize=7.5, color=color, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="none"))

ax2.set_xlabel("만족도 (Satisfaction)  →  높을수록 현재 충족", fontsize=9)
ax2.set_ylabel("중요도 (Importance)  →  높을수록 관심 높음", fontsize=9)
ax2.set_title("Opportunity Matrix", fontsize=12, fontweight="bold")
ax2.set_xlim(x_min, x_max)
ax2.set_ylim(y_min, y_max)

# ── 3-3. 중요도 vs 만족도 비교 바차트 ────────────────────
ax3 = fig.add_subplot(2, 2, (3, 4))
x      = np.arange(len(df_opp))
width  = 0.3
bars_i = ax3.bar(x - width/2, df_opp["중요도"],    width, label="중요도",    color="#1976D2", alpha=0.85)
bars_s = ax3.bar(x + width/2, df_opp["만족도"],    width, label="만족도",    color="#FF7043", alpha=0.85)
ax3.plot(x, df_opp["기회점수"] / 2, "D--", color="#6A1B9A",
         linewidth=1.8, markersize=7, label="기회점수 (÷2 스케일)", zorder=5)

ax3.set_xticks(x)
ax3.set_xticklabels(df_opp["토픽"], rotation=18, ha="right", fontsize=8.5)
ax3.set_ylabel("점수 (0~10)", fontsize=9)
ax3.set_title("토픽별 중요도 / 만족도 / 기회점수 비교", fontsize=12, fontweight="bold")
ax3.legend(fontsize=9)
ax3.set_ylim(0, 11)

for bar in bars_i:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7.5)
for bar in bars_s:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7.5)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("opportunity_score.png", dpi=150, bbox_inches="tight")
plt.close()
print("저장: opportunity_score.png")

# ─────────────────────────────────────────────────────────
# 4. 결과 테이블 출력 & 저장
# ─────────────────────────────────────────────────────────

out_cols = ["토픽", "댓글수", "긍정률", "부정률", "평균조회수",
            "중요도", "만족도", "기회점수", "Area"]
df_opp[out_cols].to_csv("opportunity_score.csv", index=False, encoding="utf-8-sig")
print("저장: opportunity_score.csv\n")

print("=" * 70)
print(f"{'토픽':<22} {'중요도':>5} {'만족도':>5} {'기회점수':>6}  Area")
print("-" * 70)
for _, row in df_opp.iterrows():
    print(f"{row['토픽']:<22} {row['중요도']:>5.2f} {row['만족도']:>5.2f} "
          f"{row['기회점수']:>6.2f}  {row['Area']}")
print("=" * 70)

print("\n[최우선 콘텐츠 기회 - 과소충족 기회 영역]")
top = df_opp[df_opp["Area"] == "과소충족 기회"].sort_values("기회점수", ascending=False)
for _, row in top.iterrows():
    print(f"  >> {row['토픽']}  (기회점수: {row['기회점수']:.1f} | 댓글수: {row['댓글수']} | 부정률: {row['부정률']}%)")
