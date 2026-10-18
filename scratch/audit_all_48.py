from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES

print("--- AUDITING ALL 48 RECIPES IN MASTER_RECIPES ---")
for idx, r in enumerate(MASTER_RECIPES):
    title = r["title"]
    cuisine = r["cuisine"]
    for ing in r["base_ingredients"]:
        name, qty, unit, storage, prod_name, spec, price, query = ing
        # check if flower bun in non-chinese
        if "꽃빵" in name or "꽃빵" in prod_name:
            if cuisine != "중식":
                print(f"[{cuisine}] {title}: Non-chinese has flower bun: {name} / {prod_name}")
        # check steps mention
        steps = " ".join(r["steps"])
        if name not in steps and prod_name.split()[0] not in steps:
            # check if short name in steps
            short_name = name.split()[-1]
            if short_name not in steps:
                print(f"[{cuisine}] {title}: ing '{name}' not found in steps!")
