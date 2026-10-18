import re

def restore_photo_engine(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Exact Modal HTML matching the user photo
    exact_modal_html = """  <!-- Batch Modal (100% 원클릭 무간섭 백그라운드 자동 담기) -->
  <div class="modal-overlay" id="batch-modal">
    <div class="modal-content" style="max-width: 560px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h3 class="modal-title" id="batch-modal-title" style="margin-bottom: 0;">⚡ 1주차 신규 주문 품목 자동 담기</h3>
        <button class="btn-action danger" id="modal-header-stop-btn" style="display: none; padding: 5px 12px; font-size: 0.8rem;" onclick="stopBatchAutoAdd()">⏹ 담기 중단</button>
      </div>
      <p class="modal-desc" id="modal-desc-text" style="margin-bottom: 6px;">
        총 20개의 식재료를 백그라운드 크롬 창에서 로켓배송 최적 상품으로 자동 탐색하여 담습니다.
      </p>

      <!-- Background Silent Mode Info Banner (from photo) -->
      <div id="batch-bg-banner" style="background: rgba(14, 165, 233, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 9px; padding: 12px 14px; margin: 12px 0 10px; display: flex; align-items: center; gap: 10px; font-size: 0.84rem; color: #bae6fd; line-height: 1.5;">
        <span style="font-size: 1.3rem; flex-shrink: 0;">📣</span>
        <div>
          <strong style="color: #38bdf8;">무간섭 백그라운드 담기 지원:</strong><br>
          담는 동안 화면을 가리거나 창이 깜빡이지 않으며, <strong>모든 품목을 다 담았을 때 쿠팡 장바구니 창이 자동으로 전면에 팝업</strong>됩니다!
        </div>
      </div>

      <!-- Progress bar (from photo) -->
      <div id="batch-progress-wrapper" style="margin: 14px 0 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 700; color: #38bdf8; margin-bottom: 6px;">
          <span id="batch-progress-status">진행 준비 중...</span>
          <span id="batch-progress-percent">0%</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); height: 10px; border-radius: 5px; overflow: hidden;">
          <div id="batch-progress-bar" style="background: linear-gradient(90deg, #06b6d4, #10b981); height: 100%; width: 0%; transition: width 0.3s ease;"></div>
        </div>
      </div>

      <!-- Item List Container (from photo) -->
      <div id="batch-items-container" style="max-height: 270px; overflow-y: auto; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
        <!-- Injected via JS -->
      </div>

      <div class="modal-actions" style="justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: center;">
          <button type="button" class="btn-action" style="background: #475569;" onclick="closeModal()">닫기</button>
          <button type="button" class="btn-action" style="background: rgba(239, 68, 68, 0.18); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); font-size: 0.85rem;" onclick="resetAllAddedStatus(true)" title="모든 상품의 담김 상태를 초기화하여 처음부터 다시 담기">🔄 담기 버튼 초기화</button>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button type="button" class="btn-action danger" id="modal-stop-btn" style="display: none;" onclick="stopBatchAutoAdd()">⏹ 담기 중단하기</button>
          <button type="button" class="btn-action success" id="btn-batch-view-cart" style="display: none;" onclick="openCartDirect()">🛍️ 내 쿠팡 장바구니 확인</button>
          <button type="button" class="btn-action orange" id="modal-confirm-btn" onclick="startBatchAutoAdd(false)">🚀 자동 담기 시작</button>
        </div>
      </div>
      <div style="text-align: center; margin-top: 10px;">
        <a href="javascript:void(0)" onclick="startBatchOpenManual()" style="font-size: 0.78rem; color: #64748b; text-decoration: underline;">
          (만약 직접 쿠팡 검색창 새 탭들을 열고 싶으신 경우 클릭)
        </a>
      </div>
    </div>
  </div>"""

    # Replace existing batch modal
    content = re.sub(r'<div class="modal-overlay" id="batch-modal">.*?</div>\s*</div>\s*</div>', exact_modal_html, content, flags=re.DOTALL)

    # 2. Exact JS logic for photo
    exact_js_logic = """
    // ==============================================
    // 🤖 100% 무간섭 백그라운드 자동 담기 엔진 (사진 원본 복원)
    // ==============================================
    let isBatchRunning = false;

    // 단일 상품 장바구니 담기 (무간섭 백그라운드 API)
    async function addSingleProductToCart(btn, query, name, qty = 1, spec = '') {
      if (btn && btn.classList.contains('loading')) return;

      if (btn) {
        btn.classList.add('loading');
        btn.innerHTML = '⏳ 담는 중...';
        btn.disabled = true;
      }
      showToast(`🛒 [${name}] 백그라운드에서 쿠팡 장바구니에 담는 중...`);

      try {
        const res = await fetch('/api/add-to-cart', {
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
        }
      } catch (err) {
        showToast(`⚠️ 서버 응답 오류. 백그라운드 엔진(server.py) 실행 여부를 확인해주세요.`);
      }
      refreshAllAddedButtons();
    }

    // 주차별 신규 품목 일괄 담기 (autoStart=true 시 "딸깍" 한 번에 바로 실행!)
    function openThisWeekGroceries(autoStart = true) {
      let itemsToOpen = allProducts.filter(p => p.orderWeek === currentSelectedWeek);
      if (currentFilter !== 'all') {
        itemsToOpen = itemsToOpen.filter(p => p.storage === currentFilter);
      }
      triggerBatchModal(itemsToOpen, `${currentSelectedWeek}주차 신규 주문 품목`, autoStart);
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

      const alreadyAdded = items.filter(it => isItemAdded(it.query));
      const pendingItems = items.filter(it => !isItemAdded(it.query));

      document.getElementById('batch-modal-title').innerText = `⚡ ${title} (${items.length}종) 자동 담기`;
      let descHtml = `총 <strong>${items.length}개</strong>의 식재료를 백그라운드 크롬 창에서 로켓배송 최적 상품으로 자동 탐색하여 담습니다.<br>`;
      if (alreadyAdded.length > 0) {
        descHtml += `<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-top: 8px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 8px 12px;">
          <span style="color: #34d399; font-weight: 700; font-size: 0.86rem;">
            💡 현재 <strong>${alreadyAdded.length}개 품목</strong>이 이미 장바구니에 담겨 있습니다. (남은 품목: <strong>${pendingItems.length}개</strong>)
          </span>
          <button type="button" onclick="resetAllAddedStatus(true)" style="background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.45); color: #f87171; border-radius: 6px; font-size: 0.78rem; font-weight: 700; padding: 4px 10px; cursor: pointer;" title="처음부터 모든 품목을 다시 담기 위해 담김 상태 리셋">
            🔄 담기 버튼 초기화
          </button>
        </div>`;
      }
      document.getElementById('modal-desc-text').innerHTML = descHtml;

      const progressWrapper = document.getElementById('batch-progress-wrapper');
      progressWrapper.style.display = 'block';

      const alreadyCount = alreadyAdded.length;
      const initialPct = Math.round((alreadyCount / items.length) * 100);
      document.getElementById('batch-progress-bar').style.width = `${initialPct}%`;
      document.getElementById('batch-progress-percent').innerText = `${initialPct}%`;
      document.getElementById('batch-progress-status').innerText = `진행 준비 중... (${alreadyCount}/${items.length}개 완료)`;

      const btnStop = document.getElementById('modal-stop-btn');
      const btnHeaderStop = document.getElementById('modal-header-stop-btn');
      if (btnStop) btnStop.style.display = 'none';
      if (btnHeaderStop) btnHeaderStop.style.display = 'none';

      const btnConfirm = document.getElementById('modal-confirm-btn');
      const btnViewCart = document.getElementById('btn-batch-view-cart');
      btnViewCart.style.display = 'none';

      if (pendingItems.length === 0) {
        btnConfirm.style.display = 'none';
        btnViewCart.style.display = 'inline-block';
        document.getElementById('batch-progress-status').innerText = '🎉 모든 품목이 이미 담겨 있습니다!';
      } else {
        btnConfirm.style.display = 'inline-block';
        btnConfirm.disabled = false;
        btnConfirm.className = 'btn-action orange';
        btnConfirm.innerText = alreadyAdded.length > 0 ? `🚀 남은 ${pendingItems.length}개만 담기` : `🚀 자동 담기 시작 (${items.length}개)`;
      }

      // Render Item rows (Exact style from photo)
      const container = document.getElementById('batch-items-container');
      container.innerHTML = '';
      items.forEach((item, idx) => {
        const isAdded = isItemAdded(item.query);
        const row = document.createElement('div');
        row.id = `batch-row-${idx}`;
        row.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 0.85rem;';
        
        row.innerHTML = `
          <div style="flex: 1; min-width: 0; padding-right: 8px;">
            <span class="type-badge ${item.storage}" style="margin-right: 6px;">${item.cat}</span>
            <span style="font-weight: 700; color: #fff;">${item.name}</span>
            <span style="font-size: 0.78rem; color: #94a3b8; margin-left: 4px;">(${item.spec})</span>
          </div>
          <div id="batch-status-${idx}" style="font-weight: 700; color: ${isAdded ? '#10b981' : '#64748b'}; font-size: 0.8rem; white-space: nowrap;">
            ${isAdded ? '✅ 담김!' : '대기 중'}
          </div>
        `;
        container.appendChild(row);
      });

      document.getElementById('batch-modal').style.display = 'flex';

      // "딸깍!" 모드: autoStart가 true이고 담을 품목이 남아있으면 0.35초 후 바로 자동 담기 시작!
      if (autoStart && pendingItems.length > 0) {
        setTimeout(() => {
          startBatchAutoAdd(true);
        }, 350);
      }
    }

    async function startBatchAutoAdd(onlyPending = true) {
      if (isBatchRunning) return;
      isBatchRunning = true;

      const btnConfirm = document.getElementById('modal-confirm-btn');
      btnConfirm.disabled = true;
      btnConfirm.innerText = '⏳ 자동 담는 중...';

      const btnStop = document.getElementById('modal-stop-btn');
      const btnHeaderStop = document.getElementById('modal-header-stop-btn');
      if (btnStop) btnStop.style.display = 'inline-flex';
      if (btnHeaderStop) btnHeaderStop.style.display = 'inline-block';

      document.getElementById('batch-progress-wrapper').style.display = 'block';

      // 대상 품목 선정
      const targetList = [];
      for (let i = 0; i < currentBatchItems.length; i++) {
        const it = currentBatchItems[i];
        if (onlyPending && isItemAdded(it.query)) {
          const statusEl = document.getElementById(`batch-status-${i}`);
          if (statusEl) statusEl.innerHTML = '<span style="color: #10b981;">✅ 보존됨</span>';
          continue;
        }
        targetList.push({ item: it, originalIndex: i });
      }

      if (targetList.length === 0) {
        if (btnStop) btnStop.style.display = 'none';
        if (btnHeaderStop) btnHeaderStop.style.display = 'none';
        document.getElementById('batch-progress-bar').style.width = '100%';
        document.getElementById('batch-progress-percent').innerText = '100%';
        document.getElementById('batch-progress-status').innerHTML = '🎉 모든 품목이 이미 담겨 있습니다! ➔ <span style="color: #38bdf8;">장바구니 창을 엽니다.</span>';
        btnConfirm.style.display = 'none';
        document.getElementById('btn-batch-view-cart').style.display = 'inline-block';
        showToast('🎉 모든 식재료가 이미 장바구니에 담겨 있어 장바구니 창을 엽니다!');
        isBatchRunning = false;
        try {
          await fetch('/api/open-cart', { method: 'POST' });
        } catch (e) {}
        return;
      }

      let successCount = 0;
      for (let step = 0; step < targetList.length; step++) {
        if (!isBatchRunning) break;
        const { item, originalIndex } = targetList[step];
        const statusEl = document.getElementById(`batch-status-${originalIndex}`);
        const rowEl = document.getElementById(`batch-row-${originalIndex}`);

        if (statusEl) {
          statusEl.innerHTML = '<span style="color: #f59e0b;">⏳ 담는 중...</span>';
          if (rowEl) rowEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        const pct = Math.round(((step) / targetList.length) * 100);
        document.getElementById('batch-progress-bar').style.width = `${pct}%`;
        document.getElementById('batch-progress-percent').innerText = `${pct}%`;
        document.getElementById('batch-progress-status').innerText = `[${step + 1}/${targetList.length}] ${item.name} 담는 중... (백그라운드)`;

        try {
          const res = await fetch('/api/add-to-cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: item.query, name: item.name, qty: item.qty || 1, spec: item.spec || '' })
          });
          const data = await res.json();
          if (data.success) {
            successCount++;
            markQueryAdded(item.query);
            if (statusEl) statusEl.innerHTML = '<span style="color: #10b981;">✅ 담김!</span>';
          } else if (data.access_denied) {
            if (statusEl) statusEl.innerHTML = '<span style="color: #f59e0b;">🛡️ 쿨다운 중</span>';
            document.getElementById('batch-progress-status').innerText = '🛡️ 쿠팡 방화벽 보호 작동: 5초 쿨다운 중...';
            for (let cd = 5; cd > 0; cd--) {
              if (!isBatchRunning) break;
              await new Promise(r => setTimeout(r, 1000));
            }
          } else {
            if (statusEl) statusEl.innerHTML = '<span style="color: #ef4444;">⚠️ 실패</span>';
          }
        } catch (e) {
          if (statusEl) statusEl.innerHTML = '<span style="color: #ef4444;">⚠️ 오류</span>';
        }

        refreshAllAddedButtons();
        if (!isBatchRunning) break;

        // [쿠팡 방화벽 Akamai 봇 차단 방지] 각 상품 사이에 2초 인간 모사 지연 시간 부여 (사진 원본 그대로)
        if (step < targetList.length - 1 && isBatchRunning) {
          const nextItemName = targetList[step + 1].item.name;
          for (let sec = 2; sec > 0; sec--) {
            if (!isBatchRunning) break;
            document.getElementById('batch-progress-status').innerText = `🛡️ [쿠팡 방화벽 보호] 다음 품목(${nextItemName}) 준비 중 (${sec}초)...`;
            await new Promise(r => setTimeout(r, 1000));
          }
        }
      }

      if (!isBatchRunning) {
        if (btnStop) btnStop.style.display = 'none';
        if (btnHeaderStop) btnHeaderStop.style.display = 'none';
        const remainingCount = targetList.filter(t => !isItemAdded(t.item.query)).length;
        document.getElementById('batch-progress-status').innerHTML =
          `<span style="color: #f87171; font-weight: 700;">⏹️ 담기 중단됨: ${successCount}개 담김 완료 (${remainingCount}개 대기 중)</span>`;
        btnConfirm.style.display = 'inline-block';
        btnConfirm.disabled = false;
        btnConfirm.innerHTML = `▶️ 남은 ${remainingCount}개 이어서 담기`;
        btnConfirm.onclick = () => startBatchAutoAdd(true);
        return;
      }

      // 100% 완료 시!
      isBatchRunning = false;
      if (btnStop) btnStop.style.display = 'none';
      if (btnHeaderStop) btnHeaderStop.style.display = 'none';
      btnConfirm.style.display = 'none';

      document.getElementById('batch-progress-bar').style.width = '100%';
      document.getElementById('batch-progress-percent').innerText = '100%';
      document.getElementById('batch-progress-status').innerHTML = '🎉 <strong>모든 품목 담기 완료!</strong> ➔ <span style="color: #38bdf8;">쿠팡 장바구니 창을 엽니다.</span>';

      const btnViewCart = document.getElementById('btn-batch-view-cart');
      if (btnViewCart) btnViewCart.style.display = 'inline-block';

      showToast(`🎉 모든 식재료(${successCount}개)가 쿠팡 장바구니에 담겼습니다! 장바구니 창을 엽니다.`);

      // 다 담았을 때 쿠팡 장바구니 창 자동 팝업!
      try {
        await fetch('/api/open-cart', { method: 'POST' });
      } catch (e) {
        openCartDirect();
      }
    }

    function stopBatchAutoAdd() {
      isBatchRunning = false;
      const btnStop = document.getElementById('modal-stop-btn');
      const btnHeaderStop = document.getElementById('modal-header-stop-btn');
      if (btnStop) btnStop.style.display = 'none';
      if (btnHeaderStop) btnHeaderStop.style.display = 'none';
      showToast('⏹️ 자동 담기를 일시 중단했습니다.');
    }

    function startBatchOpenManual() {
      if (!currentBatchItems || currentBatchItems.length === 0) return;
      if (confirm('각 식재료의 쿠팡 검색 새 탭을 직접 여시겠습니까?')) {
        currentBatchItems.forEach((it, idx) => {
          setTimeout(() => {
            window.open(getPartnerUrl(it.query), '_blank');
          }, idx * 400);
        });
      }
    }
"""

    # Replace the JS logic starting from `// 🤖 전자동 '딸깍' 장바구니 엔진` to `function refreshAllAddedButtons`
    pattern_js = r'// =+\s*// 🤖 전자동 \'딸깍\' 장바구니 엔진 \(Auto Engine\)[\s\S]*?function refreshAllAddedButtons\(\)'
    if re.search(pattern_js, content):
        content = re.sub(pattern_js, exact_js_logic + '\n\n    function refreshAllAddedButtons()', content)
        print(f"Replaced JS logic in {file_path}")
    else:
        print(f"WARNING: pattern_js not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Restored photo engine for {file_path}")

if __name__ == '__main__':
    restore_photo_engine('/Users/bohwanlee/Desktop/antigravity 폴더/cart_dashboard.html')
    restore_photo_engine('/Users/bohwanlee/Desktop/antigravity 폴더/gogaek_cart.html')
