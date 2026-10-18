import os
import re

def update_cart_file(file_path, is_gogaek=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CSS Injection
    css_to_add = """
    /* Bookmarklet Guide Hero Banner */
    .bookmarklet-hero-banner {
      background: linear-gradient(135deg, rgba(249, 115, 22, 0.18) 0%, rgba(99, 102, 241, 0.22) 100%);
      border: 2px solid #f97316;
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 25px;
      box-shadow: 0 8px 30px rgba(249, 115, 22, 0.25);
      position: relative;
    }
    .bm-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      background: #f97316;
      color: #fff;
      font-size: 0.82rem;
      font-weight: 800;
      border-radius: 20px;
      margin-bottom: 10px;
      box-shadow: 0 2px 10px rgba(249, 115, 22, 0.4);
    }
    .bm-title {
      font-size: 1.45rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }
    .bm-desc {
      color: #cbd5e1;
      font-size: 0.95rem;
      line-height: 1.6;
      margin-bottom: 18px;
    }
    .bm-step-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }
    .bm-step-card {
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 14px 16px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }
    .bm-step-badge {
      width: 58px;
      padding: 3px 0;
      border-radius: 6px;
      background: #f97316;
      color: #fff;
      font-weight: 800;
      font-size: 0.75rem;
      text-align: center;
      flex-shrink: 0;
    }
    .bm-step-content { flex: 1; min-width: 0; }
    .bm-step-tit { font-size: 0.92rem; font-weight: 800; color: #fff; margin-bottom: 3px; }
    .bm-step-sub { font-size: 0.8rem; color: #94a3b8; line-height: 1.4; }
    .bm-btn-group {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }
    .btn-bm-main {
      background: linear-gradient(135deg, #f97316, #ea580c);
      color: #fff;
      border: none;
      padding: 13px 22px;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 18px rgba(249, 115, 22, 0.5);
      transition: all 0.2s ease;
      animation: pulseBmBtn 2s infinite;
    }
    .btn-bm-main:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(249, 115, 22, 0.75);
    }
    @keyframes pulseBmBtn {
      0%, 100% { box-shadow: 0 4px 18px rgba(249, 115, 22, 0.45); }
      50% { box-shadow: 0 6px 26px rgba(249, 115, 22, 0.8); }
    }
    .btn-bm-guide {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #fff;
      padding: 12px 18px;
      border-radius: 12px;
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .btn-bm-guide:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: #fff;
    }
    .btn-bm-coupang {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      padding: 12px 18px;
      border-radius: 12px;
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .btn-bm-coupang:hover {
      background: #10b981;
      color: #fff;
    }
"""

    if '/* Bookmarklet Guide Hero Banner */' not in content:
        content = content.replace('</style>', css_to_add + '\n  </style>')

    # 2. Hero Banner HTML Injection
    banner_html = """
    <!-- ============================================== -->
    <!-- ⚡ [필독] 쿠팡 장바구니 1초 자동 담기 북마클릿 배너 -->
    <!-- ============================================== -->
    <div class="bookmarklet-hero-banner" id="bookmarklet-hero-banner">
      <div class="bm-header-row">
        <div>
          <span class="bm-badge">⚡ 1초 원클릭 자동 담기 (필수 추천)</span>
          <h2 class="bm-title">
            🛒 쿠팡 장바구니 1초 자동 담기 (사파리/크롬 1회 즐겨찾기)
          </h2>
          <p class="bm-desc">
            식재료를 하나하나 검색해서 담으실 필요가 없습니다! 스마트폰 사파리 책갈피에 <strong>[집밥봇 담기]</strong>를 <strong>딱 1번만 등록(약 30초)</strong>해두시면, 쿠팡에서 터치 한 번으로 이번 주 식재료가 모두 자동으로 담깁니다.
          </p>
        </div>
      </div>

      <!-- 3-Step Visual Strip for Beginners -->
      <div class="bm-step-strip">
        <div class="bm-step-card">
          <div class="bm-step-badge">STEP 1</div>
          <div class="bm-step-content">
            <div class="bm-step-tit">📋 이번 주 코드 복사</div>
            <div class="bm-step-sub">아래 오렌지 버튼을 눌러 이번 주차 식재료 담기 코드를 복사합니다.</div>
          </div>
        </div>

        <div class="bm-step-card">
          <div class="bm-step-badge" style="background: #3b82f6;">STEP 2</div>
          <div class="bm-step-content">
            <div class="bm-step-tit">📑 Safari 책갈피 추가</div>
            <div class="bm-step-sub">Safari [공유 ⬆️] ➔ [책갈피 추가] ➔ [편집]에서 주소에 붙여넣기합니다.</div>
          </div>
        </div>

        <div class="bm-step-card">
          <div class="bm-step-badge" style="background: #10b981;">STEP 3</div>
          <div class="bm-step-content">
            <div class="bm-step-tit">🚀 쿠팡에서 터치!</div>
            <div class="bm-step-sub">쿠팡(m.coupang.com) 접속 후 책갈피를 누르면 장바구니로 바로 담깁니다.</div>
          </div>
        </div>
      </div>

      <!-- Action Button Group -->
      <div class="bm-btn-group">
        <button type="button" class="btn-bm-main" id="btn-bm-copy-banner" onclick="copyCurrentWeekBookmarklet()">
          📋 <span id="bm-banner-week-text">1주차</span> 식재료 1초 자동 담기 코드 복사
        </button>
        <button type="button" class="btn-bm-guide" onclick="openBookmarkletModal()">
          📖 30초 설정 가이드 보기 (초보자 필독)
        </button>
        <button type="button" class="btn-bm-coupang" onclick="safeOpenUrl('https://m.coupang.com')">
          🚀 쿠팡 열기
        </button>
      </div>
    </div>
"""

    if 'id="bookmarklet-hero-banner"' not in content:
        # Insert right after </header> inside container
        # Find </header> inside <div class="container">
        # In the original file:
        # <div class="container">
        #   <header>
        #     ...
        #   </header>
        #   <!-- 4주차 분할 장보기 통계 바 ... -->
        pattern = r'(</header>\s*<!-- 4주차 분할 장보기 통계 바)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'</header>\n' + banner_html + r'\n    <!-- 4주차 분할 장보기 통계 바', content, count=1)
        else:
            # Fallback insertion before weekly-split-bar
            content = content.replace('<div class="weekly-split-bar">', banner_html + '\n    <div class="weekly-split-bar">')

    # 3. Bookmarklet Modal Injection
    modal_html = """
  <!-- Bookmarklet 3-Step Detailed Guide Modal -->
  <div class="modal-overlay" id="bookmarklet-modal" onclick="if(event.target===this)closeBookmarkletModal()">
    <div class="modal-content" style="max-width: 620px; max-height: 90vh; overflow-y: auto;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 1.4rem;">⚡</span>
          <h2 style="font-size: 1.25rem; font-weight: 800; color: #fff;">쿠팡 1초 자동 담기 북마크 설정법</h2>
        </div>
        <button onclick="closeBookmarkletModal()" style="background: rgba(255,255,255,0.1); border: none; color: #cbd5e1; width: 32px; height: 32px; border-radius: 50%; font-size: 1rem; cursor: pointer; font-weight: bold;">✕</button>
      </div>

      <div style="background: rgba(249, 115, 22, 0.12); border: 1px solid rgba(249, 115, 22, 0.35); border-radius: 10px; padding: 12px 16px; margin-bottom: 18px; font-size: 0.88rem; color: #fed7aa; line-height: 1.5;">
        💡 <strong>처음 1회만 설정(약 30초)</strong>해두시면, 앞으로 매주 장볼 때 쿠팡에서 책갈피를 누르기만 하면 모든 재료가 1초 만에 자동 담깁니다!
      </div>

      <!-- Step Cards -->
      <div style="display: flex; flex-direction: column; gap: 14px; margin-bottom: 22px;">
        <!-- STEP 1 -->
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 12px; padding: 16px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background: #f97316; color: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem;">1</span>
            <span style="font-weight: 800; color: #fff; font-size: 1rem;">자동 담기 코드 복사</span>
          </div>
          <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;">
            아래 버튼을 눌러 현재 주차(<span id="bm-modal-week-num" style="color: #f97316; font-weight: 700;">1</span>주차)의 자동 담기 코드를 클립보드에 복사합니다.
          </p>
          <button type="button" class="btn-action orange" style="width: 100%; justify-content: center; font-size: 0.92rem; padding: 10px;" onclick="copyCurrentWeekBookmarklet(true)">
            📋 <span id="bm-btn-copy-label">1주차 자동 담기 코드 복사하기</span>
          </button>
        </div>

        <!-- STEP 2 -->
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 12px; padding: 16px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background: #3b82f6; color: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem;">2</span>
            <span style="font-weight: 800; color: #fff; font-size: 1rem;">Safari(아이폰)에서 북마크 등록 (1회만)</span>
          </div>
          <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
            ① Safari 화면 하단 중앙의 <strong>[공유 버튼 ⬆️]</strong> 터치<br>
            ② <strong>[책갈피 추가]</strong>를 누르고, 이름을 <strong>[집밥봇 담기]</strong>로 입력 후 저장<br>
            ③ Safari 하단 <strong>[책 모양 아이콘 📖]</strong> 터치 ➔ 우측 하단 <strong>[편집]</strong> 터치<br>
            ④ 방금 저장한 <strong>[집밥봇 담기]</strong> 터치 ➔ <strong>주소(URL) 전체를 지우고</strong> 방금 1단계에서 복사한 코드를 <strong>[붙여넣기]</strong> 후 완료!
          </div>
        </div>

        <!-- STEP 3 -->
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 12px; padding: 16px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background: #10b981; color: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem;">3</span>
            <span style="font-weight: 800; color: #fff; font-size: 1rem;">쿠팡(m.coupang.com)에서 북마크 누르면 끝!</span>
          </div>
          <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 10px;">
            ① 사파리로 <strong>쿠팡(m.coupang.com)</strong>에 로그인합니다.<br>
            ② 책 모양(📖) 책갈피를 열어 <strong>[집밥봇 담기]</strong>를 누릅니다.<br>
            ③ 쿠팡 화면 상단에 <strong>집밥봇 장바구니 도우미</strong>가 나타나며, 이번 주 식재료가 순식간에 내 장바구니로 쏙 들어갑니다!
          </div>
        </div>
      </div>

      <div style="display: flex; gap: 10px; justify-content: flex-end; flex-wrap: wrap;">
        <button type="button" class="btn-action success" onclick="safeOpenUrl('https://m.coupang.com'); closeBookmarkletModal();">
          🚀 쿠팡 모바일 웹 열기
        </button>
        <button type="button" class="btn-action" style="background: #334155; color: #fff;" onclick="closeBookmarkletModal()">
          닫기
        </button>
      </div>
    </div>
  </div>
"""

    if 'id="bookmarklet-modal"' not in content:
        content = content.replace('<div class="modal-overlay" id="batch-modal"', modal_html + '\n  <div class="modal-overlay" id="batch-modal"')

    # 4. JavaScript Functions Injection
    js_to_add = """
    // ==============================================
    // 쿠팡 장바구니 북마클릿 (방안 B) 자동 담기 엔진
    // ==============================================
    function openBookmarkletModal() {
      const modal = document.getElementById('bookmarklet-modal');
      if (!modal) return;
      const weekNum = currentSelectedWeek || 1;
      const weekElem = document.getElementById('bm-modal-week-num');
      const labelElem = document.getElementById('bm-btn-copy-label');
      if (weekElem) weekElem.innerText = weekNum;
      if (labelElem) labelElem.innerText = `${weekNum}주차 자동 담기 코드 복사하기`;
      modal.style.display = 'flex';
    }

    function closeBookmarkletModal() {
      const modal = document.getElementById('bookmarklet-modal');
      if (modal) modal.style.display = 'none';
    }

    function generateBookmarkletCode(weekNum) {
      const weekItems = allProducts.filter(p => p.orderWeek === weekNum);
      const itemsData = weekItems.map(it => ({
        name: it.name,
        spec: it.spec,
        qty: it.qty,
        price: it.total,
        url: getPartnerUrl(it.query)
      }));
      const itemsJson = JSON.stringify(itemsData);

      const rawScript = `(function(){` +
        `var old = document.getElementById('zb-cart-overlay');if (old) old.remove();` +
        `var items = ${itemsJson};var currIndex = 0;` +
        `var o = document.createElement('div');o.id = 'zb-cart-overlay';` +
        `o.style.cssText = 'position:fixed;top:10px;left:50%;transform:translateX(-50%);width:92%;max-width:440px;max-height:86vh;overflow-y:auto;background:#0f172a;color:#f8fafc;border:2px solid #f97316;border-radius:18px;box-shadow:0 12px 35px rgba(0,0,0,0.85);z-index:99999999;padding:16px;font-family:-apple-system,BlinkMacSystemFont,sans-serif;box-sizing:border-box;';` +
        `var h = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid #334155;">';` +
        `h += '<div><div style="font-size:16px;font-weight:800;color:#f97316;">🤖 집밥봇 장바구니 도우미</div>';` +
        `h += '<div style="font-size:12px;color:#94a3b8;margin-top:2px;">${weekNum}주차 식재료 (' + items.length + '종) 자동 담기</div></div>';` +
        `h += '<button onclick="document.getElementById(\\'zb-cart-overlay\\').remove()" style="background:#334155;color:#fff;border:none;border-radius:50%;width:28px;height:28px;font-weight:bold;cursor:pointer;font-size:14px;">✕</button></div>';` +
        `h += '<div style="background:rgba(249,115,22,0.15);border:1px solid rgba(249,115,22,0.4);border-radius:10px;padding:10px 12px;margin-bottom:12px;font-size:12px;color:#fed7aa;line-height:1.4;">';` +
        `h += '👉 아래 <strong>[⚡ 차례대로 담기]</strong>를 누르시면 식재료가 순서대로 열려 장바구니에 담깁니다!</div>';` +
        `h += '<div style="display:flex;gap:8px;margin-bottom:12px;">';` +
        `h += '<button id="zb-btn-next" style="flex:1;background:linear-gradient(135deg,#f97316,#ea580c);color:#fff;border:none;padding:12px 14px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;box-shadow:0 4px 14px rgba(249,115,22,0.4);">⚡ 1번부터 차례대로 담기 (남은: ' + items.length + '개)</button>';` +
        `h += '<button onclick="location.href=\\'https://cart.coupang.com/cartView.pang\\'" style="background:#10b981;color:#fff;border:none;padding:12px 14px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;white-space:nowrap;">🛍️ 장바구니</button>';` +
        `h += '</div>';` +
        `h += '<div id="zb-list" style="display:flex;flex-direction:column;gap:7px;">';` +
        `items.forEach(function(it, i){` +
        `h += '<div id="zb-item-' + i + '" style="display:flex;justify-content:space-between;align-items:center;background:#1e293b;padding:9px 12px;border-radius:10px;border:1px solid #334155;font-size:12px;">';` +
        `h += '<div style="flex:1;min-width:0;padding-right:8px;"><div style="font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + (i+1) + '. ' + it.name + '</div>';` +
        `h += '<div style="font-size:11px;color:#94a3b8;margin-top:2px;">' + it.spec + ' (' + it.qty + '개) · ' + it.price.toLocaleString() + '원</div></div>';` +
        `h += '<button id="zb-btn-item-' + i + '" style="background:#3b82f6;color:#fff;border:none;padding:6px 12px;border-radius:8px;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap;">담기</button>';` +
        `h += '</div>';` +
        `});` +
        `h += '</div>';` +
        `o.innerHTML = h;` +
        `document.body.appendChild(o);` +
        `function markDone(idx) {` +
        `var row = document.getElementById('zb-item-' + idx);` +
        `var btn = document.getElementById('zb-btn-item-' + idx);` +
        `if (row && btn) {` +
        `row.style.borderColor = 'rgba(16,185,129,0.5)';` +
        `row.style.background = 'rgba(16,185,129,0.1)';` +
        `btn.innerText = '✅ 담김';` +
        `btn.style.background = '#10b981';` +
        `}` +
        `}` +
        `items.forEach(function(it, i){` +
        `var btn = document.getElementById('zb-btn-item-' + i);` +
        `if (btn) {` +
        `btn.onclick = function(){ window.open(it.url, '_blank'); markDone(i); };` +
        `}` +
        `});` +
        `var nextBtn = document.getElementById('zb-btn-next');` +
        `if (nextBtn) {` +
        `nextBtn.onclick = function(){` +
        `while (currIndex < items.length) {` +
        `var btn = document.getElementById('zb-btn-item-' + currIndex);` +
        `if (btn && btn.innerText !== '✅ 담김') {` +
        `window.open(items[currIndex].url, '_blank');` +
        `markDone(currIndex);` +
        `currIndex++;` +
        `var remaining = items.filter(function(_, idx){` +
        `var b = document.getElementById('zb-btn-item-' + idx);` +
        `return b && b.innerText !== '✅ 담김';` +
        `}).length;` +
        `if (remaining > 0) {` +
        `nextBtn.innerText = '⚡ 다음 품목 담기 (남은: ' + remaining + '개)';` +
        `} else {` +
        `nextBtn.innerText = '🎉 ' + items.length + '개 품목 모두 담기 완료!';` +
        `nextBtn.style.background = '#10b981';` +
        `}` +
        `return;` +
        `}` +
        `currIndex++;` +
        `}` +
        `nextBtn.innerText = '🎉 모든 품목 담기 완료!';` +
        `nextBtn.style.background = '#10b981';` +
        `};` +
        `}` +
        `})();`;

      return 'javascript:' + encodeURI(rawScript);
    }

    function copyCurrentWeekBookmarklet(skipOpenModal = false) {
      const weekNum = currentSelectedWeek || 1;
      const code = generateBookmarkletCode(weekNum);
      
      const copySuccess = () => {
        showToast(`📋 ${weekNum}주차 [집밥봇 1초 자동 담기] 코드가 복사되었습니다!`);
        if (!skipOpenModal) {
          openBookmarkletModal();
        }
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(copySuccess).catch(() => {
          fallbackCopyText(code, copySuccess);
        });
      } else {
        fallbackCopyText(code, copySuccess);
      }
    }

    function fallbackCopyText(text, cb) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        cb();
      } catch (e) {
        showToast('⚠️ 복사에 실패했습니다. Safari 주소창 권한을 확인해주세요.');
      }
      document.body.removeChild(ta);
    }
"""

    if 'function generateBookmarkletCode' not in content:
        content = content.replace('window.openThisWeekGroceries = openThisWeekGroceries;', js_to_add + '\n    window.openThisWeekGroceries = openThisWeekGroceries;\n    window.copyCurrentWeekBookmarklet = copyCurrentWeekBookmarklet;\n    window.openBookmarkletModal = openBookmarkletModal;\n    window.closeBookmarkletModal = closeBookmarkletModal;')

    # 5. In selectWeek(weekNum) / renderWeekView(weekNum), update banner text
    # In selectWeek or renderWeekView, let's update banner week button label
    update_banner_code = """
      const bannerWeekText = document.getElementById('bm-banner-week-text');
      if (bannerWeekText) bannerWeekText.innerText = `${weekNum}주차`;
"""
    if 'document.getElementById(\'bm-banner-week-text\')' not in content:
        content = content.replace("currentSelectedWeek = weekNum;", "currentSelectedWeek = weekNum;\n" + update_banner_code)

    # 6. Update Right Groceries panel header button to include bookmarklet button
    # Replace right groceries panel title button
    old_panel_btn = """            <button class="btn-action orange" style="padding: 6px 12px; font-size: 0.8rem;" onclick="openThisWeekGroceries()">
              ⚡ 1주차 품목 한 번에 담기
            </button>"""
    new_panel_btn = """            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <button class="btn-action orange" style="padding: 6px 12px; font-size: 0.8rem;" onclick="copyCurrentWeekBookmarklet()">
                📋 1초 자동담기 코드 복사
              </button>
              <button class="btn-action" style="padding: 6px 12px; font-size: 0.8rem; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #60a5fa;" onclick="openThisWeekGroceries()">
                ⚡ 차례대로 열기
              </button>
            </div>"""
    if old_panel_btn in content:
        content = content.replace(old_panel_btn, new_panel_btn)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path} successfully!")

if __name__ == '__main__':
    update_cart_file('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html', True)
    update_cart_file('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html', False)
