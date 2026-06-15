import os
import time
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─────────────────────────────────────────
# 0. 설정
# ─────────────────────────────────────────

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

KEYWORDS = [
    "신혼부부 광파오븐", "신혼집 가전추천", "신혼부부 요리",
    "새댁 광파오븐", "커플요리 오븐", "신혼살림 가전",
    "광파오븐 레시피", "광파오븐 후기", "신혼부부 에어프라이어",
    "집들이 요리", "요리초보 신혼", "신혼집 주방가전",
]

MAX_RESULTS_PER_KEYWORD = 20   # 키워드당 최대 수집 영상 수
MAX_COMMENTS_PER_VIDEO  = 100  # 영상당 최대 댓글 수

OUTPUT_VIDEOS   = "youtube_videos.csv"
OUTPUT_COMMENTS = "youtube_comments.csv"


# ─────────────────────────────────────────
# 1. API 클라이언트 초기화
# ─────────────────────────────────────────

def get_youtube_client():
    if not API_KEY:
        raise ValueError(".env 파일에 YOUTUBE_API_KEY가 없습니다.")
    return build("youtube", "v3", developerKey=API_KEY)


# ─────────────────────────────────────────
# 2. 영상 검색
# ─────────────────────────────────────────

def search_videos(youtube, keyword, max_results=20):
    """키워드로 영상 검색 → video_id 목록 반환"""
    video_ids = []
    next_page_token = None

    while len(video_ids) < max_results:
        fetch = min(50, max_results - len(video_ids))
        try:
            response = youtube.search().list(
                q=keyword,
                part="id",
                type="video",
                maxResults=fetch,
                relevanceLanguage="ko",
                pageToken=next_page_token,
            ).execute()
        except HttpError as e:
            print(f"    검색 API 오류 ({keyword}): {e}")
            break

        for item in response.get("items", []):
            vid = item["id"].get("videoId")
            if vid:
                video_ids.append(vid)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
        time.sleep(0.2)

    return video_ids


# ─────────────────────────────────────────
# 3. 영상 메타데이터 수집
# ─────────────────────────────────────────

def get_video_details(youtube, video_ids, keyword):
    """video_id 목록 → 영상 상세 정보 수집"""
    rows = []
    for i in range(0, len(video_ids), 50):  # API 한 번에 최대 50개
        chunk = video_ids[i:i + 50]
        try:
            response = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(chunk),
            ).execute()
        except HttpError as e:
            print(f"    videos API 오류: {e}")
            continue

        for item in response.get("items", []):
            snip  = item.get("snippet", {})
            stats = item.get("statistics", {})
            rows.append({
                "video_id":      item["id"],
                "keyword":       keyword,
                "title":         snip.get("title", ""),
                "channel":       snip.get("channelTitle", ""),
                "published_at":  snip.get("publishedAt", "")[:10],
                "description":   snip.get("description", "")[:300],
                "view_count":    int(stats.get("viewCount",    0) or 0),
                "like_count":    int(stats.get("likeCount",    0) or 0),
                "comment_count": int(stats.get("commentCount", 0) or 0),
                "url":           f"https://www.youtube.com/watch?v={item['id']}",
            })
        time.sleep(0.2)

    return rows


# ─────────────────────────────────────────
# 4. 댓글 수집
# ─────────────────────────────────────────

def get_comments(youtube, video_id, max_comments=100):
    """영상 ID → 댓글 목록 반환"""
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        fetch = min(100, max_comments - len(comments))
        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=fetch,
                textFormat="plainText",
                order="relevance",
                pageToken=next_page_token,
            ).execute()
        except HttpError as e:
            # 댓글 비활성화 영상 등은 조용히 스킵
            if e.resp.status in (403, 404):
                break
            print(f"    댓글 API 오류 ({video_id}): {e}")
            break

        for item in response.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "video_id":   video_id,
                "comment_id": item["id"],
                "author":     top.get("authorDisplayName", ""),
                "text":       top.get("textDisplay", ""),
                "like_count": int(top.get("likeCount", 0) or 0),
                "published_at": top.get("publishedAt", "")[:10],
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
        time.sleep(0.1)

    return comments


# ─────────────────────────────────────────
# 5. 메인
# ─────────────────────────────────────────

def main():
    print("=" * 55)
    print(" YouTube 크롤링 시작 - 신혼부부 광파오븐 콘텐츠 기획")
    print("=" * 55)

    youtube = get_youtube_client()

    all_videos   = []
    all_comments = []
    seen_video_ids = set()  # 중복 영상 제거

    for kw in KEYWORDS:
        print(f"\n[검색] '{kw}'")

        # 2-1. 영상 ID 검색
        video_ids = search_videos(youtube, kw, max_results=MAX_RESULTS_PER_KEYWORD)
        new_ids   = [vid for vid in video_ids if vid not in seen_video_ids]
        seen_video_ids.update(new_ids)
        print(f"  검색 {len(video_ids)}개 → 신규 {len(new_ids)}개 (중복 {len(video_ids)-len(new_ids)}개 제거)")

        if not new_ids:
            continue

        # 2-2. 영상 메타데이터
        videos = get_video_details(youtube, new_ids, keyword=kw)
        all_videos.extend(videos)
        print(f"  영상 메타데이터 {len(videos)}개 수집")

        # 2-3. 댓글 수집
        for v in videos:
            if v["comment_count"] == 0:
                continue
            comments = get_comments(youtube, v["video_id"], max_comments=MAX_COMMENTS_PER_VIDEO)
            all_comments.extend(comments)
            print(f"    └ {v['title'][:30]}... → 댓글 {len(comments)}개")
            time.sleep(0.3)

        time.sleep(0.5)

    # ─────────────────────────────────────────
    # 6. 저장
    # ─────────────────────────────────────────

    print("\n" + "=" * 55)
    print(f"총 영상: {len(all_videos)}개  |  총 댓글: {len(all_comments)}개")

    if all_videos:
        df_videos = pd.DataFrame(all_videos)
        df_videos = df_videos.drop_duplicates(subset="video_id").reset_index(drop=True)
        df_videos.to_csv(OUTPUT_VIDEOS, index=False, encoding="utf-8-sig")
        print(f"[저장] {OUTPUT_VIDEOS}  ({len(df_videos)}행)")
        print(df_videos[["keyword", "title", "view_count", "like_count", "comment_count"]].head(5).to_string())
    else:
        print("⚠ 수집된 영상이 없습니다.")

    if all_comments:
        df_comments = pd.DataFrame(all_comments)
        df_comments = df_comments.drop_duplicates(subset="comment_id").reset_index(drop=True)
        df_comments.to_csv(OUTPUT_COMMENTS, index=False, encoding="utf-8-sig")
        print(f"[저장] {OUTPUT_COMMENTS}  ({len(df_comments)}행)")
    else:
        print("⚠ 수집된 댓글이 없습니다.")

    print("\n✅ 완료!")
    print(f"  {OUTPUT_VIDEOS}")
    print(f"  {OUTPUT_COMMENTS}")


if __name__ == "__main__":
    main()
