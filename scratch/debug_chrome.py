import subprocess

script = '''
tell application "Google Chrome"
    set res to ""
    repeat with w in windows
        repeat with t in tabs of w
            set u to URL of t
            if u contains "cart_dashboard.html" then
                set r to execute t javascript "JSON.stringify({url: location.href, isExt: !!document.documentElement.getAttribute('data-zipbabbot-extension'), status: (document.getElementById('batch-progress-status')||{}).innerText})"
                set res to res & "DASHBOARD: " & r & "\n"
            end if
            if u contains "coupang.com" then
                set r to execute t javascript "JSON.stringify({url: location.href, title: document.title, isProductPage: location.href.indexOf('/vp/products/') !== -1, hasBtn: !!document.querySelector('.prod-cart-btn')})"
                set res to res & "COUPANG: " & r & "\n"
            end if
        end repeat
    end repeat
    return res
end tell
'''

proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
print("STDOUT:\n", proc.stdout)
print("STDERR:\n", proc.stderr)
