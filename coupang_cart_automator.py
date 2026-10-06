import os
import sys
import time
import json
import random
from playwright.sync_api import sync_playwright

CDP_URL = "http://127.0.0.1:9222"

# 30일 식단표에 따른 30가지 식재료 검색 쿼리 및 목표 스펙
GROCERY_LIST = [
    {"name": "돼지 앞다리살", "query": "돼지 앞다리살 불고기용 1kg", "target_qty": 2, "max_price": 25000, "category": "정육"},
    {"name": "우삼겹", "query": "우삼겹 바로구이용 1kg", "target_qty": 1, "max_price": 18000, "category": "정육"},
    {"name": "닭볶음탕용 닭", "query": "닭볶음탕용 닭 1kg", "target_qty": 2, "max_price": 15000, "category": "정육"},
    {"name": "훈제오리 슬라이스", "query": "훈제오리 슬라이스 500g", "target_qty": 1, "max_price": 10000, "category": "정육"},
    {"name": "소고기 국거리", "query": "소고기 국거리 양지 300g", "target_qty": 1, "max_price": 14000, "category": "정육"},
    {"name": "냉동 해물믹스", "query": "냉동 해물믹스 800g", "target_qty": 1, "max_price": 13000, "category": "수산"},
    {"name": "국산 두부", "query": "국산 두부 300g 3구", "target_qty": 2, "max_price": 8000, "category": "두부/계란"},
    {"name": "대란 30구", "query": "무항생제 대란 30구", "target_qty": 2, "max_price": 16000, "category": "두부/계란"},
    {"name": "손질 대파", "query": "손질 대파 1kg", "target_qty": 1, "max_price": 7000, "category": "채소"},
    {"name": "깐 양파", "query": "깐 양파 3kg", "target_qty": 1, "max_price": 7500, "category": "채소"},
    {"name": "햇 감자", "query": "감자 2kg", "target_qty": 1, "max_price": 7000, "category": "채소"},
    {"name": "애호박", "query": "인큐 애호박 2개", "target_qty": 2, "max_price": 7000, "category": "채소"},
    {"name": "양배추", "query": "양배추 1통", "target_qty": 1, "max_price": 5000, "category": "채소"},
    {"name": "세척 무", "query": "세척 무 1개", "target_qty": 1, "max_price": 3500, "category": "채소"},
    {"name": "콩나물", "query": "콩나물 1kg", "target_qty": 1, "max_price": 3000, "category": "채소"},
    {"name": "팽이버섯", "query": "팽이버섯 5입", "target_qty": 1, "max_price": 3000, "category": "채소"},
    {"name": "쌈채소 모둠", "query": "모둠 쌈채소 300g", "target_qty": 1, "max_price": 4500, "category": "채소"},
    {"name": "깐마늘", "query": "깐마늘 200g", "target_qty": 1, "max_price": 3500, "category": "채소"},
    {"name": "흙 당근", "query": "흙당근 1kg", "target_qty": 1, "max_price": 4000, "category": "채소"},
    {"name": "맛김치/포기김치", "query": "종가집 맛김치 1.5kg", "target_qty": 1, "max_price": 16000, "category": "김치"},
    {"name": "사각 어묵", "query": "부산어묵 사각 1kg", "target_qty": 1, "max_price": 6000, "category": "가공식품"},
    {"name": "스팸 클래식", "query": "스팸 200g 3캔", "target_qty": 1, "max_price": 11000, "category": "가공식품"},
    {"name": "살코기 참치", "query": "동원참치 100g 4캔", "target_qty": 1, "max_price": 8500, "category": "가공식품"},
    {"name": "비엔나 소시지", "query": "비엔나 소시지 500g", "target_qty": 1, "max_price": 6500, "category": "가공식품"},
    {"name": "순두부", "query": "순두부 350g", "target_qty": 2, "max_price": 3000, "category": "가공식품"},
    {"name": "카레가루", "query": "오뚜기 카레 약간매운맛 100g", "target_qty": 1, "max_price": 2500, "category": "양념/가루"},
    {"name": "짜장가루", "query": "오뚜기 짜장 100g", "target_qty": 1, "max_price": 2500, "category": "양념/가루"},
    {"name": "소면", "query": "오뚜기 소면 900g", "target_qty": 1, "max_price": 3500, "category": "면류"},
    {"name": "사골곰탕", "query": "비비고 사골곰탕 500g 2개", "target_qty": 1, "max_price": 3800, "category": "가공식품"},
    {"name": "떡볶이 떡", "query": "밀떡볶이 떡 500g", "target_qty": 1, "max_price": 3000, "category": "가공식품"}
]

