import re
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
from wordcloud import WordCloud
 
# ─────────────────────────────────────────
# 0. 설정
# ─────────────────────────────────────────
 
CLIENT_ID     = "kb5BiALUnoTPTmOfpcZq"
CLIENT_SECRET = "YHKIa5eIcA"
 
KEYWORDS = ["광파오븐", "요리 루틴", "혼밥 요리", "주방 힐링", "건강 요리"]
 
OUTPUT_CSV   = "naver_data.csv"
WC_ALL       = "wordcloud_all.png"
WC_BY_KW     = "wordcloud_by_keyword.png"
 
STOPWORDS = set([
    "이", "그", "저", "것", "수", "때", "등", "및", "를", "가",
    "은", "는", "에", "의", "로", "도", "을", "와", "과", "하", "있",
    "되", "않", "없", "나", "우리", "더", "아주", "진짜", "너무",
    "정말", "같은", "이런", "그런", "저런", "하는", "있는", "없는",
    "으로", "에서", "에게", "부터", "까지", "한", "합니다", "해요",
    "했", "했어요", "해서", "이고", "이라", "거", "게", "건", "걸",
    "좀", "제", "내", "내가", "그냥", "여기", "저기", "어디", "왜",
    "어떻게", "얼마나", "뭐", "뭔가", "뭘", "누구", "언제", "어느",
    "구매", "배송", "구입", "가격", "후기", "제품", "블로그", "포스팅",
    "클릭", "바로", "정도", "조금", "많이", "이번", "오늘", "어제",
    "최근", "항상", "매일", "처음", "마지막", "다시", "또", "계속",
])
 
 
# ─────────────────────────────────────────
# 1. 네이버 블로그 API 크롤링
# ─────────────────────────────────────────
 
def search_naver_blog(keyword, display=100):
    """네이버 블로그 검색 API"""
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
 
    results = []
    # API 최대 100개씩, start 파라미터로 페이징 (최대 1000개)
    for start in range(1, min(display, 1000), 100):
        params = {
            "query": keyword,
            "display": 100,
            "start": start,
            "sort": "sim",  # 정확도순
        }
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            if r.status_code == 200:
                items = r.json().get("items", [])
                if not items:
                    break
                for item in items:
                    # HTML 태그 제거
                    title   = re.sub(r'<[^>]+>', '', item.get("title", ""))
                    desc    = re.sub(r'<[^>]+>', '', item.get("description", ""))
                    results.append({
                        "keyword":  keyword,
                        "title":    title,
                        "text":     desc,
                        "blog_name": item.get("bloggername", ""),
                        "date":     item.get("postdate", ""),
                        "link":     item.get("link", ""),
                    })
                print(f"    start={start} → {len(items)}개 수집")
                time.sleep(0.3)
            else:
                print(f"    ⚠ API 오류: {r.status_code} {r.text[:100]}")
                break
        except Exception as e:
            print(f"    ⚠ 요청 실패: {e}")
            break
 
    return results
 
 
# ─────────────────────────────────────────
# 2. 전처리
# ─────────────────────────────────────────
 
def extract_nouns(texts):
    try:
        from konlpy.tag import Okt
        okt = Okt()
        all_nouns = []
        for text in texts:
            if not text or len(str(text).strip()) < 2:
                continue
            nouns = okt.nouns(str(text))
            filtered = [n for n in nouns if len(n) >= 2 and n not in STOPWORDS]
            all_nouns.extend(filtered)
        print("  KoNLPy Okt 사용")
        return all_nouns
    except ImportError:
        print("  KoNLPy 없음 → 정규식 대체")
        all_words = []
        for text in texts:
            words = re.findall(r'[가-힣]{2,}', str(text))
            filtered = [w for w in words if w not in STOPWORDS]
            all_words.extend(filtered)
        return all_words
 
 
# ─────────────────────────────────────────
# 3. 워드클라우드
# ─────────────────────────────────────────
 
