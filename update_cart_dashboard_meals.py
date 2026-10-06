# -*- coding: utf-8 -*-
"""
Update cart_dashboard.html weekData meals with Verified Chef Sources and Scientific Flavor Descriptions
"""

from build_chef_master_recipes import chef_recipes
import json
import re

with open("cart_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Map chef_recipes into meals by week
week_meals = {1: [], 2: [], 3: [], 4: []}

for r in chef_recipes:
    day = r["day"]
    w = 1 if day <= 7 else (2 if day <= 14 else (3 if day <= 21 else 4))
    week_meals[w].append({
        "day": f"Day {day}",
        "tag": r["flag"],
        "name": r["title"],
        "chef": r["chefSource"],
        "cal": r["cal"],
        "carb": r["carb"],
        "prot": r["prot"],
        "fat": r["fat"],
        "desc": r["chefTip"][:90] + ("..." if len(r["chefTip"]) > 90 else "")
    })

# Format each week's meals array into JS
for w in [1, 2, 3, 4]:
    meals_js = json.dumps(week_meals[w], ensure_ascii=False, indent=10)
    w_title = f"{w}주차 식단"
    pos = content.find(w_title)
    if pos != -1:
        meals_pos = content.find("meals:", pos)
        if meals_pos != -1:
            open_bracket = content.find("[", meals_pos)
            # Find matching close bracket
            close_bracket = content.find("]", open_bracket)
            # Find end of meals array
            depth = 0
            for idx in range(open_bracket, len(content)):
                if content[idx] == '[':
                    depth += 1
                elif content[idx] == ']':
                    depth -= 1
                    if depth == 0:
                        close_bracket = idx
                        break
            content = content[:open_bracket] + meals_js + content[close_bracket + 1:]
            print(f"Updated meals for Week {w}!")

# Now update the card.innerHTML in cart_dashboard.html to render meal-chef badge
old_card_html = """          <div class="meal-header">
            <span class="meal-day">${m.day}</span>
            <span class="meal-tag">${m.tag}</span>
          </div>
          <div class="meal-name">${m.name}</div>
          <div class="meal-desc">👉 ${m.desc}</div>"""

new_card_html = """          <div class="meal-header">
            <span class="meal-day">${m.day}</span>
            <span class="meal-tag">${m.tag}</span>
          </div>
          <div class="meal-name">${m.name}</div>
          ${m.chef ? `<div class="meal-chef" style="font-size: 0.78rem; font-weight: 700; color: #facc15; margin-bottom: 5px; display: flex; align-items: center; gap: 4px; background: rgba(234, 179, 8, 0.1); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(234, 179, 8, 0.25);"><span>👨‍🍳</span> <span>${m.chef}</span></div>` : ''}
          <div class="meal-desc">👉 ${m.desc}</div>"""

if old_card_html in content:
    content = content.replace(old_card_html, new_card_html)
    print("Updated card.innerHTML with meal-chef badge!")
else:
    print("old_card_html search...")
    idx = content.find('<div class="meal-name">${m.name}</div>')
    if idx != -1:
        content = content[:idx + len('<div class="meal-name">${m.name}</div>')] + '\n          ${m.chef ? `<div class="meal-chef" style="font-size: 0.78rem; font-weight: 700; color: #facc15; margin-bottom: 5px; display: flex; align-items: center; gap: 4px; background: rgba(234, 179, 8, 0.1); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(234, 179, 8, 0.25);"><span>👨‍🍳</span> <span>${m.chef}</span></div>` : \'\'}' + content[idx + len('<div class="meal-name">${m.name}</div>'):]
        print("Inserted meal-chef badge via substring replacement!")

with open("cart_dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("cart_dashboard.html updated successfully!")
