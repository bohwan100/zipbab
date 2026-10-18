from generator.recipe_engine import generate_personalized_plan

cuisines = ["중식", "일식", "양식", "한식", "한식, 일식"]
all_passed = True

print("=================================================================")
print("          ALL CUISINES FULL AUDIT & VERIFICATION")
print("=================================================================")

for c in cuisines:
    plan = generate_personalized_plan(
        client_name="테스트",
        household="1명",
        budget=500000,
        frequency="하루 한 끼 (퇴근 후 저녁 30끼)",
        concept="일반식",
        cuisine=c,
        exclude="없음",
        pantry="아무것도 없음"
    )
    spent = plan["total_spent"]
    prods = plan["products"]
    recipes = plan["recipes"]
    week_totals = plan["week_totals"]

    # Invariant 1: Budget range
    in_range = 400000 <= spent <= 500000
    if not in_range:
        print(f"[FAIL] {c}: Spent {spent:,}원 out of 400k~500k range!")
        all_passed = False

    # Invariant 2: Delivery timing orderWeek <= min_week of cooking
    timing_ok = True
    for p in prods:
        w = p["orderWeek"]
        # If it has recipes, verify
        recs = p["recipes"]
        if "Day" in recs:
            import re
            day_matches = [int(x) for x in re.findall(r'Day\s*(\d+)', recs)]
            if day_matches:
                min_cook_day = min(day_matches)
                min_cook_week = (min_cook_day - 1) // 7 + 1
                if w > min_cook_week:
                    print(f"[FAIL] {c}: {p['name']} ordered in Week {w} but cooked on Day {min_cook_day} (Week {min_cook_week})!")
                    timing_ok = False
                    all_passed = False
    
    # Invariant 3: No unconnected / phantom items
    phantoms = [p for p in prods if any(k in p["name"] for k in ["딤섬", "멘보샤", "샤인머스캣", "오설록", "샐러드팩"])]
    if phantoms:
        print(f"[FAIL] {c}: Phantom items found: {[p['name'] for p in phantoms]}")
        all_passed = False

    # Invariant 4: 꽃빵 only in Chinese
    flower_buns = [p for p in prods if "꽃빵" in p["name"]]
    if c != "중식" and flower_buns:
        print(f"[FAIL] {c}: Flower bun found in non-chinese: {[p['name'] for p in flower_buns]}")
        all_passed = False
    if c == "중식" and len(flower_buns) != 1:
        print(f"[FAIL] {c}: Chinese expected 1 flower bun pack, found {len(flower_buns)}")
        all_passed = False
    if c == "중식" and flower_buns:
        if flower_buns[0]["orderWeek"] != 2:
            print(f"[FAIL] Chinese flower bun must be ordered in Week 2, found Week {flower_buns[0]['orderWeek']}")
            all_passed = False

    print(f"[{c:10s}] Total: {spent:7,d}원 | W1:{week_totals[1]:7,d} | W2:{week_totals[2]:7,d} | W3:{week_totals[3]:7,d} | W4:{week_totals[4]:7,d} | Prods: {len(prods):2d} | Timing: {'OK' if timing_ok else 'ERR'} | Range: {'OK' if in_range else 'ERR'}")

print("=================================================================")
if all_passed:
    print(">>> ALL CUISINES VERIFIED 100% PERFECT! <<<")
else:
    print(">>> ERRORS FOUND! <<<")
print("=================================================================")
