from generator.recipe_engine import MASTER_RECIPES

print("Total MASTER_RECIPES:", len(MASTER_RECIPES))
for r in MASTER_RECIPES:
    title = r["title"]
    cuisine = r["cuisine"]
    step_text = " ".join(r["steps"])
    ing_names = [ing[0] for ing in r["base_ingredients"]]
    prod_names = [ing[4] for ing in r["base_ingredients"]]
    
    # Check if any ingredient is flower bun in non-chinese
    if "꽃빵" in str(ing_names) and cuisine != "중식":
        print(f"WARNING: Non-chinese recipe with flower bun: [{cuisine}] {title} -> {ing_names}")
