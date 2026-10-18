import sys
sys.path.insert(0, 'generator')
from recipe_engine import MASTER_RECIPES, RICE_ITEM, RICE_ITEM_PREMIUM, PREMIUM_COMPLEMENTS

def build_products_database_adaptive(recipes_list, current_budget, people_count=1, allowed_cuisines=["중식"]):
    product_map = {} # key: (prod_name, order_week)
    target_min = int(current_budget * 0.82)
    target_max = int(current_budget * 0.98)

    # 1. 쌀 등록
    rice = RICE_ITEM_PREMIUM if current_budget >= 400000 else RICE_ITEM
    product_map[(rice[4], 1)] = {
        "storage": rice[3], "cat": "🧂 조미료",
        "name": rice[4], "spec": rice[5], "price": rice[6], "query": rice[7],
        "first_day": 1, "days": [1], "recipes": ["30일 전 식단 밥"], "orderWeek": 1, "qty": 1
    }

    # 2. 고예산(>=35만) vs 실속예산(<35만) 모델 분기
    is_high_budget = current_budget >= 350000

    for r in recipes_list:
        day = r["day"]
        week_num = min(4, (day - 1) // 7 + 1)
        matched_orig = next((orig for orig in MASTER_RECIPES if orig["title"] in r["title"] or orig["title"] == r.get("base_title")), None)
        if not matched_orig:
            continue

        for ing_name, qty, unit, storage, prod_name, spec, price, query in matched_orig["base_ingredients"]:
            if storage == "seasoning":
                order_week = 1
            elif is_high_budget:
                # 고예산: 주차별 신선 구매
                order_week = week_num
            else:
                # 실속 예산: 대용량 1팩 구매 후 소분 보관
                order_week = 1 if day <= 7 else (2 if day <= 14 else (3 if day <= 21 else 4))
                # 이미 동일 품목이 있으면 재주문 안 함 (단백질 공유)
                existing = next((k for k in product_map if k[0] == prod_name), None)
                if existing:
                    product_map[existing]["days"].append(day)
                    continue

            key = (prod_name, order_week)
            if key not in product_map:
                product_map[key] = {
                    "storage": storage,
                    "cat": "🥬 신선식품" if storage == "fresh" else ("❄️ 냉동식품" if storage == "frozen" else "🧂 조미료"),
                    "name": prod_name, "spec": spec, "price": price, "query": query,
                    "first_day": day, "days": [day], "recipes": [f"Day {day} {matched_orig['title'].split()[0]}"],
                    "orderWeek": order_week, "qty": 1
                }
            else:
                product_map[key]["days"].append(day)

    current_spent = sum(item["price"] * item["qty"] for item in product_map.values())

    # 고예산 고객을 위한 프리미엄 보충
    if is_high_budget and current_spent < target_min:
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
                        "name": p_name, "spec": p_spec, "price": p_price, "query": p_query,
                        "first_day": (p_week - 1) * 7 + 1, "days": [(p_week - 1) * 7 + 1],
                        "recipes": [p_note], "orderWeek": p_week, "qty": 1
                    }
                    current_spent += p_price

    # 예산 초과 방지 (Budget Guard)
    if current_spent > target_max:
        for key in sorted(product_map.keys(), key=lambda k: product_map[k]["price"], reverse=True):
            if current_spent <= target_max:
                break
            item = product_map[key]
            # 조미료나 쌀이 아닌 중복 고기/채소 조율
            if item["orderWeek"] > 1 and item["storage"] != "seasoning":
                current_spent -= item["price"]
                del product_map[key]

    # 다인 가구 스케일링
    if people_count >= 2:
        mult = min(3, people_count)
        for item in product_map.values():
            item["qty"] = max(item["qty"], mult)
        current_spent = sum(item["price"] * item["qty"] for item in product_map.values())

    # 주차별 합계 계산
    week_totals = {
        1: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 1),
        2: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 2),
        3: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 3),
        4: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == 4)
    }

    print(f"Adaptive Results for budget {current_budget:,}원:")
    print(f"  Total spent: {current_spent:,}원 (Target: {target_min:,} ~ {target_max:,})")
    print(f"  Week totals: 1주={week_totals[1]:,}원, 2주={week_totals[2]:,}원, 3주={week_totals[3]:,}원, 4주={week_totals[4]:,}원")

import recipe_engine
plan50 = recipe_engine.generate_personalized_plan(budget=500000, cuisine="중식")
build_products_database_adaptive(plan50["recipes"], 500000, 1, ["중식"])

plan30 = recipe_engine.generate_personalized_plan(budget=300000, cuisine="한식, 일식")
build_products_database_adaptive(plan30["recipes"], 300000, 1, ["한식", "일식"])

plan20 = recipe_engine.generate_personalized_plan(budget=200000, cuisine="한식")
build_products_database_adaptive(plan20["recipes"], 200000, 1, ["한식"])
