from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES

# Let's inspect all 4 cuisines
for c in ["중식", "일식", "양식", "한식"]:
    cuisine_recipes = [r for r in MASTER_RECIPES if r["cuisine"] == c]
    print(f"\n=================== {c} Recipes ({len(cuisine_recipes)}) ===================")
    for r in cuisine_recipes:
        ings = [f"{ing[0]}({ing[1]}{ing[2]})" for ing in r["base_ingredients"][:4]]
        print(f" - {r['title']}: {', '.join(ings)}")