def get_font_path():
    import os
    for path in [
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/NanumGothic.ttf",
        "C:/Windows/Fonts/gulim.ttc",
        "/System/Library/Fonts/AppleGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    ]:
        if os.path.exists(path):
            return path
    for f in fm.findSystemFonts():
        if any(k in f.lower() for k in ["nanum", "malgun", "gulim", "gothic"]):
            return f
    return None
 
 
def make_wordcloud(words, title, save_path, colormap="RdPu"):
    if not words:
        print(f"  ⚠ '{title}' 단어 없음")
        return
    freq = Counter(words)
    font_path = get_font_path()
    kwargs = dict(
        width=1400, height=700,
        background_color="white",
        max_words=150,
        colormap=colormap,
        prefer_horizontal=0.85,
    )
    if font_path:
        kwargs["font_path"] = font_path
    wc = WordCloud(**kwargs).generate_from_frequencies(freq)
    plt.figure(figsize=(16, 8))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.title(title, fontsize=18, pad=18)    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  저장: {save_path}")
 
 
def make_wordcloud_by_keyword(df):
    """키워드별 서브플롯 워드클라우드"""
    keywords = df["keyword"].unique()
    n = len(keywords)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))
    if n == 1:
        axes = [axes]
 
    font_path = get_font_path()
 
    for ax, kw in zip(axes, keywords):
        texts = df[df["keyword"] == kw]["text"].tolist()
        nouns = extract_nouns(texts)
        if not nouns:
            ax.axis("off")
            continue
        freq = Counter(nouns)
        kwargs = dict(
            width=600, height=500,
            background_color="white",
            max_words=80,
            colormap="Blues",
            prefer_horizontal=0.85,
        )
        if font_path:
            kwargs["font_path"] = font_path
        wc = WordCloud(**kwargs).generate_from_frequencies(freq)
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(kw, fontsize=13, pad=10)
 
    plt.suptitle("키워드별 워드클라우드", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(WC_BY_KW, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  저장: {WC_BY_KW}")
 
 
# ─────────────────────────────────────────
# 4. 메인
# ─────────────────────────────────────────
 
def main():
    print("=" * 50)
    print(" 네이버 블로그 크롤링 시작")
    print("=" * 50)
 
    all_data = []
 
    for kw in KEYWORDS:
        print(f"\n[검색] '{kw}'")
        data = search_naver_blog(kw, display=100)
        all_data.extend(data)
        print(f"  → 누적 {len(all_data)}개")
        time.sleep(0.5)
 
    print(f"\n총 수집: {len(all_data)}개")
 
    if not all_data:
        print("⚠ 수집 실패 — API 키 확인해주세요")
        return
 
    # CSV 저장
    df = pd.DataFrame(all_data)
    df["text"] = df["text"].fillna("").astype(str)
    df["title"] = df["title"].fillna("").astype(str)
    df["full_text"] = df["title"] + " " + df["text"]
    df = df[df["full_text"].str.len() > 5].reset_index(drop=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[저장] {OUTPUT_CSV} ({len(df)}행)")
    print(df[["keyword", "title", "text"]].head(3).to_string())
 
    # 전처리
    print("\n[전처리] 명사 추출 중...")
    all_nouns = extract_nouns(df["full_text"].tolist())
    print(f"  전체 명사 {len(all_nouns)}개")
 
    if not all_nouns:
        print("⚠ 명사 추출 결과 없음")
        return
 
    # 워드클라우드
    print("\n[시각화] 워드클라우드 생성 중...")
    make_wordcloud(all_nouns, "전체 통합 워드클라우드", WC_ALL, "RdPu")
    make_wordcloud_by_keyword(df)
 
    # TOP 30
    print("\n[TOP 30 키워드]")
    for i, (word, cnt) in enumerate(Counter(all_nouns).most_common(30), 1):
        print(f"  {i:2}. {word} ({cnt}회)")
 
    print(f"\n✅ 완료!")
    print(f"  {OUTPUT_CSV}")
    print(f"  {WC_ALL}")
    print(f"  {WC_BY_KW}")
 
 
if __name__ == "__main__":
    main()