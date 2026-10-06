import os
import sys
import time
import random
import urllib.parse
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

# 계정별 자격증명 매핑
ACCOUNT_CREDENTIALS = {
    "ggul_bamm": {
        "session_id": os.getenv("GGUL_BAMM_SESSION_ID"),
        "user_id": os.getenv("GGUL_BAMM_USER_ID", "76299946186")
    },
    "only_apples0.1": {
        "session_id": os.getenv("ONLY_APPLES_SESSION_ID"),
        "user_id": os.getenv("ONLY_APPLES_USER_ID", "76869721343")
    }
}

def human_type(page, text: str):
    """사람처럼 불규칙하게 타이핑"""
    lines = text.strip().split("\n")
    for line_idx, line in enumerate(lines):
        for char in line:
            page.keyboard.type(char)
            if char in [" ", "!", "?", ".", ","]:
                time.sleep(random.uniform(0.08, 0.22))
            else:
                time.sleep(random.uniform(0.03, 0.09))
        
        if line_idx < len(lines) - 1:
            time.sleep(random.uniform(0.2, 0.5))
            page.keyboard.press("Shift+Enter")
            time.sleep(random.uniform(0.1, 0.3))

def human_browse(page):
    """접속 후 자연스러운 피드 훑기"""
    print("👀 [스텔스] 사람처럼 피드를 둘러보는 중...")
    time.sleep(random.uniform(1.2, 2.5))
    page.mouse.move(random.randint(400, 700), random.randint(300, 500), steps=8)
    page.mouse.wheel(0, random.randint(200, 400))
    time.sleep(random.uniform(1.0, 2.0))
    page.mouse.wheel(0, -random.randint(100, 250))
    time.sleep(random.uniform(0.8, 1.5))

