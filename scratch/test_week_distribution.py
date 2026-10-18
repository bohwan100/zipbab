from collections import defaultdict
from generator.recipe_engine import MASTER_RECIPES

chinese_recipes = [r for r in MASTER_RECIPES if r["cuisine"] == "중식"]

# Meals for 30 days
meals = []
for d in range(30):
    r = chinese_recipes[d % len(chinese_recipes)]
    meals.append({
        "day": d + 1,
        "week": min(4, d // 7 + 1),
        "title": r["title"],
        "base_ingredients": r["base_ingredients"]
    })

# Gather items
item_info = {}
for m in meals:
    day = m["day"]
    w = m["week"]
    for ing in m["base_ingredients"]:
        name, qty, unit, storage, prod_name, spec, price, query = ing
        if prod_name not in item_info:
            item_info[prod_name] = {
                "name": prod_name,
                "storage": storage,
                "spec": spec,
                "price": price,
                "query": query,
                "days": [],
                "weeks": set(),
                "recipes": []
            }
        item_info[prod_name]["days"].append(day)
        item_info[prod_name]["weeks"].add(w)
        lbl = f"Day {day} {m['title'].split()[0]}"
        if lbl not in item_info[prod_name]["recipes"] and len(item_info[prod_name]["recipes"]) < 4:
            item_info[prod_name]["recipes"].append(lbl)

# Add rice
rice_name = "임금님표이천 쌀 상등급 (10kg)"
item_info[rice_name] = {
    "name": rice_name,
    "storage": "seasoning",
    "spec": "10kg 1포",
    "price": 34900,
    "query": "임금님표이천쌀 10kg",
    "days": [1],
    "weeks": {1},
    "recipes": ["30일 전 식단 밥"]
}

# Now let's test building cart products:
# 1. Base packs: each item gets 1 pack at orderWeek = (1 if storage == 'seasoning' else min(weeks))
cart_items = []
for name, info in item_info.items():
    st = info["storage"]
    min_w = 1 if st == "seasoning" else min(info["weeks"])
    weeks_str = f"{min(info['weeks'])}~{max(info['weeks'])}주차" if min(info['weeks']) != max(info['weeks']) else f"{min(info['weeks'])}주차"
    cart_items.append({
        "name": name,
        "spec": info["spec"],
        "price": info["price"],
        "qty": 1,
        "total": info["price"],
        "storage": st,
        "orderWeek": min_w,
        "weeks": weeks_str,
        "recipes": ", ".join(info["recipes"]),
        "query": info["query"]
    })

base_total = sum(item["total"] for item in cart_items)
print(f"Base Cart (1 pack each): {len(cart_items)} items, Total: {base_total:,}원")
for w in range(1, 5):
    w_sum = sum(i["total"] for i in cart_items if i["orderWeek"] == w)
    w_cnt = len([i for i in cart_items if i["orderWeek"] == w])
    print(f"  Week {w}: {w_cnt} items, {w_sum:,}원")

# 2. Fresh multi-week replenishment (두부, 순두부, 청경채)
extra_fresh = [
    # 두부: Day 13 (W2), Day 25 (W4)
    ("풀무원 부침찌개 두부 (300g)", 2, "Day 13 사천풍", "2주차"),
    ("풀무원 부침찌개 두부 (300g)", 4, "Day 25 사천풍", "4주차"),
    # 순두부: Day 14 (W2), Day 26 (W4)
    ("풀무원 국산 순두부 (350g)", 2, "Day 14 황금", "2주차"),
    ("풀무원 국산 순두부 (350g)", 4, "Day 26 황금", "4주차"),
    # 청경채: W2, W3, W4
    ("국내산 친환경 청경채 (300g)", 2, "Day 10 탄탄풍, Day 12 마라샹궈", "2주차"),
    ("국내산 친환경 청경채 (300g)", 3, "Day 15 불맛, Day 17 굴소스, Day 18 동파육", "3주차"),
    ("국내산 친환경 청경채 (300g)", 4, "Day 22 탄탄풍, Day 24 마라샹궈, Day 27 불맛, Day 29 굴소스, Day 30 동파육", "4주차"),
]

# 3. High budget scaling (budget = 500,000원 -> target 420,000 ~ 480,000)
# Second half fresh protein & produce replenishments for W3
extra_proteins_w3 = [
    ("미국산 소고기 부채살 구이용 (1kg)", 3, "Day 17 굴소스, Day 24 마라샹궈, Day 29 굴소스", "3~4주차"),
    ("한돈 1등급 생 통삼겹살 (600g)", 3, "Day 18 동파육풍, Day 30 동파육풍", "3~4주차"),
    ("미국산 우삼겹 바로구이 (1kg)", 3, "Day 20 소고기 고추잡채", "3주차"),
    ("곰곰 해물모둠믹스 (800g)", 3, "Day 15 불맛, Day 23 유산슬풍, Day 27 불맛", "3~4주차"),
    ("한돈 불고기용 앞다리살 (1kg)", 3, "Day 13 사천풍, Day 21 어향가지, Day 22 탄탄풍, Day 25 사천풍", "3~4주차"),
    ("닭다리 순살 정육 (1kg)", 3, "Day 19 매콤 깐풍기", "3주차"),
    ("한돈 1등급 생등심 잡채용 (500g)", 3, "Day 16 바삭, Day 28 바삭 꿔바로우", "3~4주차"),
    ("풀무원 중화 생면 (4입)", 3, "Day 15 불맛, Day 22 탄탄풍, Day 27 불맛", "3~4주차"),
    ("곰곰 무항생제 신선 대란 (30구)", 3, "Day 14 황금, Day 26 황금 볶음밥", "3~4주차"),
    ("국내산 절단 대파 (500g)", 3, "3~4주차 후반 조리 대파", "3~4주차"),
    ("국내산 신선 알배기배추 (1통)", 3, "Day 15 불맛, Day 24 마라샹궈, Day 27 불맛", "3~4주차"),
    ("국내산 세척 당근 (1kg)", 4, "Day 16 바삭, Day 28 바삭 꿔바로우", "4주차"),
    ("국내산 생표고버섯 (200g)", 4, "Day 23 유산슬풍", "4주차"),
    ("국내산 신선 팽이버섯 (3입)", 4, "Day 23 유산슬풍", "4주차"),
    ("국내산 깐 양파 (1.5kg)", 4, "Day 20 소고기 고추잡채 후반 소진", "4주차"),
]

# Calculate grand total
total_sim = base_total
for p_name, w, rec, w_str in extra_fresh:
    orig = item_info[p_name]
    total_sim += orig["price"]

for p_name, w, rec, w_str in extra_proteins_w3:
    orig = item_info[p_name]
    total_sim += orig["price"]

print(f"\nScaled Grand Total: {total_sim:,}원 (Target: 400,000 ~ 500,000원)")