def check_cdp_connection():
    import urllib.request
    try:
        req = urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=3)
        data = json.loads(req.read().decode())
        print(f"✅ Chrome CDP 연결 확인 성공! (브라우저: {data.get('Browser', 'Chrome')})")
        return True
    except Exception as e:
        print(f"❌ Chrome CDP 연결 실패: {e}")
        return False

def inspect_existing_cart(page):
    """기존 장바구니 품목을 확인하고 기록하여 보존"""
    print("\n" + "=" * 60)
    print("🔍 [1단계] 기존 장바구니 상태 확인 중...")
    print("=" * 60)
    
    page.goto("https://cart.coupang.com/cartView.pang", wait_until="domcontentloaded", timeout=20000)
    time.sleep(2.5)
    
    # 로그인 여부 검증
    content = page.content()
    if "로그인" in page.title() or "login.coupang.com" in page.url:
        print("⚠️ 아직 쿠팡 로그인이 감지되지 않았습니다. 브라우저에서 로그인을 완료해주세요.")
        return None
    
    existing_items = []
    try:
        # 장바구니 상품 요소 탐색
        items = page.query_selector_all(".cart-item-component, .cart-deal-item")
        print(f"📦 현재 장바구니에 기존 보관된 품목 수: {len(items)}개")
        for idx, item in enumerate(items, 1):
            title_el = item.query_selector(".product-name, .title")
            title = title_el.inner_text().strip() if title_el else f"기존 상품 {idx}"
            existing_items.append(title)
            print(f"  • [기존 보존] {title[:35]}...")
    except Exception as e:
        print(f"기존 장바구니 분석 중 알림: {e}")

    return existing_items

