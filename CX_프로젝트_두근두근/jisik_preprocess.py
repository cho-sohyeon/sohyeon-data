import os, re, warnings
import pandas as pd
from collections import Counter

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# 0. 설정
# ─────────────────────────────────────────────────────────

INPUT_FILE  = "광파오븐_신혼부부_지식인_크롤링결과.csv"
OUTPUT_FILE = "jisik_preprocessed.csv"

STOPWORDS = set([
    # 일반 조사·어미
    "이","그","저","것","수","때","등","및","를","가","은","는","에","의","로","도",
    "을","와","과","하","있","되","않","없","나","우리","더","아주","진짜","너무",
    "정말","같은","이런","그런","저런","하는","있는","없는","으로","에서","에게",
    "부터","까지","한","합니다","해요","했","했어요","해서","이고","이라","거","게",
    "건","걸","좀","제","내","내가","그냥","여기","저기","어디","왜","어떻게",
    "얼마나","뭐","뭔가","뭘","누구","언제","어느",
    # 구매/일반 맥락
    "구매","배송","구입","가격","후기","제품","블로그","포스팅","클릭","바로",
    "정도","조금","많이","이번","오늘","어제","최근","항상","매일","처음","마지막",
    "다시","또","계속",
    # 시간·지시
    "생각","경우","부분","이용","사용","관련","내용","방법","때문","기준",
    "느낌","정보","이후","이전","가능","기능","제가","저도","저는","저희",
    # 지식인 특유 표현
    "답변","질문","안녕","감사","부탁","드립니다","드려요","드리고","싶습니다",
    "궁금","알고","싶어요","주세요","해주세요","좋겠습니다","여쭤","여쭙고",
    "혹시","도움","말씀","참고","추천","선택","비교","확인","문의",
    # 이모티콘 텍스트
    "ㅋㅋ","ㅎㅎ","ㅠㅠ","ㅜㅜ","ㅋ","ㅎ","ㅠ","ㅜ",
])

# ─────────────────────────────────────────────────────────
# 1. 데이터 로드
# ─────────────────────────────────────────────────────────

print("=" * 60)
print(" 지식인 데이터 전처리 시작")
print("=" * 60)

df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")
print(f"\n원본 데이터: {len(df)}행 × {len(df.columns)}열")
print(f"결측값 - content: {df['content'].isnull().sum()}개 | answer: {df['answer'].isnull().sum()}개")

# ─────────────────────────────────────────────────────────
# 2. Step 1 — 결측값 처리
# ─────────────────────────────────────────────────────────

print("\n[Step 1] 결측값 처리")
df["content"] = df["content"].fillna("")
df["answer"]  = df["answer"].fillna("")

# content와 answer 모두 빈 행 제거
df = df[~((df["content"].str.strip() == "") & (df["answer"].str.strip() == ""))].reset_index(drop=True)
print(f"  content+answer 모두 빈 행 제거 → {len(df)}행 남음")

# ─────────────────────────────────────────────────────────
# 3. Step 2 — 텍스트 정제
# ─────────────────────────────────────────────────────────

print("\n[Step 2] 텍스트 정제")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+|www\.\S+", "", text)          # URL 제거
    text = re.sub(r"<[^>]+>", "", text)                    # HTML 태그 제거
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", text)      # 특수문자·이모지 제거
    text = re.sub(r"\s+", " ", text).strip()               # 연속 공백 정규화
    return text

df["title_clean"]   = df["title"].apply(clean_text)
df["content_clean"] = df["content"].apply(clean_text)
df["answer_clean"]  = df["answer"].apply(clean_text)

# 분석용 통합 텍스트 (제목 + 질문 + 답변)
df["full_text"] = (df["title_clean"] + " " +
                   df["content_clean"] + " " +
                   df["answer_clean"])
df["full_text"] = df["full_text"].str.strip()

# 최소 길이 필터 (10자 미만 제거)
before = len(df)
df = df[df["full_text"].str.len() >= 10].reset_index(drop=True)
print(f"  10자 미만 제거: {before - len(df)}행 → {len(df)}행 남음")

# ─────────────────────────────────────────────────────────
# 4. Step 3 — 형태소 분석 (명사 추출)
# ─────────────────────────────────────────────────────────

print("\n[Step 3] 형태소 분석 (KoNLPy Okt) — 시간이 걸릴 수 있습니다...")

def extract_nouns_batch(texts, min_len=2):
    try:
        from konlpy.tag import Okt
        okt = Okt()
        result = []
        for i, text in enumerate(texts):
            nouns = okt.nouns(str(text))
            filtered = [n for n in nouns if len(n) >= min_len and n not in STOPWORDS]
            result.append(filtered)
            if (i + 1) % 100 == 0:
                print(f"    {i+1}/{len(texts)} 처리 중...")
        print("  KoNLPy Okt 사용 완료")
        return result
    except Exception as e:
        print(f"  KoNLPy 오류({e}) → 정규식 대체")
        result = []
        for text in texts:
            words = re.findall(r"[가-힣]{2,}", str(text))
            filtered = [w for w in words if w not in STOPWORDS]
            result.append(filtered)
        return result

# 질문·답변 각각 + 통합 토큰 추출
df["tokens_content"] = extract_nouns_batch(df["content_clean"].tolist())
df["tokens_answer"]  = extract_nouns_batch(df["answer_clean"].tolist())
df["tokens_full"]    = [c + a for c, a in zip(df["tokens_content"], df["tokens_answer"])]

# ─────────────────────────────────────────────────────────
# 5. Step 4 — 최소 토큰 필터
# ─────────────────────────────────────────────────────────

print("\n[Step 4] 최소 토큰 필터 (통합 토큰 2개 이상)")
before = len(df)
df = df[df["tokens_full"].apply(len) >= 2].reset_index(drop=True)
print(f"  제거: {before - len(df)}행 → 최종 {len(df)}행")

# ─────────────────────────────────────────────────────────
# 6. 전처리 결과 요약
# ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(" 전처리 결과 요약")
print("=" * 60)
print(f"  원본:              755행")
print(f"  결측·빈 행 제거:   {len(df) + (755 - len(df))}행 → ", end="")
print(f"최종 유효 데이터:    {len(df)}행")

print(f"\n[카테고리별 분포]")
cat_counts = df["category"].value_counts()
for cat, cnt in cat_counts.items():
    print(f"  {cat}: {cnt}개")

print(f"\n[키워드별 분포 (상위 10개)]")
kw_counts = df["keyword"].value_counts().head(10)
for kw, cnt in kw_counts.items():
    print(f"  {kw}: {cnt}개")

all_tokens = [t for tokens in df["tokens_full"] for t in tokens]
print(f"\n[토큰 통계]")
print(f"  전체 토큰 수:      {len(all_tokens):,}개")
print(f"  고유 토큰 수:      {len(set(all_tokens)):,}개")
print(f"  문서당 평균 토큰:  {len(all_tokens)/len(df):.1f}개")

print(f"\n[전체 빈출 명사 TOP 30]")
top30 = Counter(all_tokens).most_common(30)
for i, (word, cnt) in enumerate(top30, 1):
    print(f"  {i:2}. {word} ({cnt}회)")

# ─────────────────────────────────────────────────────────
# 7. 저장
# ─────────────────────────────────────────────────────────

save_cols = [
    "category", "keyword", "title",
    "content_clean", "answer_clean", "full_text",
    "tokens_content", "tokens_answer", "tokens_full",
    "url"
]
df[save_cols].to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"\n[저장] {OUTPUT_FILE} ({len(df)}행)")
print("\n완료!")
