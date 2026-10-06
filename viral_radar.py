import os
import re
import json
import time
import random
import urllib.parse
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

# 둘 중 하나의 세션을 사용해 탐색
SESSION_ID = os.getenv("ONLY_APPLES_SESSION_ID") or os.getenv("GGUL_BAMM_SESSION_ID")
USER_ID = os.getenv("ONLY_APPLES_USER_ID") or os.getenv("GGUL_BAMM_USER_ID")

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "viral_posts_db.json"))

# 탐색할 핵심 키워드 목록
SEARCH_KEYWORDS = [
    "사과", "고구마", "농부", "농장", "과수원", "사장", "주인장", 
    "스토어", "하트라도", "스친", "산지직송", "택배", "주문 폭주"
]

def parse_view_count(text: str) -> int:
    """
    텍스트에서 '실제 조회수' 숫자만 엄격하게 파싱하여 정수로 반환합니다.
    가격(1만원, 1500만원), 팔로워(1.1만), 시간(10분만) 등의 오인식을 100% 원천 차단합니다.
    """
    if not text:
        return 0

    # 1. '조회 3.5만회', '조회 12만', '조회수 1.5만', '조회수: 12,345'
    m1 = re.search(r'조회(?:수)?\s*[:\s]*([\d,]+(?:\.\d+)?)\s*(만|천)?\s*회?', text)
    if m1:
        val_str = m1.group(1).replace(",", "")
        unit = m1.group(2)
        try:
            val = float(val_str)
            if unit == "만":
                return int(val * 10000)
            elif unit == "천":
                return int(val * 1000)
            return int(val)
        except ValueError:
            pass

    # 2. '1.5만회 조회', '1.5만 조회', '350회 조회', '12,345회 조회'
    m2 = re.search(r'([\d,]+(?:\.\d+)?)\s*(만|천)?\s*회?\s*조회', text)
    if m2:
        val_str = m2.group(1).replace(",", "")
        unit = m2.group(2)
        try:
            val = float(val_str)
            if unit == "만":
                return int(val * 10000)
            elif unit == "천":
                return int(val * 1000)
            return int(val)
        except ValueError:
            pass

    # 3. 영문 '12K views', '1.2M views', '12,345 views'
    m3 = re.search(r'([\d,]+(?:\.\d+)?)\s*(K|M)?\s*views', text, re.IGNORECASE)
    if m3:
        val_str = m3.group(1).replace(",", "")
        unit = (m3.group(2) or "").upper()
        try:
            val = float(val_str)
            if unit == "M":
                return int(val * 1000000)
            elif unit == "K":
                return int(val * 1000)
            return int(val)
        except ValueError:
            pass

    return 0

def collect_viral_posts(min_views: int = 10000, max_posts: int = 30):
    """
    스레드를 탐색하여 min_views(기본 1만 뷰) 이상인 고조회수 게시물을 수집하여 DB에 저장합니다.
    """
    if not SESSION_ID:
        print("❌ 탐색을 위한 세션 쿠키가 .env에 없습니다.")
        return []

    print("=" * 60)
    print(f"📡 [스레드 바이럴 레이더] {min_views:,}회 이상 떡상 게시물 수집 가동!")
    print("=" * 60)

    # 기존 DB 로드
    existing_posts = []
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    seen_texts = set(p.get("text", "")[:30] for p in existing_posts)
    new_collected = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 850},
            locale="ko-KR",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        cookie_val = urllib.parse.unquote(SESSION_ID)
        for domain in [".threads.com", ".threads.net", ".instagram.com"]:
            context.add_cookies([
                {"name": "sessionid", "value": cookie_val, "domain": domain, "path": "/", "secure": True, "httpOnly": True},
                {"name": "ds_user_id", "value": USER_ID, "domain": domain, "path": "/", "secure": True, "httpOnly": False}
            ])

        page = context.new_page()

        # 무작위로 키워드 3~4개 선택하여 검색
        keywords_to_search = random.sample(SEARCH_KEYWORDS, min(4, len(SEARCH_KEYWORDS)))

        for keyword in keywords_to_search:
            if len(new_collected) >= max_posts:
                break

            print(f"\n🔍 키워드 탐색 중: '{keyword}'")
            search_url = f"https://www.threads.com/search?q={urllib.parse.quote(keyword)}&serp_type=default"
            page.goto(search_url, wait_until="domcontentloaded")
            time.sleep(3)

            # 피드 아래로 스크롤하며 게시물 수집
            for scroll_step in range(4):
                page.mouse.wheel(0, 800)
                time.sleep(1.5)

                # 페이지 내 모든 텍스트 블록 및 아티클 탐색
                articles = page.locator("div[data-pressable-container='true'], article").all()

                for art in articles:
                    try:
                        full_text = art.inner_text().strip()
                        if not full_text:
                            continue

                        # 조회수 확인
                        views = parse_view_count(full_text)
                        
                        # 1만 뷰 이상 조건 충족 시
                        if views >= min_views:
                            # 텍스트 정제 (UI 버튼어구 제거)
                            lines = [line.strip() for line in full_text.split("\n") if line.strip()]
                            filtered_lines = [
                                l for l in lines 
                                if not re.match(r'^(\d+:\d+|\d+시간|\d+일|좋아요|답글|공유|팔로우|스레드)', l)
                            ]
                            clean_text = "\n".join(filtered_lines[:10])

                            short_key = clean_text[:30]
                            if short_key and short_key not in seen_texts:
                                seen_texts.add(short_key)
                                post_data = {
                                    "keyword": keyword,
                                    "views": views,
                                    "text": clean_text,
                                    "collected_at": time.strftime("%Y-%m-%d %H:%M:%S")
                                }
                                new_collected.append(post_data)
                                print(f"🎯 [1만뷰 발견!] {views:,}회 조회 | 키워드: {keyword}")
                                print(f"   내용: {clean_text[:50]}...")

                    except Exception:
                        continue

        browser.close()

    # 전체 DB에 합산 저장
    all_posts = existing_posts + new_collected
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"\n✨ 바이럴 레이더 수집 완료! (새로 수집: {len(new_collected)}개 / 누적 DB: {len(all_posts)}개)")
    return new_collected

if __name__ == "__main__":
    # 테스트 실행: 1만 뷰 이상 수집
    collect_viral_posts(min_views=10000, max_posts=15)
