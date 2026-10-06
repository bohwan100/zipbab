# -*- coding: utf-8 -*-
"""
Complete refinement of all 30 menu titles and descriptions:
- Remove all pretension, exaggerations, mismatched ingredients (e.g. butter when only sesame oil exists),
  awkward parentheticals like '(전량 소진)', '(달큰한 무조림 비법)', '100% 냉장고 파먹기', etc.
- 100% intuitive, honest, and appetizing menu names.
"""

import json
import re

refined_titles = {
    1: "불맛 제육덮밥 + 몽글 계란파국",
    2: "돼지고기 덮밥 (부타동) + 맑은 두부 장국",
    3: "삼선 해물 파기름 볶음밥 + 맑은 콩나물국",
    4: "크리스피 치킨 스테이크 & 감자 구이 (단짠 간장 소스)",
    5: "콩나물 불고기 (콩불) + 볶음밥",
    6: "닭고기 계란덮밥 (오야꼬동)",
    7: "마파두부 덮밥",
    8: "소시지 에그 인 헬 (토마토 샥슈카)",
    9: "우삼겹 된장찌개 + 계란후라이",
    10: "소고기 덮밥 (우삼겹 규동) + 맑은 두부 장국",
    11: "우삼겹 양배추 볶음덮밥",
    12: "스페인식 스팸 감자 오믈렛",
    13: "돼지고기 묵은지 김치찜 & 달큰한 무조림",
    14: "진한 양파 카레라이스 & 애호박",
    15: "돼지고기 양배추 간짜장밥 + 계란후라이",
    16: "소시지 나폴리탄 소면 파스타",
    17: "소고기 뭇국 + 바삭 감자채전",
    18: "고소한 간장계란밥 & 우삼겹 구이 + 두부 팽이 장국",
    19: "바삭한 대파간장 치킨 구이 (유린기)",
    20: "치킨 카레 볶음밥 & 반숙 계란",
    21: "참치 김치찌개 + 계란말이",
    22: "데리야끼 훈제오리 덮밥 & 대파채 반숙란",
    23: "얼큰 해물 짬뽕 순두부탕 & 소면사리",
    24: "소고기 햄버그 패티 덮밥 & 양배추 샐러드",
    25: "안동식 순살 찜닭 & 소면사리",
    26: "사골 뚝배기 부대찌개 (스팸 & 소시지)",
    27: "훈제오리 김치 볶음밥 & 반숙란",
    28: "우삼겹 감자 된장 짜글이",
    29: "사골 해물 떡볶이 & 시원한 어묵국",
    30: "해물 순두부 된장 전골 & 영양 계란죽"
}

refined_descs = {
    1: "설탕 카라멜라이징과 간장 불향, 물 40ml 유화 조림 + 몽글 계란파국",
    2: "앞다리살 바싹 구워 기름 빼고 단짠 조림 + 달큰한 두부 미소장국",
    3: "해물 수분 날려 고슬고슬 볶은 파기름 볶음밥 + 시원한 콩나물국",
    4: "무거운 그릇으로 눌러 껍질 7분 바삭하게 구운 치킨 스테이크 & 감자 구이",
    5: "물 없이 콩나물 300g 채수로만 자작하게 조린 콩불 + 바삭 누룽지 볶음밥",
    6: "닭고기 양파 조림에 계란 2회 나누어 부어 만든 부드러운 반숙 오야꼬동",
    7: "소금물에 데쳐 탱글한 두부와 고추기름 불맛 마파두부 덮밥",
    8: "케첩 30초 볶아 신맛 날린 토마토 스튜 & 촉촉한 반숙란 샥슈카",
    9: "우삼겹 기름에 된장을 볶고 설탕 1/4t로 감칠맛 살린 고깃집 된장찌개",
    10: "양파 먼저 끓여 단맛 내고 우삼겹 1분 30초 쾌속 조림한 부드러운 규동",
    11: "양배추 250g을 센 불에 1분 30초 볶아 아삭함 살린 중화풍 볶음덮밥",
    12: "볶은 뜨거운 감자를 계란물에 3분 재워 속이 카스테라처럼 촉촉한 오믈렛",
    13: "바닥에 무를 깔아 눌어붙지 않고 달콤하게 조린 1인 묵은지 돼지 김치찜",
    14: "양파 8분 캐러멜라이징 + 불 끄고 카레 풀기 + 케첩 1t 산미 킥 카레라이스",
    15: "물 60ml와 양배추 채수로 1분 만에 볶아낸 불맛 가득 간짜장밥",
    16: "케첩을 기름에 30초 볶고 면수 40ml로 유화 코팅한 정통 나폴리탄 소면",
    17: "참기름에 무를 투명하게 볶아 끓인 시원한 소고기 뭇국 + 바삭 감자채전",
    18: "바삭한 우삼겹 구이와 간장 참기름 계란밥 + 아삭한 팽이버섯 두부장국",
    19: "닭다리살을 바삭하게 눌러 구워 차가운 새콤달콤 대파간장 소스 얹은 치킨",
    20: "큼직한 닭고기와 카레가루를 센 불에 고슬고슬 볶아낸 치킨 카레 볶음밥",
    21: "참치 기름에 김치 볶아 끓이고 살코기는 마지막에 넣은 참치 김치찌개",
    22: "오리기름 80% 닦아내 담백하고 단짠 소스 윤기 입힌 훈제오리 덮밥",
    23: "즉석 고추기름과 간장 불향, 치킨스톡으로 끓여낸 짬뽕 순두부탕",
    24: "30회 치대어 공기 빼고 물 30ml 뚜껑 닫아 수증기로 쪄낸 육즙 가득 함바그",
    25: "설탕 카라멜라이징과 굴소스로 짙은 윤기와 감칠맛 살린 안동식 찜닭",
    26: "사골육수에 얇은 스팸과 칼집 비엔나, 된장 0.2T 묵직 다대기 부대찌개",
    27: "고소한 오리기름에 김치 볶고 밥을 얇게 펴 센 불에 1분 눌인 누룽지 볶음밥",
    28: "소기름에 감자·무 볶고 된장:고추장 3:1로 자작하게 8분 졸인 짜글이",
    29: "사골육수에 굴소스 3g 더한 국물 떡볶이 + 시원한 사각 어묵국",
    30: "해물 순두부 된장 전골 즐긴 뒤 남은 국물에 끓이는 영양 계란죽"
}