def search_and_add_item(page, item_info, added_results):
    """상품 1건 검색 -> 가격/로켓 비교 -> 장바구니 담기 (Rate Limit 준수)"""
    name = item_info["name"]
    query = item_info["query"]
    target_qty = item_info["target_qty"]
    
    print(f"\n▶ [{name}] 검색 진행: '{query}'")
    search_url = f"https://www.coupang.com/np/search?component=&q={urllib.parse.quote(query)}&channel=user"
    
    try:
        page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(random.uniform(1.8, 3.0)) # 인간 친화적 대기
        
        # 봇 탐지 확인
        content = page.content()
        if "접근이 제한되었습니다" in content or "Access Denied" in content or "captcha" in content.lower():
            print("🚨 [경고] 쿠팡 요청 제한/캡차 화면이 감지되었습니다. 즉시 작업을 일시 중지합니다.")
            return False

        # 검색 결과 1~3순위 중 로켓배송/로켓프레시 최우선 선택
        products = page.query_selector_all("li.search-product")
        if not products:
            print(f"⚠️ '{query}' 검색 결과가 없습니다. 기본 키워드로 재검색 시도: '{name}'")
            page.goto(f"https://www.coupang.com/np/search?q={urllib.parse.quote(name)}", wait_until="domcontentloaded")
            time.sleep(2)
            products = page.query_selector_all("li.search-product")
            
        if not products:
            print(f"❌ [{name}] 상품을 찾지 못해 건너뜁니다.")
            return True

        selected_product = None
        for prod in products[:5]:
            badge = prod.query_selector(".badge.rocket, .badge.delivery, .rocket-badge")
            title_el = prod.query_selector(".name")
            price_el = prod.query_selector(".price-value")
            
            if title_el and price_el:
                title = title_el.inner_text().strip()
                price_str = price_el.inner_text().strip().replace(",", "")
                price = int(price_str) if price_str.isdigit() else 0
                
                # 로켓 상품 우선
                is_rocket = badge is not None
                if is_rocket or selected_product is None:
                    selected_product = {
                        "element": prod,
                        "title": title,
                        "price": price,
                        "is_rocket": is_rocket,
                        "link": prod.query_selector("a").get_attribute("href") if prod.query_selector("a") else None
                    }
                    if is_rocket:
                        break # 로켓 상품 발견 시 즉시 선정

        if not selected_product:
            print(f"⚠️ [{name}] 적합한 상품 정보를 추출하지 못했습니다.")
            return True

        print(f"  👉 선정 상품: {selected_product['title'][:30]}... ({selected_product['price']:,}원)")
        
        # 상품 상세 페이지로 이동하여 장바구니 담기
        if selected_product["link"]:
            prod_url = "https://www.coupang.com" + selected_product["link"] if selected_product["link"].startswith("/") else selected_product["link"]
            page.goto(prod_url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(random.uniform(1.5, 2.5))
            
            # 장바구니 담기 버튼 탐색
            cart_btn = page.query_selector(".prod-buy-cart, button:has-text('장바구니 담기'), .btnCart")
            if cart_btn:
                # 수량 조정 (target_qty > 1 인 경우)
                if target_qty > 1:
                    qty_input = page.query_selector(".prod-buy-quantity input, input.quantity-input")
                    if qty_input:
                        qty_input.fill(str(target_qty))
                        time.sleep(0.5)

                cart_btn.click()
                print(f"  🛒 장바구니 담기 클릭 완료 (수량: {target_qty}개)")
                time.sleep(1.8)
                
                added_results.append({
                    "name": name,
                    "title": selected_product["title"],
                    "price": selected_product["price"],
                    "quantity": target_qty,
                    "total_price": selected_product["price"] * target_qty,
                    "is_rocket": selected_product["is_rocket"]
                })
            else:
                print(f"  ⚠️ 장바구니 담기 버튼을 찾을 수 없어 상세 링크 저장: {prod_url}")
                
        return True

    except Exception as e:
        print(f"⚠️ [{name}] 처리 중 예외 발생: {e}")
        return True

def run_cart_automation():
    import urllib.parse
    print("=" * 60)
    print("🚀 [쿠팡 30일 식단 장바구니 자동화] 시작")
    print("=" * 60)
    
    if not check_cdp_connection():
        print("❌ 먼저 Chrome을 디버깅 모드로 실행해주세요.")
        return

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()

        # 1. 기존 장바구니 품목 보존 확인
        existing = inspect_existing_cart(page)
        if existing is None:
            return

        added_results = []
        
        # 2. 1개씩 순차 처리 (Rate Limit 준수)
        print("\n" + "=" * 60)
        print(f"🛒 [2단계] 총 {len(GROCERY_LIST)}개 식재료 순차 검색 및 장바구니 추가 시작")
        print("=" * 60)
        
        for idx, item in enumerate(GROCERY_LIST, 1):
            print(f"\n[{idx}/{len(GROCERY_LIST)}] 진행 중...")
            success = search_and_add_item(page, item, added_results)
            if not success:
                print("\n🛑 요청 제한 또는 차단으로 인해 작업을 즉시 중단합니다.")
                break
            # 사이트 요청 제한 존중: 품목 간 2~4초 지연
            sleep_time = random.uniform(2.0, 4.0)
            time.sleep(sleep_time)

        # 3. 장바구니 최종 페이지로 이동
        print("\n" + "=" * 60)
        print("📋 [3단계] 최종 장바구니 상태 조회 및 주문서 준비")
        print("=" * 60)
        page.goto("https://cart.coupang.com/cartView.pang", wait_until="domcontentloaded")
        time.sleep(3)
        
        # 결과 요약 JSON 저장
        out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "cart_added_summary.json"))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({
                "existing_items_count": len(existing),
                "added_items": added_results,
                "total_added_price": sum(x["total_price"] for x in added_results)
            }, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 장바구니 추가 결과가 '{out_path}'에 저장되었습니다.")

if __name__ == "__main__":
    run_cart_automation()
