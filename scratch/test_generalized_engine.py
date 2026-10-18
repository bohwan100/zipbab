from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES

def run_pure_cart(cuisine="중식", budget=500000, household="1명"):
    people_count = 1
    total_meals = 30
    
    # 1. Recipes
    allowed = [c for c in ["중식", "일식", "양식", "한식"] if c in cuisine]
    if not allowed:
        allowed = ["한식"]
    candidates = [r for r in MASTER_RECIPES if r["cuisine"] in allowed]
    recipes_list = []
    for day_i in range(total_meals):
        base_r = candidates[day_i % len(candidates)]
        recipes_list.append({
            "day": day_i + 1,
            "title": base_r["title"],
            "base_ingredients": base_r["base_ingredients"]
        })

    # Budget target
    if budget >= 400000:
        target_min = int(budget * 0.85)  # 425,000 for 500k
        target_max = int(budget * 0.98)  # 490,000 for 500k
    elif budget >= 250000:
        target_min = int(budget * 0.80)
        target_max = int(budget * 0.95)
    else:
        target_min = int(budget * 0.75)
        target_max = int(budget * 0.95)

    # Gather items from recipes
    ing_map = {}
    for r in recipes_list:
        day = r["day"]
        week = min(4, (day - 1) // 7 + 1)
        for ing in r["base_ingredients"]:
            name, qty, unit, storage, prod_name, spec, price, query = ing
            if prod_name not in ing_map:
                ing_map[prod_name] = {
                    "name": prod_name,
                    "spec": spec,
                    "price": price,
                    "storage": storage,
                    "query": query,
                    "days": [],
                    "weeks": set(),
                    "recipes": [],
                    "total_recipe_qty": 0,
                    "unit": unit
                }
            ing_map[prod_name]["days"].append(day)
            ing_map[prod_name]["weeks"].add(week)
            ing_map[prod_name]["total_recipe_qty"] += qty
            lbl = f"Day {day} {r['title'].split()[0]}"
            if lbl not in ing_map[prod_name]["recipes"] and len(ing_map[prod_name]["recipes"]) < 4:
                ing_map[prod_name]["recipes"].append(lbl)

    # Rice
    rice_name = "임금님표이천 쌀 상등급 (10kg)" if budget >= 400000 else ("곰곰 2024년 햅쌀 (4kg)" if budget >= 250000 else "임금님표이천 쌀 상등급 (2kg)")
    rice_price = 34900 if budget >= 400000 else (14900 if budget >= 250000 else 10800)
    rice_spec = "10kg 1포" if budget >= 400000 else ("4kg 1포" if budget >= 250000 else "2kg 1포")
    ing_map[rice_name] = {
        "name": rice_name,
        "spec": rice_spec,
        "price": rice_price,
        "storage": "seasoning",
        "query": rice_name,
        "days": [1],
        "weeks": {1},
        "recipes": ["30일 전 식단 밥"],
        "total_recipe_qty": 3000,
        "unit": "g"
    }

    # Items that must NOT be duplicated (fixed discrete count matching recipes 100%)
    NON_DUPLICABLE = ["꽃빵", "햄버거번", "바게트", "가지", "파프리카"]

    cart_items = []
    # 1. Base pack for all items
    for prod_name, info in ing_map.items():
        st = info["storage"]
        min_w = 1 if st == "seasoning" else min(info["weeks"])
        weeks_str = f"{min(info['weeks'])}~{max(info['weeks'])}주차" if min(info['weeks']) != max(info['weeks']) else f"{min(info['weeks'])}주차"
        cat = "🧂 조미료" if st == "seasoning" else ("🥬 신선식품" if st == "fresh" else "❄️ 냉동식품")
        cart_items.append({
            "name": prod_name,
            "spec": info["spec"],
            "unitPrice": info["price"],
            "qty": 1,
            "total": info["price"],
            "storage": st,
            "cat": cat,
            "orderWeek": min_w,
            "weeks": weeks_str,
            "recipes": ", ".join(info["recipes"]),
            "query": info["query"]
        })

    # 2. Perishable weekly fresh items (Tofu, Soft Tofu, Bok Choy, Bean Sprouts)
    for prod_name, info in ing_map.items():
        if info["storage"] == "fresh":
            if "두부" in prod_name and "순두부" not in prod_name:
                for later_w in [2, 4]:
                    if later_w in info["weeks"]:
                        cart_items.append({
                            "name": f"{prod_name} [{later_w}주차 신선보충]",
                            "spec": info["spec"],
                            "unitPrice": info["price"],
                            "qty": 1,
                            "total": info["price"],
                            "storage": "fresh",
                            "cat": "🥬 신선식품",
                            "orderWeek": later_w,
                            "weeks": f"{later_w}주차",
                            "recipes": f"{later_w}주차 마파두부 소진용",
                            "query": info["query"]
                        })
            elif "순두부" in prod_name:
                for later_w in [2, 4]:
                    if later_w in info["weeks"]:
                        cart_items.append({
                            "name": f"{prod_name} [{later_w}주차 신선보충]",
                            "spec": info["spec"],
                            "unitPrice": info["price"],
                            "qty": 1,
                            "total": info["price"],
                            "storage": "fresh",
                            "cat": "🥬 신선식품",
                            "orderWeek": later_w,
                            "weeks": f"{later_w}주차",
                            "recipes": f"{later_w}주차 순두부탕 소진용",
                            "query": info["query"]
                        })
            elif "청경채" in prod_name:
                for later_w in [2, 3, 4]:
                    if later_w in info["weeks"]:
                        cart_items.append({
                            "name": f"{prod_name} [{later_w}주차 신선보충]",
                            "spec": info["spec"],
                            "unitPrice": info["price"],
                            "qty": 1,
                            "total": info["price"],
                            "storage": "fresh",
                            "cat": "🥬 신선식품",
                            "orderWeek": later_w,
                            "weeks": f"{later_w}주차",
                            "recipes": f"{later_w}주차 청경채 소진용",
                            "query": info["query"]
                        })

    # 3. High budget scaling (budget >= 350,000)
    current_spent = sum(item["total"] for item in cart_items)
    if current_spent < target_min:
        # Scale actual recipe proteins and produce for second half (W3 or W4)
        scalable = []
        for prod_name, info in ing_map.items():
            if any(nd in prod_name for nd in NON_DUPLICABLE):
                continue
            if info["storage"] in ["fresh", "frozen"]:
                # Check if cooked in W3 or W4
                if any(w in [3, 4] for w in info["weeks"]):
                    scalable.append(info)

        # Sort: meats/proteins first, then high price
        def sort_key(x):
            is_prot = any(k in x["name"] for k in ["살", "고기", "육", "등심", "삼겹", "우삼겹", "새우", "연어", "바지락", "해물", "치킨", "대란", "생면"])
            return (0 if is_prot else 1, -x["price"])

        scalable.sort(key=sort_key)

        for p_info in scalable:
            if current_spent >= target_min:
                break
            if current_spent + p_info["price"] <= target_max:
                w_order = 3 if 3 in p_info["weeks"] else 4
                cart_items.append({
                    "name": f"{p_info['name']} [{w_order}주차 2차 신선보충]",
                    "spec": p_info["spec"],
                    "unitPrice": p_info["price"],
                    "qty": 1,
                    "total": p_info["price"],
                    "storage": p_info["storage"],
                    "cat": "🥬 신선식품" if p_info["storage"] == "fresh" else "❄️ 냉동식품",
                    "orderWeek": w_order,
                    "weeks": f"{w_order}~4주차",
                    "recipes": f"3~4주차 후반 소진용 ({', '.join(p_info['recipes'][:2])})",
                    "query": p_info["query"]
                })
                current_spent += p_info["price"]

    # If still below target_min (e.g. for huge budgets like 600k+), allow second round of proteins for multi-week
    if current_spent < target_min:
        for p_info in scalable:
            if current_spent >= target_min:
                break
            if current_spent + p_info["price"] <= target_max:
                w_order = 4 if 4 in p_info["weeks"] else 3
                cart_items.append({
                    "name": f"{p_info['name']} [4주차 파이널 보충]",
                    "spec": p_info["spec"],
                    "unitPrice": p_info["price"],
                    "qty": 1,
                    "total": p_info["price"],
                    "storage": p_info["storage"],
                    "cat": "🥬 신선식품" if p_info["storage"] == "fresh" else "❄️ 냉동식품",
                    "orderWeek": w_order,
                    "weeks": "4주차",
                    "recipes": f"4주차 완판 소진용 ({', '.join(p_info['recipes'][:2])})",
                    "query": p_info["query"]
                })
                current_spent += p_info["price"]

    # Budget Guard
    while current_spent > budget:
        removed = cart_items.pop()
        current_spent -= removed["total"]

    print(f"\n=================== {cuisine} RESULT (Budget: {budget:,}원) ===================")
    print(f"Total Cart Items: {len(cart_items)}")
    print(f"Total Spent: {current_spent:,}원 (Target: {target_min:,} ~ {target_max:,}원, Ceiling: {budget:,}원)")
    for w in range(1, 5):
        w_items = [i for i in cart_items if i["orderWeek"] == w]
        w_sum = sum(i["total"] for i in w_items)
        print(f"  [{w}주차] {len(w_items):2d} items | {w_sum:7,d}원")
    
    # Check 꽃빵
    fb = [i for i in cart_items if "꽃빵" in i["name"]]
    print(f"꽃빵 items count: {len(fb)}")
    for f in fb:
        print(f"  -> [{f['orderWeek']}주차] {f['name']} ({f['spec']}) | recipes: {f['recipes']}")

run_pure_cart("중식", 500000)
run_pure_cart("일식", 500000)
run_pure_cart("양식", 500000)
run_pure_cart("한식", 500000)
