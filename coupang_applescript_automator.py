import os
import sys
import time
import json
import urllib.parse
import subprocess

def run_applescript(script: str) -> str:
    """AppleScript를 실행하고 결과를 반환"""
    try:
        proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
        return proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

def exec_chrome_js(js_code: str) -> str:
    """활성화된 Chrome 탭에서 자바스크립트 실행"""
    # 따옴표 이스케이프
    escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"')
    script = f'tell application "Google Chrome" to execute front window\'s active tab javascript "{escaped_js}"'
    return run_applescript(script)

def check_js_permission():
    """Apple Events JS 허용 여부 체크"""
    res = exec_chrome_js("document.title")
    if "오류 발생" in res or "ERROR" in res:
        return False, res
    return True, res

def set_chrome_url(url: str):
    script = f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'
    run_applescript(script)

def inspect_cart():
    """장바구니 이동 및 기존 담긴 상품 확인"""
    print("\n" + "=" * 60)
    print("🛒 [1단계] 현재 장바구니 확인 중 (기존 상품 보존)...")
    print("=" * 60)
    
    set_chrome_url("https://cart.coupang.com/cartView.pang")
    time.sleep(3)
    
    # 로그인 상태 및 상품 목록 확인 JS
    js = """
    (() => {
        const title = document.title;
        const isLogin = !window.location.href.includes('login') && (document.body.innerText.includes('마이쿠팡') || document.body.innerText.includes('장바구니'));
        const items = Array.from(document.querySelectorAll('.cart-deal-item, .cart-item-component, .product-name')).map(el => el.innerText.trim()).filter(t => t.length > 0);
        return JSON.stringify({ isLogin, title, itemsCount: items.length, sample: items.slice(0, 5) });
    })()
    """
    res = exec_chrome_js(js)
    try:
        data = json.loads(res)
        print(f"✅ 접속 성공! (로그인 상태: {data.get('isLogin')}, 기존 장바구니 품목 수: {data.get('itemsCount')}개)")
        if data.get('sample'):
            print("📦 기존 보관 품목 일부:")
            for s in data['sample']:
                print(f"  • {s[:30]}...")
        return data
    except Exception as e:
        print(f"장바구니 파싱 알림: {res} (오류: {e})")
        return None

if __name__ == "__main__":
    allowed, msg = check_js_permission()
    if not allowed:
        print("❌ [설정 필요] Chrome 메뉴 바에서 [보기] > [개발자] > [Apple Events의 자바스크립트 허용]을 클릭해주세요.")
        print(f"상세 메시지: {msg}")
    else:
        print(f"🎉 Chrome 자바스크립트 제어 권한 확인 성공! (현재 탭 제목: {msg})")
        inspect_cart()
