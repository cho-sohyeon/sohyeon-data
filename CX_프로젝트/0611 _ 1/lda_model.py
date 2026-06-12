"""
네이버 블로그 LDA 토픽 모델링
실행: python lda_model.py
"""

import re
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore")

from collections import Counter

# ─────────────────────────────────────────
# 0. 설정
# ─────────────────────────────────────────

INPUT_CSV  = "naver_data.csv"
NUM_TOPICS = 5       # 토픽 수 (나중에 조정 가능)
NUM_WORDS  = 10      # 토픽별 상위 단어 수

STOPWORDS = set([
    "이", "그", "저", "것", "수", "때", "등", "및", "를", "가",
    "은", "는", "에", "의", "로", "도", "을", "와", "과", "하", "있",
    "되", "않", "없", "나", "우리", "더", "아주", "진짜", "너무",
    "정말", "같은", "이런", "그런", "저런", "하는", "있는", "없는",
    "으로", "에서", "에게", "부터", "까지", "한", "합니다", "해요",
    "했", "했어요", "해서", "이고", "이라", "거", "게", "건", "걸",
    "좀", "제", "내", "내가", "그냥", "여기", "저기", "어디", "왜",
    "어떻게", "얼마나", "뭐", "뭔가", "뭘", "누구", "언제", "어느",
    "구매", "배송", "구입", "가격", "후기", "블로그", "포스팅",
    "클릭", "바로", "정도", "조금", "많이", "이번", "오늘", "어제",
    "최근", "항상", "매일", "처음", "다시", "또", "계속", "정말",
    "사용", "제품", "하나", "모든", "매우", "그리고", "하지만",
    "그래서", "그러나", "따라서", "또한", "즉", "만약", "비록",
])


# ─────────────────────────────────────────
# 1. 데이터 로드
# ─────────────────────────────────────────

def load_data():
    df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
    df["full_text"] = df["full_text"].fillna("").astype(str)
    print(f"데이터 로드: {len(df)}행")
    print(f"키워드 분포:\n{df['keyword'].value_counts().to_string()}")
    return df


# ─────────────────────────────────────────
# 2. 전처리 + 명사 추출
# ─────────────────────────────────────────

def extract_nouns(texts):
    try:
        from konlpy.tag import Okt
        okt = Okt()
        result = []
        for i, text in enumerate(texts):
            if not text or len(str(text).strip()) < 2:
                result.append([])
                continue
            nouns = okt.nouns(str(text))
            filtered = [n for n in nouns if len(n) >= 2 and n not in STOPWORDS]
            result.append(filtered)
            if (i + 1) % 100 == 0:
                print(f"  전처리 진행: {i+1}/{len(texts)}")
        print("  KoNLPy Okt 완료")
        return result
    except ImportError:
        print("  KoNLPy 없음 → 정규식 대체")
        result = []
        for text in texts:
            words = re.findall(r'[가-힣]{2,}', str(text))
            filtered = [w for w in words if w not in STOPWORDS]
            result.append(filtered)
        return result


# ─────────────────────────────────────────
# 3. LDA 모델링
# ─────────────────────────────────────────

def run_lda(tokenized_docs, num_topics=5):
    from gensim import corpora
    from gensim.models import LdaModel

    # 사전 + 코퍼스 생성
    dictionary = corpora.Dictionary(tokenized_docs)
    dictionary.filter_extremes(no_below=2, no_above=0.9)  # 희귀/과다 단어 제거
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

    print(f"\n사전 크기: {len(dictionary)}개 단어")
    print(f"코퍼스 크기: {len(corpus)}개 문서")

    # LDA 학습
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=15,
        alpha="auto",
        eta="auto",
        per_word_topics=True,
    )

    return lda_model, corpus, dictionary


# ─────────────────────────────────────────
# 4. 결과 시각화
# ─────────────────────────────────────────

