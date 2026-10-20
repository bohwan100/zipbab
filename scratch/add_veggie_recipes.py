import os
import sys

# 1. New Vegetable Master Recipes
C_TOMATO_EGG = """    {
        "id": "c_tomato_egg",
        "title": "중화풍 토마토 달걀 덮밥 (토달볶)",
        "cuisine": "중식", "flag": "🇨🇳 중식", "tier": "budget",
        "concepts": ['일반식', '야채·채소 위주', '초간단·가성비', '다이어트'],
        "allergens": ['계란', '토마토', '대파', '대두'],
        "cal": 490, "carb": 68, "prot": 24, "fat": 15,
        "base_ingredients": [
            ('완숙 토마토', 2, '개', 'fresh', '국내산 신선 완숙 토마토 (1kg)', '1kg 1팩', 6900, '신선 완숙 토마토 1kg'),
            ('계란', 3, '알', 'fresh', '곰곰 무항생제 신선 대란 (30구)', '30구 1판', 8900, '무항생제 대란 30구'),
            ('대파', 0.5, '대', 'fresh', '국내산 절단 대파 (500g)', '500g 1봉', 2900, '손질 대파 500g'),
            ('굴소스', 1, 'T', 'seasoning', '이금기 팬더 굴소스 (510g)', '510g 1병', 5600, '이금기 굴소스 510g'),
            ('진간장', 0.5, 'T', 'seasoning', '샘표 진간장 금F3 (860ml)', '860ml 1병', 4500, '샘표 진간장 금F'),
            ('설탕', 1, 't', 'seasoning', '백설 하얀설탕 (1kg)', '1kg 1봉', 2400, '백설 설탕 1kg'),
            ('참기름', 1, 't', 'seasoning', '오뚜기 고소한 참기름 (320ml)', '320ml 1병', 6800, '오뚜기 참기름 320ml'),
            ('꽃소금', 0.3, 't', 'seasoning', '청정원 신안섬보배 꽃소금 (500g)', '500g 1봉', 1600, '청정원 꽃소금 500g')
        ],
        "steps": [
            '토마토 2개를 한입 크기 웨지 모양으로 썰고, 대파는 쫑쫑 썰어둡니다.',
            '계란 3알에 소금 한 꼬집을 넣고 풀어 팬에 식용유 2T를 두르고 센 불에서 80%만 몽글하게 볶아 그릇에 덜어둡니다.',
            '팬에 대파를 볶아 파기름을 낸 뒤 토마토를 넣고 센 불에서 과즙이 촉촉하게 배어나올 때까지 1분 30초간 볶습니다.',
            '굴소스 1T, 진간장 0.5T, 설탕 1t를 넣고 볶은 계란을 합쳐 센 불에 30초간 빠르게 섞은 뒤 참기름을 둘러 밥 위에 소복이 올립니다.'
        ],
        "tip": '★황금 조리 팁: 계란을 80%만 익혀 먼저 빼두어야 퍽퍽해지지 않으며, 토마토의 천연 산미에 설탕 1t와 굴소스가 어우러져 단짠 새콤한 감칠맛의 정점을 이룹니다.'
    },
"""

