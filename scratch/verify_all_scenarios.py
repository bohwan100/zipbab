import sys
import re
sys.path.append('.')
from generator.recipe_engine import MASTER_RECIPES, PREMIUM_COMPLEMENTS, RICE_ITEM, RICE_ITEM_PREMIUM

def build_products_database_v2(recipes_list, current_budget, allowed_cuisines, people_count=1, raw_pantry=[]):
    # 1. Budget targets
    if current_budget >= 400000:
        target_min = int(current_budget * 0.88)
        target_max = int(current_budget * 0.97)
    elif current_budget >= 250000:
        target_min = int(current_budget * 0.82)
        target_max = int(current_budget * 0.95)
    else:
        target_min = int(current_budget * 0.80)
        target_max = int(current_budget * 0.95)

    product_map = {}

    # 2. Rice (Week 1)
    if current_budget >= 400000:
        rice = RICE_ITEM_PREMIUM
    elif current_budget >= 250000:
        rice = ("쌀", 100, "g", "seasoning", "곰곰 2024년 햅쌀 (4kg)", "4kg 1포", 14900, "곰곰 쌀 4kg")
    else:
        rice = RICE_ITEM

    product_map[rice[4]] = {
        "storage": rice[3], "cat": "🧂 조미료", "name": rice[4], "spec": rice[5],
        "price": rice[6], "query": rice[7], "orderWeek": 1,
        "recipes": ["30일 전 식단 밥"], "first_day": 1, "days": [1], "qty": 1
    }

    # 3. Collect ingredients from recipes
    for r in recipes_list:
        day = r["day"]
        day_w = min(4, (day - 1) // 7 + 1)
        matched_orig = next((orig for orig in MASTER_RECIPES if orig["title"] in r["title"] or orig["title"] == r.get("base_title")), None)
        if not matched_orig: continue

        for ing_name, qty, unit, storage, prod_name, spec, price, query in matched_orig["base_ingredients"]:
            if storage == "seasoning":
                if prod_name not in product_map:
                    product_map[prod_name] = {
                        "storage": storage, "cat": "🧂 조미료", "name": prod_name, "spec": spec,
                        "price": price, "query": query, "orderWeek": 1,
                        "recipes": [f"Day {day} {matched_orig['title'].split()[0]}"],
                        "first_day": day, "days": [day], "qty": 1
                    }
                else:
                    product_map[prod_name]["days"].append(day)
                    lbl = f"Day {day} {matched_orig['title'].split()[0]}"
                    if lbl not in product_map[prod_name]["recipes"] and len(product_map[prod_name]["recipes"]) < 4:
                        product_map[prod_name]["recipes"].append(lbl)
            else:
                if prod_name not in product_map:
                    cat = "🥬 신선식품" if storage == "fresh" else "❄️ 냉동식품"
                    product_map[prod_name] = {
                        "storage": storage, "cat": cat, "name": prod_name, "spec": spec,
                        "price": price, "query": query, "orderWeek": day_w,
                        "recipes": [f"Day {day} {matched_orig['title'].split()[0]}"],
                        "first_day": day, "days": [day], "qty": 1
                    }
                else:
                    product_map[prod_name]["days"].append(day)
                    lbl = f"Day {day} {matched_orig['title'].split()[0]}"
                    if lbl not in product_map[prod_name]["recipes"] and len(product_map[prod_name]["recipes"]) < 4:
                        product_map[prod_name]["recipes"].append(lbl)

    # 4. Weekly distribution of fresh & frozen products
    # Distribute fresh produce and proteins evenly across the 4 weeks based on when recipes appear
    non_seasonings = [p for p in product_map.values() if p["storage"] != "seasoning"]
    for idx, item in enumerate(non_seasonings):
        item["orderWeek"] = (idx % 4) + 1

    # 5. Premium complements for budget >= 350,000
    if current_budget >= 350000:
        prime_list = []
        for c in allowed_cuisines:
            prime_list.extend(PREMIUM_COMPLEMENTS.get(c, []))
        if not prime_list:
            prime_list = PREMIUM_COMPLEMENTS["한식"]
        for p_name, p_spec, p_price, p_storage, p_query, p_week, p_note in prime_list:
            if p_name not in product_map:
                product_map[p_name] = {
                    "storage": p_storage,
                    "cat": "🥬 신선식품" if p_storage == "fresh" else ("❄️ 냉동식품" if p_storage == "frozen" else "🧂 조미료"),
                    "name": p_name, "spec": p_spec, "price": p_price, "query": p_query,
                    "orderWeek": p_week, "recipes": [p_note],
                    "first_day": (p_week - 1) * 7 + 1, "days": [(p_week - 1) * 7 + 1], "qty": 1
                }

    # 6. Apply household count multiplier
    if people_count >= 2:
        mult = min(3, people_count)
        for item in product_map.values():
            item["qty"] = max(item["qty"], mult)

    # 7. Scale quantities to reach target_min (without exceeding target_max)
    # Calculate current spent excluding pantry items
    current_spent = 0
    for item in product_map.values():
        is_in_pantry = any(p in item["name"] or p in item["query"] for p in raw_pantry)
        if not is_in_pantry:
            current_spent += item["price"] * item["qty"]

    if current_spent < target_min:
        for loop in range(4):
            for w in [2, 3, 4, 1]:
                w_prods = [p for p in product_map.values() if p["orderWeek"] == w and p["storage"] != "seasoning"]
                w_prods.sort(key=lambda x: x["price"], reverse=True)
                for p in w_prods:
                    is_in_pantry = any(pi in p["name"] or pi in p["query"] for pi in raw_pantry)
                    if is_in_pantry: continue
                    if current_spent >= target_min:
                        break
                    if current_spent + p["price"] <= target_max:
                        p["qty"] += 1
                        current_spent += p["price"]
                if current_spent >= target_min:
                    break
            if current_spent >= target_min:
                break

    # 8. Budget Guard: Strictly cut if current_spent > current_budget
    if current_spent > current_budget:
        # First reduce quantities > 1
        for p in reversed(list(product_map.values())):
            if current_spent <= current_budget:
                break
            is_in_pantry = any(pi in p["name"] or pi in p["query"] for pi in raw_pantry)
            if is_in_pantry: continue
            while p["qty"] > 1 and current_spent > current_budget:
                p["qty"] -= 1
                current_spent -= p["price"]

        # If still over budget, remove non-essential expensive items from week 4/3
        if current_spent > current_budget:
            candidates = [p for p in product_map.values() if p["storage"] != "seasoning" and "쌀" not in p["name"]]
            candidates.sort(key=lambda x: x["price"], reverse=True)
            for p in candidates:
                if current_spent <= current_budget:
                    break
                is_in_pantry = any(pi in p["name"] or pi in p["query"] for pi in raw_pantry)
                if is_in_pantry: continue
                del product_map[p["name"]]
                current_spent -= p["price"] * p["qty"]

    # 9. Build final products list
    products_list = []
    tot_spent = 0
    tot_saved_pantry = 0

    sorted_items = sorted(product_map.values(), key=lambda x: (x["orderWeek"], 0 if x["storage"] == "seasoning" else 1, x["first_day"]))

    for idx, item in enumerate(sorted_items):
        storage = item["storage"]
        order_week = item["orderWeek"]
        is_in_pantry = any(p in item["name"] or p in item["query"] for p in raw_pantry)

        buy_qty = item["qty"] if not is_in_pantry else 0
        item_total = (item["price"] * buy_qty)

        if is_in_pantry:
            tot_saved_pantry += item["price"] * item["qty"]
            display_name = f"{item['name']} [🏠 보유 재료 0원 공제]"
        else:
            tot_spent += item_total
            display_name = item["name"]

        min_day = min(item["days"])
        max_day = max(item["days"])
        min_wk = (min_day - 1) // 7 + 1
        max_wk = min(4, (max_day - 1) // 7 + 1)
        weeks_str = f"{min_wk}~{max_wk}주차" if min_wk != max_wk else f"{min_wk}주차"

        products_list.append({
            "id": idx + 1,
            "orderWeek": order_week,
            "storage": storage,
            "cat": item["cat"],
            "name": display_name,
            "spec": item["spec"],
            "qty": buy_qty,
            "unitPrice": item["price"] if not is_in_pantry else 0,
            "total": item_total,
            "weeks": weeks_str,
            "recipes": ", ".join(item["recipes"]),
            "query": item["query"]
        })

    week_totals = {
        1: sum(p["total"] for p in products_list if p["orderWeek"] == 1),
        2: sum(p["total"] for p in products_list if p["orderWeek"] == 2),
        3: sum(p["total"] for p in products_list if p["orderWeek"] == 3),
        4: sum(p["total"] for p in products_list if p["orderWeek"] == 4)
    }

    # Rocket Fresh minimum order check (15,000원)
    for w in [2, 3, 4]:
        if week_totals[w] < 15000:
            for p in products_list:
                if p["orderWeek"] == 1 and p["total"] >= 15000 and "쌀" not in p["name"]:
                    p["orderWeek"] = w
                    week_totals[1] -= p["total"]
                    week_totals[w] += p["total"]
                    break

    return products_list, tot_spent, tot_saved_pantry, week_totals

# Run tests
for (b, c, p) in [(500000, "중식", "아무것도 없음"), (300000, "한식, 일식", "아무것도 없음"), (200000, "한식", "아무것도 없음")]:
    allowed_c = [x for x in ["중식", "일식", "양식", "한식"] if x in c] or ["한식"]
    cands = [r for r in MASTER_RECIPES if r["cuisine"] in allowed_c]
    r_list = [{"day": i+1, "title": cands[i % len(cands)]["title"], "base_title": cands[i % len(cands)]["title"]} for i in range(30)]
    prods, spent, saved_pantry, wtots = build_products_database_v2(r_list, b, allowed_c, 1, [])
    print(f"\n==========================================")
    print(f"Budget: {b:,}원 | Cuisine: {c}")
    print(f"Total Spent: {spent:,}원 ({spent/b*100:.1f}%) | Strictly <= Budget: {spent <= b}")
    for w in [1, 2, 3, 4]:
        w_prods = [p for p in prods if p["orderWeek"] == w]
        w_names = [p["name"].split()[0] for p in w_prods]
        print(f"  Week {w}: {wtots[w]:,}원 ({len(w_prods)}종: {', '.join(w_names[:5])}...)")
