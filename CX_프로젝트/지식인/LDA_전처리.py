"""
네이버 지식인 크롤링 데이터 → LDA 토픽 모델링 전처리 코드
컬럼 구성: 제목 | 본문 | 답변
실행 환경: Google Colab / VS Code (conda py310)
필수 패키지: pip install konlpy pandas
"""

import re
import pandas as pd
from konlpy.tag import Okt

okt = Okt()


# =============================================
# 1. 복합어 사전 (전처리 전 치환)
# =============================================
# Okt가 쪼개기 전에 미리 하나의 단어로 묶어두는 사전
COMPOUND_MAP = {
    # 에어프라이 계열
    '에어프라이어': '에어프라이어',
    '에어프라이기': '에어프라이어',
    '에어프라이': '에어프라이어',
    # 광파오븐 계열
    '광파오븐': '광파오븐',
    '광파렌지': '광파오븐',
    '광파 오븐': '광파오븐',
    '광파 렌지': '광파오븐',
    # 오븐레인지 계열
    '오븐레인지': '오븐레인지',
    '오븐렌지': '오븐레인지',
    '오븐 레인지': '오븐레인지',
    '오븐 렌지': '오븐레인지',
    # 전자레인지 계열
    '전자레인지': '전자레인지',
    '전자렌지': '전자레인지',
    '전자 레인지': '전자레인지',
    '전자 렌지': '전자레인지',
    # 기타 도메인 복합어
    '홈베이킹': '홈베이킹',
    '홈 베이킹': '홈베이킹',
    '사용설명서': '사용설명서',
    '사용 설명서': '사용설명서',
    '멀티클린': '멀티클린',
    '멀티 클린': '멀티클린',
    '스팀청소': '스팀청소',
    '스팀 청소': '스팀청소',
}

# =============================================
# 2. 명사 추출 후 재합치기 사전 (post-merge)
# =============================================
# COMPOUND_MAP으로도 못 막은 분리를 명사 추출 후 재합치기로 처리
# Okt가 '베이킹' → ['베이', '킹'] 으로 쪼개는 경우 등

POST_MERGE_3 = {
    # 3-gram 패턴 (3개 토큰 → 1개 단어)
    ('홈', '베이', '킹'): '홈베이킹',
}

POST_MERGE_2 = {
    # 2-gram 패턴 (2개 토큰 → 1개 단어)
    ('에어', '프라이어'): '에어프라이어',
    ('에어', '프라이'): '에어프라이어',
    ('광파', '오븐'): '광파오븐',
    ('오븐', '레인지'): '오븐레인지',
    ('전자', '레인지'): '전자레인지',
    ('베이', '킹'): '베이킹',
    ('멀티', '클린'): '멀티클린',
    ('오버', '쿡'): '오버쿡',
    ('빌트', '인'): '빌트인',
}


# =============================================
# 3. 불용어 사전
# =============================================
STOPWORDS = set([
    # 조사/어미류
    '것', '수', '이', '가', '을', '를', '은', '는', '에', '의', '도', '로',
    '와', '과', '에서', '으로', '께서',
    # 지시대명사/관형사
    '이것', '저것', '그것', '이거', '저거', '그거', '이게', '저게', '그게',
    '이런', '저런', '그런', '어떤', '무슨',
    # 부사/감탄사
    '정말', '진짜', '너무', '좀', '더', '안', '못', '잘', '다시', '이제',
    '그냥', '막', '약간', '아직', '이미', '항상', '매우', '꼭', '반드시',
    # 시간 표현
    '오늘', '내일', '어제', '이번', '지난', '다음', '요즘', '최근', '지금',
    # 수량/단위
    '분', '점', '번', '개', '원', '년', '월', '일', '시간', '분간',
    # 커뮤니티 관용어
    '문의', '질문', '답변', '채택', '부탁', '감사', '혹시', '드립니다',
    '알려주세요', '해주세요', '도와주세요', '궁금합니다', '감사합니다',
    # 기타 불필요 명사
    '거', '게', '걸', '건', '저', '제', '그', '뭐', '왜', '어디',
    '말', '곳', '모두', '전부', '경우', '정도', '방법', '이유',
])


# =============================================
# 4. 핵심 전처리 함수
# =============================================

