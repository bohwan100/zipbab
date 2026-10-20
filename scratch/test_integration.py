#!/usr/bin/env python3
import sys
import os
import re

ROOT = "/Users/bohwanlee/Desktop/antigravity 폴더"
sys.path.insert(0, os.path.join(ROOT, "generator"))
sys.path.insert(0, os.path.join(ROOT, "scratch"))

import recipe_engine
from expand_korean_recipes_and_nlp import NEW_KOREAN_RECIPES

# Test adding new recipes
existing_ids = {r["id"] for r in recipe_engine.MASTER_RECIPES}
added = 0
for r in NEW_KOREAN_RECIPES:
    if r["id"] not in existing_ids:
        recipe_engine.MASTER_RECIPES.append(r)
        added += 1

print(f"Added {added} new recipes to MASTER_RECIPES. Total now: {len(recipe_engine.MASTER_RECIPES)}")

# Test exclusion expansion
EXCLUSION_ONTOLOGY = {
    "seafood": {
        "triggers": ["어류", "생선", "어패류", "해산물", "해물", "수산물", "물고기", "바다"],
        "expands": [
            "어류", "생선", "해물", "해산물", "어패류", "수산물", "갑각류", "조개류", "패류",
            "새우", "대하", "명란", "날치알", "연어", "고등어", "참치", "삼치", "갈치", "꽁치",
            "명태", "대구", "동태", "조기", "가자미", "우럭", "광어", "도미", "가쓰오", "가츠오",
            "멸치", "디포리", "게", "꽃게", "오징어", "낙지", "문어", "쭈꾸미", "주꾸미",
            "바지락", "홍합", "굴", "전복", "소라", "꼬막", "골뱅이", "가리비", "미역", "다시마",
            "김", "굴소스", "액젓", "멸치액젓", "까나리", "피시소스", "어간장", "해초"
        ]
    },
    "shellfish": {
        "triggers": ["갑각류", "새우", "게", "꽃게", "크랩"],
        "expands": ["새우", "대하", "게", "꽃게", "랍스터", "가재", "크랩", "킹크랩"]
    },
    "clam": {
        "triggers": ["조개", "조개류", "패류"],
        "expands": ["바지락", "조개", "홍합", "굴", "전복", "소라", "꼬막", "골뱅이", "가리비"]
    },
    "pork": {
        "triggers": ["돼지고기", "돈육", "돼지", "포크"],
        "expands": ["돼지", "돈육", "삼겹살", "목살", "앞다리", "뒷다리", "제육", "돈카츠", "돈가스", "베이컨", "스팸", "소시지", "소세지", "부타동", "차슈", "등갈비", "두루치기"]
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
        "triggers": ["계란", "달걀", "난류", "알"],
        "expands": ["계란", "달걀", "노른자", "흰자", "메추리알"]
    },
    "peanut": {
        "triggers": ["견과류", "땅콩", "호두"],
        "expands": ["땅콩", "호두", "아몬드", "캐슈넛", "잣", "피스타치오", "피칸"]
    },
    "spicy": {
        "triggers": ["매운", "맵찔이", "고추", "매운맛"],
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

def parse_and_expand_exclusions(text):
    text = str(text or "")
    expanded = set()
    raw_tokens = [t.strip() for t in re.split(r'[,/ ]+', text) if t.strip() and t.strip() not in ["없음", "아무것도 없음", "-"]]
    for t in raw_tokens:
        expanded.add(t)
        for cat, data in EXCLUSION_ONTOLOGY.items():
            if any(trig in t for trig in data["triggers"]):
                for exp in data["expands"]:
                    expanded.add(exp)
    return expanded

# Test Tae-young Kim
exps = parse_and_expand_exclusions("어패류")
print(f"Exclusions for '어패류': {len(exps)} keywords")

safe_korean = []
for r in recipe_engine.MASTER_RECIPES:
    if r["cuisine"] != "한식":
        continue
    all_texts = " ".join(
        [r["title"]] +
        r.get("allergens", []) +
        [ing[0] for ing in r.get("base_ingredients", [])] +
        [r.get("tip", "")]
    )
    hit = [ex for ex in exps if ex in all_texts]
    if not hit:
        safe_korean.append(r["title"])
    else:
        print(f"  [REJECTED] {r['title']} -> due to {hit}")

print(f"\nTotal safe Korean recipes for Tae-young: {len(safe_korean)}")
for i, t in enumerate(safe_korean, 1):
    print(f"  {i}. {t}")
