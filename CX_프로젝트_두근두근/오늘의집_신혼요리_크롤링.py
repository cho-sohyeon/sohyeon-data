"""
오늘의집 '신혼요리' 커뮤니티 크롤러
- 검색 결과 목록 수집 (무한 스크롤)
- 게시글 본문 + 댓글 수집 (로그인 세션 쿠키 사용)
- 1년치 게시글 필터링
- 결과: 오늘의집_신혼요리_커뮤니티.csv

실행 전 준비:
  pip install selenium pandas webdriver-manager
  Chrome 브라우저에 오늘의집 로그인 상태 유지
"""

import time
import csv
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# ── 설정 ──────────────────────────────────────────────
QUERIES = ["신혼요리", "신혼집밥"]   # 수집할 키워드 목록
OUTPUT_FILE = "오늘의집_신혼커뮤니티.csv"
MONTHS_BACK = 36          # 3년치
SCROLL_PAUSE = 2.0        # 목록 스크롤 대기(초)
PAGE_LOAD_WAIT = 3.0      # 게시글 로드 대기(초)
COMMENT_WAIT = 2.0        # 댓글 페이지 전환 대기(초)
MAX_POSTS = 500           # 최대 수집 게시글 수 (0 = 무제한)
# ──────────────────────────────────────────────────────


def make_driver():
    """Chrome 드라이버 생성 (현재 로그인된 Chrome 프로필 사용)"""
    options = Options()
    # 현재 로그인된 Chrome 사용자 프로필 경로 (Windows 기준)
    import os
    user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    options.add_argument(f"--user-data-dir={user_data}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1280,900")
    # options.add_argument("--headless")  # 필요 시 주석 해제

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def parse_date(date_str):
    """
    오늘의집 날짜 형식 파싱
    - '05.12' → 연도 추정 (올해 또는 작년)
    - '2025.08.31' → 그대로 파싱
    """
    date_str = date_str.strip()
    now = datetime.now()

    # 연도 포함 형식: 2025.08.31
    if re.match(r'\d{4}\.\d{2}\.\d{2}', date_str):
        try:
            return datetime.strptime(date_str, "%Y.%m.%d")
        except:
            return None

    # MM.DD 형식: 05.12
    m = re.match(r'(\d{2})\.(\d{2})', date_str)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        # 현재 월보다 크면 작년으로 판단
        year = now.year if month <= now.month else now.year - 1
        try:
            return datetime(year, month, day)
        except:
            return None
    return None


def is_within_one_year(date_obj):
    if date_obj is None:
        return True  # 날짜 파싱 실패 시 포함
    cutoff = datetime.now() - timedelta(days=365)
    return date_obj >= cutoff


def collect_post_urls(driver, query):
    """커뮤니티 검색 목록에서 게시글 URL과 날짜 수집 (무한 스크롤)"""
    search_url = f"https://ohou.se/search/community?query={query}&search_affect_type=Typing"
    driver.get(search_url)
    time.sleep(3)

    post_data = []   # [(url, date_str), ...]
    seen_urls = set()
    stop_scroll = False
    last_height = 0
    no_new_count = 0

    print(f"[목록 수집] 검색 URL: {search_url}")

    while not stop_scroll:
        # 현재 페이지의 게시글 카드 수집
        cards = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/community/posts/"]')

        for card in cards:
            url = card.get_attribute("href")
            if not url or url in seen_urls:
                continue

            # 날짜 추출: 부모 요소에서 MM.DD 또는 YYYY.MM.DD 패턴 찾기
            try:
                parent = card.find_element(By.XPATH, "./ancestor::li[1] | ./ancestor::article[1] | ./parent::*")
                parent_text = parent.text
            except:
                parent_text = card.text

            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2}|\d{2}\.\d{2})', parent_text)
            date_str = date_match.group(1) if date_match else ""
            date_obj = parse_date(date_str) if date_str else None

            # 1년 이상 지난 글이면 스크롤 중단
            if date_obj and not is_within_one_year(date_obj):
                print(f"  → 1년 초과 게시글 발견 ({date_str}), 수집 종료")
                stop_scroll = True
                break

            seen_urls.add(url)
            post_data.append((url, date_str))
            print(f"  [{len(post_data)}] {url.split('/')[-1][:50]} | {date_str}")

            if MAX_POSTS > 0 and len(post_data) >= MAX_POSTS:
                stop_scroll = True
                break

        if stop_scroll:
            break

        # 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            no_new_count += 1
            if no_new_count >= 3:
                print("  → 더 이상 로드되지 않음, 수집 종료")
                break
        else:
            no_new_count = 0
        last_height = new_height

    print(f"[목록 수집 완료] 총 {len(post_data)}건")
    return post_data


