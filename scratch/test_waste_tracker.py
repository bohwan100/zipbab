from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES

chinese_recipes = [r for r in MASTER_RECIPES if r["cuisine"] == "중식"]
total_meals = 30

# Calculate total usage for each ingredient across 30 days
totals = defaultdict(float)
units = {}
for day_i in range(total_meals):
    r = chinese_recipes[day_i % len(chinese_recipes)]
    for ing in r["base_ingredients"]:
        name, qty, unit, storage, prod_name, spec, price, query = ing
        if storage != "seasoning":
            totals[name] += qty
            units[name] = unit

# Now simulate daily tracking
cum_usage = defaultdict(float)
for day_i in range(total_meals):
    day_num = day_i + 1
    r = chinese_recipes[day_i % len(chinese_recipes)]
    day_parts = []
    
    # Pick top 2-3 non-seasoning ingredients
    tracked_ings = [ing for ing in r["base_ingredients"] if ing[3] != "seasoning"]
    for ing in tracked_ings[:2]:
        name, qty, unit, storage, prod_name, spec, price, query = ing
        cum_usage[name] += qty
        total_for_ing = totals[name]
        pct = min(100, round((cum_usage[name] / total_for_ing) * 100))
        
        # Format cleanly
        qty_str = f"{int(qty)}" if qty == int(qty) else f"{qty:.1f}"
        cum_str = f"{int(cum_usage[name])}" if cum_usage[name] == int(cum_usage[name]) else f"{cum_usage[name]:.1f}"
        tot_str = f"{int(total_for_ing)}" if total_for_ing == int(total_for_ing) else f"{total_for_ing:.1f}"
        
        if pct == 100:
            day_parts.append(f"{name} {qty_str}{unit} 소진 (누적 {cum_str}/{tot_str}{unit}, 100% 완판 소진!)")
        else:
            day_parts.append(f"{name} {qty_str}{unit} 소진 (누적 {cum_str}/{tot_str}{unit}, {pct}%)")

    overall_pct = min(100, max(3, round((day_num / total_meals) * 100)))
    waste_text = f"누적 {overall_pct}% 식단 소진 | " + ", ".join(day_parts)
    if day_num in [1, 4, 6, 8, 9, 13, 16, 18, 20, 21, 28, 30]:
        print(f"Day {day_num:02d} [{r['title']}]:\n  -> {waste_text}\n")