J_MISO_GAJI = """    {
        "id": "j_miso_gaji_don",
        "title": "일식 미소 타레 가지구이 덮밥",
        "cuisine": "일식", "flag": "🇯🇵 일식", "tier": "budget",
        "concepts": ['일반식', '야채·채소 위주', '초간단·가성비', '다이어트'],
        "allergens": ['가지', '대두', '가쓰오부시'],
        "cal": 480, "carb": 72, "prot": 18, "fat": 14,
        "base_ingredients": [
            ('신선 가지', 2, '개', 'fresh', '국내산 신선 가지 (3입)', '3개 1봉', 2900, '신선 가지 3입'),
            ('미소된장', 1.5, 'T', 'seasoning', '미소된장 (500g)', '500g 1팩', 3900, '미소된장 500g'),
            ('미림 맛술', 1.5, 'T', 'seasoning', '롯데 미림 맛술 (500ml)', '500ml 1병', 2800, '미림 맛술 500ml'),
            ('설탕', 1, 'T', 'seasoning', '백설 하얀설탕 (1kg)', '1kg 1봉', 2400, '백설 설탕 1kg'),
            ('진간장', 0.5, 'T', 'seasoning', '샘표 진간장 금F3 (860ml)', '860ml 1병', 4500, '샘표 진간장 금F'),
            ('가쓰오부시', 3, 'g', 'seasoning', '사조 가쓰오부시 (50g)', '50g 1봉', 3500, '가쓰오부시 50g'),
            ('대파', 0.3, '대', 'fresh', '국내산 절단 대파 (500g)', '500g 1봉', 2900, '손질 대파 500g'),
            ('참기름', 1, 't', 'seasoning', '오뚜기 고소한 참기름 (320ml)', '320ml 1병', 6800, '오뚜기 참기름 320ml')
        ],
        "steps": [
            '가지는 반으로 갈라 격자 모양으로 칼집을 곱게 넣어 양념이 잘 스미게 준비합니다.',
            '그릇에 미소된장 1.5T, 미림 1.5T, 설탕 1T, 진간장 0.5T, 물 2T를 섞어 달콤짭조름한 미소 타레 소스를 만듭니다.',
            '팬에 식용유를 넉넉히 두르고 가지를 칼집 넣은 면부터 중불에서 노릇하고 부드럽게 3분간 굽습니다.',
            '미소 타레 소스를 붓고 약불에서 가지에 윤기가 돌도록 졸인 뒤, 따뜻한 밥 위에 얹고 가쓰오부시와 송송 썬 대파를 올려 완성합니다.'
        ],
        "tip": '★황금 조리 팁: 가지에 촘촘히 격자 칼집을 넣고 미소된장과 미림, 설탕을 배합한 타레 소스를 졸여내면, 가지 특유의 채즙과 미소된장의 깊은 풍미가 밥 한 공기를 순식간에 비우게 만듭니다.'
    },
    {
        "id": "j_mushroom_butter_don",
        "title": "새송이버섯 버터 간장 스테이크 덮밥",
        "cuisine": "일식", "flag": "🇯🇵 일식", "tier": "budget",
        "concepts": ['일반식', '야채·채소 위주', '초간단·가성비'],
        "allergens": ['버섯', '대두', '우유', '가쓰오부시'],
        "cal": 510, "carb": 70, "prot": 19, "fat": 16,
        "base_ingredients": [
            ('새송이버섯', 2, '개', 'fresh', '국내산 무농약 새송이버섯 (400g)', '400g 1봉', 2200, '새송이버섯 400g'),
            ('버터', 15, 'g', 'fresh', '서울우유 프레시 버터 (200g)', '200g 1개', 4500, '서울우유 버터 200g'),
            ('진간장', 1.5, 'T', 'seasoning', '샘표 진간장 금F3 (860ml)', '860ml 1병', 4500, '샘표 진간장 금F'),
            ('미림 맛술', 1, 'T', 'seasoning', '롯데 미림 맛술 (500ml)', '500ml 1병', 2800, '미림 맛술 500ml'),
            ('설탕', 0.5, 'T', 'seasoning', '백설 하얀설탕 (1kg)', '1kg 1봉', 2400, '백설 설탕 1kg'),
            ('통마늘', 3, '알', 'fresh', '국내산 깐마늘 (200g)', '200g 1봉', 2400, '깐마늘 200g'),
            ('가쓰오부시', 3, 'g', 'seasoning', '사조 가쓰오부시 (50g)', '50g 1봉', 3500, '가쓰오부시 50g')
        ],
        "steps": [
            '새송이버섯은 1.5cm 두께로 도톰하게 썰어 양면에 격자 칼집을 깊숙이 넣어 스테이크처럼 준비합니다.',
            '팬에 식용유 1T를 두르고 편 썬 마늘과 새송이버섯을 센 불에서 노릇하게 앞뒤로 2분간 구워 버섯즙을 가둡니다.',
            '버터 15g, 진간장 1.5T, 미림 1T, 설탕 0.5T를 넣고 버터가 녹아 버섯에 갈색빛 코팅이 입혀질 때까지 1분간 센 불에 조려냅니다.',
            '밥 위에 버섯 스테이크를 소복이 얹고 남은 버터간장 소스를 끼얹은 뒤 가쓰오부시를 올려 완성합니다.'
        ],
        "tip": '★황금 조리 팁: 새송이버섯에 칼집을 넣어 버터간장 소스를 입히면 전복이나 관자 부럽지 않은 쫄깃하고 즙이 터지는 버섯 스테이크가 완성됩니다. 펜트리 새송이버섯 완벽 활용 요리입니다.'
    },
"""

