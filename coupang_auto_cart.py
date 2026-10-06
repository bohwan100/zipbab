import os
import sys
import time
import json
import urllib.parse
import subprocess

def run_applescript(script: str) -> str:
    """AppleScript 실행"""
    try:
        proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
        return proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

def exec_chrome_js(js_code: str) -> str:
    """Chrome 활성 탭에서 자바스크립트 실행"""
    escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    script = f'tell application "Google Chrome" to execute front window\'s active tab javascript "{escaped_js}"'
    return run_applescript(script)

def check_permission():
    """Apple Events 권한 상태 체크"""
    res = exec_chrome_js("document.title")
    if "오류 발생" in res or "ERROR" in res:
        return False, res
    return True, res

def set_chrome_url(url: str):
    """현재 탭 URL 변경"""
    script = f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'
    run_applescript(script)

def open_new_tab(url: str):
    """새 탭 열기"""
    script = f'tell application "Google Chrome" to tell front window to make new tab with properties {{URL:"{url}"}}'
    run_applescript(script)

def add_single_item_to_cart(query: str, item_name: str):
    """
    단일 품목 쿠팡 자동 장바구니 담기 플로우:
    1. 검색 URL로 이동
    2. 1위 로켓배송 상품 클릭하여 상세 페이지 진입
    3. '장바구니 담기' 버튼 클릭
    """
    print(f"\n🛒 [{item_name}] 자동 장바구니 담기 시작 (검색어: {query})")
    
    search_url = f"https://www.coupang.com/np/search?q={urllib.parse.quote(query)}&channel=user"
    set_chrome_url(search_url)
    time.sleep(2.5) # 페이지 로딩 대기
    
    # 1위 로켓배송 상품 링크 찾아서 이동
    find_product_js = """
    (() => {
        // 로켓배송 배지가 있는 상품 우선, 없으면 첫 번째 상품
        const items = Array.from(document.querySelectorAll('li.search-product'));
        let target = items.find(el => el.querySelector('.badge.rocket, .badge.delivery-badge, .badge-rocket-fresh'));
        if (!target && items.length > 0) target = items[0];
        
        if (target) {
            const link = target.querySelector('a.search-product-link');
            if (link) {
                const url = link.href;
                window.location.href = url;
                return JSON.stringify({ success: true, url: url });
            }
        }
        return JSON.stringify({ success: false, reason: '상품을 찾을 수 없음' });
    })()
    """
    res = exec_chrome_js(find_product_js)
    print(f"  👉 상품 페이지 이동: {res}")
    time.sleep(3.0) # 상품 상세 페이지 로딩 대기
    
    # 장바구니 담기 버튼 클릭
    click_cart_js = """
    (() => {
        // 장바구니 담기 버튼 찾기
        const btn = document.querySelector('.prod-cart-btn, .btn-cart, .prod-buy-btn') ||
                    Array.from(document.querySelectorAll('button, a')).find(b => b.innerText.includes('장바구니 담기'));
        if (btn) {
            btn.click();
            return JSON.stringify({ success: true, message: '장바구니 담기 버튼 클릭 완료' });
        }
        return JSON.stringify({ success: false, message: '버튼을 찾을 수 없음' });
    })()
    """
    res_cart = exec_chrome_js(click_cart_js)
    print(f"  ✨ 담기 결과: {res_cart}")
    time.sleep(1.5)
    return res_cart

if __name__ == "__main__":
    allowed, msg = check_permission()
    if not allowed:
        print("❌ [Chrome 권한 필요]")
        print("Chrome 상단 메뉴 바에서 [보기] -> [개발자] -> [Apple Events의 자바스크립트 허용]을 클릭해주세요!")
        sys.exit(1)
    
    print("✅ Chrome 제어 권한 확인 성공! 테스트 1건 진행...")
    # 테스트로 콩나물 1건 장바구니 담기 시도
    add_single_item_to_cart("콩나물 500g", "국산 콩나물")