def collect_comments(driver):
    """
    현재 게시글 페이지의 모든 댓글 수집 (페이지 넘김 포함)
    댓글 페이지네이션: 숫자 버튼 또는 '다음' 버튼
    """
    all_comments = []
    page_num = 1

    while True:
        time.sleep(COMMENT_WAIT)

        # 댓글 아이템 선택자 (오늘의집 구조)
        comment_selectors = [
            'li[class*="comment"]',
            'div[class*="CommentItem"]',
            'div[class*="comment-item"]',
            'article[class*="comment"]',
        ]

        comments_found = []
        for sel in comment_selectors:
            items = driver.find_elements(By.CSS_SELECTOR, sel)
            if items:
                comments_found = items
                break

        # 선택자로 못 찾으면 텍스트 기반으로 추출
        if not comments_found:
            # 페이지 전체 텍스트에서 댓글 영역 추출 시도
            try:
                # 댓글 영역 컨테이너 찾기
                comment_container = driver.find_element(
                    By.XPATH,
                    '//*[contains(@class,"comment") or contains(@id,"comment")]'
                )
                comment_text = comment_container.text.strip()
                if comment_text:
                    all_comments.append(f"[페이지{page_num}] {comment_text}")
            except:
                pass
            break

        for item in comments_found:
            text = item.text.strip()
            if text:
                all_comments.append(text)

        # 다음 페이지 버튼 찾기
        next_btn = None

        # 방법 1: '다음' 텍스트 버튼
        try:
            btns = driver.find_elements(By.XPATH, '//button[contains(text(),"다음")]')
            for btn in btns:
                if btn.is_displayed() and btn.is_enabled():
                    next_btn = btn
                    break
        except:
            pass

        # 방법 2: 페이지 번호 버튼 (현재 페이지+1)
        if not next_btn:
            try:
                next_page_btn = driver.find_element(
                    By.XPATH,
                    f'//button[text()="{page_num + 1}"]'
                )
                if next_page_btn.is_displayed() and next_page_btn.is_enabled():
                    next_btn = next_page_btn
            except:
                pass

        if not next_btn:
            break  # 더 이상 페이지 없음

        driver.execute_script("arguments[0].click();", next_btn)
        page_num += 1

        if page_num > 20:  # 안전장치
            break

    return "\n---\n".join(all_comments)


