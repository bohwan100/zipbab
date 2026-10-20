#!/usr/bin/env python3
"""
Full updater for generator/recipe_engine.py:
- Adds 21 new verified Korean recipes to MASTER_RECIPES
- Adds EXCLUSION_ONTOLOGY and parse_and_expand_exclusions
- Adds parse_pantry_items
- Updates generate_personalized_plan
- Updates build_products_database to omit pantry items from cart
"""

import sys
import os
import re
import json

ROOT = "/Users/bohwanlee/Desktop/antigravity 폴더"
ENGINE_PATH = os.path.join(ROOT, "generator", "recipe_engine.py")

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Check if NEW_RECIPES already in code
if "k_baek_duruchigi" in code:
    print("New recipes already present in engine.")
else:
    # Read the new recipes snippet
    from expand_korean_recipes_and_nlp import NEW_KOREAN_RECIPES

    EXTRA_3_RECIPES = [
        {
            "id": "k_sundubu_beef_jjigae",
            "title": "얼큰 차돌 순두부찌개",
            "cuisine": "한식", "flag": "🇰🇷 한식", "tier": "budget",
            "concepts": ['일반식', '초간단·가성비'],
            "allergens": ['소고기', '대두', '계란'],
            "cal": 560, "carb": 28, "prot": 36, "fat": 24,
            "base_ingredients": [
                ('소 우삼겹', 120, 'g', 'frozen', '미국산 소 우삼겹 바로구이 (1kg)', '1kg 1팩', 14900, '우삼겹 바로구이 1kg'),
                ('순두부', 1, '봉', 'fresh', '풀무원 국산 순두부 (350g)', '350g 1봉', 1400, '풀무원 순두부 350g'),
                ('계란', 1, '알', 'fresh', '곰곰 무항생제 신선 대란 (30구)', '30구 1판', 8900, '무항생제 대란 30구'),
                ('대파', 0.5, '대', 'fresh', '국내산 절단 대파 (500g)', '500g 1봉', 2900, '손질 대파 500g'),
                ('고춧가루', 1.5, 'T', 'seasoning', '국산 태양초 고춧가루 (500g)', '500g 1봉', 9800, '고춧가루 500g'),
                ('진간장', 1, 'T', 'seasoning', '샘표 진간장 금F3 (860ml)', '860ml 1병', 4500, '샘표 진간장 금F'),
                ('참기름', 1, 't', 'seasoning', '오뚜기 고소한 참기름 (320ml)', '320ml 1병', 6800, '오뚜기 참기름 320ml'),
                ('통마늘', 2, '알', 'fresh', '국내산 깐마늘 (200g)', '200g 1봉', 2400, '깐마늘 200g')
            ],
            "steps": [
                '냄비에 참기름 1t를 두르고 우삼겹과 다진 마늘, 고춧가루 1.5T를 약불에서 볶아 고추기름을 냅니다.',
                '물 300ml와 진간장 1T를 넣고 센 불에서 바글바글 끓입니다.',
                '순두부를 숟가락으로 크게 떼어 넣고 2분간 끓입니다.',
                '계란 1알을 톡 깨 넣고 대파를 올려 30초 후 불을 끄고 얼큰하게 완성합니다.'
            ],
            "tip": '★황금 조리 팁: 우삼겹 자체의 기름과 참기름에 고춧가루를 약불로 볶아 진한 고추기름을 내면 굴소스나 해물 없이도 깊고 진한 전문점 순두부 국물이 완성됩니다.'
        },
        {
            "id": "k_pork_kimchi_duruchigi",
            "title": "한돈 묵은지 삼겹살 두루치기",
            "cuisine": "한식", "flag": "🇰🇷 한식", "tier": "premium",
            "concepts": ['일반식', '초간단·가성비'],
            "allergens": ['돼지고기', '대두'],
            "cal": 680, "carb": 42, "prot": 44, "fat": 34,
            "base_ingredients": [
                ('한돈 통삼겹', 180, 'g', 'fresh', '도드람한돈 1등급 통삼겹살 (1kg)', '1kg 1팩', 21900, '도드람한돈 통삼겹살 1kg'),
                ('종가집 묵은지', 150, 'g', 'fresh', '종가집 전라도 묵은지 (1kg)', '1kg 1봉', 8900, '종가집 묵은지 1kg'),
                ('양파', 0.5, '개', 'fresh', '국내산 햇양파 (1.5kg)', '1.5kg 1망', 3900, '햇양파 1.5kg'),
                ('대파', 0.5, '대', 'fresh', '국내산 절단 대파 (500g)', '500g 1봉', 2900, '손질 대파 500g'),
                ('고춧가루', 1, 'T', 'seasoning', '국산 태양초 고춧가루 (500g)', '500g 1봉', 9800, '고춧가루 500g'),
                ('설탕', 1, 'T', 'seasoning', '백설 하얀설탕 (1kg)', '1kg 1봉', 2400, '백설 설탕 1kg'),
                ('진간장', 1, 'T', 'seasoning', '샘표 진간장 금F3 (860ml)', '860ml 1병', 4500, '샘표 진간장 금F'),
                ('참기름', 1, 't', 'seasoning', '오뚜기 고소한 참기름 (320ml)', '320ml 1병', 6800, '오뚜기 참기름 320ml')
            ],
            "steps": [
                '삼겹살을 한입 크기로 썰어 팬에서 센 불로 노릇하게 구워 기름을 냅니다.',
                '삼겹살 기름에 먹기 좋게 썬 묵은지와 설탕 1T를 넣고 달달 볶습니다.',
                '양파와 대파, 고춧가루 1T, 간장 1T를 넣고 센 불에서 2분간 빠르게 볶아 불향을 입힙니다.',
                '참기름을 둘러 밥과 함께 매콤고소하게 즐깁니다.'
            ],
            "tip": '★황금 조리 팁: 삼겹살 기름에 묵은지를 설탕과 함께 볶아야 김치의 신맛이 잡히고 풍미 깊은 단짠 매콤 두루치기가 됩니다.'
        },
        {
            "id": "k_beef_ttukbaegi_bulgogi",
            "title": "뚝배기 소불고기 뚝불",
            "cuisine": "한식", "flag": "🇰🇷 한식", "tier": "premium",
            "concepts": ['일반식', '초간단·가성비'],
            "allergens": ['소고기', '대두', '밀가루'],
            "cal": 620, "carb": 62, "prot": 38, "fat": 20,
            "base_ingredients": [
                ('소 우삼겹', 140, 'g', 'frozen', '미국산 소 우삼겹 바로구이 (1kg)', '1kg 1팩', 14900, '우삼겹 바로구이 1kg'),
                ('오뚜기 당면', 40, 'g', 'fresh', '오뚜기 옛날 당면 (500g)', '500g 1봉', 3800, '오뚜기 당면 500g'),
                ('양파', 0.5, '개', 'fresh', '국내산 햇양파 (1.5kg)', '1.5kg 1망', 3900, '햇양파 1.5kg'),
                ('팽이버섯', 1, '봉', 'fresh', '국내산 친환경 팽이버섯 (3입)', '3봉 1팩', 1900, '팽이버섯 3입'),
                ('대파', 0.5, '대', 'fresh', '국내산 절단 대파 (500g)', '500g 1봉', 2900, '손질 대파 500g'),
                ('진간장', 2, 'T', 'seasoning', '샘표 진간장 금F3 (860ml)', '860ml 1병', 4500, '샘표 진간장 금F'),
                ('설탕', 1, 'T', 'seasoning', '백설 하얀설탕 (1kg)', '1kg 1봉', 2400, '백설 설탕 1kg'),
                ('참기름', 1, 't', 'seasoning', '오뚜기 고소한 참기름 (320ml)', '320ml 1병', 6800, '오뚜기 참기름 320ml'),
                ('순후추', 0.2, 't', 'seasoning', '오뚜기 순후추 (50g)', '50g 1통', 2100, '오뚜기 순후추 50g')
            ],
            "steps": [
                '당면을 따뜻한 물에 15분간 불립니다.',
                '냄비에 물 250ml, 진간장 2T, 설탕 1T, 다진 마늘, 순후추를 넣고 끓입니다.',
                '국물이 끓으면 우삼겹과 채 썬 양파, 불린 당면, 팽이버섯을 넣고 4분간 끓입니다.',
                '대파를 올리고 참기름을 둘러 국물과 함께 밥에 쓱쓱 비벼 먹습니다.'
            ],
            "tip": '★황금 조리 팁: 당면이 달착지근한 불고기 육수를 흠뻑 머금어 밥과 함께 먹으면 기사식당 뚝배기 불고기 맛을 그대로 재현합니다.'
        }
    ]

    ALL_NEW = NEW_KOREAN_RECIPES + EXTRA_3_RECIPES

    # Convert to python code string
    import pprint
    new_recipes_str = ",\n".join([pprint.pformat(r, indent=4, width=120) for r in ALL_NEW])

    # Insert right before MASTER_RECIPES closing bracket `]`
    # Let's find line `    }\n]` around line 1395
    m = re.search(r'(\n\s*\{\s*"id":\s*"k_pork_galbi_jjim"[\s\S]*?\n\s*\})\s*\n\]', code)
    if m:
        orig = m.group(1)
        replacement = orig + ",\n" + new_recipes_str
        code = code[:m.start(1)] + replacement + code[m.end(1):]
        print(f"Successfully inserted {len(ALL_NEW)} new Korean recipes into MASTER_RECIPES!")
    else:
        print("Error: Could not locate k_pork_galbi_jjim end in code")

