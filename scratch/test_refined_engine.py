import sys
sys.path.insert(0, 'generator')
from recipe_engine import MASTER_RECIPES, RICE_ITEM, RICE_ITEM_PREMIUM, PREMIUM_COMPLEMENTS

def build_products_database_new(recipes_list, current_budget, people_count=1, allowed_cuisines=["중식"]):
    # Weekly fresh distribution
    # Each week has its own groceries
    # Seasoning goes to Week 1
    # Fresh and frozen go to the week they are used
    product_map = {} # key: (prod_name, order_week)

    # 1. 쌀 등록
    rice = RICE_ITEM_PREMIUM if current_budget >= 400000 else RICE_ITEM
    product_map[(rice[4], 1)] = {
        "storage": rice[3],
        "cat": "🧂 조미료",
        "name": rice[4],
        "spec": rice[5],
        "price": rice[6],
        "query": rice[7],
        "first_day": 1,
        "days": [1],
        "recipes": ["30일 전 식단 밥"],
        "orderWeek": 1,
        "qty": 1
    }

    # 2. 레시피별 식재료를 주차별로 배치
    for r in recipes_list:
        day = r["day"]
        week_num = min(4, (day - 1) // 7 + 1)
        matched_orig = next((orig for orig in MASTER_RECIPES if orig["title"] in r["title"] or orig["title"] == r.get("base_title")), None)
        if not matched_orig:
            continue

        for ing_name, qty, unit, storage, prod_name, spec, price, query in matched_orig["base_ingredients"]:
            order_week = 1 if storage == "seasoning" else week_num
            key = (prod_name, order_week)
            if key not in product_map:
                product_map[key] = {
                    "storage": storage,
                    "cat": "🥬 신선식품" if storage == "fresh" else ("❄️ 냉동식품" if storage == "frozen" else "🧂 조미료"),
                    "name": prod_name,
                    "spec": spec,
                    "price": price,
                    "query": query,
                    "first_day": day,
                    "days": [day],
                    "recipes": [f"Day {day} {matched_orig['title'].split()[0]}"],
                    "orderWeek": order_week,
                    "qty": 1
                }
            else:
                product_map[key]["days"].append(day)
                rec_label = f"Day {day} {matched_orig['title'].split()[0]}"
                if rec_label not in product_map[key]["recipes"] and len(product_map[key]["recipes"]) < 3:
                    product_map[key]["recipes"].append(rec_label)

    # 3. 예산 맞춤 스케일링
    current_spent = sum(item["price"] * item["qty"] for item in product_map.values())
    target_min = int(current_budget * 0.84)
    target_max = int(current_budget * 0.98)

    # 고예산(35만원 이상) 고객을 위한 주차별 프리미엄 보충
    if current_spent < target_min and current_budget >= 350000:
        prime_list = []
        for c in allowed_cuisines:
            prime_list.extend(PREMIUM_COMPLEMENTS.get(c, []))
        if not prime_list:
            prime_list = PREMIUM_COMPLEMENTS["한식"]

        for p_name, p_spec, p_price, p_storage, p_query, p_week, p_note in prime_list:
            key = (p_name, p_week)
            if current_spent + p_price <= target_max:
                if key not in product_map:
                    product_map[key] = {
                        "storage": p_storage,
                        "cat": "🥬 신선식품" if p_storage == "fresh" else ("❄️ 냉동식품" if p_storage == "frozen" else "🧂 조미료"),
                        "name": p_name,
                        "spec": p_spec,
                        "price": p_price,
                        "query": p_query,
                        "first_day": (p_week - 1) * 7 + 1,
                        "days": [(p_week - 1) * 7 + 1],
                        "recipes": [p_note],
                        "orderWeek": p_week,
                        "qty": 1
                    }
                    current_spent += p_price

    # 주차별 단백질 보충
    while current_spent < target_min:
        added = False
        for key, item in list(product_map.items()):
            if any(k in item["name"] for k in ["부채살", "삼겹살", "새우", "해물", "앞다리살", "우삼겹", "닭다리살"]):
                if current_spent + item["price"] <= target_max:
                    item["qty"] += 1
                    current_spent += item["price"]
                    added = True
                    if current_spent >= target_min:
                        break
        if not added:
            break

    # 주차별 합계 계산
    week_totals = {
        1: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 1),
        2: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 2),
        3: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 3),
        4: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 4)
    }

    print(f"Results for budget {current_budget:,}원:")
    print(f"  Total spent: {current_spent:,}원 (Target: {target_min:,} ~ {target_max:,})")
    print(f"  Week totals: 1주={week_totals[1]:,}원, 2주={week_totals[2]:,}원, 3주={week_totals[3]:,}원, 4주={week_totals[4]:,}원")

import recipe_engine
plan = recipe_engine.generate_personalized_plan(budget=500000, cuisine="중식")
build_products_database_new(plan["recipes"], 500000, 1, ["중식"])

plan30 = recipe_engine.generate_personalized_plan(budget=300000, cuisine="한식, 일식")
build_products_database_new(plan30["recipes"], 300000, 1, ["한식", "일식"])

plan20 = recipe_engine.generate_personalized_plan(budget=200000, cuisine="한식")
build_products_database_new(plan20["recipes"], 200000, 1, ["한식"])
