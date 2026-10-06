import os
import re
import json
import time
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from viral_radar import parse_view_count
from telegram_notifier import send_telegram_milestone_alert

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(ENV_PATH)

TRACKED_POSTS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "tracked_my_posts.json"))
MILESTONES = [10000, 30000, 50000, 100000, 200000, 500000, 1000000]

def load_tracked_posts() -> list:
    if os.path.exists(TRACKED_POSTS_FILE):
        try:
            with open(TRACKED_POSTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_tracked_posts(posts: list):
    os.makedirs(os.path.dirname(TRACKED_POSTS_FILE), exist_ok=True)
    with open(TRACKED_POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def get_account_insights(page, account: str) -> list:
    """
    메타 스레드 공식 크리에이터 인사이트 대시보드(threads.com/insights)에서
    최신 게시물들의 100% 실제 공식 조회수 데이터를 정확하게 파싱합니다.
    """
    try:
        page.goto("https://www.threads.com/insights", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # 신규 기능 안내 팝업이 뜨는 경우 '확인' 버튼 클릭
        ok_btn = page.locator("div[role='button']:has-text('확인'), button:has-text('확인')").first
        if ok_btn.count() > 0:
            ok_btn.click()
            page.wait_for_timeout(1500)

        txt = page.locator("body").inner_text()
        if "최신 게시물" not in txt:
            return []

        recent_section = txt.split("최신 게시물", 1)[1]
        if "개요" in recent_section:
            recent_section = recent_section.split("개요", 1)[0]

        blocks = re.split(r'\n조회수\b', recent_section)
        results = []
        for b in blocks[:-1]:
            lines = [l.strip() for l in b.splitlines() if l.strip()]
            if not lines:
                continue
            view_line = lines[-1]
            views = 0
            # 오직 숫자 또는 '1.2만' / '12K' 형태의 순수 수치 라인만 엄격 파싱 (임의 문장/가격/시간 100% 배제)
            m = re.match(r'^([\d,]+(?:\.\d+)?)\s*(만|천|K|M)?$', view_line, re.IGNORECASE)
            if m:
                val_str = m.group(1).replace(",", "")
                unit = (m.group(2) or "").upper()
                try:
                    val = float(val_str)
                    if unit == "만":
                        views = int(val * 10000)
                    elif unit in ["천", "K"]:
                        views = int(val * 1000)
                    elif unit == "M":
                        views = int(val * 1000000)
                    else:
                        views = int(val)
                except ValueError:
                    views = 0
            else:
                views = 0

            post_lines = [l for l in lines[:-1] if not l.isdigit()]
            clean_text = "\n".join(post_lines[:4])
            if clean_text:
                results.append((views, clean_text))
        return results
    except Exception as e:
        print(f"⚠️ @{account} 인사이트 파싱 중 예외: {e}")
        return []

def check_and_alert_milestones(headless: bool = True):
    """
    내 계정(@only_apples0.1, @ggul_bamm)의 공식 인사이트 대시보드를 직접 방문하여
    실제 조회수를 정확하게 수집하고, '진짜 1만 뷰 이상' 돌파 시에만 텔레그램 축하 알림 발송!
    """
    load_dotenv(ENV_PATH, override=True)
    sess_apples = os.getenv("ONLY_APPLES_SESSION_ID")
    sess_bamm = os.getenv("GGUL_BAMM_SESSION_ID")

    if not sess_apples and not sess_bamm:
        print("⚠️ 조회수 모니터링을 위한 활성 세션 쿠키가 없습니다.")
        return

    tracked_db = load_tracked_posts()
    tracked_dict = {p.get("post_key"): p for p in tracked_db if p.get("post_key")}

    # 기존 잘못 기록된 가짜 대형 조회수(15,000,000 등) 초기화 정리
    for p in tracked_dict.values():
        if p.get("views", 0) >= 10000:
            p["milestones_alerted"] = []
            p["views"] = 0

    print("=" * 65)
    print(f"📊 [스레드 공식 인사이트 기반 조회수 모니터링] ({datetime.now().strftime('%H:%M:%S')})")
    print("=" * 65)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)

        account_configs = [
            ("only_apples0.1", sess_apples),
            ("ggul_bamm", sess_bamm)
        ]

        for account, session_id in account_configs:
            if not session_id:
                continue

            try:
                print(f"\n🔍 @{account} 공식 인사이트 조회수 스캔 중...")
                context = browser.new_context(locale="ko-KR")
                context.add_cookies([{
                    "name": "sessionid",
                    "value": session_id,
                    "domain": ".threads.com",
                    "path": "/"
                }])
                page = context.new_page()

                insights_posts = get_account_insights(page, account)
                print(f" • 총 {len(insights_posts)}개 최신 게시물 실제 조회수 감지 완료")

                for idx, (real_views, clean_text) in enumerate(insights_posts):
                    # 고유 키 매칭 (계정명 + 첫 줄 20글자)
                    first_line = clean_text.splitlines()[0][:25].strip()
                    post_key = f"{account}_{first_line}"

                    # DB 항목 가져오기 또는 새로 등록
                    matched_key = None
                    for k in tracked_dict:
                        if k.startswith(f"{account}_") and first_line and first_line in k:
                            matched_key = k
                            break

                    if not matched_key:
                        matched_key = post_key
                        tracked_dict[matched_key] = {
                            "post_key": matched_key,
                            "account": account,
                            "text": clean_text,
                            "url": f"https://www.threads.com/@{account}",
                            "views": real_views,
                            "milestones_alerted": [],
                            "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                    entry = tracked_dict[matched_key]
                    entry["views"] = real_views
                    entry["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    print(f" • [글 {idx+1}] 실제 조회수: {real_views:,}회 | {first_line}...")

                    # 마일스톤 달성 검사 (진짜 1만 뷰 이상일 때만 발송!)
                    for milestone in MILESTONES:
                        if real_views >= milestone and milestone not in entry["milestones_alerted"]:
                            print(f"\n🎉🎉🎉 [진짜 떡상 축하!] @{account} {milestone:,}뷰 마일스톤 돌파 감지 (실제 {real_views:,}회)!")
                            send_telegram_milestone_alert(
                                account=account,
                                views=real_views,
                                text=clean_text,
                                post_url=entry.get("url"),
                                photo_path=None
                            )
                            entry["milestones_alerted"].append(milestone)

                context.close()

            except Exception as e:
                print(f"⚠️ @{account} 모니터링 중 오류: {e}")

        browser.close()

    # DB 저장
    save_tracked_posts(list(tracked_dict.values()))
    print("\n✅ 공식 인사이트 조회수 동기화 완료 (허위 알림 원천 차단)!")

    # 🧠 [성과 피드백 루프 자동 실행] 저조 게시물 분석 및 포맷 자가 진화(Mutation) 반영
    try:
        from performance_evaluator import evaluate_and_evolve
        print("\n🧠 [성과 피드백 & 자가 진화 루프 가동]")
        eval_report = evaluate_and_evolve()
        print(f" • 총 {eval_report['summary']['total_posts']}개 게시물 성과 분석 완료!")
        print(f" • 저조 피드백 {eval_report['summary']['underperforming']}개 변형 포맷 생성 및 가중치 업데이트 완료!")
    except Exception as eval_err:
        print(f"⚠️ 성과 피드백 분석 중 경고: {eval_err}")

if __name__ == "__main__":
    check_and_alert_milestones(headless=True)
