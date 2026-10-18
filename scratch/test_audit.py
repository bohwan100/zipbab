from generator.recipe_engine import generate_personalized_plan, MASTER_RECIPES

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
products = res["products"]
summary = res

print("Total products:", len(products))
print("Total spent:", summary.get("total_spent", 0))
for p in products:
    w = p["orderWeek"]
    n = p["name"]
    s = p["spec"]
    q = p["qty"]
    r = p["recipes"]
    tot = p["total"]
    print(f"[{w}주차] {n} ({s}) x{q} = {tot}원 | 연결: {r}")