def print_topics(lda_model, num_words=10):
    print("\n" + "=" * 50)
    print(f" LDA 토픽 {lda_model.num_topics}개")
    print("=" * 50)
    for i in range(lda_model.num_topics):
        words = lda_model.show_topic(i, topn=num_words)
        word_str = " | ".join([f"{w}({round(p, 3)})" for w, p in words])
        print(f"\nTopic {i+1}: {word_str}")


def plot_topics(lda_model, num_words=10, save_path="lda_topics.png"):
    """토픽별 상위 단어 바 차트"""
    n = lda_model.num_topics
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 5))
    if n == 1:
        axes = [axes]

    colors = ["#C2185B", "#7B1FA2", "#1976D2", "#00796B", "#F57C00"]

    for i, ax in enumerate(axes):
        words = lda_model.show_topic(i, topn=num_words)
        words_sorted = sorted(words, key=lambda x: x[1])
        terms  = [w for w, _ in words_sorted]
        probs  = [round(p, 4) for _, p in words_sorted]

        ax.barh(terms, probs, color=colors[i % len(colors)], alpha=0.85)
        ax.set_title(f"Topic {i+1}", fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("확률", fontsize=10)
        ax.tick_params(axis="y", labelsize=11)
        ax.spines[["top", "right"]].set_visible(False)

    plt.suptitle("LDA 토픽 모델링 결과", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n토픽 차트 저장: {save_path}")


def plot_topic_distribution(lda_model, corpus, df, save_path="lda_distribution.png"):
    """키워드별 토픽 분포 히트맵"""
    import numpy as np

    # 문서별 주요 토픽 추출
    topic_assignments = []
    for doc_bow in corpus:
        topics = lda_model.get_document_topics(doc_bow)
        if topics:
            dominant = max(topics, key=lambda x: x[1])[0]
        else:
            dominant = 0
        topic_assignments.append(dominant)

    df = df.copy()
    df["dominant_topic"] = topic_assignments

    # 키워드 × 토픽 분포
    pivot = pd.crosstab(df["keyword"], df["dominant_topic"])
    pivot.columns = [f"Topic {c+1}" for c in pivot.columns]

    fig, ax = plt.subplots(figsize=(10, 4))
    im = ax.imshow(pivot.values, cmap="RdPu", aspect="auto")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=11)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=11)

    # 값 표시
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            ax.text(j, i, pivot.values[i, j],
                    ha="center", va="center", fontsize=11,
                    color="white" if pivot.values[i, j] > pivot.values.max() * 0.5 else "black")

    plt.colorbar(im, ax=ax, label="문서 수")
    ax.set_title("키워드별 토픽 분포", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"토픽 분포 저장: {save_path}")


def plot_coherence(tokenized_docs, dictionary, corpus, max_topics=10, save_path="lda_coherence.png"):
    """최적 토픽 수 탐색 (Coherence Score)"""
    from gensim.models import LdaModel
    from gensim.models.coherencemodel import CoherenceModel

    scores = []
    topic_range = range(2, max_topics + 1)

    print("\n최적 토픽 수 탐색 중...")
    for n in topic_range:
        model = LdaModel(corpus=corpus, id2word=dictionary,
                         num_topics=n, random_state=42, passes=10)
        cm = CoherenceModel(model=model, texts=tokenized_docs,
                            dictionary=dictionary, coherence="c_v")
        score = cm.get_coherence()
        scores.append(score)
        print(f"  Topics={n} → Coherence={round(score, 4)}")

    best_n = list(topic_range)[scores.index(max(scores))]
    print(f"\n최적 토픽 수: {best_n} (Coherence={round(max(scores), 4)})")

    plt.figure(figsize=(8, 4))
    plt.plot(list(topic_range), scores, marker="o", color="#C2185B", linewidth=2)
    plt.axvline(x=best_n, color="gray", linestyle="--", alpha=0.6)
    plt.xlabel("토픽 수", fontsize=12)
    plt.ylabel("Coherence Score", fontsize=12)
    plt.title("최적 토픽 수 탐색", fontsize=14)
    plt.xticks(list(topic_range))
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Coherence 차트 저장: {save_path}")

    return best_n