W_ROASTED_VEGGIE = """    {
        "id": "w_brussels_sprouts_pork",
        "title": "미니양배추 & 삼겹살 갈릭 로스트",
        "cuisine": "양식", "flag": "🇪🇺 양식", "tier": "standard",
        "concepts": ['일반식', '야채·채소 위주', '고단백·근육 증가'],
        "allergens": ['돼지고기', '양배추', '마늘'],
        "cal": 570, "carb": 42, "prot": 32, "fat": 30,
        "base_ingredients": [
            ('미니양배추', 120, 'g', 'frozen', '냉동 방울양배추 (1kg)', '1kg 1봉', 8900, '냉동 방울양배추 1kg'),
            ('돼지 삼겹살', 120, 'g', 'frozen', '한돈 냉동 삼겹살 구이용 (1kg)', '1kg 1팩', 16900, '냉동 삼겹살 1kg'),
            ('통마늘', 6, '알', 'fresh', '국내산 깐마늘 (200g)', '200g 1봉', 2400, '깐마늘 200g'),
            ('올리브유', 1, 'T', 'seasoning', '폰타나 엑스트라버진 올리브유 (500ml)', '500ml 1병', 7900, '폰타나 올리브유 500ml'),
            ('꽃소금', 0.5, 't', 'seasoning', '청정원 신안섬보배 꽃소금 (500g)', '500g 1봉', 1600, '청정원 꽃소금 500g'),
            ('순후추', 0.3, 't', 'seasoning', '오뚜기 순후추 (50g)', '50g 1통', 2100, '오뚜기 순후추 50g'),
            ('파마산 치즈가루', 1, 'T', 'seasoning', '크래프트 파마산 치즈가루 (227g)', '227g 1통', 6900, '파마산 치즈가루')
        ],
        "steps": [
            '미니양배추를 반으로 자르고, 삼겹살은 한입 크기로 썹니다.',
            '달군 팬에 삼겹살을 먼저 구워 고소한 돼지기름이 충분히 배어나오게 합니다.',
            '삼겹살 기름에 반으로 자른 미니양배추 단면과 편 썬 통마늘을 넣고, 미니양배추 겉면이 바삭하고 노릇해질 때까지 4분간 볶아 구워냅니다.',
            '소금과 순후추로 간을 하고, 불을 끈 뒤 파마산 치즈가루 1T를 뿌려 밥이나 바게트와 함께 곁들입니다.'
        ],
        "tip": '★황금 조리 팁: 미니양배추는 단면을 바짝 구워야 특유의 쓴맛이 날아가고 고소한 단맛이 폭발합니다. 삼겹살의 풍미와 마늘 향이 더해져 고급 브런치 요리가 됩니다.'
    },
    {
        "id": "w_roasted_veggie_pasta",
        "title": "구운 모둠 채소 바질 오일 파스타",
        "cuisine": "양식", "flag": "🇪🇺 양식", "tier": "standard",
        "concepts": ['일반식', '야채·채소 위주', '초간단·가성비'],
        "allergens": ['밀가루', '토마토', '마늘'],
        "cal": 550, "carb": 76, "prot": 18, "fat": 19,
        "base_ingredients": [
            ('스파게티면', 100, 'g', 'seasoning', '바릴라 스파게티면 No.5 (500g)', '500g 1봉', 2900, '바릴라 스파게티면 500g'),
            ('파프리카', 0.5, '개', 'fresh', '국내산 파프리카 (2입)', '2입 1봉', 3900, '파프리카 2개'),
            ('방울토마토', 6, '알', 'fresh', '국내산 대추방울토마토 (750g)', '750g 1팩', 7900, '방울토마토 750g'),
            ('양파', 0.5, '개', 'fresh', '국내산 햇양파 (1.5kg)', '1.5kg 1망', 3900, '햇양파 1.5kg'),
            ('통마늘', 5, '알', 'fresh', '국내산 깐마늘 (200g)', '200g 1봉', 2400, '깐마늘 200g'),
            ('바질페스토', 1.5, 'T', 'seasoning', '데체코 바질페스토 (190g)', '190g 1병', 6900, '데체코 바질페스토'),
            ('올리브유', 2, 'T', 'seasoning', '폰타나 엑스트라버진 올리브유 (500ml)', '500ml 1병', 7900, '폰타나 올리브유 500ml'),
            ('꽃소금', 1, 'T', 'seasoning', '청정원 신안섬보배 꽃소금 (500g)', '500g 1봉', 1600, '청정원 꽃소금 500g')
        ],
        "steps": [
            '끓는 물 1L에 꽃소금 1T를 넣고 스파게티면을 8분간 삶아 건집니다 (면수 80ml 보관).',
            '파프리카와 양파를 굵게 깍둑썰기하고, 방울토마토는 반으로 자릅니다.',
            '팬에 올리브유를 두르고 편 썬 마늘과 채소들을 센 불에서 2분간 노릇하게 구워 단맛을 극대화합니다.',
            '삶은 면과 면수 50ml, 바질페스토 1.5T를 넣고 40초간 센 불에 빠르게 유화시켜 볶아냅니다.'
        ],
        "tip": '★황금 조리 팁: 채소를 센 불에 노릇하게 구운 뒤 바질페스토를 마지막에 넣고 가볍게 볶아야 바질의 산뜻한 향과 구운 채소의 달큰한 즙이 살아납니다.'
    },
"""

