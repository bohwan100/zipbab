from generator.recipe_engine import MASTER_RECIPES

chinese = [r for r in MASTER_RECIPES if r["cuisine"] == "중식"]
for idx, r in enumerate(chinese):
    print(f"\n[{idx+1}] {r['title']}")
    for ing in r["base_ingredients"]:
        print(f"    - {ing[0]} {ing[1]}{ing[2]} ({ing[3]}) -> {ing[4]} | {ing[5]} | {ing[6]}원")
