import re

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove leftover modal bottom half
    old_modal_tail = """      <!-- Item List Container -->
      <div id="batch-items-container" style="max-height: 250px; overflow-y: auto; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
        <!-- Injected via JS -->
      </div>

      <div class="modal-actions" style="justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="btn-action" style="background: #475569;" onclick="closeModal()">닫기</button>
          <button type="button" class="btn-action" style="background: rgba(239, 68, 68, 0.18); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); font-size: 0.85rem;" onclick="resetAllAddedStatus(true)" title="모든 상품의 담김 상태를 초기화하여 처음부터 다시 담기">🔄 초기화</button>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="btn-action success" id="btn-batch-view-cart" style="display: none;" onclick="openCartDirect()">🛍️ 내 쿠팡 장바구니 확인</button>
          <button class="btn-action orange" id="modal-confirm-btn" onclick="openNextPendingModalItem()">👉 1번 상품 쿠팡에서 담기</button>
        </div>
      </div>
    </div>
  </div>"""

    if old_modal_tail in content:
        content = content.replace(old_modal_tail, '')
        print(f"Removed old modal tail from {file_path}")
    else:
        # Regex removal between end of new batch modal and <script>
        pattern_modal_tail = r'(<div class="modal-overlay" id="batch-modal">[\s\S]*?</div>\s*</div>\s*</div>)\s*<!-- Item List Container -->[\s\S]*?</div>\s*</div>\s*(\s*<script>)'
        if re.search(pattern_modal_tail, content):
            content = re.sub(pattern_modal_tail, r'\1\n\2', content)
            print(f"Regex removed modal tail from {file_path}")

    # 2. Remove leftover JS junk around %`;
    junk_pattern = r'%\`;\s*if \(percentEl\) percentEl\.innerText[\s\S]*?openNextPendingModalItem\(\);\s*\}\s*\}\s*\}'
    if re.search(junk_pattern, content):
        content = re.sub(junk_pattern, '', content)
        print(f"Removed JS junk from {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    clean_file('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html')
    clean_file('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html')
