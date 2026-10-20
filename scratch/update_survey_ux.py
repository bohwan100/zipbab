import os

SURVEY_PATH = "/Users/bohwanlee/Desktop/antigravity 폴더/survey.html"

with open(SURVEY_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add id="btn-copy-link" to copy button
old_button = '<button type="button" onclick="copyUnifiedUrl()"'
new_button = '<button id="btn-copy-link" type="button" onclick="copyUnifiedUrl()"'
if old_button in content:
    content = content.replace(old_button, new_button, 1)

# 2. Replace the LAST <script> block
last_script_idx = content.rfind('<script>')
last_script_end_idx = content.rfind('</script>') + len('</script>')

if last_script_idx != -1 and last_script_end_idx != -1:
    new_script = """<script>
    let loadingInterval = null;

    async function handleFormSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('btn-submit');
      btn.disabled = true;

      // 단계별 친절한 로딩 안내 (Render 슬립 모드 대비)
      const loadingStages = [
        '⚙️ 107종 레시피 분석 및 고객 목표 매칭 중...',
        '🛒 쿠팡 4주 분할 최저가 장바구니 계산 중...',
        '🏠 보유 양념 0원 자동 공제 적용 중...',
        '❄️ 식재료 보관법 및 맞춤 웹사이트 빌드 중...',
        '🚀 클라우드 데이터 동기화 중... 거의 다 됐어요!'
      ];
      let stageIdx = 0;
      btn.innerHTML = `<span>${loadingStages[0]}</span>`;
      loadingInterval = setInterval(() => {
        stageIdx = (stageIdx + 1) % loadingStages.length;
        btn.innerHTML = `<span>${loadingStages[stageIdx]}</span>`;
      }, 3500);

      const name = document.getElementById('client_name').value.trim() || '고객님';
      const age = document.getElementById('client_age').value.trim() || '30대';
      const household = document.querySelector('input[name="household"]')?.value || '1명';
      
      let rawBudget = (document.getElementById('budget')?.value || '300000').replace(/,/g, '').trim();
      let budget = 300000;
      if (rawBudget.includes('만')) {
        const numPart = parseFloat(rawBudget.replace(/[^0-9.]/g, '')) || 30;
        budget = Math.round(numPart * 10000);
      } else {
        const parsedNum = parseInt(rawBudget.replace(/[^0-9]/g, ''), 10);
        if (!isNaN(parsedNum)) {
          if (parsedNum >= 5 && parsedNum <= 200) {
            budget = parsedNum * 10000;
          } else {
            budget = parsedNum;
          }
        }
      }

      const frequency = document.querySelector('input[name="frequency"]')?.value || '하루 한 끼 (퇴근 후 저녁 30끼)';
      const concept = document.querySelector('input[name="concept"]')?.value || '일반식';
      const cuisineElements = Array.from(document.querySelectorAll('input[name="cuisine"]:checked'));
      const cuisine = cuisineElements.map(el => el.value).join(', ') || '한식';
      const exclude = document.getElementById('exclude').value.trim() || '없음';
      const pantry = document.getElementById('pantry').value.trim() || '아무것도 없음';
      const goal_notes = document.getElementById('goal_notes')?.value.trim() || '';

      const payload = {
        name,
        age,
        household,
        budget,
        frequency,
        concept,
        cuisine,
        exclude,
        pantry,
        goal_notes
      };

      try {
        const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const apiBase = isLocal ? '' : 'https://zipbabot.onrender.com';
        const endpoint = apiBase + '/api/create-client';

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 90000); // 90초 타임아웃

        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        const result = await res.json();

        if (result.success && (result.portal_url || result.cdn_portal_url)) {
          showModal(name, result);
        } else {
          throw new Error(result.error || '맞춤 식단 사이트 생성에 실패했습니다.');
        }
      } catch (err) {
        console.error('Create client error:', err);
        if (err.name === 'AbortError') {
          alert('⚠️ 서버 응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요.');
        } else {
          alert('⚠️ 맞춤 사이트 생성 중 오류가 발생했습니다:\\n\\n' + (err.message || err));
        }
      } finally {
        if (loadingInterval) clearInterval(loadingInterval);
        btn.disabled = false;
        btn.innerHTML = '<span>🚀 맞춤 30일 식단 & 장바구니 생성하기</span>';
      }
    }

    let activeCdnUrl = '';
    let activeRenderUrl = '';

    function showModal(name, result) {
      activeCdnUrl = result.cdn_portal_url || result.portal_url || '';
      activeRenderUrl = result.render_portal_url || result.portal_url || '';
      
      document.getElementById('modal-desc').innerText = `${name}님의 30일 맞춤 식단과 장바구니가 통합 생성되었습니다.`;
      
      try {
        document.getElementById('unified-link-text').innerText = decodeURIComponent(activeCdnUrl);
      } catch (e) {
        document.getElementById('unified-link-text').innerText = activeCdnUrl;
      }

      document.getElementById('btn-open-portal').href = activeRenderUrl;
      document.getElementById('result-modal').style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('result-modal').style.display = 'none';
    }

    function copyUnifiedUrl() {
      const copyBtn = document.getElementById('btn-copy-link');
      navigator.clipboard.writeText(activeCdnUrl).then(() => {
        if (copyBtn) {
          const originalHtml = copyBtn.innerHTML;
          copyBtn.style.background = '#059669';
          copyBtn.innerHTML = '<span>✅ 링크가 복사되었습니다!</span>';
          setTimeout(() => {
            copyBtn.style.background = '#0f172a';
            copyBtn.innerHTML = originalHtml;
          }, 2500);
        } else {
          alert('📋 [글로벌 CDN 링크]가 복사되었습니다!\\n카카오톡에 붙여넣어 전송하세요.\\n\\n' + activeCdnUrl);
        }
      }).catch(() => {
        prompt('아래 링크를 복사하여 카카오톡에 전송해 주세요:', activeCdnUrl);
      });
    }
  </script>"""
    content = content[:last_script_idx] + new_script + content[last_script_end_idx:]
    with open(SURVEY_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Perfectly replaced bottom <script> block in survey.html!")
else:
    print("ERROR: Could not find script block!")
