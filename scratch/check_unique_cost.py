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

# Unique required ingredients from recipes
unique_items = {}
for r in recipes:
    orig = next((o for o in MASTER_RECIPES if o["title"] == r["base_title"]), None)
    if not orig:
        continue
    for ing_name, qty, unit, storage, prod_name, spec, price, query in orig["base_ingredients"]:
        if prod_name not in unique_items:
            unique_items[prod_name] = {
                "name": prod_name,
                "spec": spec,
                "price": price,
                "storage": storage,
                "query": query,
                "days": []
            }
        unique_items[prod_name]["days"].append(r["day"])

# Add rice
rice_price = 34900 # 10kg
total_base_price = sum(item["price"] for item in unique_items.values()) + rice_price
print(f"Total unique recipe items: {len(unique_items)}")
print(f"Sum of 1 pack of each unique item + 10kg rice: {total_base_price:,}원")
for item in sorted(unique_items.values(), key=lambda x: (x["storage"], -x["price"])):
    print(f"[{item['storage']:9s}] {item['name']:35s} ({item['spec']:10s}) : {item['price']:,}원 | Used on days: {item['days']}")
