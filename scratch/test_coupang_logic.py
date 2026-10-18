import subprocess
import time
import json

def run_js_in_tab(tab_url_match, js_code):
    # Escape for AppleScript
    escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"')
    script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t) contains "{tab_url_match}" then
                    return execute t javascript "{escaped_js}"
                end if
            end repeat
        end repeat
        return "TAB_NOT_FOUND"
    end tell
    '''
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return proc.stdout.strip()

def navigate_tab(tab_url_match, target_url):
    script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t) contains "{tab_url_match}" then
                    set URL of t to "{target_url}"
                    return "NAVIGATED"
                end if
            end repeat
        end repeat
        return "TAB_NOT_FOUND"
    end tell
    '''
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return proc.stdout.strip()

print("1. Navigating Coupang tab to search '콩나물 500g'...")
nav_res = navigate_tab("coupang.com", "https://www.coupang.com/np/search?q=%EC%BD%A9%EB%82%98%EB%AC%BC%20500g&channel=user")
print("Nav result:", nav_res)

time.sleep(3.5)

print("2. Extracting best product link...")
extract_js = """
(() => {
    let cards = Array.from(document.querySelectorAll('li.search-product, li.baby-product, .search-product'));
    if (!cards.length) {
        const rawLinks = Array.from(document.querySelectorAll('a[href*="/vp/products/"]'));
        const validLinks = rawLinks.filter(a => !a.href.includes('view_together') && !a.closest('.recently-viewed-item') && !a.closest('#recent-view'));
        cards = validLinks.map(a => a.closest('li') || a.parentElement || a);
    }

    function parseCard(card) {
        const linkEl = card.tagName === 'A' ? card : card.querySelector('a.search-product-link, a[href*="/vp/products/"], a');
        if (!linkEl) return null;
        let href = linkEl.getAttribute('href') || linkEl.href;
        if (!href || !href.includes('/vp/products/')) return null;
        if (href.startsWith('/')) href = window.location.origin + href;

        const titleEl = card.querySelector('.name, .title, h2, h3') || linkEl;
        const title = (titleEl.textContent || card.textContent || '').trim();
        const fullText = (card.textContent || '').trim();
        const isSoldOut = fullText.includes('일시품절') || fullText.includes('품절');
        const isFresh = card.querySelector('.badge-rocket-fresh, .rocket-fresh-badge, [class*="fresh"]') !== null || fullText.includes('로켓프레시');
        const isRocket = card.querySelector('.badge.rocket, .rocket-badge, [class*="rocket"]') !== null || fullText.includes('로켓배송');

        return { href, title, fullText, isSoldOut, isFresh, isRocket };
    }

    const items = cards.map(parseCard).filter(Boolean);
    let candidates = items.filter(p => !p.isSoldOut);
    if (!candidates.length) candidates = items;

    if (!candidates.length) return JSON.stringify({ error: 'NO_CANDIDATES', count: cards.length });

    // Pick top item
    return JSON.stringify({ success: true, count: candidates.length, best: candidates[0] });
})()
"""

res = run_js_in_tab("coupang.com", extract_js)
print("Extract result:", res)

data = json.loads(res) if res and res.startswith('{') else {}
if not data.get("success"):
    print("Failed to extract:", res)
    exit(1)

best_url = data["best"]["href"]
print(f"3. Navigating to product page: {best_url}")
navigate_tab("coupang.com", best_url)

time.sleep(3.5)

print("4. Attempting to click '장바구니 담기'...")
click_js = """
(() => {
    const titleEl = document.querySelector('h1.prod-buy-header__title, .prod-title, .title');
    const title = titleEl ? titleEl.textContent.trim() : '';

    const btn = document.querySelector('.prod-cart-btn, .prod-buy-cart, .btn-cart, .btnCart') ||
                Array.from(document.querySelectorAll('button, a')).find(b => {
                    const t = (b.textContent || '').trim();
                    return (t.includes('장바구니 담기') || t === '장바구니') && !b.disabled;
                });

    if (!btn) {
        return JSON.stringify({ success: false, error: 'NO_BUTTON', bodySnippet: document.body.innerText.slice(0, 100) });
    }

    if (btn.disabled) {
        return JSON.stringify({ success: false, error: 'DISABLED' });
    }

    btn.scrollIntoView({ behavior: 'instant', block: 'center' });
    btn.focus();
    btn.click();
    btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
    btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window }));
    btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));

    return JSON.stringify({ success: true, title: title, buttonText: btn.textContent.trim() });
})()
"""

click_res = run_js_in_tab("coupang.com", click_js)
print("Click result:", click_res)

time.sleep(1.5)
print("5. Checking cart page...")
navigate_tab("coupang.com", "https://cart.coupang.com/cartView.pang")
time.sleep(2.5)

check_cart_js = """
(() => {
    const items = Array.from(document.querySelectorAll('.cart-deal-item, .cart-item, [class*=\"cart-item\"], .product-title, .cart-bundle-title'));
    return JSON.stringify({ count: items.length, sample: items.slice(0, 3).map(e => e.innerText.slice(0, 40)) });
})()
"""
cart_res = run_js_in_tab("cart.coupang.com", check_cart_js)
print("Final cart check:", cart_res)