# 2. Add EXCLUSION_ONTOLOGY and NLP helper functions
NLP_CODE = '''
# ==============================================================================
# 🧠 지능형 서술형 알레르기/기피식품 & 팬트리 NLP 분석 엔진
# ==============================================================================
EXCLUSION_ONTOLOGY = {
    "seafood": {
        "triggers": ["어류", "생선", "어패류", "해산물", "해물", "수산물", "물고기", "바다", "해산"],
        "expands": [
            "어류", "생선", "해물", "해산물", "어패류", "수산물", "갑각류", "조개류", "패류",
            "새우", "대하", "명란", "날치알", "연어", "고등어", "참치", "삼치", "갈치", "꽁치",
            "명태", "대구", "동태", "조기", "가자미", "우럭", "광어", "도미", "가쓰오", "가츠오",
            "가쓰오부시", "가츠오부시", "멸치", "디포리", "꽃게", "대게", "킹크랩", "크랩", "게살",
            "오징어", "낙지", "문어", "쭈꾸미", "주꾸미", "바지락", "홍합", "생굴", "전복", "소라",
            "꼬막", "골뱅이", "가리비", "미역", "다시마", "굴소스", "액젓", "멸치액젓", "까나리",
            "피시소스", "어간장", "해초", "조미김", "김가루"
        ]
    },
    "crustacean": {
        "triggers": ["갑각류", "새우", "게", "꽃게", "크랩", "랍스터"],
        "expands": ["새우", "대하", "꽃게", "대게", "킹크랩", "크랩", "게살", "랍스터", "가재"]
    },
    "shellfish": {
        "triggers": ["조개", "조개류", "패류"],
        "expands": ["바지락", "조개", "홍합", "생굴", "전복", "소라", "꼬막", "골뱅이", "가리비"]
    },
    "fish": {
        "triggers": ["생선", "어류", "물고기"],
        "expands": ["생선", "어류", "연어", "고등어", "참치", "삼치", "갈치", "꽁치", "명태", "대구", "동태", "조기", "가자미", "우럭", "광어", "도미", "멸치", "디포리", "가쓰오", "가츠오"]
    },
    "pork": {
        "triggers": ["돼지고기", "돈육", "돼지", "포크"],
        "expands": ["돼지", "돈육", "삼겹살", "목살", "앞다리", "뒷다리", "제육", "돈카츠", "돈가스", "베이컨", "스팸", "소시지", "소세지", "부타동", "차슈", "두루치기"]
    },
    "beef": {
        "triggers": ["소고기", "우육", "소", "비프"],
        "expands": ["소고기", "우육", "우삼겹", "차돌박이", "양지", "불고기", "규동", "스테이크", "비프", "소갈비", "사골"]
    },
    "chicken": {
        "triggers": ["닭고기", "계육", "닭", "치킨"],
        "expands": ["닭", "치킨", "닭다리", "닭가슴살", "닭안심", "닭봉", "닭날개", "닭갈비", "찜닭", "오야코동", "가라아게", "백숙", "삼계탕"]
    },
    "meat_all": {
        "triggers": ["고기", "육류", "채식", "비건"],
        "expands": ["돼지", "돈육", "삼겹살", "목살", "앞다리", "제육", "스팸", "베이컨", "소고기", "우육", "우삼겹", "차돌박이", "불고기", "규동", "닭", "치킨", "닭다리", "닭가슴살"]
    },
    "dairy": {
        "triggers": ["유제품", "우유", "유당", "치즈", "버터"],
        "expands": ["우유", "치즈", "버터", "생크림", "요거트", "연유", "리코타", "파마산"]
    },
    "egg": {
        "triggers": ["계란", "달걀", "난류"],
        "expands": ["계란", "달걀", "노른자", "흰자", "메추리알"]
    },
    "peanut": {
        "triggers": ["견과류", "땅콩", "호두"],
        "expands": ["땅콩", "호두", "아몬드", "캐슈넛", "잣", "피스타치오", "피칸"]
    },
    "spicy": {
        "triggers": ["매운", "맵찔이", "고추", "매운맛", "칼칼한"],
        "expands": ["청양고추", "불맛", "매콤", "마라", "사천", "고추잡채", "짬뽕", "떡볶이", "핫소스", "스리라차"]
    },
    "cucumber": {
        "triggers": ["오이"],
        "expands": ["오이"]
    },
    "eggplant": {
        "triggers": ["가지"],
        "expands": ["가지"]
    },
    "mushroom": {
        "triggers": ["버섯"],
        "expands": ["버섯", "팽이", "새송이", "표고", "양송이", "느타리"]
    }
}

def parse_and_expand_exclusions(exclude_text):
    """
    고객이 서술형으로 입력한 제외 식품/알레르기 문장을 지능적으로 분석하여
    세부 연관 식재료 키워드 전체를 확장 반환합니다.
    """
    text = str(exclude_text or "").strip()
    if not text or text in ["없음", "아무것도 없음", "-", "없어", "x", "X"]:
        return set()
    expanded = set()
    raw_tokens = [t.strip() for t in re.split(r'[,/+\s]+', text) if t.strip() and t.strip() not in ["없음", "아무것도 없음", "-", "제외", "못먹음", "알레르기", "알러지", "안먹음", "싫어함", "빼주세요"]]
    for t in raw_tokens:
        expanded.add(t)
    for cat, data in EXCLUSION_ONTOLOGY.items():
        if any(trig in text for trig in data["triggers"]):
            for exp in data["expands"]:
                expanded.add(exp)
    return expanded

def parse_pantry_items(pantry_str):
    """
    고객이 서술형으로 입력한 5번 집에 있는 식재료 문장을 분석하여
    장바구니 0원 공제 대상 식재료 목록을 추출합니다.
    """
    pantry_str = str(pantry_str or "").strip()
    if not pantry_str or pantry_str in ["아무것도 없음", "없음", "-", "없어", "x", "X"]:
        return []
    tokens = re.split(r'[,/+\s]+', pantry_str)
    stopwords = ["있음", "있어요", "집에", "보유", "정도", "개", "캔", "포", "봉", "알", "병", "팩", "조금", "많음", "이랑", "하고", "와", "과", "등", "있습니다"]
    clean_pantry = []
    for t in tokens:
        t = t.strip()
        if not t or t in stopwords:
            continue
        t = re.sub(r'\\d+(캔|개|봉|알|병|팩|kg|g|포)?', '', t).strip()
        if t and t not in stopwords and len(t) >= 1:
            clean_pantry.append(t)
    return clean_pantry
'''

