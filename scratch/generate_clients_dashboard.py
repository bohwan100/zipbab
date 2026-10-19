import os
import json
import re

def get_live_tunnel_url():
    tunnel_log = os.path.join(os.path.dirname(__file__), "tunnel.log")
    if os.path.exists(tunnel_log):
        try:
            with open(tunnel_log, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                matches = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', content)
                if matches:
                    return matches[-1]
        except Exception:
            pass
    return "https://zipbabot.onrender.com"

tunnel_base = get_live_tunnel_url()

clients_dir = 'clients'
clients_data = []

if os.path.exists(clients_dir):
    for c in sorted(os.listdir(clients_dir)):
        c_path = os.path.join(clients_dir, c)
        if not os.path.isdir(c_path):
            continue
        info_file = os.path.join(c_path, 'client_info.json')
        if os.path.exists(info_file):
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['folder_name'] = c
                    clients_data.append(data)
            except Exception:
                pass
        else:
            clients_data.append({
                'client_id': c,
                'client_name': c,
                'folder_name': c,
                'household_size': '1명',
                'budget': 300000,
                'goal': '일반식',
                'cuisine': '한식, 일식',
                'pages': {
                    'portal': f'clients/{c}/index.html',
                    'cart': f'clients/{c}/cart.html',
                    'recipes': f'clients/{c}/recipes.html',
                    'storage': f'clients/{c}/storage.html'
                }
            })

# 정유진_37부터 최상단에 뜨도록 우선순위 정렬
priority_order = [
    '정유진_37',
    '최민석_26',
    '차민홍_34',
    '정진향_41',
    '노한석_30',
    '정수원_21세',
    '최종본_100세_2',
    '테스트_22',
    '테스트_30대'
]

def get_sort_key(item):
    fname = item.get('folder_name', item.get('client_id', ''))
    if fname in priority_order:
        return (0, priority_order.index(fname))
    return (1, fname)

clients_data.sort(key=get_sort_key)

total_clients = len(clients_data)
avg_budget = int(sum(c.get('budget', 300000) for c in clients_data) / max(total_clients, 1))
total_meals = sum(c.get('total_meals', 30) for c in clients_data)

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>👥 집밥봇 회원/고객 관리 매니저</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: rgba(18, 24, 38, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #38bdf8;
      --accent: #f97316;
      --danger: #ef4444;
      --success: #34d399;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 30px 20px 80px;
      min-height: 100vh;
    }}
    .container {{
      max-width: 1280px;
      margin: 0 auto;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
      margin-bottom: 30px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
    }}
    .brand-title {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .brand-icon {{
      font-size: 2.2rem;
      background: rgba(56, 189, 248, 0.15);
      width: 56px;
      height: 56px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    h1 {{
      font-size: 1.7rem;
      font-weight: 800;
      letter-spacing: -0.5px;
    }}
    .header-desc {{
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-top: 4px;
    }}
    .header-actions {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .btn {{
      padding: 10px 18px;
      border-radius: 12px;
      font-size: 0.92rem;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s;
    }}
    .btn-orange {{
      background: linear-gradient(135deg, #f97316, #ea580c);
      color: #fff;
      box-shadow: 0 4px 14px rgba(249, 115, 22, 0.4);
    }}
    .btn-orange:hover {{
      background: linear-gradient(135deg, #ea580c, #c2410c);
      transform: translateY(-2px);
    }}
    .btn-ghost {{
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.15);
      color: #cbd5e1;
    }}
    .btn-ghost:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }}

    /* Stats Overview */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 26px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
    }}
    .stat-label {{
      font-size: 0.82rem;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .stat-val {{
      font-size: 1.8rem;
      font-weight: 800;
      color: #fff;
      margin-top: 6px;
    }}

    /* Filter & Batch Action Bar */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
      flex-wrap: wrap;
      background: rgba(18, 24, 38, 0.6);
      padding: 16px 20px;
      border-radius: 16px;
      border: 1px solid var(--card-border);
    }}
    .search-input {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 16px;
      font-size: 0.95rem;
      color: #fff;
      width: 280px;
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
      background: rgba(255, 255, 255, 0.08);
    }}

    /* Batch Selection & Delete Controls */
    .batch-controls {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .select-all-label {{
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      user-select: none;
      font-size: 0.88rem;
      font-weight: 700;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.05);
      padding: 9px 14px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      transition: all 0.2s;
    }}
    .select-all-label:hover {{
      background: rgba(255, 255, 255, 0.09);
      color: #fff;
    }}
    .select-all-chk {{
      width: 18px;
      height: 18px;
      cursor: pointer;
      accent-color: var(--danger);
    }}
    .btn-batch-delete {{
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #94a3b8;
      padding: 9px 16px;
      border-radius: 10px;
      font-size: 0.88rem;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: not-allowed;
      transition: all 0.2s;
    }}
    .btn-batch-delete:not(:disabled) {{
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      color: #fff;
      border-color: #dc2626;
      box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
      cursor: pointer;
    }}
    .btn-batch-delete:not(:disabled):hover {{
      background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
      transform: translateY(-1px);
    }}

    /* Clients Grid */
    .client-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 20px;
    }}
    .client-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      backdrop-filter: blur(12px);
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }}
    .client-card:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    }}
    .client-card.is-selected {{
      border-color: rgba(239, 68, 68, 0.6) !important;
      background: rgba(239, 68, 68, 0.06) !important;
      box-shadow: 0 0 24px rgba(239, 68, 68, 0.2) !important;
    }}
    .client-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
      gap: 10px;
    }}
    .client-select-chk {{
      width: 20px;
      height: 20px;
      margin-top: 3px;
      cursor: pointer;
      accent-color: var(--danger);
      flex-shrink: 0;
    }}
    .client-name {{
      font-size: 1.3rem;
      font-weight: 800;
      color: #fff;
    }}
    .client-meta {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 3px;
    }}
    .head-right-tools {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .badge-goal {{
      background: rgba(249, 115, 22, 0.15);
      color: #fb923c;
      border: 1px solid rgba(249, 115, 22, 0.3);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 700;
    }}
    .btn-card-delete {{
      background: rgba(239, 68, 68, 0.12);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #fca5a5;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s;
    }}
    .btn-card-delete:hover {{
      background: #ef4444;
      color: #fff;
      border-color: #ef4444;
      transform: scale(1.08);
      box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
    }}

    .client-details {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 0.88rem;
      color: #cbd5e1;
      margin-bottom: 20px;
      background: rgba(0, 0, 0, 0.2);
      padding: 14px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }}
    .detail-row {{
      display: flex;
      justify-content: space-between;
    }}
    .detail-row span.k {{
      color: var(--text-muted);
    }}
    .detail-row span.v {{
      font-weight: 600;
      color: #f1f5f9;
    }}
    .client-actions {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .action-link {{
      padding: 12px 16px;
      border-radius: 12px;
      font-size: 0.92rem;
      font-weight: 700;
      text-align: center;
      text-decoration: none;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }}
    .btn-kakao-copy {{
      background: linear-gradient(135deg, #fee500 0%, #facc15 100%);
      color: #1e1b4b;
      font-weight: 800;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(250, 204, 21, 0.35);
    }}
    .btn-kakao-copy:hover {{
      background: linear-gradient(135deg, #facc15 0%, #eab308 100%);
      transform: translateY(-1px);
    }}
    .action-portal {{
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #fff;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }}
    .action-portal:hover {{
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-1px);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand-title">
        <div class="brand-icon">👥</div>
        <div>
          <h1>집밥봇 고객 & 회원 통합 관리 매니저</h1>
          <div class="header-desc">개인 맞춤 30일 식단, 장바구니, 보관 가이드 고객 목록 및 관리</div>
        </div>
      </div>
      <div class="header-actions">
        <a href="survey.html" class="btn btn-orange">➕ 신규 고객 등록 (설문)</a>
        <a href="index.html" class="btn btn-ghost">🏠 포털 홈</a>
      </div>
    </header>

    <!-- 📢 고객 전달용 설문지 배포 배너 (스마트폰 카톡 전송 가능) -->
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%); border: 1.5px solid #eab308; border-radius: 16px; padding: 18px 24px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
      <div style="display: flex; align-items: center; gap: 14px;">
        <span style="font-size: 2rem;">📢</span>
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <strong style="color: #facc15; font-size: 1.05rem;">고객 전달용 맞춤 식단 설문지 링크</strong>
            <span style="background: #eab308; color: #1e1b4b; font-size: 0.72rem; font-weight: 800; padding: 2px 7px; border-radius: 6px;">모바일 1초 접속 보장</span>
          </div>
          <div style="color: #94a3b8; font-size: 0.86rem; margin-top: 3px;">
            새로운 고객에게 카톡으로 이 링크를 보내주시면, 고객이 스마트폰에서 설문을 작성하는 즉시 모바일 맞춤 사이트가 완성됩니다.
          </div>
        </div>
      </div>
      <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <button type="button" onclick="copySurveyLink()" style="background: linear-gradient(135deg, #fee500 0%, #facc15 100%); color: #1e1b4b; border: none; padding: 10px 18px; border-radius: 10px; font-weight: 800; font-size: 0.88rem; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 10px rgba(250, 204, 21, 0.35);">
          📋 고객 배포용 설문 링크 복사
        </button>
        <a href="{tunnel_base}/survey.html" target="_blank" style="background: rgba(255, 255, 255, 0.08); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.2); padding: 10px 16px; border-radius: 10px; font-weight: 700; font-size: 0.85rem; text-decoration: none;">
          🌐 설문지 열기 ➔
        </a>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">등록된 고객 수</div>
        <div class="stat-val"><span id="stat-total-clients">{total_clients}</span><span style="font-size: 1rem; color: var(--text-muted); font-weight: normal;"> 명</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-label">평균 식비 예산</div>
        <div class="stat-val">{avg_budget:,}<span style="font-size: 1rem; color: var(--text-muted); font-weight: normal;"> 원</span></div>
      </div>
    </div>

    <!-- Filter & Batch Action Bar -->
    <div class="filter-bar">
      <div class="batch-controls">
        <input type="text" class="search-input" id="search" placeholder="🔍 고객 성함 또는 키워드 검색..." onkeyup="filterClients()">
        <label class="select-all-label">
          <input type="checkbox" id="select-all-chk" class="select-all-chk" onchange="toggleSelectAll(this)">
          <span>전체 선택</span>
        </label>
        <button type="button" id="btn-batch-delete" onclick="deleteSelectedClients()" disabled class="btn-batch-delete">
          🗑️ 선택 고객 삭제 (<span id="selected-count">0</span>)
        </button>
      </div>
      <div style="color: var(--text-muted); font-size: 0.88rem;">
        총 <strong style="color: #fff;" id="client-count">{total_clients}</strong>명의 고객이 등록되어 있습니다.
      </div>
    </div>

    <!-- Grid -->
    <div class="client-grid" id="grid">
"""

for c in clients_data:
    cid = c.get('folder_name', c.get('client_id'))
    name = c.get('client_name', cid)
    age = c.get('client_age', '')
    household = c.get('household_size', '1명')
    budget = c.get('budget', 300000)
    spent = c.get('total_spent', budget)
    goal = c.get('goal', '일반식')
    cuisine = c.get('cuisine', '한식, 일식')
    goal_notes = c.get('goal_notes', '')
    portal_link = f"clients/{cid}/index.html"
    recipe_link = f"clients/{cid}/recipes.html"
    cart_link = f"clients/{cid}/cart.html"
    storage_link = f"clients/{cid}/storage.html"

    goal_notes_html = ""
    if goal_notes and goal_notes.strip():
        goal_notes_html = f"""            <div class="detail-row" style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38bdf8; border-radius: 6px; padding: 8px 10px; margin-top: 8px; flex-direction: column; align-items: flex-start; gap: 4px;">
              <span class="k" style="color: #38bdf8; font-weight: 800; font-size: 0.78rem;">🎯 고객 목표 (설문 6번)</span>
              <span class="v" style="color: #f1f5f9; font-size: 0.84rem; max-width: 100%; white-space: normal; line-height: 1.45; font-weight: 500;">"{goal_notes}"</span>
            </div>"""

    html_content += f"""      <div class="client-card" id="card-{cid}" data-name="{name} {cid} {goal} {cuisine}">
        <div>
          <div class="client-head">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <input type="checkbox" class="client-select-chk" value="{cid}" data-name="{name}" onchange="onSelectionChange(this)" title="삭제 대상 선택">
              <div>
                <div class="client-name">{name}</div>
                <div class="client-meta">📁 {cid}</div>
              </div>
            </div>
            <div class="head-right-tools">
              <span class="badge-goal">{goal}</span>
              <button type="button" onclick="deleteSingleClient('{cid}', '{name}')" class="btn-card-delete" title="[{name}] 고객 폴더 및 파일 영구 삭제">
                🗑️
              </button>
            </div>
          </div>

          <div class="client-details">
            <div class="detail-row">
              <span class="k">구성 인원</span>
              <span class="v">{household} ({age})</span>
            </div>
            <div class="detail-row">
              <span class="k">한 달 예산</span>
              <span class="v">{budget:,}원 (실구매 {spent:,}원)</span>
            </div>
            <div class="detail-row">
              <span class="k">선호 취향</span>
              <span class="v">{cuisine}</span>
            </div>
{goal_notes_html}
          </div>
        </div>

        <div class="client-actions">
          <button type="button" onclick="copyKakaoLink('{name}', '{cid}')" class="action-link btn-kakao-copy">
            💬 카톡 전송용 맞춤 링크 복사 (1초 접속)
          </button>
          <a href="{portal_link}" target="_blank" class="action-link action-portal">
            🏠 고객 맞춤 포털 열기 ➔
          </a>
        </div>
      </div>
"""

html_content += f"""    </div>
  </div>

  <script>
    // file:// 로 직접 열었을 경우 자동으로 백그라운드 서버(http://localhost:8080/clients.html)로 즉시 전환
    if (window.location.protocol === 'file:') {{
      fetch('http://localhost:8080/api/ping', {{ mode: 'no-cors' }}).then(() => {{
        window.location.replace('http://localhost:8080/clients.html');
      }}).catch(() => {{}});
    }}

    const publicTunnelUrl = (window.location.origin && !window.location.origin.includes('file:')) ? window.location.origin : '{tunnel_base}';

    function copySurveyLink() {{
      const surveyUrl = `${{publicTunnelUrl}}/survey.html`;
      navigator.clipboard.writeText(surveyUrl).then(() => {{
        showCopyToast(`📋 고객 배포용 설문지 링크가 복사되었습니다!\\n스마트폰 카카오톡에 바로 붙여넣어 고객에게 전송하세요.\\n\\n${{surveyUrl}}`);
      }}).catch(() => {{
        prompt('아래 설문 링크를 복사하여 고객에게 전송해 주세요:', surveyUrl);
      }});
    }}

    function copyKakaoLink(name, cid) {{
      const mobileUrl = `${{publicTunnelUrl}}/clients/${{encodeURIComponent(cid)}}/index.html`;
      navigator.clipboard.writeText(mobileUrl).then(() => {{
        showCopyToast(`💬 [${{name}}]님의 맞춤 링크가 복사되었습니다!\\n스마트폰 카카오톡에 바로 붙여넣어 전송하세요.\\n\\n${{mobileUrl}}`);
      }}).catch(() => {{
        prompt('아래 링크를 복사하여 카카오톡에 전송해 주세요:', mobileUrl);
      }});
    }}

    function showCopyToast(msg) {{
      let toast = document.getElementById('copy-toast');
      if (!toast) {{
        toast = document.createElement('div');
        toast.id = 'copy-toast';
        toast.style.cssText = 'position: fixed; bottom: 30px; right: 30px; background: #0f172a; border: 1.5px solid #eab308; color: #fff; padding: 14px 22px; border-radius: 12px; font-weight: 700; font-size: 0.92rem; z-index: 9999; box-shadow: 0 10px 25px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 8px; white-space: pre-line;';
        document.body.appendChild(toast);
      }}
      toast.innerText = msg;
      toast.style.display = 'flex';
      setTimeout(() => {{ toast.style.display = 'none'; }}, 3500);
    }}

    function filterClients() {{
      const q = document.getElementById('search').value.toLowerCase();
      const cards = document.querySelectorAll('.client-card');
      let visible = 0;
      cards.forEach(c => {{
        const text = c.getAttribute('data-name').toLowerCase();
        if (text.includes(q)) {{
          c.style.display = 'flex';
          visible++;
        }} else {{
          c.style.display = 'none';
        }}
      }});
      document.getElementById('client-count').innerText = visible;
    }}

    /* Selection & Delete Logic */
    function onSelectionChange(chk) {{
      const card = chk.closest('.client-card');
      if (chk.checked) {{
        card.classList.add('is-selected');
      }} else {{
        card.classList.remove('is-selected');
      }}
      updateBatchButtonState();
    }}

    function toggleSelectAll(masterChk) {{
      const visibleCards = Array.from(document.querySelectorAll('.client-card')).filter(c => c.style.display !== 'none');
      visibleCards.forEach(card => {{
        const chk = card.querySelector('.client-select-chk');
        if (chk) {{
          chk.checked = masterChk.checked;
          if (masterChk.checked) {{
            card.classList.add('is-selected');
          }} else {{
            card.classList.remove('is-selected');
          }}
        }}
      }});
      updateBatchButtonState();
    }}

    function updateBatchButtonState() {{
      const checked = document.querySelectorAll('.client-select-chk:checked');
      const countEl = document.getElementById('selected-count');
      const btn = document.getElementById('btn-batch-delete');
      const masterChk = document.getElementById('select-all-chk');
      
      const count = checked.length;
      if (countEl) countEl.innerText = count;
      if (btn) btn.disabled = (count === 0);

      const allChks = document.querySelectorAll('.client-select-chk');
      if (masterChk && allChks.length > 0) {{
        masterChk.checked = (count === allChks.length && count > 0);
      }}
    }}

    async function deleteSingleClient(cid, name) {{
      if (!confirm(`⚠️ 정말 [${{name}}] 고객 데이터를 영구 삭제하시겠습니까?\\n\\n- clients/${{cid}} 폴더 및 모든 맞춤 페이지(식단/장바구니/보관법) 파일이 실제 컴퓨터에서 영구 삭제됩니다.\\n- 삭제 후 복구할 수 없습니다.`)) {{
        return;
      }}
      await sendDeleteRequest([cid], [name]);
    }}

    async function deleteSelectedClients() {{
      const checked = Array.from(document.querySelectorAll('.client-select-chk:checked'));
      if (checked.length === 0) return;

      const cids = checked.map(c => c.value);
      const names = checked.map(c => c.getAttribute('data-name') || c.value);

      if (!confirm(`⚠️ 정말 선택한 ${{cids.length}}명의 고객 데이터를 영구 삭제하시겠습니까?\\n\\n삭제 대상: ${{names.join(', ')}}\\n\\n실제 폴더와 파일이 영구 삭제되며 복구할 수 없습니다.`)) {{
        return;
      }}
      await sendDeleteRequest(cids, names);
    }}

    async function sendDeleteRequest(cids, names) {{
      const btn = document.getElementById('btn-batch-delete');
      const originalText = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '⏳ 실제 파일 삭제 중...';

      // file:// 환경이거나 외부 접속 환경이어도 localhost 또는 현재 도메인으로 정상 라우팅
      const isFile = window.location.protocol === 'file:' || !window.location.origin || window.location.origin === 'null';
      const apiBase = isFile ? 'http://localhost:8080' : '';
      const endpoint = apiBase + '/api/delete-client';

      try {{
        const res = await fetch(endpoint, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ client_ids: cids }})
        }});
        const result = await res.json();
        if (result.success) {{
          showCopyToast(`🗑️ ${{result.deleted.length}}명의 고객 데이터가 실제 파일에서 완전히 삭제되었습니다!`);
          setTimeout(() => {{
            if (window.location.protocol === 'file:') {{
              window.location.replace('http://localhost:8080/clients.html');
            }} else {{
              window.location.reload();
            }}
          }}, 600);
        }} else {{
          alert('삭제 중 오류가 발생했습니다: ' + (result.errors || []).join(', '));
          btn.disabled = false;
          btn.innerHTML = originalText;
        }}
      }} catch (err) {{
        console.error('Delete request error:', err);
        alert('⚠️ 삭제 요청 중 통신 오류가 발생했습니다: ' + err.message + '\\n\\n로컬 서버(http://localhost:8080)가 실행 중인지 확인해 주세요.');
        btn.disabled = false;
        btn.innerHTML = originalText;
      }}
    }}
  </script>
</body>
</html>
"""

with open('clients.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully generated clients.html')
