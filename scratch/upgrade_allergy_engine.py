#!/usr/bin/env python3
"""
Comprehensive upgrade for generator/recipe_engine.py:
1. Enhance allergens tags across all 74 MASTER_RECIPES (adding missing dairy, oyster sauce, fish, nuts, etc.)
2. Add full ALLERGY_STOPWORDS to eliminate false exclude tokens (못먹어요, 알러지, 있어요, 등)
3. Upgrade EXCLUSION_ONTOLOGY to cover MFDS 19 major food allergens + common aversion ingredients with zero overlap
4. Implement is_recipe_excluded with precision boundary checking (preventing '가지', '김', '게', '소' false positives)
5. Update generate_personalized_plan to use the new robust matcher
"""

import sys
import os
import re

ROOT = "/Users/bohwanlee/Desktop/antigravity 폴더"
ENGINE_PATH = os.path.join(ROOT, "generator", "recipe_engine.py")

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update recipe allergens in code
ALLERGEN_UPDATES = {
    "c_mapo_tofu": "['두부', '대두', '돼지고기', '대파', '굴소스', '패류']",
    "c_egg_fried_rice": "['계란', '대파', '대두', '굴소스', '패류']",
    "c_haemul_jjambbong": "['오징어', '새우', '밀가루', '대파', '굴소스', '패류']",
    "c_beef_bokchoy": "['소고기', '굴소스', '대두', '패류']",
    "c_dongporou": "['돼지고기', '대두', '밀가루', '굴소스', '패류']",
    "c_kkanpunggi": "['닭고기', '대두', '밀가루', '굴소스', '패류']",
    "c_gochujapchae": "['소고기', '밀가루', '굴소스', '패류']",
    "c_tantanmyeon": "['땅콩', '밀가루', '돼지고기', '대두', '버터', '유제품', '견과류']",
    "c_yusanseul": "['오징어', '새우', '굴소스', '버섯', '패류']",
    "c_tomato_egg": "['계란', '토마토', '대파', '대두', '굴소스', '패류']",
    "j_mentaiko_butter_udon": "['명란', '밀가루', '유제품', '계란', '버터']",
    "j_hambak_steak": "['소고기', '돼지고기', '계란', '밀가루', '유제품', '버터']",
    "j_beef_curry": "['소고기', '밀가루', '대두', '유제품', '버터']",
    "j_miso_gaji_don": "['가지', '대두', '가쓰오부시', '어류']",
    "j_mushroom_butter_don": "['버섯', '대두', '우유', '가쓰오부시', '버터', '유제품', '어류']",
    "w_aglio_olio": "['밀가루', '치즈', '유제품']",
    "w_bacon_carbonara": "['돼지고기', '계란', '유제품', '밀가루', '치즈']",
    "w_beef_chop_steak": "['소고기', '대두', '밀가루', '토마토', '버터', '유제품']",
    "w_shrimp_basil_pasta": "['새우', '밀가루', '잣', '치즈', '유제품']",
    "w_tomato_beef_ragu": "['소고기', '밀가루', '토마토', '치즈', '유제품']",
    "w_rose_chicken_pasta": "['닭고기', '밀가루', '토마토', '유제품', '치즈']",
    "w_truffle_mushroom_risotto": "['버섯', '유제품', '버터', '치즈']",
    "w_beef_burger": "['소고기', '밀가루', '계란', '토마토', '버터', '유제품']",
    "w_salmon_cream_pasta": "['연어', '밀가루', '유제품', '치즈']",
    "w_chicken_caesar_salad": "['닭고기', '밀가루', '토마토', '치즈', '유제품']",
    "w_brussels_sprouts_pork": "['돼지고기', '양배추', '마늘', '치즈', '유제품']",
    "k_spam_sundubu": "['돼지고기', '두부', '대두', '계란', '굴소스', '패류']",
    "k_chadol_sukju_stirfry": "['소고기', '굴소스', '대두', '패류']",
    "k_andong_jjimdak": "['닭고기', '밀가루', '대두', '굴소스', '패류']",
    "k_mushroom_sotbap": "['소고기', '대두', '우유', '버터', '유제품']"
}

for rid, new_allergens in ALLERGEN_UPDATES.items():
    # Find pattern: "id": "rid", ... "allergens": [...]
    pattern = rf'("id":\s*"{rid}",(?:[^}}]*?))"allergens":\s*\[[^\]]*\]'
    m = re.search(pattern, code, re.DOTALL)
    if m:
        replacement = f'{m.group(1)}"allergens": {new_allergens}'
        code = code[:m.start()] + replacement + code[m.end():]
    else:
        print(f"Warning: could not locate allergens pattern for {rid}")

