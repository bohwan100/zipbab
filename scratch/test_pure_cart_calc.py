from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES, generate_personalized_plan

# Test script for pure recipe cart calculation
res = generate_personalized_plan(
    cuisine="중식",
    household="1명",
    budget=500000,
    frequency="하루 한 끼 (퇴근 후 저녁 30끼)",
    concept="일반식",
    exclude="없음",
    pantry="아무것도 없음"
)
recipes = res["recipes"]

# Let us see how many items are currently in recipes
print("30 Days Recipes:")
for r in recipes[:8]:
    print(f"Day {r['day']}: {r['title']}")
print("...")
for r in recipes[19:22]:
    print(f"Day {r['day']}: {r['title']}")