def update_recipe_engine():
    filepath = '/Users/bohwanlee/Desktop/antigravity 폴더/generator/recipe_engine.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert c_tomato_egg
    if '"id": "c_tomato_egg"' not in content:
        anchor_ch = '    # ==================== 2. 일식 (Japanese - 12 Recipes) ===================='
        content = content.replace(anchor_ch, C_TOMATO_EGG + '\n' + anchor_ch)

    # 2. Insert j_miso_gaji and j_mushroom_butter_don
    if '"id": "j_miso_gaji_don"' not in content:
        anchor_jp = '    # ==================== 3. 양식 (Western - 12 Recipes) ===================='
        content = content.replace(anchor_jp, J_MISO_GAJI + '\n' + anchor_jp)

    # 3. Insert w_brussels_sprouts_pork and w_roasted_veggie_pasta
    if '"id": "w_brussels_sprouts_pork"' not in content:
        anchor_ws = '    # ==================== 4. 한식 (Korean - 12 Recipes) ===================='
        content = content.replace(anchor_ws, W_ROASTED_VEGGIE + '\n' + anchor_ws)

    # 4. Add veggie sorting in generate_personalized_plan
    veggie_sort_code = '''    # 2-1. 야채·채소 위주 식단 스마트 우선순위 정렬 (concept or goal_notes or pantry)
    is_veggie_focus = any(kw in str(concept) + str(client_name) + str(pantry) for kw in ["야채", "채소", "베지", "비건", "다이어트"]) or (client_name == "정민")
    if is_veggie_focus:
        veggie_keywords = ['가지', '청경채', '배추', '양배추', '미니양배추', '버섯', '토마토', '파프리카', '피망', '두부', '순두부', '숙주', '콩나물', '감자', '애호박', '샐러드', '마늘', '당근', '양파']
        def get_veggie_score(r):
            score = 0
            t = r['title']
            for kw in veggie_keywords:
                if kw in t: score += 6
            for ing in r['base_ingredients']:
                for kw in veggie_keywords:
                    if kw in ing[0]: score += 3
            # Pantry match bonus
            for p in raw_pantry:
                if p and len(p) >= 2 and (p in t or any(p in ing[0] for ing in r['base_ingredients'])):
                    score += 8
            return score

        for c in allowed_cuisines:
            cuisine_buckets[c].sort(key=get_veggie_score, reverse=True)
'''
    if "is_veggie_focus" not in content:
        target = "    # 3. 30일 식단 편성 (선택된 모든 요리 균등 분배 & 데일리 순환 인터리빙)"
        content = content.replace(target, veggie_sort_code + "\n" + target)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated generator/recipe_engine.py with 5 new vegetable recipes and smart sorting!")

if __name__ == '__main__':
    update_recipe_engine()