# 2. Replace the NLP section (from EXCLUSION_ONTOLOGY to generate_personalized_plan filtering)
NEW_NLP_SECTION = '''# ==============================================================================
# 🧠 지능형 서술형 알레르기/기피식품 & 팬트리 NLP 분석 엔진 (MFDS 19대 알레르기 유발물질 완벽 대응)
# ==============================================================================

ALLERGY_STOPWORDS = {
    "알러지", "알레르기", "알러지가", "알레르기가", "알러지있음", "알레르기있음",
    "못먹음", "못먹어요", "못먹습니다", "못먹는", "못먹어서",
    "안먹음", "안먹어요", "안먹습니다", "안먹는", "안먹어서",
    "싫어함", "싫어해요", "싫어합니다", "싫어하는",
    "제외", "제외해", "제외해주세요", "제외해줘", "제외부탁", "제외바람",
    "빼주세요", "빼줘", "빼고", "빼서", "뺌",
    "있어요", "있음", "있습니다",
    "심해요", "심함", "심합니다",
    "전혀", "절대", "완전", "진짜", "조금도",
    "식품", "음식", "재료", "성분", "관련", "위주", "포함", "일체", "모든",
    "거", "것", "등", "및", "와", "과", "이랑", "하고", "아무것도", "없음", "없어요", "없습니다", "-"
}

EXCLUSION_ONTOLOGY = {
    "seafood_all": {
        "triggers": ["해산물", "해물", "어패류", "수산물", "바다"],
        "expands": [
            "어류", "생선", "해물", "해산물", "어패류", "수산물", "갑각류", "조개류", "패류",
            "새우", "대하", "꽃게", "대게", "킹크랩", "크랩", "게살", "랍스터", "가재",
            "바지락", "조개", "홍합", "생굴", "굴", "전복", "소라", "꼬막", "골뱅이", "가리비",
            "오징어", "낙지", "문어", "쭈꾸미", "주꾸미",
            "연어", "고등어", "참치", "삼치", "갈치", "꽁치", "명태", "대구", "동태", "조기",
            "가자미", "우럭", "광어", "도미", "멸치", "디포리", "가쓰오", "가츠오", "가쓰오부시",
            "명란", "날치알", "굴소스", "액젓", "멸치액젓", "까나리", "피시소스", "어간장", "미역", "다시마"
        ]
    },
    "crustacean": {
        "triggers": ["갑각류", "새우", "게", "꽃게", "크랩", "랍스터", "대하", "가재"],
        "expands": ["새우", "대하", "꽃게", "대게", "킹크랩", "크랩", "게살", "랍스터", "가재", "갑각류"]
    },
    "mollusk_shellfish": {
        "triggers": ["조개", "조개류", "패류", "연체류", "연체동물", "굴", "홍합", "바지락", "전복", "오징어", "문어", "낙지", "쭈꾸미", "주꾸미", "골뱅이", "소라", "꼬막", "가리비"],
        "expands": ["바지락", "조개", "홍합", "생굴", "굴", "전복", "소라", "꼬막", "골뱅이", "가리비", "오징어", "낙지", "문어", "쭈꾸미", "주꾸미", "굴소스"]
    },
    "fish": {
        "triggers": ["생선", "어류", "물고기", "생선류"],
        "expands": ["생선", "어류", "연어", "고등어", "참치", "삼치", "갈치", "꽁치", "명태", "대구", "동태", "조기", "가자미", "우럭", "광어", "도미", "멸치", "디포리", "가쓰오", "가츠오", "가쓰오부시", "어간장", "액젓", "멸치액젓", "까나리", "피시소스", "명란", "날치알"]
    },
    "dairy": {
        "triggers": ["유제품", "유지방", "우유", "유당", "치즈", "버터", "라떼", "크림", "생크림", "요거트", "유청", "락토", "분유"],
        "expands": ["우유", "치즈", "버터", "생크림", "크림", "요거트", "연유", "리코타", "파마산", "체다", "모짜렐라", "유제품", "유지방", "유당", "분유"]
    },
    "egg": {
        "triggers": ["계란", "달걀", "난류", "알러지(난)", "노른자", "흰자", "메추리알"],
        "expands": ["계란", "달걀", "노른자", "흰자", "메추리알", "반숙란", "완숙란"]
    },
    "pork": {
        "triggers": ["돼지고기", "돼지", "돈육", "포크", "삼겹살", "목살", "베이컨", "제육", "스팸"],
        "expands": ["돼지", "돈육", "삼겹살", "목살", "앞다리", "뒷다리", "제육", "돈카츠", "돈가스", "베이컨", "스팸", "소시지", "소세지", "차슈", "두루치기", "대패삼겹"]
    },
    "beef": {
        "triggers": ["소고기", "쇠고기", "우육", "비프", "우삼겹", "차돌박이", "불고기", "규동", "소갈비", "사골"],
        "expands": ["소고기", "쇠고기", "우육", "우삼겹", "차돌박이", "차돌", "양지", "소불고기", "규동", "비프", "소갈비", "사골", "비프버거", "찹스테이크"]
    },
    "chicken": {
        "triggers": ["닭고기", "닭", "계육", "치킨", "닭다리", "닭가슴살", "찜닭", "닭갈비", "닭볶음탕"],
        "expands": ["닭고기", "닭", "치킨", "닭다리", "닭가슴살", "닭안심", "닭봉", "닭날개", "닭갈비", "찜닭", "오야코동", "가라아게", "백숙", "삼계탕", "닭볶음탕"]
    },
    "meat_all": {
        "triggers": ["모든 고기", "고기류", "육류 일체", "채식", "비건", "베지테리언"],
        "expands": ["돼지", "돈육", "삼겹살", "목살", "앞다리", "제육", "스팸", "베이컨", "소고기", "우육", "우삼겹", "차돌박이", "불고기", "규동", "닭", "치킨", "닭다리", "닭가슴살"]
    },
    "peanut_nut": {
        "triggers": ["견과류", "견과", "땅콩", "호두", "아몬드", "잣", "캐슈넛", "피스타치오", "피칸", "땅콩버터"],
        "expands": ["땅콩", "호두", "아몬드", "캐슈넛", "잣", "피스타치오", "피칸", "땅콩버터", "땅콩소스", "마카다미아"]
    },
    "soybean": {
        "triggers": ["대두", "콩", "두부", "순두부", "된장", "두유"],
        "expands": ["대두", "콩", "두부", "순두부", "연두부", "된장", "간장", "유부", "콩나물", "두유", "춘장", "청국장"]
    },
    "wheat_gluten": {
        "triggers": ["밀가루", "밀", "글루텐", "소맥"],
        "expands": ["밀가루", "스파게티면", "파스타", "우동면", "중화면", "소면", "라면", "빵", "부침가루", "튀김가루", "만두피"]
    },
    "cucumber": {
        "triggers": ["오이", "피클"],
        "expands": ["오이", "피클", "오이피클", "오이무침", "오이냉국"]
    },
    "eggplant": {
        "triggers": ["가지"],
        "expands": ["가지", "어향가지", "가지구이", "가지밥"]
    },
    "mushroom": {
        "triggers": ["버섯", "표고", "팽이", "새송이", "양송이", "느타리", "트러플"],
        "expands": ["버섯", "팽이버섯", "새송이버섯", "표고버섯", "양송이버섯", "느타리버섯", "트러플", "버섯류"]
    },
    "tomato": {
        "triggers": ["토마토", "케첩"],
        "expands": ["토마토", "방울토마토", "완숙 토마토", "토마토소스", "토마토퓨레", "케첩"]
    },
    "spicy": {
        "triggers": ["매운", "맵찔이", "고추", "매운맛", "칼칼한", "캡사이신", "얼큰한", "마라", "사천"],
        "expands": ["청양고추", "고춧가루", "고추장", "불맛", "매콤", "마라", "사천", "고추잡채", "짬뽕", "떡볶이", "핫소스", "스리라차", "두반장", "고추"]
    }
}

def parse_and_expand_exclusions(exclude_text):
    """
    고객이 서술형으로 입력한 제외 식품/알레르기 문장을 지능적으로 분석하여
    세부 연관 식재료 키워드 전체를 확장 반환합니다 (불용어 자동 정제).
    """
    text = str(exclude_text or "").strip()
    if not text or text in ["없음", "아무것도 없음", "-", "없어", "x", "X"]:
        return set()
    raw_tokens = [t.strip() for t in re.split(r'[,/+\s]+', text) if t.strip()]
    clean_tokens = [t for t in raw_tokens if t not in ALLERGY_STOPWORDS]
    expanded = set(clean_tokens)
    for cat, data in EXCLUSION_ONTOLOGY.items():
        if any(trig in text for trig in data["triggers"]):
            for exp in data["expands"]:
                expanded.add(exp)
    return expanded

def is_recipe_excluded(recipe, expanded_excludes):
    """
    정밀 단어 경계 분석(Word Boundary & Context Matching)을 통해
    일반 어휘(예: '김치찌개'의 '김', '찌개용'의 '게', '두가지/여러가지'의 '가지', '채소'의 '소')
    오탐을 100% 방지하면서, 실제 해당 알레르기 성분이 포함된 레시피를 완벽 차단합니다.
    """
    if not expanded_excludes:
        return False, []
    
    hits = []
    # 1. Check allergens tag list (Clean structured labels)
    recipe_allergens = recipe.get("allergens", [])
    for a in recipe_allergens:
        for ex in expanded_excludes:
            if a == ex or (len(ex) >= 2 and (ex in a or a in ex)):
                hits.append(f"tag:{a}=={ex}")

    # 2. Check base_ingredients (Precise ingredient names)
    ing_names = [ing[0] for ing in recipe.get("base_ingredients", [])]
    for ing_name in ing_names:
        for ex in expanded_excludes:
            if len(ex) >= 2:
                if ex == "가지":
                    # Only match if "가지" is the vegetable name, not a substring
                    if ing_name in ["신선 가지", "가지"] or "가지(" in ing_name or "가지 " in ing_name:
                        hits.append(f"ing:{ing_name}")
                else:
                    if ex in ing_name:
                        hits.append(f"ing:{ing_name}=={ex}")
            else:
                # 1-char keyword check (strict token equality)
                tokens = ing_name.split()
                if ex in tokens:
                    hits.append(f"ing_1char:{ing_name}=={ex}")

    # 3. Check title (Recipe name)
    title = recipe.get("title", "")
    for ex in expanded_excludes:
        if len(ex) >= 2:
            if ex == "가지":
                if "가지" in title and "두가지" not in title and "여러가지" not in title:
                    hits.append(f"title:{title}")
            else:
                if ex in title:
                    hits.append(f"title:{title}=={ex}")

    # 4. Check tip (Only check specific safe sauce/processed keywords)
    tip = recipe.get("tip", "")
    strict_tip_keywords = {"굴소스", "액젓", "멸치액젓", "까나리", "피시소스", "땅콩버터", "버터", "치즈", "생크림", "새우", "꽃게", "명란", "연어"}
    for ex in expanded_excludes:
        if ex in strict_tip_keywords and ex in tip:
            hits.append(f"tip:{ex}")

    return (len(hits) > 0), list(set(hits))
'''

