import subprocess

script = '''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t) contains "cart.coupang.com" then
                set r to execute t javascript "
                    (() => {
                        const items = Array.from(document.querySelectorAll('.cart-deal-item, .cart-item, [class*=\"cart-item\"], .product-title, .cart-bundle-title'));
                        const emptyEl = document.querySelector('.cart-empty, .empty-cart, .no-item');
                        return JSON.stringify({
                            itemsCount: items.length,
                            itemsText: items.slice(0, 5).map(e => e.innerText.slice(0, 40)),
                            isEmptyVisible: emptyEl ? emptyEl.innerText.slice(0, 60) : false,
                            bodySnippet: document.body.innerText.slice(0, 200)
                        });
                    })()
                "
                return r
            end if
        end repeat
    end repeat
    return "NO_CART_TAB"
end tell
'''

proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
print("STDOUT:\n", proc.stdout)