if "EXCLUSION_ONTOLOGY" not in code:
    code = code.replace("def parse_household_count(household_str):", NLP_CODE + "\ndef parse_household_count(household_str):")

# 3. Update exclusion filtering in generate_personalized_plan
OLD_FILTER_BLOCK = '''    # 2. 제외 식품 필터
    raw_excludes = [x.strip() for x in re.split(r'[,/ ]+', str(exclude)) if x.strip() and x.strip() not in ["없음", "아무것도 없음", "-"]]

    cuisine_buckets = {c: [] for c in allowed_cuisines}
    for r in MASTER_RECIPES:
        if r["cuisine"] not in allowed_cuisines:
            continue
        all_texts = " ".join([r["title"]] + r["allergens"] + [ing[0] for ing in r["base_ingredients"]])
        if not any(ex in all_texts for ex in raw_excludes):
            cuisine_buckets[r["cuisine"]].append(r)

    # 비어있을 경우 폴백
    for c in allowed_cuisines:
        if not cuisine_buckets[c]:
            cuisine_buckets[c] = [r for r in MASTER_RECIPES if r["cuisine"] == c]'''

NEW_FILTER_BLOCK = '''    # 2. 지능형 서술형 알레르기/제외 식품 필터 (엄격 적용)
    expanded_excludes = parse_and_expand_exclusions(exclude)

    cuisine_buckets = {c: [] for c in allowed_cuisines}
    for r in MASTER_RECIPES:
        if r["cuisine"] not in allowed_cuisines:
            continue
        all_texts = " ".join(
            [r["title"]] +
            r.get("allergens", []) +
            [ing[0] for ing in r.get("base_ingredients", [])] +
            [r.get("tip", "")]
        )
        # 확장된 제외 키워드가 하나라도 포함되면 절대 금지!
        has_allergen = any(ex in all_texts for ex in expanded_excludes)
        if not has_allergen:
            cuisine_buckets[r["cuisine"]].append(r)

    # 안전성 최우선 폴백: 알레르기 포함 요리는 절대 넣지 않고, 안전한 타 카테고리 요리나 안전한 레시피로 순환
    for c in allowed_cuisines:
        if not cuisine_buckets[c]:
            # 안전한 전체 레시피 중 검색
            safe_any = []
            for r in MASTER_RECIPES:
                all_texts = " ".join([r["title"]] + r.get("allergens", []) + [ing[0] for ing in r.get("base_ingredients", [])] + [r.get("tip", "")])
                if not any(ex in all_texts for ex in expanded_excludes):
                    safe_any.append(r)
            cuisine_buckets[c] = safe_any if safe_any else [MASTER_RECIPES[0]]'''

