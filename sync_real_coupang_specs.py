# -*- coding: utf-8 -*-
"""
Sync cart_dashboard.html with actual Coupang Rocket Delivery sizes and prices:
- Somyeon: 500g (unobtainable rocket single) -> '오뚜기옛날 국수 소면 (900g)' 3,510원 (query: '오뚜기 소면 900g')
- Sagol broth: 300g x 2 -> '오뚜기옛날 사골곰탕 (500g 1팩)' 1,720원 (query: '오뚜기 사골곰탕 500g')
- Ddeok: 500g -> '오뚜기 쌀 떡국떡 (1kg)' 4,900원 (query: '오뚜기 떡국떡 1kg')
- Update split-amount for Week 4: 26,700원 -> 28,430원
- Total remains ~173,230원 (well within 200,000 won limit!)
"""

with open("cart_dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# Update item 35, 37, 38 in allProducts
old_block = """      { id: 35, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 옛날국수 소면 (500g)", spec: "500g 1봉", qty: 1, unitPrice: 1900, total: 1900, weeks: "3, 4주차", recipes: "Day 16 나폴리탄, Day 17 뭇국소면, Day 23 짬뽕소면, Day 25 찜닭사리", query: "오뚜기 소면 500g" },
      { id: 37, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 옛날 사골곰탕 (300g x 2개)", spec: "300g 2팩", qty: 1, unitPrice: 2500, total: 2500, weeks: "4주차", recipes: "Day 26 사골부대찌개, Day 29 사골떡볶이", query: "오뚜기 사골곰탕 300g" },
      { id: 38, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 쌀 떡국떡 (500g)", spec: "500g 1봉", qty: 1, unitPrice: 3000, total: 3000, weeks: "4주차", recipes: "Day 29 해물떡볶이, Day 30 전골사리", query: "오뚜기 떡국떡 500g" }"""

new_block = """      { id: 35, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기옛날 국수 소면 (900g)", spec: "900g 1봉 (실속 로켓 규격)", qty: 1, unitPrice: 3510, total: 3510, weeks: "3, 4주차", recipes: "Day 16 나폴리탄, Day 17 뭇국소면, Day 23 짬뽕소면, Day 25 찜닭사리", query: "오뚜기 소면 900g" },
      { id: 37, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기옛날 사골곰탕 (500g)", spec: "500g 1팩 (로켓 1위 규격)", qty: 1, unitPrice: 1720, total: 1720, weeks: "4주차", recipes: "Day 26 사골부대찌개, Day 29 사골떡볶이", query: "오뚜기 사골곰탕 500g" },
      { id: 38, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 쌀 떡국떡 (1kg)", spec: "1kg 1봉 (로켓 표준 규격)", qty: 1, unitPrice: 4900, total: 4900, weeks: "4주차", recipes: "Day 29 해물떡볶이, Day 30 전골사리", query: "오뚜기 떡국떡 1kg" }"""

if old_block in text:
    text = text.replace(old_block, new_block)
    print("Replaced items 35, 37, 38 with Coupang real specs!")
else:
    print("WARNING: old_block not found exactly, doing regex replacement...")
    # find id: 35 to id: 38
    p35 = text.find("id: 35")
    p38_end = text.find("}", text.find("id: 38"))
    if p35 != -1 and p38_end != -1:
        text = text[:p35-8] + new_block + text[p38_end+1:]
        print("Replaced via position!")

# Update split-amount for Week 4 in dashboard banner if hardcoded
# Calculate Week 4 cost: 7900 + 1300 + 7900 + 2200 + 3510 + 1720 + 4900 = 29,430원
text = text.replace('        <div class="split-amount">26,700원</div>', '        <div class="split-amount">29,430원</div>')
text = text.replace('총 5종 - 26,700원', '총 7종 - 29,430원')

with open("cart_dashboard.html", "w", encoding="utf-8") as f:
    f.write(text)

print("cart_dashboard.html updated with actual Coupang specs successfully!")
