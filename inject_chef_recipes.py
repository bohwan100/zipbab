# -*- coding: utf-8 -*-
"""
Inject Chef-Verified 30-Day Recipes and High-End Culinary Science UI into recipe_viewer.html
"""

import re
from build_chef_master_recipes import chef_recipes
import json

with open("recipe_viewer.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS styles for Chef Badge and Flavor Science Box
additional_css = """
    /* Chef Badge & Food Science Styling */
    .chef-source-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(135deg, rgba(234, 179, 8, 0.15), rgba(202, 138, 4, 0.25));
      border: 1px solid rgba(234, 179, 8, 0.4);
      color: #fde047;
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 700;
      margin-bottom: 12px;
      line-height: 1.4;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .chef-icon { color: #facc15; font-size: 0.95rem; }
    .chef-name { color: #fef08a; font-weight: 700; }

    .science-tip-box {
      background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(234, 179, 8, 0.35);
      border-left: 4px solid #eab308;
      padding: 13px 15px;
      border-radius: 10px;
      margin-bottom: 16px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .science-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 7px;
    }
    .science-badge {
      font-size: 0.82rem;
      font-weight: 800;
      color: #facc15;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .star-rating {
      font-size: 0.72rem;
      font-weight: 800;
      color: #fb923c;
      background: rgba(251, 146, 60, 0.15);
      padding: 2px 8px;
      border-radius: 12px;
      border: 1px solid rgba(251, 146, 60, 0.3);
    }
    .science-desc {
      font-size: 0.84rem;
      color: #fef08a;
      line-height: 1.55;
      letter-spacing: -0.2px;
    }

    .recipe-steps {
      font-size: 0.88rem;
      color: #e2e8f0;
      margin-bottom: 16px;
      padding-left: 0;
      list-style: none;
      counter-reset: step-counter;
    }
    .recipe-steps li {
      position: relative;
      padding-left: 28px;
      margin-bottom: 10px;
      line-height: 1.5;
    }
    .recipe-steps li::before {
      counter-increment: step-counter;
      content: counter(step-counter);
      position: absolute;
      left: 0;
      top: 2px;
      width: 20px;
      height: 20px;
      background: rgba(56, 189, 248, 0.2);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 50%;
      font-size: 0.72rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .step-label {
      color: #fdba74;
      font-weight: 800;
      font-size: 0.86rem;
      margin-right: 4px;
    }
    .step-desc {
      color: #f1f5f9;
    }
"""

if "/* Chef Badge & Food Science Styling */" not in content:
    content = content.replace("</style>", additional_css + "\n  </style>")

# 2. Update Header subtitle in recipe_viewer.html
old_p = "<p>한 주에 장을 보고, 일주일간 단 1g의 낭비 없이 완벽하게 소진하는 셰프급 1인 식단표</p>"
new_p = "<p>👨‍🍳 대한민국 1타 셰프(백종원·이연복·정호영·류수영) & 세계 미식 명장 검증 10,000% 극상 맛 보장 레시피</p>"
if old_p in content:
    content = content.replace(old_p, new_p)

# 3. Replace the recipes array and renderRecipes script
recipes_json = json.dumps(chef_recipes, ensure_ascii=False, indent=2)

new_script = f"""<script>
    const recipes = {recipes_json};

    function renderRecipes(cuisineFilter = 'all', searchQuery = '') {{
      const container = document.getElementById('recipe-container');
      container.innerHTML = '';

      const q = searchQuery.toLowerCase().trim();
      const filtered = recipes.filter(r => {{
        const matchCuisine = cuisineFilter === 'all' || r.cuisine === cuisineFilter;
        const matchSearch = !q || 
          r.title.toLowerCase().includes(q) || 
          (r.chefSource && r.chefSource.toLowerCase().includes(q)) ||
          (r.chefTip && r.chefTip.toLowerCase().includes(q)) ||
          r.ingredients.some(i => i.toLowerCase().includes(q)) ||
          r.steps.some(s => s.toLowerCase().includes(q));
        return matchCuisine && matchSearch;
      }});

      if (filtered.length === 0) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #94a3b8;">
          <h3 style="font-size: 1.3rem; margin-bottom: 8px;">검색 결과가 없습니다 😢</h3>
          <p>다른 셰프명, 요리명, 조리법(마이야르, 카라멜, 불향 등) 또는 식재료를 검색해 보세요.</p>
        </div>`;
        return;
      }}

      filtered.forEach(r => {{
        const card = document.createElement('div');
        card.className = 'recipe-card';

        const formattedSteps = r.steps.map(step => {{
          const match = step.match(/^(\\[.*?\\])\\s*(.*)$/);
          if (match) {{
            return `<li><span class="step-label">${{match[1]}}</span><span class="step-desc">${{match[2]}}</span></li>`;
          }}
          return `<li><span class="step-desc">${{step}}</span></li>`;
        }}).join('');

        card.innerHTML = `
          <div>
            <div class="card-header">
              <span class="day-badge">Day ${{r.day}}</span>
              <span class="cuisine-tag">${{r.flag}}</span>
            </div>
            <h2 class="recipe-title">${{r.title}}</h2>

            <!-- Chef Verification Badge -->
            <div class="chef-source-badge">
              <span class="chef-icon">👨‍🍳</span>
              <div class="chef-name"><strong>셰프 검증:</strong> ${{r.chefSource}}</div>
            </div>

            <!-- Science & Chef Secret Box -->
            <div class="science-tip-box">
              <div class="science-header">
                <span class="science-badge">🔬 셰프의 조리 과학 & 맛 극대화 킥</span>
                <span class="star-rating">★★★★★ 10,000% 맛 보장</span>
              </div>
              <p class="science-desc">${{r.chefTip}}</p>
            </div>

            <!-- Nutrition -->
            <div class="nutrition-box">
              <div class="nutrition-header">
                <span>1인분 기준 (공깃밥 포함)</span>
                <span class="cal-val">${{r.cal}} kcal</span>
              </div>
              <div class="macro-row">
                <div class="macro-item">탄수화물<strong>${{r.carb}}g</strong></div>
                <div class="macro-item">단백질<strong>${{r.prot}}g</strong></div>
                <div class="macro-item">지방<strong>${{r.fat}}g</strong></div>
              </div>
            </div>

            <!-- Ingredients -->
            <div class="section-title">🥩 1인분 정밀 계량 식재료 (그램 & 숟가락)</div>
            <div class="ingredient-tags">
              ${{r.ingredients.map(i => `<span class="ing-tag">${{i}}</span>`).join('')}}
            </div>

            <!-- Steps -->
            <div class="section-title">🍳 셰프 마스터 15분 조리 프로세스</div>
            <ul class="recipe-steps">
              ${{formattedSteps}}
            </ul>
          </div>

          <div>
            <!-- Zero Waste Tracker -->
            <div class="waste-tag">
              <span>♻️</span> <strong>식재료 100% 소진 트래커:</strong> ${{r.waste}}
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    function filterCuisine(cuisine) {{
      document.querySelectorAll('.btn-filter').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      const searchVal = document.getElementById('recipe-search').value;
      renderRecipes(cuisine, searchVal);
    }}

    function searchRecipe() {{
      const activeBtn = document.querySelector('.btn-filter.active');
      const cuisine = activeBtn.innerText.includes('한식') ? '한식' :
                      activeBtn.innerText.includes('일식') ? '일식' :
                      activeBtn.innerText.includes('중식') ? '중식' :
                      activeBtn.innerText.includes('양식') ? '양식' : 'all';
      const query = document.getElementById('recipe-search').value.trim();
      renderRecipes(cuisine, query);
    }}

    renderRecipes();
  </script>
</body>
</html>"""

script_start = content.find("<script>")
if script_start != -1:
    content = content[:script_start] + new_script
else:
    raise ValueError("Could not find <script> in recipe_viewer.html")

with open("recipe_viewer.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully injected all 30 Chef Recipes into recipe_viewer.html!")