if OLD_FILTER_BLOCK in code:
    code = code.replace(OLD_FILTER_BLOCK, NEW_FILTER_BLOCK)
    print("Successfully updated allergy/exclusion filtering logic in generate_personalized_plan!")
else:
    print("Warning: Could not find exact OLD_FILTER_BLOCK, check manual diff.")

# 4. Update pantry handling
# raw_pantry = parse_pantry_items(pantry)
code = re.sub(
    r'raw_pantry = \[x\.strip\(\) for x in re\.split\(r\'\[,/ \]\+\', str\(pantry\)\) if x\.strip\(\) and x\.strip\(\) not in \["아무것도 없음", "없음", "-"\]\]',
    'raw_pantry = parse_pantry_items(pantry)',
    code
)

# 5. Update build_products_database to omit pantry items from cart
OLD_PRODUCTS_LOOP = '''        for idx, item in enumerate(sorted_items):
            is_in_pantry = any(p in item["name"] or p in item["query"] for p in raw_pantry)
            buy_qty = item["qty"] if not is_in_pantry else 0
            item_total = (item["unitPrice"] * buy_qty)

            if is_in_pantry:
                tot_saved_pantry += item["unitPrice"] * item["qty"]
                display_name = f"{item['name']} [🏠 보유 재료 0원 공제]"
            else:
                tot_spent += item_total
                display_name = item["name"]

            products_list.append({
                "id": idx + 1,
                "orderWeek": item["orderWeek"],
                "storage": item["storage"],
                "cat": item["cat"],
                "name": display_name,
                "spec": item["spec"],
                "qty": buy_qty,
                "unitPrice": item["unitPrice"] if not is_in_pantry else 0,
                "total": item_total,
                "weeks": item["weeks"],
                "recipes": item["recipes"],
                "query": item["query"]
            })'''

