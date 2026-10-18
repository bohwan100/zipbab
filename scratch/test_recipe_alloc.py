import re
from generator.recipe_engine import MASTER_RECIPES, PREMIUM_COMPLEMENTS, RICE_ITEM, RICE_ITEM_PREMIUM

def test_allocation(budget=500000, cuisine="중식", household="1명", pantry="아무것도 없음"):
    people_count = 1
    total_meals = 30
    
    # 1. Cuisines
    allowed_cuisines = [c for c in ["중식", "일식", "양식", "한식"] if c in cuisine]
    if not allowed_cuisines:
        allowed_cuisines = ["한식"]
        
    cuisine_buckets = {c: [] for c in allowed_cuisines}
    for r in MASTER_RECIPES:
        if r["cuisine"] in allowed_cuisines:
            cuisine_buckets[r["cuisine"]].append(r)
            
    candidate_recipes = []
    for c in allowed_cuisines:
        candidate_recipes.extend(cuisine_buckets[c])
    if not candidate_recipes:
        candidate_recipes = MASTER_RECIPES[:]
        
    num_cand = len(candidate_recipes)
    final_recipes = []
    for day_i in range(total_meals):
        base_r = candidate_recipes[day_i % num_cand]
        final_recipes.append({
            "day": day_i + 1,
            "title": base_r["title"],
            "base_title": base_r["title"],
            "cuisine": base_r["cuisine"],
            "flag": base_r["flag"]
        })
        
    print(f"Generated {len(final_recipes)} meals. Distinct titles:", len(set(r['title'] for r in final_recipes)))
    
test_allocation()
