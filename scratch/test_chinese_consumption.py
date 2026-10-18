from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES, generate_personalized_plan

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

usage_by_prod = defaultdict(lambda: {"total_qty": 0, "unit": "", "days": []})
for r in recipes:
    day = r["day"]
    orig = next((o for o in MASTER_RECIPES if o["title"] == r["base_title"]), None)
    if not orig:
        continue
    for ing_name, qty, unit, storage, prod_name, spec, price, query in orig["base_ingredients"]:
        usage_by_prod[prod_name]["total_qty"] += qty
        usage_by_prod[prod_name]["unit"] = unit
        usage_by_prod[prod_name]["spec"] = spec
        usage_by_prod[prod_name]["storage"] = storage
        usage_by_prod[prod_name]["days"].append(day)
        usage_by_prod[prod_name]["price"] = price

print("=================== 중식 (30 days total recipe consumption) ===================")
for prod_name, data in sorted(usage_by_prod.items(), key=lambda x: (x[1]["storage"], x[0])):
    tot_used = round(data["total_qty"], 1)
    spec = data["spec"]
    st = data["storage"]
    days = data["days"]
    u = data["unit"]
    first_day = min(days)
    print(f"[{st:9s}] {prod_name:35s} | Used: {tot_used:6.1f} {u:4s} | Spec: {spec:12s} | FirstDay: D{first_day:02d} | Cooked {len(days)} times")
