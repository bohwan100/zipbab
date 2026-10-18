from generator.recipe_engine import MASTER_RECIPES, generate_personalized_plan

# Test script for splitting recipe labels between primary and replenishment packs
all_cuisines = ["중식", "일식", "양식", "한식", "한식, 일식"]

for c in all_cuisines:
    candidates = [r for r in MASTER_RECIPES if any(ac in r["cuisine"] for ac in c.split(", "))]
    print(f"\n--- Cuisine: {c} ---")
    for d in range(30):
        r = candidates[d % len(candidates)]
        day = d + 1
        week = min(4, (day - 1) // 7 + 1)
        # Check flower bun
        if "꽃빵" in str(r["base_ingredients"]):
            print(f"Day {day:02d} (Week {week}): {r['title']}")
