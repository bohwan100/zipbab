import re

def add_local_guide(file_path, is_gogaek=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    page_name = 'gogaek_cart.html' if is_gogaek else 'cart_dashboard.html'

    guide_html = f"""      <!-- Localhost Redirect Helper Banner (Only visible on GitHub Pages / HTTPS) -->
      <div id="https-local-guide" style="display: none; background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 12px; padding: 12px 18px; margin: 12px 0 16px; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div style="font-size: 0.9rem; color: #bae6fd;">
          🤖 <strong>맥북 무간섭 백그라운드 전자동 담기 모드:</strong><br>
          화면 깜빡임이나 창 열림 없이 100% 백그라운드에서 담으시려면 <strong>로컬 주소(http://localhost:8080)</strong>로 접속해 주세요!
        </div>
        <button type="button" onclick="location.href='http://localhost:8080/{page_name}'" style="background: #3b82f6; color: #fff; border: none; padding: 9px 18px; border-radius: 8px; font-weight: 800; font-size: 0.88rem; cursor: pointer; box-shadow: 0 4px 12px rgba(59,130,246,0.4);">
          🚀 무간섭 백그라운드 모드로 열기
        </button>
      </div>"""

    if 'id="https-local-guide"' not in content:
        content = content.replace('<!-- KakaoTalk In-App Notice Bar -->', guide_html + '\n\n      <!-- KakaoTalk In-App Notice Bar -->')

    js_check = """
    // GitHub Pages HTTPS 접속 시 로컬 무간섭 안내 배너 표시
    if (window.location.protocol === 'https:') {
      const guide = document.getElementById('https-local-guide');
      if (guide) guide.style.display = 'flex';
    }
"""

    if 'id="https-local-guide"' in content and '// GitHub Pages HTTPS 접속 시 로컬 무간섭 안내 배너 표시' not in content:
        content = content.replace('window.onload =', js_check + '\n    window.onload =')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added local guide to {file_path}")

if __name__ == '__main__':
    add_local_guide('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html', False)
    add_local_guide('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html', True)