def collect_post_detail(driver, url, date_str):
    """게시글 상세 페이지에서 본문 + 댓글 수집"""
    try:
        driver.get(url)
        time.sleep(PAGE_LOAD_WAIT)

        # 본문 수집 - 페이지 전체 스크롤로 lazy load 유도
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        # 제목
        title = ""
        for sel in ['h1', 'h2[class*="title"]', '[class*="PostTitle"]', '[class*="post-title"]']:
            try:
                title = driver.find_element(By.CSS_SELECTOR, sel).text.strip()
                if title:
                    break
            except:
                pass

        # 카테고리
        category = ""
        for sel in ['[class*="category"]', '[class*="Category"]', 'span[class*="tag"]']:
            try:
                category = driver.find_element(By.CSS_SELECTOR, sel).text.strip()
                if category:
                    break
            except:
                pass

        # 작성자
        author = ""
        for sel in ['[class*="author"]', '[class*="Author"]', '[class*="username"]', '[class*="UserName"]']:
            try:
                author = driver.find_element(By.CSS_SELECTOR, sel).text.strip()
                if author:
                    break
            except:
                pass

        # 본문 텍스트 수집 (이미지 제외한 텍스트)
        body_text = ""
        for sel in [
            '[class*="PostBody"]', '[class*="post-body"]',
            '[class*="Content"]', 'article',
            'main', '[class*="content"]'
        ]:
            try:
                el = driver.find_element(By.CSS_SELECTOR, sel)
                body_text = el.text.strip()
                if len(body_text) > 50:
                    break
            except:
                pass

        # 본문이 너무 짧으면 body 전체 텍스트 사용
        if len(body_text) < 50:
            full_text = driver.find_element(By.TAG_NAME, 'body').text
            # 네비게이션/푸터 제거를 위해 중간 부분 추출
            body_text = full_text[:5000]

        # 좋아요/댓글 수
        like_count = ""
        comment_count_str = ""
        try:
            counts = driver.find_elements(By.CSS_SELECTOR, '[class*="count"], [class*="Count"]')
            nums = [c.text.strip() for c in counts if c.text.strip().isdigit()]
            if len(nums) >= 1:
                like_count = nums[0]
            if len(nums) >= 2:
                comment_count_str = nums[1]
        except:
            pass

        # 댓글 수집
        comments = collect_comments(driver)

        return {
            "url": url,
            "date": date_str,
            "title": title,
            "category": category,
            "author": author,
            "body": body_text.replace("\n", " ").strip(),
            "comments": comments.replace("\n", " ").strip(),
            "like_count": like_count,
            "comment_count": comment_count_str,
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

    except Exception as e:
        print(f"  [오류] {url}: {e}")
        return {
            "url": url,
            "date": date_str,
            "title": "",
            "category": "",
            "author": "",
            "body": "",
            "comments": "",
            "like_count": "",
            "comment_count": "",
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }


def main():
    print("=" * 60)
    print("오늘의집 커뮤니티 크롤러 시작")
    print(f"키워드: {QUERIES}")
    print(f"수집 기간: 최근 {MONTHS_BACK}개월")
    print("=" * 60)

    driver = make_driver()

    try:
        # 1단계: 모든 키워드의 게시글 목록 수집 (중복 URL 제거)
        all_post_data = {}  # {url: date_str} — URL을 키로 중복 제거

        for query in QUERIES:
            print(f"\n[키워드: {query}] 목록 수집 중...")
            post_data = collect_post_urls(driver, query)
            before = len(all_post_data)
            for url, date_str in post_data:
                if url not in all_post_data:
                    all_post_data[url] = date_str
            added = len(all_post_data) - before
            print(f"  → 신규 {added}건 추가 (중복 제거 후 누적 {len(all_post_data)}건)")

        if not all_post_data:
            print("[경고] 수집된 게시글이 없습니다.")
            return

        post_list = list(all_post_data.items())  # [(url, date_str), ...]

        # 2단계: 각 게시글 상세 수집
        results = []
        total = len(post_list)
        print(f"\n[상세 수집 시작] 총 {total}건")

        for i, (url, date_str) in enumerate(post_list, 1):
            print(f"  [{i}/{total}] 수집 중: {url.split('/')[-1][:60]}")
            detail = collect_post_detail(driver, url, date_str)
            results.append(detail)

            # 중간 저장 (50건마다)
            if i % 50 == 0:
                df_temp = pd.DataFrame(results)
                df_temp.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
                print(f"  → 중간 저장 완료 ({i}건)")

            time.sleep(1.0)  # 서버 부하 방지

        # 최종 저장
        df = pd.DataFrame(results)
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

        print("\n" + "=" * 60)
        print(f"[완료] 총 {len(results)}건 수집")
        print(f"[저장] {OUTPUT_FILE}")
        print(f"[컬럼] url, date, title, category, author, body, comments, like_count, comment_count, collected_at")
        print("=" * 60)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