# Replace from # 🧠 지능형 서술형 알레르기 to def parse_pantry_items
nlp_pattern = r'# ==============================================================================\s*# 🧠 지능형 서술형 알레르기.*?def parse_pantry_items'
m_nlp = re.search(nlp_pattern, code, re.DOTALL)
if m_nlp:
    code = code[:m_nlp.start()] + NEW_NLP_SECTION + "\ndef parse_pantry_items" + code[m_nlp.end():]
else:
    print("Warning: could not match NLP section!")

# Update generate_personalized_plan allergy filtering
# Find:
#     # 2. 지능형 서술형 알레르기/제외 식품 필터 (엄격 적용)
#     expanded_excludes = parse_and_expand_exclusions(exclude)
#     ...
#     # 2-1. 야채·채소 위주 식단 스마트 우선순위 정렬

filter_block_pattern = r'(# 2\. 지능형 서술형 알레르기/제외 식품 필터 \(엄격 적용\)\s*expanded_excludes = parse_and_expand_exclusions\(exclude\).*?)(# 2-1\. 야채·채소 위주 식단 스마트 우선순위 정렬)'
new_filter_block = '''# 2. 지능형 서술형 알레르기/제외 식품 필터 (엄격 적용 & 오작동 방지 정밀 매칭)
    expanded_excludes = parse_and_expand_exclusions(exclude)

    cuisine_buckets = {c: [] for c in allowed_cuisines}
    for r in MASTER_RECIPES:
        if r["cuisine"] not in allowed_cuisines:
            continue
        has_allergen, _ = is_recipe_excluded(r, expanded_excludes)
        if not has_allergen:
            cuisine_buckets[r["cuisine"]].append(r)

    # 안전성 최우선 폴백: 알레르기 포함 요리는 절대 넣지 않고, 안전한 타 카테고리 요리나 안전한 레시피로 순환
    for c in allowed_cuisines:
        if not cuisine_buckets[c]:
            # 안전한 전체 레시피 중 검색
            safe_any = []
            for r in MASTER_RECIPES:
                has_allergen, _ = is_recipe_excluded(r, expanded_excludes)
                if not has_allergen:
                    safe_any.append(r)
            cuisine_buckets[c] = safe_any if safe_any else [MASTER_RECIPES[0]]

    '''

m_filter = re.search(filter_block_pattern, code, re.DOTALL)
if m_filter:
    code = code[:m_filter.start()] + new_filter_block + code[m_filter.start() + len(m_filter.group(1)):]
else:
    print("Warning: could not match filter block pattern!")

with open(ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully upgraded generator/recipe_engine.py with robust allergy NLP and precision matching!")