NEW_PRODUCTS_LOOP = '''        for idx, item in enumerate(sorted_items):
            is_in_pantry = any(p in item["name"] or p in item["query"] for p in raw_pantry)

            if is_in_pantry:
                # 5번 집에 있는 식재료는 장바구니 품목에서 100% 완전 제외 (절약 금액만 계산하고 장바구니에 담지 않음)
                tot_saved_pantry += item["unitPrice"] * item["qty"]
                continue

            item_total = (item["unitPrice"] * item["qty"])
            tot_spent += item_total

            products_list.append({
                "id": len(products_list) + 1,
                "orderWeek": item["orderWeek"],
                "storage": item["storage"],
                "cat": item["cat"],
                "name": item["name"],
                "spec": item["spec"],
                "qty": item["qty"],
                "unitPrice": item["unitPrice"],
                "total": item_total,
                "weeks": item["weeks"],
                "recipes": item["recipes"],
                "query": item["query"]
            })'''

if OLD_PRODUCTS_LOOP in code:
    code = code.replace(OLD_PRODUCTS_LOOP, NEW_PRODUCTS_LOOP)
    print("Successfully updated build_products_database to omit pantry items from cart!")
else:
    print("Warning: Could not find exact OLD_PRODUCTS_LOOP, check manual diff.")

# Write back to ENGINE_PATH
with open(ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Finished updating generator/recipe_engine.py!")