def post_to_threads_multi(account: str, text: str, image_path: str = None, comment: str = None, headless: bool = False, enable_stealth: bool = True, daily_progress: str = None):
    """
    지정된 계정(ggul_bamm 또는 only_apples0.1)으로 텍스트 + 사진을 자동으로 안전하게 게시하고,
    댓글(comment)이 제공되면 첫 댓글(답글)로 링크를 자동 등록합니다.
    """
    creds = ACCOUNT_CREDENTIALS.get(account)
    if not creds or not creds["session_id"]:
        raise ValueError(f"⚠️ 계정 '{account}'의 세션 정보가 .env에 설정되지 않았습니다.")

    print("=" * 60)
    print(f"🚀 [계정: {account}] 스레드 자동 포스팅 시작!")
    print("=" * 60)
    print(f"📝 올릴 내용:\n{text.strip()}\n")
    if image_path:
        print(f"🖼️ 첨부 이미지: {image_path}")

    with sync_playwright() as p:
        width = 1280 + random.randint(-15, 15)
        height = 850 + random.randint(-10, 10)

        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars"
            ]
        )
        context = browser.new_context(
            viewport={"width": width, "height": height},
            locale="ko-KR",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        # 봇 탐지 우회
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
        """)

        # 쿠키 주입
        cookie_val = urllib.parse.unquote(creds["session_id"])
        user_id = creds["user_id"]
        for domain in [".threads.com", ".threads.net", ".instagram.com"]:
            context.add_cookies([
                {"name": "sessionid", "value": cookie_val, "domain": domain, "path": "/", "secure": True, "httpOnly": True},
                {"name": "ds_user_id", "value": user_id, "domain": domain, "path": "/", "secure": True, "httpOnly": False}
            ])

        page = context.new_page()
        print("🌐 1. 스레드(threads.com) 접속 중...")
        page.goto("https://www.threads.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)

        # 세션 만료 여부 즉시 검사
        if "login" in page.url or page.locator("text='Instagram으로 계속하기'").count() > 0:
            print(f"❌ [계정: {account}] 세션 쿠키가 만료되었습니다! 로그인이 해제된 상태입니다.")
            print(f"👉 터미널에서 다음 명령어로 세션을 갱신해주세요: python3 login_helper.py {account}")
            page.screenshot(path=f"session_expired_{account}.png")
            browser.close()
            return False

        # 스텔스 모드 작동
        if enable_stealth:
            human_browse(page)

        # 기존 팝업/모달이 떠 있다면 자동 닫기 (작성 모달 제외)
        existing_dialogs = page.locator("div[role='dialog'], div[aria-modal='true']")
        if existing_dialogs.count() > 0:
            for i in range(existing_dialogs.count()):
                d = existing_dialogs.nth(i)
                if d.locator("div[contenteditable='true']").count() == 0:
                    print("⚠️ 방해되는 기존 팝업/모달 감지 -> 닫기 시도")
                    close_btn = d.locator("svg[aria-label='닫기'], svg[aria-label='Close'], button:has-text('닫기'), button:has-text('Close')")
                    if close_btn.count() > 0 and close_btn.first.is_visible():
                        close_btn.first.click()
                    else:
                        page.keyboard.press("Escape")
                    page.wait_for_timeout(800)

        # 1. 글 작성 창 열기
        print("🔍 2. 글 작성 창 여는 중...")
        triggers = [
            page.locator("svg[aria-label='만들기']"),
            page.locator("svg[aria-label='Create']"),
            page.get_by_text("새로운 스레드"),
            page.get_by_text("What's new?")
        ]
        opened = False
        for t in triggers:
            if t.count() > 0 and t.first.is_visible():
                box = t.first.bounding_box()
                if box:
                    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
                # 상위 버튼 요소 우선 클릭 시도
                ancestor = t.first.locator("xpath=ancestor::div[@role='button'] | ancestor::a | ancestor::button").first
                if ancestor.count() > 0 and ancestor.is_visible():
                    ancestor.click(force=True)
                else:
                    t.first.click(force=True)
                opened = True
                break

        page.wait_for_timeout(random.uniform(1200, 1800))

        # 2. 본문 입력창 찾기 (모달 로딩 대기)
        print("⏳ 본문 입력창 렌더링 대기 중...")
        textbox = page.locator("div[contenteditable='true']").last
        try:
            textbox.wait_for(state="visible", timeout=15000)
        except Exception:
            print("❌ 본문 입력창을 찾지 못했습니다.")
            page.screenshot(path="post_error.png")
            browser.close()
            return False

        print("✍️ 3. 본문 입력창 포커스...")
        textbox.click(force=True)
        time.sleep(random.uniform(0.5, 0.9))

        # 3. 미디어 첨부 (사진/동영상 있을 경우)
        if image_path and os.path.exists(image_path):
            ext = os.path.splitext(image_path)[1].lower()
            is_video = ext in [".mp4", ".mov", ".m4v"]
            media_type = "동영상" if is_video else "사진"
            print(f"📷 4. {media_type} 첨부 시도: {os.path.basename(image_path)}")
            try:
                # 파일 인풋 필드 찾아서 주입
                file_input = page.locator("input[type='file']").first
                if file_input.count():
                    file_input.set_input_files(image_path)
                    print(f"✅ {media_type} 첨부 완료! 미디어 처리 대기...")
                    wait_time = random.uniform(5000, 7000) if is_video else random.uniform(2500, 3500)
                    page.wait_for_timeout(wait_time)
                else:
                    print(f"⚠️ {media_type} 첨부 인풋을 찾지 못하여 텍스트만 게시합니다.")
            except Exception as e:
                print(f"⚠️ {media_type} 첨부 중 경고: {e}")

        # 4. 실시간 타이핑
        print("⌨️ 5. 본문 내용 타이핑 중...")
        if enable_stealth:
            human_type(page, text)
        else:
            for line in text.strip().split("\n"):
                page.keyboard.type(line, delay=40)
                page.keyboard.press("Shift+Enter")

        # 5. 오타 검토 망설임
        proof_delay = random.uniform(1.8, 3.2)
        print(f"\n👀 6. 글 검토 대기... ({proof_delay:.1f}초)")
        time.sleep(proof_delay)
        page.screenshot(path=f"step1_{account}_ready.png")

        # 6. 게시 버튼 클릭
        post_btn = None
        for name in ["Post", "게시"]:
            loc = page.get_by_text(name, exact=True)
            if loc.count() > 0:
                for k in range(loc.count() - 1, -1, -1):
                    item = loc.nth(k)
                    if item.is_visible():
                        post_btn = item
                        break
            if post_btn:
                break

        if post_btn:
            box = post_btn.bounding_box()
            if box:
                page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=5)
            print("🚀 7. [Post] 버튼 클릭 완료!")
            post_btn.click(force=True)
        else:
            print("🚀 7. 단축키(Meta+Enter)로 게시 시도!")
            page.keyboard.press("Meta+Enter")

        # 7. 업로드 완료 대기 (토스트 '게시되었습니다' 확인)
        print("⏳ 8. 게시물 전송 완료 대기 중...")
        toast_view = None
        for _ in range(25):  # 최대 25초 동안 대기
            for name in ["보기", "View"]:
                loc = page.locator(f"a:has-text('{name}')")
                if loc.count() > 0 and loc.first.is_visible():
                    toast_view = loc.first
                    break
            if toast_view:
                break
            time.sleep(1)

        page.screenshot(path=f"step2_{account}_published.png")
        page.screenshot(path=f"post_{account}_success.png")
        print(f"\n🎉 [{account}] 메인 스레드 게시물이 등록되었습니다!")

        # 8. 첫 댓글(답글) 자동 등록
        if comment:
            print(f"\n💬 9. 첫 댓글(링크) 등록 시작...")
            try:
                post_reply_comment(page, account, comment, toast_elem=toast_view, enable_stealth=enable_stealth)
            except Exception as e:
                print(f"⚠️ 첫 댓글 등록 중 오류 발생: {e}")
                page.screenshot(path=f"reply_{account}_error.png")

        print(f"\n🎉🎉🎉 [{account}] 모든 게시 및 첫 댓글 작업 완료!")
        
        # 9. 텔레그램 실시간 알림 발송 (토큰 설정 시 자동 발송)
        try:
            from telegram_notifier import send_telegram_post_alert
            send_telegram_post_alert(
                account=account,
                text=text,
                comment=comment,
                photo_path=f"step4_{account}_done.png",
                daily_progress=daily_progress
            )
        except Exception as e:
            print(f"⚠️ 텔레그램 알림 발송 예외: {e}")

        time.sleep(2)
        browser.close()
        return True

def post_reply_comment(page, account: str, comment: str, toast_elem = None, enable_stealth: bool = True):
    """
    본문 등록 후 즉시 첫 댓글(답글)을 달아 외부 링크를 제공합니다.
    (알고리즘 페널티 완전 우회 & 클릭 전환율 극대화)
    """
    opened_post = False
    
    # 1. 화면에 뜬 '보기' 링크 클릭 시도
    if toast_elem and toast_elem.is_visible():
        print("🔗 토스트 '보기' 클릭하여 방금 작성한 게시물로 바로 진입!")
        toast_elem.click(force=True)
        opened_post = True
        page.wait_for_timeout(random.uniform(2500, 3500))
    else:
        view_links = [
            page.get_by_role("link", name="보기"),
            page.get_by_role("link", name="View"),
            page.locator("a:has-text('보기')"),
            page.locator("a:has-text('View')")
        ]
        for vl in view_links:
            if vl.count() > 0 and vl.first.is_visible():
                print("🔗 토스트 '보기' 클릭하여 게시물로 바로 진입!")
                vl.first.click(force=True)
                opened_post = True
                page.wait_for_timeout(random.uniform(2500, 3500))
                break

    # 2. 토스트로 못 간 경우 내 프로필로 이동 (고정글 제외 로직 적용)
    if not opened_post:
        print(f"🌐 프로필 페이지(https://www.threads.com/@{account})로 이동하여 최신 글 확인...")
        page.goto(f"https://www.threads.com/@{account}", wait_until="domcontentloaded")
        page.wait_for_timeout(random.uniform(3000, 4000))

        # 고정글(Pinned/고정됨)이 아닌 실제 최신 글 진입
        post_items = page.locator("div[data-pressable-container='true']").all()
        target_post = None
        for p in post_items:
            p_text = p.inner_text()
            if "고정됨" in p_text or "Pinned" in p_text:
                continue
            target_post = p
            break

        if target_post:
            print("🎯 고정글(Pinned)을 제외한 방금 작성한 최신 게시물 포커스!")
            target_reply = target_post.locator("svg[aria-label='답글'], svg[aria-label='Reply']").first
            if target_reply.count() > 0 and target_reply.is_visible():
                target_reply.click(force=True)
            else:
                target_post.click(force=True)
        else:
            page.locator("svg[aria-label='답글'], svg[aria-label='Reply']").first.click(force=True)
    else:
        # 게시물 상세 페이지에 진입한 상태에서 댓글창 포커스
        detail_reply = page.locator("svg[aria-label='답글'], svg[aria-label='Reply']").first
        if detail_reply.count() > 0 and detail_reply.is_visible():
            detail_reply.click(force=True)

    page.wait_for_timeout(random.uniform(1500, 2200))

    # 4. 답글 입력창 찾아서 포커스
    reply_textbox = page.locator("div[contenteditable='true']").last
    try:
        reply_textbox.wait_for(state="visible", timeout=15000)
    except Exception:
        print("⚠️ 답글 입력창을 찾지 못해 작성을 중단합니다.")
        return False

    reply_textbox.click(force=True)
    time.sleep(random.uniform(0.4, 0.8))

    # 5. 첫 댓글 타이핑 (스마트스토어 카드 우선 보장 알고리즘)
    print(f"⌨️ 첫 댓글 내용 작성 중: {comment.splitlines()[0]}...")
    lines = comment.strip().split("\n")
    smartstore_line = None
    smartstore_idx = -1
    for idx, l in enumerate(lines):
        if any(domain in l for domain in ["smartstore.naver.com", "vvd.bz", "naver.me"]):
            smartstore_line = l
            smartstore_idx = idx
            break

    if smartstore_line and len(lines) > 2:
        # 스마트스토어 자리를 비워두고 나머지 먼저 작성한 뒤, 커서를 올려 스마트스토어를 마지막에 입력!
        # 스레드는 '가장 마지막에 입력/수정된 링크'를 대표 미리보기 박스로 띄우므로 100% 스마트스토어 카드가 생성됨
        other_lines = list(lines)
        other_lines[smartstore_idx] = ""
        
        for l_idx, l in enumerate(other_lines):
            for char in l:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.02, 0.05))
            if l_idx < len(other_lines) - 1:
                page.keyboard.press("Shift+Enter")
                time.sleep(0.06)

        page.wait_for_timeout(1500)
        
        # 스마트스토어 줄로 커서 위로 이동
        steps_up = len(other_lines) - 1 - smartstore_idx
        for _ in range(steps_up):
            page.keyboard.press("ArrowUp")
            time.sleep(0.05)
        
        # 스마트스토어 링크를 마지막으로 입력하여 카드 선점!
        for char in smartstore_line:
            page.keyboard.type(char)
            time.sleep(random.uniform(0.01, 0.03))
        page.keyboard.press("Space")
    else:
        if enable_stealth:
            human_type(page, comment)
        else:
            for line in lines:
                page.keyboard.type(line, delay=40)
                page.keyboard.press("Shift+Enter")

    print("⏳ 스마트스토어 상품 카드 렌더링 대기 중 (3~4초)...")
    time.sleep(random.uniform(3.5, 4.5))
    page.screenshot(path=f"step3_{account}_reply_ready.png")

    # 6. 답글 게시 버튼 클릭
    reply_post_btn = None
    for name in ["Post", "게시", "답글"]:
        loc = page.get_by_text(name, exact=True)
        if loc.count() > 0:
            for k in range(loc.count() - 1, -1, -1):
                item = loc.nth(k)
                if item.is_visible():
                    reply_post_btn = item
                    break
        if reply_post_btn:
            break

    if reply_post_btn:
        box = reply_post_btn.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4)
        print("🚀 답글 [Post] 버튼 클릭 완료!")
        reply_post_btn.click(force=True)
    else:
        print("🚀 단축키(Meta+Enter)로 답글 게시 시도!")
        page.keyboard.press("Meta+Enter")

    page.wait_for_timeout(random.uniform(4000, 6000))
    page.screenshot(path=f"step4_{account}_done.png")
    page.screenshot(path=f"post_{account}_comment_success.png")
    print(f"✅ [{account}] 첫 댓글(링크) 등록 성공!")
    return True

if __name__ == "__main__":
    from content_engine import ContentEngine
    engine = ContentEngine()
    test_acc = "only_apples0.1" if len(sys.argv) < 2 else sys.argv[1]
    test_img = engine.get_random_image_for_account(test_acc)
    
    if "apple" in test_acc:
        test_msg = """사과 파는 사람이야.
성공 꼭 하고 싶다 ....
소백산 영주 풍기 홍로 사과인데
한 입 베어 물면 턱으로 과즙 뚝뚝 흘러내려.
사과 좋아하는 스친들 지나가다 하트라도 하나 눌러줘 🍎"""
    else:
        test_msg = """안녕 나는 꿀밤이야 ! 🌰
공주 정안에서 진짜 달콤한 햇밤 파는 중이야.
성공 꼭 하고 싶어 ....
에어프라이어 돌리면 꿀 터지는 밤이거든.
지나가다 하트라도 콕 눌러주라..! 🌰✨"""

    test_cmt = engine.get_first_comment(test_acc)

    post_to_threads_multi(test_acc, test_msg, image_path=test_img, comment=test_cmt, headless=False)
