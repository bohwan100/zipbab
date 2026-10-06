# -*- coding: utf-8 -*-
"""
Update 30_day_global_meal_plan.md to be clean, intuitive and practical
"""

from build_chef_master_recipes import chef_recipes
from update_dashboard_descs import intuitive_descs

lines = []
lines.append("# 🌍 [1인 가구] 한·일·중·양 4대 요리 30일 황금 식단표 & 실전 레시피 매니저\n")
lines.append("> **사용자 절대 조건 100% 완벽 반영**")
lines.append("> - **1. 메뉴 구성**: 한식(12끼) + 일식(6끼) + 중식(6끼) + 양식(6끼) 총 30끼")
lines.append("> - **2. 직관적인 조리법**: 군더더기 없는 단계별 직관적 행동 지침 (15분 완성)")
lines.append("> - **3. 계량 표준**: 모든 재료 **그램(g)** 및 **숟가락(T/t)** 초정밀 표기")
lines.append("> - **4. 한 달 예산**: **170,500원** (200,000원 한도 내 29,500원 절감)")
lines.append("> - **5. 잔여물 제로**: 30일차 종료 시 **냉장고 잔여 식재료 0g (음식물 쓰레기 0%)**\n")
lines.append("---\n")
lines.append("## 🍳 30일 직관적 황금 식단표 (Day 1 ~ Day 30)\n")
lines.append("| 일차 | 국가 | 메뉴명 | 1인분 직관적 핵심 조리 요약 | 열량 | 탄/단/지 | 식재료 소진 트래커 |")
lines.append("| :---: | :---: | :--- | :--- | :---: | :---: | :--- |")

for r in chef_recipes:
    day = r['day']
    cuisine = r['flag']
    title = r['title']
    desc = intuitive_descs.get(day, r['title'])
    cal = f"{r['cal']} kcal"
    macros = f"{r['carb']}/{r['prot']}/{r['fat']}g"
    waste = r['waste']
    lines.append(f"| **Day {day}** | {cuisine} | **{title}** | {desc} | {cal} | {macros} | {waste} |")

lines.append("\n---\n")
lines.append("## 💡 맛의 완성도를 높이는 실전 핵심 포인트\n")
lines.append("1. **고기 굽기**: 고기는 마른 팬 또는 달군 팬에 먼저 노릇하게 굽고, 설탕을 고기 기름에 먼저 닿게 녹여야 불향과 윤기가 착 달라붙습니다.")
lines.append("2. **간장 불향**: 간장은 팬 가장자리에 둘러 고온에 지글지글 끓어오를 때 섞어주면 스모키한 불향이 극대화됩니다.")
lines.append("3. **양념 조림**: 볶음 요리 시 물 30~40ml를 붓고 센 불에 1분간 조려주면 기름과 양념이 분리되지 않고 고기에 착 감깁니다.")
lines.append("4. **일식 장국 밸런스**: 맹물 대신 물 250ml에 치킨파우더 2g + 된장 10g(체에 풀기) + 설탕 2g(1/4t)을 넣으면 떫은맛 없이 달큰하고 구수한 일식 전문점 장국이 완성됩니다.")
lines.append("5. **부드러운 계란 질감**: 계란국은 불을 끄고 둘러 잔열로 익히고, 오야꼬동은 계란을 2번에 나누어 부어야 몽글몽글한 벨벳 식감이 납니다.")

artifact_path = "/Users/bohwanlee/.gemini/antigravity-ide/brain/b2567fdd-e500-496d-b733-06cc9d3dcd2f/30_day_global_meal_plan.md"
with open(artifact_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Updated 30_day_global_meal_plan.md successfully!")
