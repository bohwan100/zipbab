from generator.recipe_engine import MASTER_RECIPES, generate_personalized_plan

# Test script for timing verification
res = generate_personalized_plan(
    client_name="앙기모",
    household="1명",
    budget=500000,
    frequency="하루 한 끼 (퇴근 후 저녁 30끼)",
    concept="일반식",
    cuisine="중식",
    exclude="없음",
    pantry="아무것도 없음"
)

prods = res["products"]
print("--- ALL 61 PRODUCTS IN CHINESE CART ---")
for p in prods:
    w = p["orderWeek"]
    n = p["name"]
    tot = p["total"]
    recs = p["recipes"]
    wks = p["weeks"]
    print(f"[{w}주차] {n:40s} | {tot:6,d}원 | {wks:10s} | {recs}")
