import sys
sys.path.append('.')
from generator.recipe_engine import MASTER_RECIPES, PREMIUM_COMPLEMENTS, RICE_ITEM, RICE_ITEM_PREMIUM

def simulate_distribution(budget=500000, cuisine="중식", household="1명", pantry="아무것도 없음"):
    people_count = 1
    total_meals = 30
    allowed_cuisines = [c for c in ["중식", "일식", "양식", "한식"] if c in cuisine] or ["한식"]
    
    # Target range:
    # If budget == 500,000: target is 430,000 ~ 485,000 (strictly <= 500,000)
    # In general: target_min = int(budget * 0.85), target_max = int(budget * 0.97)
    target_min = int(budget * 0.85)
    target_max = int(budget * 0.97)
    
    # 1. 30 recipes
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
        
    # 2. Seasonings & Rice in Week 1
    seasonings = {}
    rice = RICE_ITEM_PREMIUM if budget >= 400000 else RICE_ITEM
    seasonings[rice[4]] = {
        "storage": rice[3], "cat": "🧂 조미료", "name": rice[4], "spec": rice[5],
        "price": rice[6], "query": rice[7], "orderWeek": 1,
        "recipes": ["30일 전 식단 밥"], "weeks": "1~4주차", "qty": 1
    }
    
    # Collect all seasonings from recipes
    for r in final_recipes:
        matched_orig = next((orig for orig in MASTER_RECIPES if orig["title"] in r["title"] or orig["title"] == r.get("base_title")), None)
        if not matched_orig: continue
        for ing_name, qty, unit, storage, prod_name, spec, price, query in matched_orig["base_ingredients"]:
            if storage == "seasoning":
                if prod_name not in seasonings:
                    seasonings[prod_name] = {
                        "storage": storage, "cat": "🧂 조미료", "name": prod_name, "spec": spec,
                        "price": price, "query": query, "orderWeek": 1,
                        "recipes": [f"Day {r['day']} {matched_orig['title'].split()[0]}"],
                        "weeks": "1~4주차", "qty": 1
                    }
                else:
                    if len(seasonings[prod_name]["recipes"]) < 3:
                        seasonings[prod_name]["recipes"].append(f"Day {r['day']} {matched_orig['title'].split()[0]}")
                        
    # 3. Weekly fresh & frozen items per week (Weeks 1, 2, 3, 4)
    weekly_items = {1: {}, 2: {}, 3: {}, 4: {}}
    for r in final_recipes:
        day = r["day"]
        w = min(4, (day - 1) // 7 + 1)
        matched_orig = next((orig for orig in MASTER_RECIPES if orig["title"] in r["title"] or orig["title"] == r.get("base_title")), None)
        if not matched_orig: continue
        for ing_name, qty, unit, storage, prod_name, spec, price, query in matched_orig["base_ingredients"]:
            if storage != "seasoning":
                if prod_name not in weekly_items[w]:
                    cat = "🥬 신선식품" if storage == "fresh" else "❄️ 냉동식품"
                    weekly_items[w][prod_name] = {
                        "storage": storage, "cat": cat, "name": prod_name, "spec": spec,
                        "price": price, "query": query, "orderWeek": w,
                        "recipes": [f"Day {day} {matched_orig['title'].split()[0]}"],
                        "weeks": f"{w}주차", "qty": 1
                    }
                else:
                    if len(weekly_items[w][prod_name]["recipes"]) < 3:
                        weekly_items[w][prod_name]["recipes"].append(f"Day {day} {matched_orig['title'].split()[0]}")

    # 4. If budget < 400000, deduplicate high-cost frozen meats across weeks
    if budget < 400000:
        seen_frozen = set()
        for w in [1, 2, 3, 4]:
            for p_name in list(weekly_items[w].keys()):
                item = weekly_items[w][p_name]
                if item["storage"] == "frozen":
                    if p_name in seen_frozen:
                        del weekly_items[w][p_name]
                    else:
                        seen_frozen.add(p_name)
                        
    # If budget < 250000, also consolidate fresh vegetables if bought in week 1/2
    if budget < 250000:
        for w in [3, 4]:
            for p_name in list(weekly_items[w].keys()):
                item = weekly_items[w][p_name]
                # If already bought in week 1 or 2 and total would exceed budget, drop
                # Keep essentials
                pass

    all_prods = list(seasonings.values())
    for w in [1, 2, 3, 4]:
        all_prods.extend(weekly_items[w].values())

    # Add Premium Complements if budget >= 350000
    if budget >= 350000:
        prime_list = []
        for c in allowed_cuisines:
            prime_list.extend(PREMIUM_COMPLEMENTS.get(c, []))
        if not prime_list:
            prime_list = PREMIUM_COMPLEMENTS["한식"]
        for p_name, p_spec, p_price, p_storage, p_query, p_week, p_note in prime_list:
            all_prods.append({
                "storage": p_storage,
                "cat": "🥬 신선식품" if p_storage == "fresh" else ("❄️ 냉동식품" if p_storage == "frozen" else "🧂 조미료"),
                "name": p_name, "spec": p_spec, "price": p_price, "query": p_query,
                "orderWeek": p_week, "recipes": [p_note], "weeks": f"{p_week}주차", "qty": 1
            })

    # Calculate spent
    current_spent = sum(p["price"] * p["qty"] for p in all_prods)
    
    # Scale if under budget
    if current_spent < target_min:
        for p in all_prods:
            if current_spent >= target_min:
                break
            if any(k in p["name"] for k in ["앞다리살", "우삼겹", "부채살", "삼겹살", "새우", "해물", "닭다리살", "생등심"]):
                if current_spent + p["price"] <= target_max:
                    p["qty"] += 1
                    current_spent += p["price"]

    # Budget cut if over budget
    while current_spent > budget:
        # Find item with qty > 1
        reduced = False
        for p in reversed(all_prods):
            if p["qty"] > 1:
                p["qty"] -= 1
                current_spent -= p["price"]
                reduced = True
                break
        if not reduced:
            # Drop lowest priority item from week 4 or 3
            drop_candidates = [p for p in all_prods if p["orderWeek"] in [3, 4] and p["storage"] != "seasoning"]
            if drop_candidates:
                drop_candidates.sort(key=lambda x: x["price"], reverse=True)
                drop_p = drop_candidates[0]
                all_prods.remove(drop_p)
                current_spent -= drop_p["price"]
            else:
                break

    week_totals = {
        w: sum(p["price"] * p["qty"] for p in all_prods if p["orderWeek"] == w)
        for w in [1, 2, 3, 4]
    }
    
    # Check minimum order rule (15,000원)
    for w in [2, 3, 4]:
        if week_totals[w] < 15000:
            # Shift an item from week 1 to week w if needed
            for p in all_prods:
                if p["orderWeek"] == 1 and p["price"] >= 15000 and "쌀" not in p["name"]:
                    p["orderWeek"] = w
                    p["weeks"] = f"{w}주차"
                    week_totals[1] -= p["price"] * p["qty"]
                    week_totals[w] += p["price"] * p["qty"]
                    break

    return all_prods, current_spent, week_totals

for b in [500000, 300000, 200000]:
    prods, spent, w_tots = simulate_distribution(b, "중식")
    print(f"=== Budget: {b:,}원 ===")
    print(f"Total Spent: {spent:,}원 ({spent/b*100:.1f}%) | Under Budget: {spent <= b}")
    for w in [1, 2, 3, 4]:
        w_items = [p["name"].split()[0] for p in prods if p["orderWeek"] == w][:5]
        print(f"  Week {w}: {w_tots[w]:,}원 ({', '.join(w_items)}...)")
