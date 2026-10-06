# -*- coding: utf-8 -*-
"""
Unbundle artificially merged items in cart_dashboard.html:
1. Item 35: '오뚜기 소면 & 사골육수 & 떡' (7,400원) -> Split into:
   - 오뚜기 옛날국수 소면 (500g): 1,900원 (query: '오뚜기 소면 500g')
   - 오뚜기 옛날 사골곰탕 (300g x 2개): 2,500원 (query: '오뚜기 사골곰탕 300g')
   - 오뚜기 쌀 떡국떡 (500g): 3,000원 (query: '오뚜기 떡국떡 500g')
2. Item 34: '오뚜기 카레 & 짜장가루' (4,000원) -> Split into:
   - 오뚜기 카레 약간매운맛 (100g): 1,900원 (query: '오뚜기 카레 약간매운맛 100g')
   - 오뚜기 직접볶은 짜장가루 (100g): 2,100원 (query: '오뚜기 짜장가루 100g')
"""

with open("cart_dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# Replace Item 34 in allProducts
old_item_34 = '{ id: 34, orderWeek: 2, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 카레 & 짜장가루", spec: "카레 100g + 짜장 100g", qty: 1, unitPrice: 4000, total: 4000, weeks: "2, 3주차", recipes: "Day 14 일식 양파카레, Day 15 양배추 간짜장밥, Day 20 카레볶음밥", query: "오뚜기 카레 약간매운맛 100g" }'

new_item_34 = """      { id: 34, orderWeek: 2, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 카레 약간매운맛 (100g)", spec: "100g 1봉", qty: 1, unitPrice: 1900, total: 1900, weeks: "2, 3주차", recipes: "Day 14 일식 양파카레, Day 20 치킨 카레 볶음밥", query: "오뚜기 카레 약간매운맛 100g" },
      { id: 36, orderWeek: 2, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 직접볶은 짜장가루 (100g)", spec: "100g 1봉", qty: 1, unitPrice: 2100, total: 2100, weeks: "3주차", recipes: "Day 15 양배추 간짜장밥", query: "오뚜기 짜장가루 100g" }"""

if old_item_34 in text:
    text = text.replace(old_item_34, new_item_34)
    print("Replaced Item 34!")
else:
    print("WARNING: old_item_34 not found directly, checking substring...")
    pos = text.find('id: 34')
    if pos != -1:
        line_end = text.find('\n', pos)
        text = text[:pos-8] + new_item_34 + text[line_end:]
        print("Replaced Item 34 via position!")

# Replace Item 35 in allProducts
old_item_35 = '{ id: 35, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 소면 & 사골육수 & 떡", spec: "소면500g+사골2팩+떡500g", qty: 1, unitPrice: 7400, total: 7400, weeks: "3, 4주차", recipes: "Day 16 나폴리탄, Day 17 뭇국소면, Day 23 짬뽕소면, Day 25 찜닭사리, Day 26 부대찌개, Day 29 떡볶이", query: "오뚜기 소면 500g" }'

new_item_35 = """      { id: 35, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 옛날국수 소면 (500g)", spec: "500g 1봉", qty: 1, unitPrice: 1900, total: 1900, weeks: "3, 4주차", recipes: "Day 16 나폴리탄, Day 17 뭇국소면, Day 23 짬뽕소면, Day 25 찜닭사리", query: "오뚜기 소면 500g" },
      { id: 37, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 옛날 사골곰탕 (300g x 2개)", spec: "300g 2팩", qty: 1, unitPrice: 2500, total: 2500, weeks: "4주차", recipes: "Day 26 사골부대찌개, Day 29 사골떡볶이", query: "오뚜기 사골곰탕 300g" },
      { id: 38, orderWeek: 4, storage: "seasoning", cat: "🧂 조미료", name: "오뚜기 쌀 떡국떡 (500g)", spec: "500g 1봉", qty: 1, unitPrice: 3000, total: 3000, weeks: "4주차", recipes: "Day 29 해물떡볶이, Day 30 전골사리", query: "오뚜기 떡국떡 500g" }"""

if old_item_35 in text:
    text = text.replace(old_item_35, new_item_35)
    print("Replaced Item 35!")
else:
    print("WARNING: old_item_35 not found directly, checking substring...")
    pos = text.find('id: 35')
    if pos != -1:
        line_end = text.find('\n', pos)
        text = text[:pos-8] + new_item_35 + text[line_end:]
        print("Replaced Item 35 via position!")

with open("cart_dashboard.html", "w", encoding="utf-8") as f:
    f.write(text)

print("cart_dashboard.html updated successfully with properly unbundled items!")