def post_merge(tokens: list) -> list:
    """명사 추출 후 인접 토큰 재합치기"""
    merged = []
    i = 0
    while i < len(tokens):
        # 3-gram 먼저 체크
        if i + 2 < len(tokens):
            tri = (tokens[i], tokens[i+1], tokens[i+2])
            if tri in POST_MERGE_3:
                merged.append(POST_MERGE_3[tri])
                i += 3
                continue
        # 2-gram 체크
        if i + 1 < len(tokens):
            bi = (tokens[i], tokens[i+1])
            if bi in POST_MERGE_2:
                merged.append(POST_MERGE_2[bi])
                i += 2
                continue
        merged.append(tokens[i])
        i += 1
    return merged


def preprocess_for_lda(text: str) -> str:
    """
    LDA 입력용 전처리 함수
    입력: 원문 텍스트
    출력: 공백 구분 명사 토큰 문자열
    """
    text = str(text)

    # Step 1. 유튜브/광고 자동삽입 노이즈 제거
    noise_patterns = [
        '광고 후 계속됩니다', '다음 동영상', 'subject author',
        '재생 (space', '재생 (k', '0초', '취소', '재생', '음소거',
    ]
    for n in noise_patterns:
        text = text.replace(n, ' ')

    # Step 2. URL 제거
    text = re.sub(r'http\S+|www\S+', '', text)

    # Step 3. 복합어 치환 (Okt 명사 추출 전에 적용)
    for src, tgt in COMPOUND_MAP.items():
        text = text.replace(src, tgt)

    # Step 4. 특수문자 제거 (한글, 영문, 숫자, 공백만 유지)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 5. Okt 명사 추출
    nouns = okt.nouns(text)

    # Step 6. 불용어 제거 + 2글자 이상만 유지
    nouns = [n for n in nouns if n not in STOPWORDS and len(n) >= 2]

    # Step 7. 인접 토큰 재합치기 (베이킹, 홈베이킹 등 복원)
    nouns = post_merge(nouns)

    return ' '.join(nouns)


# =============================================
# 5. 데이터 로드 & 전처리 실행
# =============================================

print("=" * 60)
print("📂 데이터 로드 중...")
print("=" * 60)

df = pd.read_csv('광파오븐_지식인.csv')
print(f"  원본 행수: {len(df)}건")

# 중복 제거
df = df.drop_duplicates(subset=['제목', '본문']).copy()
print(f"  중복 제거 후: {len(df)}건")

# 제목 + 본문 합치기
df['본문_clean'] = df['본문'].str.replace(r'\n|\t', ' ', regex=True).str.strip()
df['전체텍스트'] = df['제목'].fillna('') + ' ' + df['본문_clean'].fillna('')

# 전처리 적용
print("\n⚙️  전처리 중... (약 1~2분 소요)")
df['tokens'] = df['전체텍스트'].apply(preprocess_for_lda)

# 빈 토큰 제거
empty_count = (df['tokens'].str.strip() == '').sum()
print(f"  빈 토큰 문서: {empty_count}건 → 제거")
df = df[df['tokens'].str.strip() != ''].reset_index(drop=True)
print(f"  최종 문서 수: {len(df)}건")


# =============================================
# 6. 전처리 결과 확인
# =============================================

print("\n" + "=" * 60)
print("✅ 전처리 샘플 확인 (5건)")
print("=" * 60)
for _, row in df.head(5).iterrows():
    print(f"  원문: {str(row['전체텍스트'])[:60]}...")
    print(f"  토큰: {row['tokens']}")
    print()

# 토큰 빈도 상위 20개
from collections import Counter
all_tokens = ' '.join(df['tokens'].tolist()).split()
token_freq = Counter(all_tokens)
print("📊 토큰 빈도 Top 20:")
for token, count in token_freq.most_common(20):
    bar = '█' * min(count // 5, 30)
    print(f"  {token:12s} {bar} {count}")


# =============================================
# 7. LDA 입력용 저장
# =============================================

# 방법 A: 토큰 문자열 CSV 저장 (gensim Dictionary용)
df[['제목', 'tokens']].to_csv(
    '광파오븐_LDA입력.csv',
    index=False,
    encoding='utf-8-sig'
)
print("\n💾 광파오븐_LDA입력.csv 저장 완료")

# 방법 B: 토큰 리스트로 변환 (gensim 바로 사용 가능)
tokenized = [doc.split() for doc in df['tokens'].tolist()]
print(f"   토큰 리스트: {len(tokenized)}개 문서")
print(f"   예시: {tokenized[0]}")

print("\n🎉 전처리 완료! LDA 모델에 tokenized 또는 CSV를 입력하세요.")
