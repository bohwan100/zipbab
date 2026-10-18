import sys
sys.path.append('.')
from generator.recipe_engine import MASTER_RECIPES, PREMIUM_COMPLEMENTS, RICE_ITEM, RICE_ITEM_PREMIUM

def test_smart_budget_engine(budget=500000, cuisine="중식", household="1명", pantry="아무것도 없음"):
    people_count = 1
    total_meals = 30
    allowed_cuisines = [c for c in ["중식", "일식", "양식", "한식"] if c in cuisine] or ["한식"]
    
    # Target spending: between 85% and 97% of budget
    target_min = int(budget * 0.85)
    target_max = int(budget * 0.97)
    
    # 1. Select recipes
    cands = [r for r in MASTER_RECIPES if r["cuisine"] in allowed_cuisines]
    final_recipes = []
    for day_i in range(total_meals):
        base_r = cands[day_i % len(cands)]
        final_recipes.append({
            "day": day_i + 1,
            "title": base_r["title"],
            "base_title": base_r["title"],
            "cuisine": base_r["cuisine"],
            "flag": base_r["flag"]
        })
        
    # 2. Seasonings & Rice (Week 1)
    product_map = {}
    rice = RICE_ITEM_PREMIUM if budget >= 400000 else RICE_ITEM
    product_map[rice[4]] = {
        "storage": rice[3], "cat": "🧂 조미료", "name": rice[4], "spec": rice[5],
        "price": rice[6], "query": rice[7], "orderWeek": 1,
        "recipes": ["30일 전 식단 밥"], "first_day": 1, "days": [1], "qty": 1
    }
    
    # Distinct meat/seafood/fresh assignment by week:
    # We assign recipes to week:
    # Week 1: days 1..7
    # Week 2: days 8..14
    # Week 3: days 15..21
    # Week 4: days 22..30
    
    # Let's map each recipe to its week:
    for r in final_recipes:
        day = r["day"]
        day_w = min(4, (day - 1) // 7 + 1)
        matched_orig = next((orig for orig in MASTER_RECIPES if orig["title"] in r["title"] or orig["title"] == r.get("base_title")), None)
        if not matched_orig: continue
        
        for ing_name, qty, unit, storage, prod_name, spec, price, query in matched_orig["base_ingredients"]:
            if storage == "seasoning":
                # Seasoning is ordered once in week 1
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
                # Fresh or Frozen
                # If prod_name not in product_map yet:
                if prod_name not in product_map:
                    # Assign orderWeek to the week of this day
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

    # Balance weeks:
    # If some fresh/frozen items are all in week 1, distribute them evenly across 4 weeks:
    # We want week 1, 2, 3, 4 to each have some fresh protein/produce
    # Let's see: items with storage != 'seasoning'
    fresh_items = [p for p in product_map.values() if p["storage"] != "seasoning"]
    # Group items into weeks 1, 2, 3, 4 based on their recipe rotation:
    # We can assign each meat/produce to the week where it is prominently used
    # e.g., if there are 16 fresh items, put 4 in W1, 4 in W2, 4 in W3, 4 in W4!
    for idx, item in enumerate(fresh_items):
        item["orderWeek"] = (idx % 4) + 1

    # Add Premium Complements if budget >= 350000
    if budget >= 350000:
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

    # Now calculate current_spent
    current_spent = sum(p["price"] * p["qty"] for p in product_map.values())
    
    # Scale up if under target_min
    if current_spent < target_min:
        # Scale proteins & produce in weeks 1, 2, 3, 4
        # We loop through weeks to distribute qty increases evenly!
        for loop in range(3):
            for w in [1, 2, 3, 4]:
                w_prods = [p for p in product_map.values() if p["orderWeek"] == w and p["storage"] != "seasoning"]
                w_prods.sort(key=lambda x: x["price"], reverse=True)
                for p in w_prods:
                    if current_spent >= target_min:
                        break
                    if current_spent + p["price"] <= target_max:
                        p["qty"] += 1
                        current_spent += p["price"]
                if current_spent >= target_min:
                    break
            if current_spent >= target_min:
                break

    # Strict cut if over budget
    while current_spent > budget:
        reduced = False
        for p in reversed(list(product_map.values())):
            if p["qty"] > 1:
                p["qty"] -= 1
                current_spent -= p["price"]
                reduced = True
                if current_spent <= budget:
                    break
        if not reduced:
            break

    week_totals = {
        w: sum(p["price"] * p["qty"] for p in product_map.values() if p["orderWeek"] == w)
        for w in [1, 2, 3, 4]
    }
    
    return product_map, current_spent, week_totals

for test_b in [500000, 300000, 200000]:
    pmap, spent, wtots = test_smart_budget_engine(test_b, "중식")
    print(f"=== Budget: {test_b:,}원 ===")
    print(f"Total Spent: {spent:,}원 ({spent/test_b*100:.1f}%) | <= Budget: {spent <= test_b}")
    for w in [1, 2, 3, 4]:
        items_summary = [p["name"].split()[0] for p in pmap.values() if p["orderWeek"] == w]
        print(f"  Week {w}: {wtots[w]:,}원 ({len(items_summary)}종: {', '.join(items_summary[:4])}...)")
