import re

def remove_duplicate_modal_tail(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    duplicate_block = """      <!-- Item List Container -->
      <div id="batch-items-container" style="max-height: 260px; overflow-y: auto; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
        <!-- Injected via JS -->
      </div>

      <div class="modal-actions" style="justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: center;">
          <button type="button" class="btn-action" style="background: #475569;" onclick="closeModal()">닫기</button>
          <button type="button" class="btn-action" id="modal-stop-btn" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); display: none;" onclick="stopBatchAutoAdd()">⏹️ 일시 정지</button>
          <button type="button" class="btn-action" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); font-size: 0.85rem;" onclick="resetAllAddedStatus(true)">🔄 초기화</button>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button type="button" class="btn-action success" id="btn-batch-view-cart" style="display: none;" onclick="openCartDirect()">🛍️ 내 쿠팡 장바구니 확인</button>
          <button type="button" class="btn-action orange" id="modal-confirm-btn" onclick="startBatchAutoAdd()">⚡ 전자동 담기 시작</button>
        </div>
      </div>
    </div>
  </div>"""

    if duplicate_block in content:
        content = content.replace(duplicate_block, '')
        print(f"Removed duplicate modal tail from {file_path}")
    else:
        # Regex search
        pattern = r'(\(만약 직접 쿠팡 검색창 새 탭들을 열고 싶으신 경우 클릭\)\s*</a>\s*</div>\s*</div>\s*</div>)\s*<!-- Item List Container -->[\s\S]*?</div>\s*</div>'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1', content)
            print(f"Regex removed duplicate modal tail from {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    remove_duplicate_modal_tail('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html')
    remove_duplicate_modal_tail('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html')
