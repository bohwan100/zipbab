import re

def polish_buttons(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace right panel buttons
    old_panel_btns = """            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button class="btn-action orange" style="padding: 6px 12px; font-size: 0.8rem;" onclick="copyCurrentWeekBookmarklet()">
                📋 1초 자동담기 코드 복사
              </button>
              <button class="btn-action" style="padding: 6px 12px; font-size: 0.8rem; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #60a5fa;" onclick="openThisWeekGroceries()">
                ⚡ 차례대로 열기
              </button>
            </div>"""

    new_panel_btns = """            <button class="btn-action orange" style="padding: 7px 15px; font-size: 0.85rem; font-weight: 800;" onclick="openThisWeekGroceries(true)">
              ⚡ 이번 주 품목 전자동 담기 (딸깍!)
            </button>"""

    if old_panel_btns in content:
        content = content.replace(old_panel_btns, new_panel_btns)

    # Action banner button
    content = content.replace('onclick="openThisWeekGroceries()"', 'onclick="openThisWeekGroceries(true)"')
    content = content.replace('>⚡ 현재 주차 품목 모아 담기<', '>⚡ 현재 주차 품목 전자동 담기 (딸깍!)<')

    # In renderWeekView, update btn-week-batch-top text
    content = content.replace("`⚡ ${weekNum}주차 품목 한 번에 담기`", "`⚡ ${weekNum}주차 전 품목 전자동 담기 (딸깍!)`")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Polished {file_path}")

if __name__ == '__main__':
    polish_buttons('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html')
    polish_buttons('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html')
