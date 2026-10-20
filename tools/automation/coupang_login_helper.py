import os
import sys
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "coupang_session_profile"))
os.makedirs(PROFILE_DIR, exist_ok=True)

def open_login_window():
    print("=" * 60)
    print("🛒 [쿠팡 로그인 헬퍼] 전용 브라우저 창을 화면에 엽니다.")
    print("=" * 60)
    print("화면에 열린 크롬 창에서 쿠팡 로그인을 진행해주세요.")
    print("로그인이 완료되면 자동으로 감지하여 세션을 저장합니다.\n")

    with sync_playwright() as p:
        launch_kwargs = {
            "user_data_dir": PROFILE_DIR,
            "headless": False,
            "locale": "ko-KR",
            "viewport": {"width": 1280, "height": 900},
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        }
        
        try:
            context = p.chromium.launch_persistent_context(channel="chrome", **launch_kwargs)
        except Exception as e:
            print(f"ℹ️ Google Chrome 채널 실행 대체(기본 Chromium 사용): {e}")
            context = p.chromium.launch_persistent_context(**launch_kwargs)

        page = context.pages[0] if context.pages else context.new_page()
        
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        print("🌐 쿠팡 로그인 페이지로 이동 중...")
        try:
            page.goto("https://login.coupang.com/login/login.pang", wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"⚠️ 페이지 로딩 알림: {e}")

        print("⏳ 화면에 열린 창에서 로그인을 완료해주세요. (최대 5분 대기)")
        
        logged_in = False
        start_time = time.time()
        
        while time.time() - start_time < 300:
            time.sleep(2)
            try:
                current_url = page.url
                cookies = context.cookies()
                has_auth_cookie = any(c['name'] in ['sid', 'CPINFO', 'MARKET_SESSION_ID'] for c in cookies)
                
                if "login" not in current_url:
                    content = page.content()
                    if "로그아웃" in content or "마이쿠팡" in content or has_auth_cookie:
                        print("\n" + "=" * 60)
                        print("🎉 [성공] 쿠팡 로그인이 정상 감지되었습니다!")
                        print("=" * 60)
                        
                        print("🛒 현재 장바구니 상태 확인 중...")
                        page.goto("https://cart.coupang.com/cartView.pang", wait_until="domcontentloaded", timeout=15000)
                        time.sleep(2)
                        
                        screenshot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "screenshots", "coupang_logged_in.png"))
                        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                        page.screenshot(path=screenshot_path)
                        print(f"📸 확인 스크린샷 저장 완료: {screenshot_path}")
                        
                        logged_in = True
                        break
            except Exception as e:
                if "Target page, context or browser has been closed" in str(e):
                    print("\n⚠️ 사용자에 의해 브라우저 창이 닫혔습니다.")
                    break
                time.sleep(1)

        if logged_in:
            print("\n✅ 세션이 'coupang_session_profile'에 안전하게 저장되었습니다.")
            print("이제 자동 장바구니 담기를 실행할 준비가 되었습니다!")
            time.sleep(2)
        else:
            print("\n⚠️ 시간 초과 또는 창이 닫혀 로그인이 완료되지 않았습니다.")

        context.close()
        return logged_in

if __name__ == "__main__":
    open_login_window()
