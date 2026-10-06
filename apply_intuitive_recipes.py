# -*- coding: utf-8 -*-
"""
Make recipe_viewer.html and cart_dashboard.html ultra-clean and intuitive:
1. Remove chef badge (셰프 검증) and kick box (조리 과학 & 맛 극대화 킥).
2. Remove cumbersome step subheadings like [1단계: 고기 시어링 & 마이야르].
3. Format steps as clean, direct, intuitive numbered steps (1, 2, 3, 4, 5, 6).
4. Remove chef badge from cart_dashboard.html as well.
"""

from build_chef_master_recipes import chef_recipes
import re
import json

# =============================================================================
# 1. CLEAN RECIPES DATASET
# =============================================================================
clean_recipes_list = []
for r in chef_recipes:
    item = {
        "day": r["day"],
        "title": r["title"],
        "cuisine": r["cuisine"],
        "flag": r["flag"],
        "cal": r["cal"],
        "carb": r["carb"],
        "prot": r["prot"],
        "fat": r["fat"],
        "ingredients": r["ingredients"],
        "waste": r["waste"]
    }
    cleaned_steps = []
    for s in r["steps"]:
        # Strip [1단계: ...], [2단계: ...] prefixes
        clean_s = re.sub(r"^\[\d+단계:\s*.*?\]\s*", "", s)
        # Strip unnecessary author parentheticals
        clean_s = re.sub(r"\s*\((?:백종원|어남선생|이연복|정호영|고든 램지|노포).*?\)", "", clean_s)
        cleaned_steps.append(clean_s.strip())
    item["steps"] = cleaned_steps
    clean_recipes_list.append(item)

# =============================================================================
# 2. UPDATE recipe_viewer.html
# =============================================================================
with open("recipe_viewer.html", "r", encoding="utf-8") as f:
    viewer_content = f.read()

# Update subtitle to be direct and intuitive
viewer_content = re.sub(
    r"<p>👨‍🍳 대한민국 1타 셰프.*?레시피</p>",
    "<p>직관적이고 따라하기 쉬운 1인분 정밀 계량 15분 완성 레시피</p>",
    viewer_content
)

# Clean CSS: Remove unused chef-badge & science-tip styles, enhance .recipe-steps styling
clean_css = """
    /* Clean & Intuitive Step List Styling */
    .recipe-steps {
      list-style: none;
      counter-reset: step-counter;
      margin-bottom: 18px;
      padding-left: 0;
    }
    .recipe-steps li {
      position: relative;
      padding-left: 30px;
      margin-bottom: 10px;
      font-size: 0.9rem;
      line-height: 1.6;
      color: #e2e8f0;
    }
    .recipe-steps li::before {
      counter-increment: step-counter;
      content: counter(step-counter);
      position: absolute;
      left: 0;
      top: 3px;
      width: 20px;
      height: 20px;
      background: rgba(249, 115, 22, 0.2);
      color: #fb923c;
      border: 1px solid rgba(249, 115, 22, 0.45);
      border-radius: 50%;
      font-size: 0.75rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }
"""

# Replace any old chef css if present
viewer_content = re.sub(r"/\* Chef Badge & Food Science Styling \*/.*?(?=</style>)", clean_css, viewer_content, flags=re.DOTALL)

# Re-generate the clean script section
recipes_json = json.dumps(clean_recipes_list, ensure_ascii=False, indent=2)

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
          r.ingredients.some(i => i.toLowerCase().includes(q)) ||
          r.steps.some(s => s.toLowerCase().includes(q));
        return matchCuisine && matchSearch;
      }});

      if (filtered.length === 0) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #94a3b8;">
          <h3 style="font-size: 1.3rem; margin-bottom: 8px;">검색 결과가 없습니다 😢</h3>
          <p>다른 요리명이나 식재료를 검색해 보세요.</p>
        </div>`;
        return;
      }}

      filtered.forEach(r => {{
        const card = document.createElement('div');
        card.className = 'recipe-card';

        card.innerHTML = `
          <div>
            <div class="card-header">
              <span class="day-badge">Day ${{r.day}}</span>
              <span class="cuisine-tag">${{r.flag}}</span>
            </div>
            <h2 class="recipe-title">${{r.title}}</h2>

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
            <div class="section-title">🥩 1인분 계량 식재료 (그램 & 숟가락)</div>
            <div class="ingredient-tags">
              ${{r.ingredients.map(i => `<span class="ing-tag">${{i}}</span>`).join('')}}
            </div>

            <!-- Steps -->
            <div class="section-title">🍳 15분 조리 순서</div>
            <ol class="recipe-steps">
              ${{r.steps.map(s => `<li>${{s}}</li>`).join('')}}
            </ol>
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

script_start = viewer_content.find("<script>")
if script_start != -1:
    viewer_content = viewer_content[:script_start] + new_script
else:
    raise ValueError("Could not find <script> in recipe_viewer.html")

with open("recipe_viewer.html", "w", encoding="utf-8") as f:
    f.write(viewer_content)

print("recipe_viewer.html successfully cleaned and updated!")

# =============================================================================
# 3. UPDATE cart_dashboard.html
# =============================================================================
with open("cart_dashboard.html", "r", encoding="utf-8") as f:
    dash_content = f.read()

# Remove the meal-chef element
dash_content = re.sub(
    r'\s*\$\{m\.chef \? `<div class="meal-chef".*?</div>` : \'\'\}',
    '',
    dash_content
)

with open("cart_dashboard.html", "w", encoding="utf-8") as f:
    f.write(dash_content)

print("cart_dashboard.html successfully cleaned of chef badges!")
