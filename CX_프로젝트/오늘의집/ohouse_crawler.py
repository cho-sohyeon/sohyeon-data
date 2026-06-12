"""
오늘의집 크롤링 + 전처리 + 워드클라우드
터미널 전용 실행 (python ohouse_crawler.py)
"""

import asyncio
import re
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
from wordcloud import WordCloud
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

KEYWORDS = ["광파오븐", "요리 루틴", "혼밥", "주방 힐링", "건강 요리"]

OUTPUT_CSV   = "ohouse_data.csv"
WC_COMMUNITY = "wordcloud_community.png"
WC_REVIEW    = "wordcloud_review.png"
WC_ALL       = "wordcloud_all.png"

STOPWORDS = set([
    "이", "그", "저", "것", "수", "때", "등", "및", "를", "가",
    "은", "는", "에", "의", "로", "도", "을", "와", "과", "하", "있",
    "되", "않", "없", "나", "우리", "더", "아주", "진짜", "너무",
    "정말", "같은", "이런", "그런", "저런", "하는", "있는", "없는",
    "으로", "에서", "에게", "부터", "까지", "한", "합니다", "해요",
    "했", "했어요", "해서", "이고", "이라", "거", "게", "건", "걸",
    "좀", "제", "내", "내가", "그냥", "여기", "저기", "어디", "왜",
    "어떻게", "얼마나", "뭐", "뭔가", "뭘", "누구", "언제", "어느",
    "구매", "배송", "사용", "구입", "가격", "후기", "제품",
])

async def crawl_community(page, keyword, max_posts=30):
    print(f"\n[커뮤니티] '{keyword}' 수집 중...")
    results = []
    url = f"https://contents.ohou.se/community?query={keyword}"
    await page.goto(url, timeout=30000)
    await page.wait_for_timeout(3000)
    for _ in range(5):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1500)
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    for sel in ["[class*='CommunityPost']","[class*='PostCard']","[class*='FeedCard']","[class*='CardItem']","article"]:
        posts = soup.select(sel)
        if len(posts) >= 3:
            print(f"    셀렉터 '{sel}' → {len(posts)}개")
            break
    for post in posts[:max_posts]:
        title = post.select_one("h1,h2,h3,[class*='title'],[class*='Title']")
        body  = post.select_one("p,[class*='content'],[class*='desc'],[class*='body'],[class*='text']")
        likes = post.select_one("[class*='like'],[class*='heart']")
        title_val = title.get_text(strip=True) if title else ""
        text_val  = body.get_text(strip=True)  if body  else title_val
        if text_val and len(text_val) > 5:
            results.append({"type":"community","keyword":keyword,"title":title_val,"text":text_val,"likes":likes.get_text(strip=True) if likes else "0"})
    if not results:
        print("    셀렉터 미발견 → 텍스트 직접 추출")
        all_text = soup.get_text(separator="\n")
        lines = [l.strip() for l in all_text.split("\n") if len(l.strip()) > 15 and re.search(r'[가-힣]{4,}', l)]
        for line in lines[:max_posts]:
            results.append({"type":"community","keyword":keyword,"title":"","text":line,"likes":"0"})
    print(f"  → {len(results)}개 수집")
    return results

