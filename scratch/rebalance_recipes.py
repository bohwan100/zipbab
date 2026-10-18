import json, re

with open('recipe_viewer.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const recipes = (\[.*?\]);', html, re.DOTALL)
if not m:
    print("Recipes not found!")
    exit(1)

recipes = json.loads(m.group(1))

# Adjustments for realistic 1-person meal balance
for r in recipes:
    day = r['day']
    
    if day == 11:
        r['ingredients'] = [i.replace('양배추 250g', '양배추 140g') for i in r['ingredients']]
        r['steps'] = [s.replace('양배추 250g', '양배추 140g') for s in r['steps']]
        r['waste'] = "우삼겹 120g 소진, 양배추 140g 소진"
        r['cal'] = "630.0"
        
    elif day == 13:
        r['ingredients'] = [
            i.replace('돼지 앞다리살 170g', '돼지 앞다리살 130g')
             .replace('맛김치 200g', '맛김치 120g')
             .replace('무 200g', '무 120g')
            for i in r['ingredients']
        ]
        r['steps'] = [
            s.replace('앞다리살 170g', '앞다리살 130g')
             .replace('김치 200g', '김치 120g')
             .replace('무 200g', '무 120g')
            for s in r['steps']
        ]
        r['waste'] = "앞다리살 130g 소진, 김치 120g 소진, 무 120g 소진"
        r['cal'] = "620.0"
        
    elif day == 15:
        r['ingredients'] = [i.replace('양배추 250g', '양배추 140g') for i in r['ingredients']]
        r['steps'] = [s.replace('양배추 250g', '양배추 140g') for s in r['steps']]
        r['waste'] = "앞다리살 150g 소진, 양배추 140g 소진"
        r['cal'] = "640.0"
        
    elif day == 17:
        r['ingredients'] = [
            i.replace('무 250g', '무 130g')
             .replace('소면 100g', '소면 70g')
            for i in r['ingredients']
        ]
        r['steps'] = [
            s.replace('무 250g', '무 130g')
             .replace('소면 100g', '소면 70g')
            for s in r['steps']
        ]
        r['waste'] = "소고기 양지 80g 소진, 무 130g 소진, 소면 70g 소진"
        r['cal'] = "610.0"
        
    elif day == 23:
        r['ingredients'] = [
            i.replace('순두부 350g', '순두부 180g (반 봉)')
             .replace('해물믹스 150g', '해물믹스 100g')
             .replace('소면 100g', '소면 70g')
            for i in r['ingredients']
        ]
        r['steps'] = [
            s.replace('해물믹스 150g', '해물믹스 100g')
             .replace('순두부 350g', '순두부 180g')
             .replace('소면 100g', '소면 70g')
            for s in r['steps']
        ]
        r['waste'] = "순두부 180g 소진, 해물믹스 100g 소진, 소면 70g 소진"
        r['cal'] = "580.0"

    elif day == 25:
        r['ingredients'] = [
            i.replace('닭다리살 240g', '닭다리살 160g')
             .replace('소면 100g', '소면 70g')
            for i in r['ingredients']
        ]
        r['steps'] = [
            s.replace('닭다리살 240g', '닭다리살 160g')
             .replace('소면 100g', '소면 70g')
            for s in r['steps']
        ]
        r['waste'] = "닭다리살 160g 소진, 감자 1개 소진, 소면 70g 소진"
        r['cal'] = "640.0"
        
    elif day == 26:
        r['ingredients'] = [
            "스팸 80g",
            "비엔나 소시지 5알 (60g)",
            "떡국떡 70g",
            "사각어묵 50g (1장)",
            "사골곰탕 250ml (반 팩)",
            "맛김치 80g",
            "두부 80g",
            "대파 1/2대",
            "물 150ml",
            "고춧가루 1T",
            "고추장 0.5T",
            "진간장 0.5T",
            "된장 0.2T",
            "다진마늘 0.5T"
        ]
        r['steps'] = [
            "냄비에 썬 스팸, 비엔나, 떡국떡, 어묵, 김치, 두부를 둘러 담습니다.",
            "고춧가루 1T, 고추장 0.5T, 진간장 0.5T, 된장 0.2T, 다진마늘 0.5T를 가운데 올립니다.",
            "사골육수 250ml와 물 150ml를 붓고 끓입니다.",
            "끓어오르면 중불로 줄여 5분간 끓입니다.",
            "대파를 넣고 1분간 더 끓여 밥과 함께 먹습니다."
        ]
        r['waste'] = "스팸 80g 소진, 비엔나 소진, 떡사리 70g, 어묵 50g, 사골육수 반 팩 소진"
        r['cal'] = "660.0"

    elif day == 28:
        r['ingredients'] = [i.replace('무 150g', '무 80g') for i in r['ingredients']]
        r['steps'] = [s.replace('무 150g', '무 80g') for s in r['steps']]
        r['waste'] = "우삼겹 120g 소진, 감자 소진, 무 80g 소진, 애호박 소진"
        r['cal'] = "640.0"
        
    elif day == 29:
        r['ingredients'] = [
            "떡국떡 140g",
            "사각어묵 70g (2장)",
            "해물믹스 80g",
            "사골육수 250ml (반 팩)",
            "물 150ml",
            "대파 1/2대",
            "고추장 1T",
            "고춧가루 0.7T",
            "진간장 0.5T",
            "설탕 1T",
            "[어묵국] 물 300ml",
            "치킨파우더 0.5t",
            "진간장 0.5T",
            "후추 약간"
        ]
        r['steps'] = [
            "냄비에 사골육수 250ml, 물 150ml, 고추장 1T, 고춧가루 0.7T, 진간장 0.5T, 설탕 1T를 풀고 끓입니다.",
            "떡국떡 140g, 썬 어묵 1장(35g), 해물믹스 80g을 넣고 중불에서 4분간 조립니다.",
            "대파를 넣고 1분간 조려 떡볶이를 완성합니다.",
            "다른 냄비에 물 300ml, 치킨파우더 0.5t, 진간장 0.5T, 어묵 1장(35g), 대파를 넣고 2분간 끓여 어묵국을 만듭니다.",
            "떡볶이와 어묵국을 함께 냅니다."
        ]
        r['waste'] = "떡 140g 소진, 어묵 70g 소진, 해물믹스 80g 소진, 사골육수 반 팩 소진"
        r['cal'] = "630.0"
        r['carb'] = "78.0"
        r['prot'] = "28.0"
        r['fat'] = "14.0"
        
    elif day == 30:
        r['ingredients'] = [
            "순두부 180g (반 봉)",
            "해물믹스 100g",
            "무 60g",
            "팽이버섯 60g (반 봉)",
            "대파 1/3대",
            "물 300ml",
            "된장 1T",
            "치킨파우더 0.5t",
            "고춧가루 0.5T",
            "다진마늘 0.5T",
            "[계란죽] 밥 0.5공기",
            "계란 1알",
            "참기름 0.5T",
            "김치 약간"
        ]
        r['steps'] = [
            "냄비에 물 300ml, 치킨파우더 0.5t, 된장 1T, 고춧가루 0.5T, 다진마늘 0.5T를 넣고 끓입니다.",
            "썬 무 60g을 넣고 2분간 먼저 끓입니다.",
            "해물믹스 100g, 순두부 180g, 팽이버섯 60g, 대파를 넣고 2분간 끓여 전골을 즐깁니다.",
            "남은 국물에 밥 반 공기를 넣고 주걱으로 으깨며 약불에서 2분간 끓입니다.",
            "푼 계란 1알과 참기름을 넣고 섞어 고소한 계란죽으로 마무리합니다."
        ]
        r['waste'] = "순두부 180g 소진, 해물믹스 100g 소진, 무 60g 소진, 팽이버섯 소진"
        r['cal'] = "540.0"
        r['carb'] = "48.0"
        r['prot'] = "32.0"
        r['fat'] = "16.0"

new_json = json.dumps(recipes, ensure_ascii=False, indent=2)

new_html = html[:m.start(1)] + new_json + html[m.end(1):]
with open('recipe_viewer.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

with open('gogaek_recipe.html', 'r', encoding='utf-8') as f:
    g_html = f.read()
gm = re.search(r'const recipes = (\[.*?\]);', g_html, re.DOTALL)
if gm:
    new_g_html = g_html[:gm.start(1)] + new_json + g_html[gm.end(1):]
    with open('gogaek_recipe.html', 'w', encoding='utf-8') as f:
        f.write(new_g_html)

print("Successfully rebalanced all recipes in recipe_viewer.html and gogaek_recipe.html!")
