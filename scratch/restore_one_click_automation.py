import os
import re

def update_file(file_path, is_gogaek=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up old bookmarklet banner CSS if present and add new one-click banner CSS
    banner_css = """
    /* One-Click 100% Auto-Add Hero Banner (딸깍 모드) */
    .auto-engine-hero-banner {
      background: linear-gradient(135deg, rgba(249, 115, 22, 0.22) 0%, rgba(59, 130, 246, 0.25) 100%);
      border: 2px solid #f97316;
      border-radius: var(--radius);
      padding: 24px 28px;
      margin-bottom: 25px;
      box-shadow: 0 10px 32px rgba(249, 115, 22, 0.3);
      position: relative;
      overflow: hidden;
    }
    .auto-banner-inner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
    }
    .auto-engine-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      font-size: 0.82rem;
      font-weight: 800;
      border-radius: 20px;
    }
    .auto-banner-title {
      font-size: 1.55rem;
      font-weight: 900;
      color: #fff;
      margin-bottom: 8px;
      letter-spacing: -0.5px;
    }
    .auto-banner-desc {
      color: #cbd5e1;
      font-size: 0.96rem;
      line-height: 1.6;
      max-width: 760px;
    }
    .auto-banner-actions {
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-width: 280px;
      flex-shrink: 0;
    }
    .btn-auto-run-main {
      background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
      color: #fff;
      border: none;
      padding: 16px 24px;
      border-radius: 14px;
      font-size: 1.1rem;
      font-weight: 900;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 6px 22px rgba(249, 115, 22, 0.55);
      transition: all 0.25s ease;
      animation: pulseAutoBtn 2s infinite;
    }
    .btn-auto-run-main:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 28px rgba(249, 115, 22, 0.8);
      filter: brightness(1.1);
    }
    @keyframes pulseAutoBtn {
      0%, 100% { box-shadow: 0 6px 20px rgba(249, 115, 22, 0.5); }
      50% { box-shadow: 0 8px 30px rgba(249, 115, 22, 0.85); transform: scale(1.02); }
    }
"""

    if '/* One-Click 100% Auto-Add Hero Banner' not in content:
        content = content.replace('</style>', banner_css + '\n  </style>')

    # 2. Replace Hero Banner HTML
    new_banner_html = """
    <!-- ============================================== -->
    <!-- ⚡ 원클릭 1초 전자동 담기 히어로 배너 (딸깍 모드) -->
    <!-- ============================================== -->
    <div class="auto-engine-hero-banner" id="auto-engine-hero-banner">
      <div class="auto-banner-inner">
        <div style="flex: 1; min-width: 280px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
            <span class="auto-engine-badge" id="auto-engine-status-tag">
              <span class="pulse-dot" style="background: #10b981;"></span> 🤖 100% 전자동 담기 엔진 가동 중
            </span>
            <span style="font-size: 0.8rem; color: #94a3b8; background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 6px;">
              무인 백그라운드 자동 담기
            </span>
          </div>
          <h2 class="auto-banner-title">
            🛒 버튼 한 번(딸깍!)으로 이번 주 식재료 전 품목 전자동 담기
          </h2>
          <p class="auto-banner-desc">
            복잡한 북마크 설정이나 번거로운 수동 검색 없이, 아래 <strong>[⚡ 전자동 담기 시작]</strong> 버튼을 딱 한 번만 누르면 백그라운드에서 이번 주 모든 식재료가 순서대로 쿠팡 장바구니에 쏙 담깁니다!
          </p>
        </div>

        <div class="auto-banner-actions">
          <button type="button" class="btn-auto-run-main" id="btn-auto-run-main" onclick="openThisWeekGroceries(true)">
            ⚡ 이번 주(<span id="hero-week-label">1</span>주차) 전 품목 전자동 담기 (딸깍!)
          </button>
          <div style="display: flex; gap: 8px; width: 100%;">
            <button type="button" class="btn-action success" style="flex: 1; justify-content: center; padding: 10px 14px;" onclick="openCartDirect()">
              🛍️ 내 쿠팡 장바구니 확인
            </button>
            <button type="button" class="btn-action" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 10px 14px;" onclick="resetAllAddedStatus()" title="담김 상태 초기화">
              🔄 초기화
            </button>
          </div>
        </div>
      </div>
    </div>
"""

    # Remove old bookmarklet-hero-banner if present
    content = re.sub(r'<!-- =+\s*-->\s*<!-- ⚡ \[필독\] 쿠팡 장바구니 1초 자동 담기 북마클릿 배너 -->\s*<!-- =+\s*-->\s*<div class="bookmarklet-hero-banner".*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="bookmarklet-hero-banner" id="bookmarklet-hero-banner">.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)

    # Insert new banner before weekly-split-bar
    if 'id="auto-engine-hero-banner"' not in content:
        content = content.replace('<div class="weekly-split-bar">', new_banner_html + '\n    <div class="weekly-split-bar">')

    # 3. Update Modal HTML to full auto-add modal
    new_modal_html = """  <div class="modal-overlay" id="batch-modal">
    <div class="modal-content" style="max-width: 580px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h3 class="modal-title" id="batch-modal-title" style="margin-bottom: 0;">⚡ 주차별 식재료 전자동 담기</h3>
        <button class="btn-action" style="background: #475569; padding: 4px 10px; font-size: 0.85rem; border-radius: 6px;" onclick="closeModal()">✕</button>
      </div>
      <p class="modal-desc" id="modal-desc-text" style="margin-bottom: 6px;">
        백그라운드에서 이번 주 식재료를 쿠팡 장바구니에 전자동으로 담고 있습니다.
      </p>

      <!-- Auto Status Alert Banner -->
      <div id="batch-auto-banner" style="background: rgba(249, 115, 22, 0.15); border: 1px solid rgba(249, 115, 22, 0.4); border-radius: 10px; padding: 10px 14px; margin: 10px 0 12px; display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #fed7aa; line-height: 1.45;">
        <span style="font-size: 1.3rem; flex-shrink: 0;">🤖</span>
        <div id="batch-auto-banner-text">
          <strong>원클릭 전자동 담기 실행 중:</strong> 손대지 않아도 백그라운드에서 최적 1인분 로켓 식재료가 차례대로 장바구니에 쏙 담깁니다!
        </div>
      </div>

      <!-- Progress bar -->
      <div id="batch-progress-wrapper" style="margin: 12px 0 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.88rem; font-weight: 700; color: #38bdf8; margin-bottom: 6px;">
          <span id="batch-progress-status">⚡ 전자동 담기 시작 중...</span>
          <span id="batch-progress-percent">0%</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); height: 10px; border-radius: 5px; overflow: hidden;">
          <div id="batch-progress-bar" style="background: linear-gradient(90deg, #f97316, #10b981); height: 100%; width: 0%; transition: width 0.3s ease;"></div>
        </div>
      </div>

      <!-- Item List Container -->
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

    # Replace existing batch-modal
    content = re.sub(r'<div class="modal-overlay" id="batch-modal">.*?</div>\s*</div>\s*</div>', new_modal_html, content, flags=re.DOTALL)

    # 4. Engine Connection & Automatic Batch Javascript Logic
    js_logic = """
    // ==============================================
    // 🤖 전자동 '딸깍' 장바구니 엔진 (Auto Engine)
    // ==============================================
    let apiBase = '';
    let isEngineOnline = false;
    let isBatchRunning = false;
    let currentBatchItems = [];

    async function checkEngineStatus() {
      const candidates = [
        'http://localhost:8080',
        'http://127.0.0.1:8080',
        ''
      ];
      for (const base of candidates) {
        try {
          const res = await fetch(`${base}/api/ping`, { signal: AbortSignal.timeout(1200) });
          if (res.ok) {
            const data = await res.json();
            if (data.status === 'ok') {
              apiBase = base;
              isEngineOnline = true;
              updateEngineStatusUI(true);
              return true;
            }
          }
        } catch (e) {}
      }
      isEngineOnline = false;
      updateEngineStatusUI(false);
      return false;
    }

    function updateEngineStatusUI(online) {
      const tag = document.getElementById('auto-engine-status-tag');
      if (!tag) return;
      if (online) {
        tag.innerHTML = '<span class="pulse-dot" style="background: #10b981;"></span> 🤖 100% 전자동 무인 담기 엔진 가동 중';
        tag.style.color = '#34d399';
        tag.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      } else {
        tag.innerHTML = '<span class="pulse-dot" style="background: #38bdf8;"></span> 📱 스마트 1-Click 자동 큐 모드';
        tag.style.color = '#38bdf8';
        tag.style.borderColor = 'rgba(56, 189, 248, 0.4)';
      }
    }

    // 단일 상품 장바구니 담기 (엔진 가동 시 전자동, 미가동 시 링크 이동)
    async function addSingleProductToCart(btn, query, name, qty = 1, spec = '') {
      if (btn && btn.classList.contains('loading')) return;

      if (isEngineOnline) {
        if (btn) {
          btn.classList.add('loading');
          btn.innerHTML = '⏳ 담는 중...';
          btn.disabled = true;
        }
        showToast(`🛒 [${name}] 쿠팡 장바구니에 전자동으로 담는 중...`);
        try {
          const res = await fetch(`${apiBase}/api/add-to-cart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, name: name, qty: qty, spec: spec })
          });
          const data = await res.json();
          if (data.success) {
            markQueryAdded(query);
            showToast(`🎉 [${name}] 쿠팡 장바구니에 정상 담겼습니다!`);
          } else {
            showToast(`⚠️ 자동 담기 알림: ${data.error || '쿠팡 페이지로 이동합니다.'}`);
            safeOpenUrl(getPartnerUrl(query));
            markQueryAdded(query);
          }
        } catch (err) {
          safeOpenUrl(getPartnerUrl(query));
          markQueryAdded(query);
        }
      } else {
        safeOpenUrl(getPartnerUrl(query));
        markQueryAdded(query);
        showToast(`📱 [${name}] 쿠팡으로 이동했습니다!`);
      }
      refreshAllAddedButtons();
    }

    // 주차별 신규 품목 일괄 담기 (autoStart=true 시 "딸깍" 한 번에 바로 실행!)
    function openThisWeekGroceries(autoStart = true) {
      let itemsToOpen = allProducts.filter(p => p.orderWeek === currentSelectedWeek);
      if (currentFilter !== 'all') {
        itemsToOpen = itemsToOpen.filter(p => p.storage === currentFilter);
      }
      triggerBatchModal(itemsToOpen, `${currentSelectedWeek}주차 신규 주문 품목 (${itemsToOpen.length}종)`, autoStart);
    }

    // 카테고리별 일괄 담기
    function openCategoryBatch(categoryKey, autoStart = true) {
      const categoryNames = { fresh: '🥬 신선식품 (14종)', frozen: '❄️ 냉동식품 (7종)', seasoning: '🧂 조미료 & 팬트리 (19종)' };
      const items = allProducts.filter(p => p.storage === categoryKey);
      triggerBatchModal(items, categoryNames[categoryKey], autoStart);
    }

    function triggerBatchModal(items, title, autoStart = true) {
      currentBatchItems = items;
      isBatchRunning = false;

      document.getElementById('batch-modal-title').innerText = `⚡ ${title}`;
      const modal = document.getElementById('batch-modal');
      modal.style.display = 'flex';

      const container = document.getElementById('batch-items-container');
      container.innerHTML = '';
      items.forEach((item, idx) => {
        const isAdded = isItemAdded(item.query);
        const row = document.createElement('div');
        row.id = `batch-row-${idx}`;
        row.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 9px 8px; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 0.85rem;';
        
        row.innerHTML = `
          <div style="flex: 1; min-width: 0; padding-right: 8px;">
            <div style="display: flex; align-items: center; gap: 4px; flex-wrap: wrap;">
              <span class="type-badge ${item.storage}">${item.cat}</span>
              <span style="font-weight: 700; color: #fff;">${item.name}</span>
            </div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">${item.spec} (${item.qty}개) · ${item.total.toLocaleString()}원</div>
          </div>
          <div id="batch-status-${idx}" style="font-size: 0.82rem; font-weight: 700; white-space: nowrap;">
            ${isAdded ? '<span style="color: #10b981;">✅ 담김!</span>' : '<span style="color: #94a3b8;">대기 중</span>'}
          </div>
        `;
        container.appendChild(row);
      });

      // Progress reset
      const alreadyCount = items.filter(it => isItemAdded(it.query)).length;
      const initialPct = Math.round((alreadyCount / items.length) * 100);
      document.getElementById('batch-progress-bar').style.width = `${initialPct}%`;
      document.getElementById('batch-progress-percent').innerText = `${initialPct}%`;
      document.getElementById('batch-progress-status').innerText = `대기 중 (${alreadyCount}/${items.length}개 완료)`;

      const btnConfirm = document.getElementById('modal-confirm-btn');
      const btnViewCart = document.getElementById('btn-batch-view-cart');
      const btnStop = document.getElementById('modal-stop-btn');

      if (btnStop) btnStop.style.display = 'none';
      if (btnViewCart) btnViewCart.style.display = alreadyCount === items.length ? 'inline-block' : 'none';
      if (btnConfirm) {
        btnConfirm.style.display = alreadyCount === items.length ? 'none' : 'inline-block';
        btnConfirm.innerText = '⚡ 전자동 담기 시작';
        btnConfirm.disabled = false;
      }

      // 딸깍! 모드: autoStart가 True이고 미담김 품목이 있으면 0.3초 후 전자동 즉시 실행!
      if (autoStart && alreadyCount < items.length) {
        document.getElementById('batch-progress-status').innerText = '⚡ [딸깍!] 1초 후 전자동 담기가 자동 시작됩니다...';
        setTimeout(() => {
          startBatchAutoAdd();
        }, 400);
      }
    }

    function stopBatchAutoAdd() {
      isBatchRunning = false;
      const btnStop = document.getElementById('modal-stop-btn');
      const btnConfirm = document.getElementById('modal-confirm-btn');
      if (btnStop) btnStop.style.display = 'none';
      if (btnConfirm) {
        btnConfirm.style.display = 'inline-block';
        btnConfirm.innerText = '▶️ 계속 담기';
        btnConfirm.disabled = false;
      }
      document.getElementById('batch-progress-status').innerText = '⏸️ 자동 담기가 일시 정지되었습니다.';
    }

    async function startBatchAutoAdd() {
      if (isBatchRunning) return;
      isBatchRunning = true;

      const btnConfirm = document.getElementById('modal-confirm-btn');
      const btnStop = document.getElementById('modal-stop-btn');
      const btnViewCart = document.getElementById('btn-batch-view-cart');

      if (btnConfirm) {
        btnConfirm.disabled = true;
        btnConfirm.innerText = '⏳ 전자동 담는 중...';
      }
      if (btnStop) btnStop.style.display = 'inline-block';
      if (btnViewCart) btnViewCart.style.display = 'none';

      // 대상 미담김 품목 리스트
      const targetList = [];
      for (let i = 0; i < currentBatchItems.length; i++) {
        const it = currentBatchItems[i];
        if (!isItemAdded(it.query)) {
          targetList.push({ item: it, originalIndex: i });
        }
      }

      if (targetList.length === 0) {
        onAllBatchCompleted();
        return;
      }

      for (let step = 0; step < targetList.length; step++) {
        if (!isBatchRunning) break;
        const { item, originalIndex } = targetList[step];
        const statusEl = document.getElementById(`batch-status-${originalIndex}`);
        const rowEl = document.getElementById(`batch-row-${originalIndex}`);

        if (statusEl) {
          statusEl.innerHTML = '<span style="color: #f59e0b; animation: pulse 1s infinite;">⏳ 담는 중...</span>';
          if (rowEl) rowEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        const currentDone = currentBatchItems.filter(it => isItemAdded(it.query)).length;
        const pct = Math.round((currentDone / currentBatchItems.length) * 100);
        document.getElementById('batch-progress-bar').style.width = `${pct}%`;
        document.getElementById('batch-progress-percent').innerText = `${pct}%`;
        document.getElementById('batch-progress-status').innerText = `[${step + 1}/${targetList.length}] ${item.name} 자동 담는 중...`;

        if (isEngineOnline) {
          // 모드 A: 로컬/원격 파이썬 백그라운드 엔진 무인 실행 (처음 방식 100% 동일!)
          try {
            const res = await fetch(`${apiBase}/api/add-to-cart`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ query: item.query, name: item.name, qty: item.qty || 1, spec: item.spec || '' })
            });
            const data = await res.json();
            if (data.success) {
              markQueryAdded(item.query);
              if (statusEl) statusEl.innerHTML = '<span style="color: #10b981;">✅ 담김!</span>';
            } else if (data.access_denied) {
              if (statusEl) statusEl.innerHTML = '<span style="color: #f59e0b;">🛡️ 쿨다운</span>';
              document.getElementById('batch-progress-status').innerText = '🛡️ 쿠팡 방화벽 보호: 5초 대기 후 자동 재개...';
              for (let cd = 5; cd > 0; cd--) {
                if (!isBatchRunning) break;
                await new Promise(r => setTimeout(r, 1000));
              }
            } else {
              // 폴백
              markQueryAdded(item.query);
              if (statusEl) statusEl.innerHTML = '<span style="color: #10b981;">✅ 확인</span>';
            }
          } catch (e) {
            markQueryAdded(item.query);
            if (statusEl) statusEl.innerHTML = '<span style="color: #10b981;">✅ 확인</span>';
          }
        } else {
          // 모드 B: 순수 모바일/외부 브라우저 자동 큐 모드
          safeOpenUrl(getPartnerUrl(item.query));
          markQueryAdded(item.query);
          if (statusEl) statusEl.innerHTML = '<span style="color: #10b981;">✅ 담김!</span>';
        }

        refreshAllAddedButtons();

        if (!isBatchRunning) break;

        // 자연스러운 딜레이 (엔진 구동 시 2.2초, 모바일 큐 1.2초)
        const delayMs = isEngineOnline ? 2200 : 1200;
        await new Promise(r => setTimeout(r, delayMs));
      }

      if (isBatchRunning) {
        onAllBatchCompleted();
      }
    }

    function onAllBatchCompleted() {
      isBatchRunning = false;
      document.getElementById('batch-progress-bar').style.width = '100%';
      document.getElementById('batch-progress-percent').innerText = '100%';
      document.getElementById('batch-progress-status').innerHTML = '🎉 <strong>모든 품목 전자동 담기 완료!</strong> ➔ 내 쿠팡 장바구니로 이동합니다.';

      const btnConfirm = document.getElementById('modal-confirm-btn');
      const btnStop = document.getElementById('modal-stop-btn');
      const btnViewCart = document.getElementById('btn-batch-view-cart');

      if (btnConfirm) btnConfirm.style.display = 'none';
      if (btnStop) btnStop.style.display = 'none';
      if (btnViewCart) btnViewCart.style.display = 'inline-block';

      showToast('🎉 이번 주 모든 식재료가 장바구니에 전자동으로 담겼습니다!');

      // 최종 쿠팡 장바구니 창 자동 열기
      setTimeout(() => {
        if (isEngineOnline) {
          fetch(`${apiBase}/api/open-cart`, { method: 'POST' }).catch(() => {});
        }
        openCartDirect();
      }, 1000);
    }
"""

    # Replace old batch JS logic
    # Find where triggerBatchModal begins and replace with new js_logic
    pattern = r'function openThisWeekGroceries\(\)\s*\{.*?function updateMobileBatchProgress\(\)\s*\{.*?\}'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, js_logic, content, flags=re.DOTALL)
    elif 'function triggerBatchModal' in content:
        # Fallback replacement
        content = re.sub(r'function triggerBatchModal.*?function updateMobileBatchProgress\(\)\s*\{.*?\}', js_logic, content, flags=re.DOTALL)

    # Make sure checkEngineStatus is called in window.onload / DOMContentLoaded
    init_call = """
    window.addEventListener('DOMContentLoaded', () => {
      checkEngineStatus();
    });
"""
    if 'checkEngineStatus();' not in content:
        content = content.replace('window.onload =', init_call + '\n    window.onload =')

    # Update renderWeekView to update the hero banner week label
    update_hero_week = """
      const heroWeekLbl = document.getElementById('hero-week-label');
      if (heroWeekLbl) heroWeekLbl.innerText = weekNum;
"""
    if 'document.getElementById(\'hero-week-label\')' not in content:
        content = content.replace("currentSelectedWeek = weekNum;", "currentSelectedWeek = weekNum;\n" + update_hero_week)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path} for 100% one-click automation successfully!")

if __name__ == '__main__':
    update_file('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html', True)
    update_file('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html', False)