async def crawl_reviews(page, max_products=5, max_reviews=30):
    print(f"\n[제품 리뷰] 광파오븐 수집 중...")
    results = []
    await page.goto("https://ohou.se/store/search?query=광파오븐&order=review_count", timeout=30000)
    await page.wait_for_timeout(3000)
    for _ in range(3):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1200)
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")
    seen, product_links = set(), []
    for a in soup.select("a[href*='/products/']"):
        href  = a.get("href","")
        match = re.search(r"/products/(\d+)", href)
        if match:
            pid = match.group(1)
            if pid not in seen:
                seen.add(pid)
                name_tag = a.select_one("[class*='name'],[class*='title'],span,p")
                name = name_tag.get_text(strip=True)[:20] if name_tag else f"광파오븐_{pid}"
                product_links.append((pid, name))
        if len(product_links) >= max_products:
            break
    print(f"  제품 {len(product_links)}개 발견")
    for pid, pname in product_links:
        await page.goto(f"https://ohou.se/products/{pid}", timeout=30000)
        await page.wait_for_timeout(2000)
        for _ in range(4):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
        html2 = await page.content()
        soup2 = BeautifulSoup(html2, "html.parser")
        review_items = []
        for sel in ["[class*='ReviewItem']","[class*='review-item']","[class*='Review_review']","[class*='ReviewContent']"]:
            review_items = soup2.select(sel)
            if review_items:
                break
        for item in review_items[:max_reviews]:
            t = item.select_one("[class*='content'],[class*='text'],p")
            s = item.select_one("[class*='star'],[class*='rating'],[class*='score']")
            if t and len(t.get_text(strip=True)) > 5:
                results.append({"type":"review","keyword":"광파오븐","title":pname,"text":t.get_text(strip=True),"likes":s.get_text(strip=True) if s else ""})
        print(f"  → '{pname}' 리뷰 {len(review_items)}개")
        await asyncio.sleep(1)
    return results

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

def get_font_path():
    import os
    for path in ["C:/Windows/Fonts/malgun.ttf","C:/Windows/Fonts/NanumGothic.ttf","C:/Windows/Fonts/gulim.ttc"]:
        if os.path.exists(path):
            return path
    for f in fm.findSystemFonts():
        if any(k in f.lower() for k in ["nanum","malgun","gulim","gothic"]):
            return f
    return None

def make_wordcloud(words, title, save_path, colormap="RdPu"):
    if not words:
        print(f"  ⚠ '{title}' 단어 없음")
        return
    freq = Counter(words)
    font_path = get_font_path()
    kwargs = dict(width=1200, height=600, background_color="white", max_words=100, colormap=colormap, prefer_horizontal=0.85)
    if font_path:
        kwargs["font_path"] = font_path
    wc = WordCloud(**kwargs).generate_from_frequencies(freq)
    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=16, pad=16)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  저장: {save_path}")

async def main():
    print("=" * 50)
    print(" 오늘의집 크롤링 시작")
    print("=" * 50)
    all_data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await context.new_page()
        for kw in KEYWORDS:
            data = await crawl_community(page, kw, max_posts=30)
            all_data.extend(data)
            await asyncio.sleep(1.5)
        review_data = await crawl_reviews(page, max_products=5, max_reviews=30)
        all_data.extend(review_data)
        await browser.close()
    print(f"\n총 수집: {len(all_data)}개")
    if not all_data:
        print("⚠ 수집 실패")
        return
    df = pd.DataFrame(all_data)
    df["text"] = df["text"].fillna("").astype(str)
    df = df[df["text"].str.len() > 5].reset_index(drop=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[저장] {OUTPUT_CSV} ({len(df)}행)")
    community_nouns = extract_nouns(df[df["type"]=="community"]["text"].tolist())
    review_nouns    = extract_nouns(df[df["type"]=="review"]["text"].tolist())
    all_nouns       = extract_nouns(df["text"].tolist())
    print(f"  커뮤니티 {len(community_nouns)}개 / 리뷰 {len(review_nouns)}개 / 전체 {len(all_nouns)}개")
    if not all_nouns:
        print("⚠ 명사 추출 결과 없음")
        return
    make_wordcloud(community_nouns, "커뮤니티 워드클라우드",      WC_COMMUNITY, "Blues")
    make_wordcloud(review_nouns,    "광파오븐 리뷰 워드클라우드", WC_REVIEW,    "Oranges")
    make_wordcloud(all_nouns,       "전체 통합 워드클라우드",      WC_ALL,       "RdPu")
    print("\n[TOP 20 키워드]")
    for i, (word, cnt) in enumerate(Counter(all_nouns).most_common(20), 1):
        print(f"  {i:2}. {word} ({cnt}회)")
    print(f"\n✅ 완료!")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())