# ─────────────────────────────────────────
# 5. 메인
# ─────────────────────────────────────────

def main():
    print("=" * 50)
    print(" LDA 토픽 모델링 시작")
    print("=" * 50)

    # 데이터 로드
    df = load_data()

    # 전처리
    print("\n[전처리] 명사 추출 중...")
    tokenized = extract_nouns(df["full_text"].tolist())

    # 빈 문서 제거
    valid = [(tok, i) for i, tok in enumerate(tokenized) if len(tok) >= 3]
    tokenized_valid = [t for t, _ in valid]
    idx_valid = [i for _, i in valid]
    df_valid = df.iloc[idx_valid].reset_index(drop=True)
    print(f"유효 문서: {len(tokenized_valid)}개")

    # gensim 임포트 확인
    try:
        from gensim import corpora
        from gensim.models import LdaModel
    except ImportError:
        print("\n⚠ gensim 없음. 설치해줘요:")
        print("  pip install gensim")
        return

    # 사전 + 코퍼스
    from gensim import corpora
    dictionary = corpora.Dictionary(tokenized_valid)
    dictionary.filter_extremes(no_below=2, no_above=0.9)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_valid]

    # 최적 토픽 수 탐색 (선택)
    print("\n최적 토픽 수 탐색할까요? 시간이 걸려요 (약 1~2분)")
    print("탐색하려면 Enter, 건너뛰려면 숫자 입력 후 Enter:")
    user_input = input(f"  (기본값 {NUM_TOPICS}): ").strip()

    if user_input == "":
        best_n = plot_coherence(tokenized_valid, dictionary, corpus, max_topics=10)
    elif user_input.isdigit():
        best_n = int(user_input)
        print(f"  토픽 수 {best_n}개로 진행")
    else:
        best_n = NUM_TOPICS

    # LDA 학습
    print(f"\n[LDA] 토픽 {best_n}개로 학습 중...")
    lda_model, corpus, dictionary = run_lda(tokenized_valid, num_topics=best_n)

    # 결과 출력
    print_topics(lda_model, num_words=NUM_WORDS)

    # 시각화
    print("\n[시각화] 차트 생성 중...")
    plot_topics(lda_model, num_words=NUM_WORDS, save_path="lda_topics.png")
    plot_topic_distribution(lda_model, corpus, df_valid, save_path="lda_distribution.png")

    # 토픽별 문서 샘플 출력
    print("\n[토픽별 대표 문서 샘플]")
    topic_assignments = []
    for doc_bow in corpus:
        topics = lda_model.get_document_topics(doc_bow)
        dominant = max(topics, key=lambda x: x[1])[0] if topics else 0
        topic_assignments.append(dominant)
    df_valid["dominant_topic"] = topic_assignments

    for t in range(best_n):
        subset = df_valid[df_valid["dominant_topic"] == t]
        print(f"\nTopic {t+1} 샘플 ({len(subset)}개 문서):")
        for _, row in subset.head(2).iterrows():
            print(f"  [{row['keyword']}] {row['title'][:40]}")

    # 결과 CSV 저장
    df_valid[["keyword","title","text","dominant_topic"]].to_csv(
        "lda_result.csv", index=False, encoding="utf-8-sig")
    print("\n결과 저장: lda_result.csv")

    print("\n✅ 완료!")
    print("  lda_topics.png      — 토픽별 키워드 바 차트")
    print("  lda_distribution.png — 키워드별 토픽 분포 히트맵")
    print("  lda_coherence.png   — 최적 토픽 수 탐색 (탐색한 경우)")
    print("  lda_result.csv      — 문서별 토픽 할당 결과")


if __name__ == "__main__":
    main()