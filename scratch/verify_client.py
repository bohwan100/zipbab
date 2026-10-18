import json, re

with open("clients/앙기모_31세/cart.html", "r", encoding="utf-8") as f:
    cart_content = f.read()

# Extract allProducts
m = re.search(r"const allProducts = (\[[\s\S]*?\]);", cart_content)
if m:
    prods = json.loads(m.group(1))
    print(f"Total Cart Products: {len(prods)}")
    fb = [p for p in prods if "꽃빵" in p["name"]]
    print("Flower Bun in Cart:")
    for p in fb:
        w = p["orderWeek"]
        n = p["name"]
        q = p["qty"]
        t = p["total"]
        r = p["recipes"]
        print(f"  -> id: {p['id']}, orderWeek: {w}주차, qty: {q}, total: {t}원, recipes: {r}")

    phantom = [p for p in prods if "하가우" in p["name"] or "멘보샤" in p["name"] or "샤인머스캣" in p["name"] or "오설록" in p["name"]]
    print(f"Phantom Items: {len(phantom)}")
    for p in phantom:
        print(f"  -> {p['name']}")

with open("clients/앙기모_31세/recipes.html", "r", encoding="utf-8") as f:
    recipe_content = f.read()

m2 = re.search(r"const recipes = (\[[\s\S]*?\]);", recipe_content)
if m2:
    recs = json.loads(m2.group(1))
    d8 = recs[7]
    d20 = recs[19]
    print(f"\nDay 8: {d8['title']}")
    print(f"  Ingredients: {d8['ingredients']}")
    print(f"  Waste: {d8['waste']}")
    print(f"\nDay 20: {d20['title']}")
    print(f"  Ingredients: {d20['ingredients']}")
    print(f"  Waste: {d20['waste']}")
