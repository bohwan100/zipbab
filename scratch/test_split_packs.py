from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES

# Let's inspect Chinese recipes and simulate the pure recipe cart engine
chinese_recipes = [r for r in MASTER_RECIPES if r["cuisine"] == "중식"]
print(f"Total Chinese Recipes: {len(chinese_recipes)}")

# Simulate 30 meals
meals = []
for d in range(30):
    r = chinese_recipes[d % len(chinese_recipes)]
    meals.append({
        "day": d + 1,
        "week": min(4, d // 7 + 1),
        "title": r["title"],
        "base_ingredients": r["base_ingredients"]
    })

# Track ingredients
# For each ingredient: which weeks is it cooked in?
ing_usage = defaultdict(lambda: {
    "days": [],
    "weeks": set(),
    "total_qty": 0,
    "unit": "",
    "storage": "",
    "prod_name": "",
    "spec": "",
    "price": 0,
    "query": "",
    "recipes": []
})

for m in meals:
    day = m["day"]
    week = m["week"]
    for ing in m["base_ingredients"]:
        name, qty, unit, storage, prod_name, spec, price, query = ing
        u = ing_usage[prod_name]
        u["days"].append(day)
        u["weeks"].add(week)
        u["total_qty"] += qty
        u["unit"] = unit
        u["storage"] = storage
        u["prod_name"] = prod_name
        u["spec"] = spec
        u["price"] = price
        u["query"] = query
        lbl = f"Day {day} {m['title'].split()[0]}"
        if lbl not in u["recipes"] and len(u["recipes"]) < 4:
            u["recipes"].append(lbl)

print("\n--- INGREDIENTS USAGE ACROSS WEEKS ---")
for prod_name, u in sorted(ing_usage.items(), key=lambda x: (x[1]["storage"], min(x[1]["weeks"]))):
    weeks_str = ", ".join(f"{w}주차" for w in sorted(u["weeks"]))
    min_w = min(u["weeks"])
    print(f"[{u['storage']:9s}] {prod_name:32s} | First Week: {min_w}주차 | Cooked in: {weeks_str} | Cooked {len(u['days'])} times")