# =============================================================================
# 1. Update recipe_viewer.html
# =============================================================================
with open("recipe_viewer.html", "r", encoding="utf-8") as f:
    viewer_text = f.read()

match = re.search(r"const recipes = (\[.*?\]);\s+function renderRecipes", viewer_text, re.DOTALL)
if match:
    recipes_data = json.loads(match.group(1))
    for r in recipes_data:
        day = r["day"]
        if day in refined_titles:
            r["title"] = refined_titles[day]
        # Day 4: Fix any butter mention
        if day == 4:
            r["ingredients"] = [i.replace("간장버터", "단짠 간장") for i in r["ingredients"]]
            r["steps"] = [s.replace("간장버터", "단짠 간장") for s in r["steps"]]
        # Day 18: Fix butter mention
        if day == 18:
            r["ingredients"] = [i.replace("버터 대체 고소함 킥", "고소한 풍미") for i in r["ingredients"]]
            r["steps"] = [s.replace("버터", "참기름") for s in r["steps"]]

    new_recipes_json = json.dumps(recipes_data, ensure_ascii=False, indent=2)
    viewer_text = viewer_text[:match.start(1)] + new_recipes_json + viewer_text[match.end(1):]

with open("recipe_viewer.html", "w", encoding="utf-8") as f:
    f.write(viewer_text)
print("Updated recipe_viewer.html with refined titles and clean ingredients!")

# =============================================================================
# 2. Update cart_dashboard.html
# =============================================================================
with open("cart_dashboard.html", "r", encoding="utf-8") as f:
    dash_text = f.read()

# Update titles and descs in weekData
for day_num in range(1, 31):
    new_title = refined_titles[day_num]
    new_desc = refined_descs[day_num]
    # Replace name and desc in { day: "Day X", ... name: "...", ... desc: "..." }
    # Using regex per day
    pattern = rf'(\{{\s*\"?day\"?:\s*\"Day {day_num}\",\s*\"?tag\"?:\s*\".*?\",\s*\"?name\"?:\s*\").*?(\",.*?\"?desc\"?:\s*\").*?(\".*?\}}\s*,?)'
    dash_text = re.sub(pattern, rf'\g<1>{new_title}\g<2>{new_desc}\g<3>', dash_text, flags=re.DOTALL)

with open("cart_dashboard.html", "w", encoding="utf-8") as f:
    f.write(dash_text)
print("Updated cart_dashboard.html with refined titles and descs!")

# =============================================================================
# 3. Update 30_day_global_meal_plan.md
# =============================================================================
md_path = "/Users/bohwanlee/.gemini/antigravity-ide/brain/b2567fdd-e500-496d-b733-06cc9d3dcd2f/30_day_global_meal_plan.md"
with open(md_path, "r", encoding="utf-8") as f:
    md_text = f.read()

for day_num in range(1, 31):
    new_title = refined_titles[day_num]
    new_desc = refined_descs[day_num]
    # In table: | **Day X** | 🇨🇳 중식 | **Old Title** | Old Desc | ...
    pattern = rf'(\| \*\*Day {day_num}\*\* \| .*? \| \*\*).*?(\*\* \| ).*?(\| \d+.*? \|)'
    md_text = re.sub(pattern, rf'\g<1>{new_title}\g<2>{new_desc} \g<3>', md_text)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_text)
print("Updated 30_day_global_meal_plan.md successfully!")
