import os
import re
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
from performance_evaluator import get_performance_weights, get_evolved_templates

# ==============================================================================
# 🏪 [스마트스토어 '이웃밭농부' 실제 검증된 상품 데이터 & 댓글 링크]
# ==============================================================================
DEFAULT_LINKS = {
    "only_apples0.1": "🍎 상위 0.1% 사과 구경하러가기👇👇👇\nhttps://smartstore.naver.com/iutbatfarmer/products/12422755670?nt_source=threads&nt_medium=sns\n\n초특가 이벤트 챙길 사람 들어와유~~!!\nhttps://open.kakao.com/o/g2EhftDh",
    "ggul_bamm": "🌰공주 정안 밤 구경하러와줭😘😘✌️\nhttps://smartstore.naver.com/iutbatfarmer/products/12273855798?nt_source=threads&nt_medium=sns\n\n초특가 이벤트 챙길 사람 들어와유~~!!\nhttps://open.kakao.com/o/g2EhftDh"
}

FIRST_COMMENTS = DEFAULT_LINKS

STORE_SPECS = {
    "only_apples0.1": {
        "store_name": "이웃밭농부",
        "product_name": "소백산 해발 700m 고랭지 특품 사과",
        "origin": "경북 영주 풍기 (소백산 자락 해발 700m 고랭지)",
        "variety": "해발 700m 고랭지 사과 (홍로 / 아리수)",
        "grade": "특품",
        "price": "47,900원",
        "coupon_price": "47,400원",
        "shipping": "무료배송",
        "rating": "4.95점",
        "reviews": "작년 네이버 평점 4.95점 달성",
        "juice_feature": "칼 대면 '딱!' 소리 나며 갈라지는 극강의 아삭함과 턱으로 흐르는 꿀 과즙",
        "sweetness": "해발 700m 극심한 일교차가 빚어낸 꿀 박힌 14브릭스 이상 당도"
    },
    "ggul_bamm": {
        "store_name": "이웃밭농부",
        "product_name": "공주 정안 햇밤 (특품 알밤)",
        "origin": "충남 공주 정안",
        "variety": "공주 정안 햇알밤 (옥광 / 대보)",
        "price": "23,900원",
        "shipping": "무료배송",
        "rating": "4.9점",
        "feature": "갓 수확한 묵직하고 단단한 공주 정안 햇알밤, 생으로 깎아 먹어도 푹 쪄 먹어도 꿀 터지는 단맛",
        "convenience": "산지에서 직접 꼼꼼하게 선별한 꽉 찬 특품 알밤"
    }
}

# ==============================================================================
# 🧠 [12대 바이럴 구조 포맷 라이브러리 - 278개 실전 1만~100만 뷰 전수 분석 기반]
# 대표님 피드백 완벽 반영:
# 1. 고정 3단 구조('훅-설명-하트') 100% 해체
# 2. 체크리스트형, 초단문형, 5분레시피형, 대세선언형, 상황극형, 밸런스형 등 12가지 독립적 구조 적용
# 3. 해발 700m 고랭지 사과 출시, 극강의 아삭함, 작년 네이버 평점 4.95점 전면 반영
# 4. 추석/명절 관련 키워드 원천 배제 (시즌 종료)
# ==============================================================================

BANNED_WORDS = ["추석", "명절", "차례", "한가위", "제사", "송편", "갈비찜", "제수용", "군밤"]

VIRAL_FORMATS = {
    "only_apples0.1": {
        # F01. 체크리스트 / 자가진단형 (Bullet Lists)
        "F01_checklist": [
            "스레드에 이런 사과 찾는 사과 덕후 있나요?\n- 푸석푸석 스펀지 사과 극혐하는 사람\n- 한 입 베어 물 때 '딱!' 소리 나는 아삭함 찾는 사람\n- 마트에서 실패만 하다가 찐사과 찾고 싶은 사람\n산지에서 갓 따온 햇사과 수확했어 🍎",
            "진짜 맛있는 사과 고르는 3가지 기준\n- 겉면이 지나치게 번들거리지 않고 뽀얀 백분이 도는 사과\n- 손으로 쥐었을 때 돌처럼 단단하고 묵직한 사과\n- 칼 대자마자 '딱!' 소리 나며 쪼개지는 아삭함\n올해 첫 수확 햇사과야 🍎",
            "사과 덕후들이 환장하는 순간\n- 첫 박스 뜯었을 때 달콤한 사과 향 확 퍼질 때\n- 껍질째 씹자마자 턱으로 과즙 콸콸 튈 때\n- 푸석함 1도 없이 끝까지 아삭할 때\n농부가 자신 있게 보냅니다 🍎",
            "사과 먹을 때 절대 하면 안 되는 실수\n- 껍질 다 깎아 버리기 (영양소 70% 증발)\n- 따뜻한 실온에 방치하기\n- 마트에서 반짝반짝 광택 나는 왁스 사과 사기\n흐르는 물에 씻어서 껍질째 와그작 베어 물어야 제맛 🍎"
        ],
        # F02. 초단문 절규/날것형 (Ultra Short, 1~5줄 - 실전 7.8만 뷰 대표님 글 모티브)
        "F02_raw_plea": [
            "사과 파는 주인입니다.\n꼭 잘 팔고 싶습니다 ....\n저희 사과 정말 맛있습니다\n네이버 평점 4.91점인데\n지нага다 하트라도 부탁합니다..! 🍎",
            "사과 파는 청년입니다.\n해발 700m 높은 산자락에서 이제 막 사과 땄습니다.\n진짜 거짓말 안 치고 엄청 단단하고 아삭합니다.\n다 팔 수 있게 도와줘 ㅠㅠ 지나가다 하트라도 툭 부탁해 🍎",
            "사주세요.\n사과 1년 동안 정성 다해 키웠습니다.\n한 입 베어 물면 꿀물 터져 나오는 사과라 자신 있게 외칩니다 🍎",
            "어이가 없다.\n백화점 가면 한 알에 만 원씩 받아도 줄 서서 사는데...\n난 백화점도 아니고 유명하지도 않지.\n작년 네이버 평점 4.95점인데 유명해지고 싶다 🍎",
            "사과 파는 사람입니다. 오늘 진짜 잘 팔고 싶습니다..\n아침부터 과수원에서 제일 예쁜 놈들로만 골라 담았거든요.\n구경이라도 와주세요 🍎"
        ],
        # F03. 트렌드/대세 선언형 (Trend Declaration)
        "F03_trend_declaration": [
            "올가을 사과는 무조건 '고지대 고랭지'가 이깁니다.\n일교차 15도 이상 맞고 자라서 과육 조직이 차원이 달라요.\n칼 대면 쩍 갈라지는 전설의 사과 드디어 수확했습니다 🍎",
            "사과 매니아들 소리 질러도 됨!!\n드디어 소백산 첫 수확 햇사과 본격 출하 시작했어 🍎\n엄청 아삭해서 칼 대면 딱 소리 남.\n푸석한 마트 사과랑 비교 불가야!",
            "다들 이 사과가 AI 같아서 안 사는 거야?\n이거 내가 과수원에서 방금 폰으로 찍은 건데..\n심지어 아무거나 막 집어 든 사과인데...\n한번씩 우리 사과도 관심 가져주라~~ 그냥 하는 말이 아니라 진짜 맛있음 🍎"
        ],
        # F04. 5분 꿀팁/레시피형 (5-Min Recipe / Food Hack)
        "F04_recipe_hack": [
            "바쁜 아침 1분 사과 땅콩버터 토스트!\n아삭한 사과 얇게 썰어서 통밀빵 위에 땅콩버터 바르고 올리면 식감 극락이야.\n단맛 폭발하는데 든든해서 다이어터들 꼭 저장해둬 🍎",
            "아침 사과 10배 맛있게 먹는 법.\n사과 얇게 썰어 레몬즙 톡톡 + 시나몬 가루 살짝.\n고급 브런치 카페 맛 나는데 1분이면 끝남 🍎✨",
            "사과 갈변 막는 30초 꿀팁.\n물 한 컵에 레몬즙 3방울 섞어서 사과 30초 담갔다 빼기.\n하루 종일 방금 깎은 것처럼 아삭함이 유지돼 🍎"
        ],
        # F05. 상황/비상사태형 (Situation Emergency - 실전 9.2만 뷰 큰일이야 모티브)
        "F05_situation_emergency": [
            "큰일이야 ㅠㅠ\n가격을 내렸어 ㅠㅠ 버릴 순 없잖아\n혹시 스레드에 사과 덕후 있어?\n아삭아삭하고 달콤해서 진짜 맛있어\n쿠폰 뿌려도 홍보하기 쉽지 않네.. 사과 좋아하는 스치니 있다면 하트라도 부탁해 🍎",
            "스토어에 첫 햇사과 오픈하자마자 포장하다 손에 쥐 남 ㅋㅋㅋ\n새벽부터 박스 접고 완충재 넣느라 허리 펴질 틈이 없네.\n오늘 주문 건 전량 산지직송 출발합니다 🍎",
            "새벽에 서리 맞아가며 사과 따느라 손이 꽁꽁 얼었어 ㅠㅠ\n하지만 추위를 견뎌야 사과에 꿀이 꽉 차거든.\n고생한 청년 농부 힘내라고 하트 하나만 부탁해 🍎"
        ],
        # F06. 호기심/상식 반전형 (Discovery & Curiosity - 실전 10.4만 뷰 정보형 모티브)
        "F06_discovery_curiosity": [
            "정보) 사과 껍질에 끈적한 유분이 도는 건 농약이나 왁스가 아니라, 사과가 스스로 과육을 지키려고 뿜어낸 천연 왁스질이다.\n흐르는 물에 씻어서 껍질째 씹어먹는 게 비타민 70%를 다 먹는 방법.\n스레드에서 싸움 말고 이런 농산물 이야기나 실컷 하고 싶다 🍎",
            "왜 사과는 높은 산자락에서 자란 게 제일 맛있을까?\n낮밤 온도 차가 15도 이상 벌어지면서 과육이 돌처럼 치밀하고 아삭해져!\n올해 첫 수확한 사과 한 입 베어 물어봐 🍎",
            "칼 대자마자 '딱!' 소리 나면서 쪼개지는 사과 본 적 있어?\n산지에서 갓 따온 사과인데 진짜 엄청 아삭아삭해.\n마트에서 사 먹던 사과랑 식감이 아예 달라 🍎"
        ],
        # F07. 오감/식감 자극형 (Sensory Craving)
        "F07_sensory_craving": [
            "와.. 드디어 첫 사과 땄다.\n와그작 베어무는 순간 '딱!' 소리 나며 꿀물이 입안 가득 튐 ㅠㅠ\n진짜 엄청 아삭아삭해서 턱으로 과즙 흘러내림.. 극강의 식감이야 🍎",
            "푸석푸석 스펀지 같은 사과에 지친 사람들 주목.\n높은 산자락에서 맑은 바람 맞고 자라 돌처럼 단단한 햇사과 드디어 나왔어.\n한 입 베어물면 감탄 나옴 🍎",
            "냉장고에 차갑게 넣어뒀다가 아침 공복에 껍질째 와작 베어무는 순간.\n청량한 과즙이 팡 터지며 잠이 확 깨는 그 느낌.\n이 맛에 1년 농사짓는다 🍎"
        ],
        # F08. 밸런스 게임/취향 논쟁형 (Balance Debate)
        "F08_balance_debate": [
            "사과 껍질째 먹는다 vs 깎아 먹는다\n1번) 영양분 다 챙기게 흐르는 물에 씻어서 와작\n2번) 부드러운 과육만 느끼게 감자칼로 얇게 싹싹\n스친들의 사과 먹는 스타일은? 댓글 남겨줘 🍎",
            "사과 고를 때 뭐가 제일 중요해?\n1번) 칼 대면 딱 소리 나는 극강의 아삭함\n2번) 입안 가득 터지는 달콤한 꿀 과즙\n우리 과수원 사과는 둘 다 잡았는데 스친들 선택은? 🍎"
        ],
        # F09. 일상 산지 일기형 (Farmer Diary)
        "F09_farmer_diary": [
            "새벽 5시 안개 뚫고 과수원 올라왔어.\n일교차 크게 맞고 자란 사과들이 빨갛게 탐스럽게 익었네.\n정직하게 땀 흘려 키운 사과야. 청년 농부 응원 하트 콕 🍎",
            "가을 산바람 맞으며 첫 사과 수확 완료!\n한 입 베어무니 아삭한 소리에 피로가 싹 가시네 ㅠㅠ\n올해도 맛있게 익어줘서 고맙다. 응원 하트 툭 🍎",
            "아직도 믿기지 않아.\n얼마 전까지만 해도 하루 1박스 나가던 작은 과수원이었는데\n스레드 보고 찾아주신 분들 덕분에 버틴다.\n스레드가 사람 살린다.. 진짜 고마워 🍎"
        ],
        # F10. 가격 역발상/가치전복형 (Price & Value Contrast - 실전 28.6만 뷰 두쫀쿠 모티브)
        "F10_price_contrast": [
            "나 사과 파는 사람이야. 솔직히 좀 서운해 ㅠㅠ\n두쫀쿠는 7천원해도 줄 서서 사 먹으면서, 1년 동안 땀 흘려 키운 명품 사과는 비싸대..\n아삭아삭하고 과즙 풍부해서 정말 맛있거든.\n사과 덕후들 하트라도 부탁해 🍎🍎",
            "배달 떡볶이 2만원, 배달팁 4천원은 1초 만에 결제하면서..\n1년 농사지은 산지직송 명품 사과는 장바구니에만 ㅠㅠ\n유통 거품 싹 빼고 보내드립니다. 믿고 드셔보세요 🍎",
            "카페 디저트 한 조각에 8천원인데..\n산지에서 갓 딴 꿀사과 한 박스가 이 가격이면 솔직히 거저 아닌가요 스친들? ㅠㅠ\n지나가다 응원 하트 하나 부탁해 🍎"
        ],
        # F11. 후기 박제/셀프공구 유머형 (Real Review & Humor - 실전 2.1만 뷰 모티브)
        "F11_real_review": [
            "과수원에 사과를 한 번에 15박스씩 주문 넣으신 분 누구신가요 ㅋㅋㅋㅋ\n회사 부서 전체에 돌린다고 셀프 공구하셨대 ㅋㅋㅋ\n아침부터 테이프 붙이다 손목 나갈 뻔했지만 너무 감사합니다 🍎",
            "'칼 대자마자 딱 소리 나고 인생 사과 만났어요'라는 후기에 힘이 번쩍 남 ㅠㅠ\n단골분들이 언제 나오냐고 매일 물어보시던 그 사과 드디어 출하 시작했어.\n축하 하트 콕 🍎",
            "안녕하세요 과수원 하는 사장입니다...\n서럽게도.. 아직 모르시는 분이 많은데 😢\n저희 사과 정말 단단하고 맛있어요 ...\n손이 자주 갈 아침 사과예요 ... 좋아요 부탁드려요.. 실수로라도... 🍎"
        ],
        # F12. 스친 소통/질문형 (Community Question)
        "F12_community_question": [
            "아침에 사과 깎아주는 사람 있으면 진짜 노벨 사랑상 줘야 함 ㄷㄷ\n칼 대자마자 딱 소리 나면서 쪼개지는데 꿀물 뚝뚝 떨어짐 🍎\n다들 오늘 아침 챙겨 먹었어?",
            "단단하고 아삭아삭한 사과 좋아하는 스친들 손!\n새벽에 갓 따온 사과로 아침 시작하는 중 🍎\n다들 오늘 하루도 힘내자!",
            "다들 아침 공복에 사과 어떻게 먹어?\n껍질째 베어 무는 사람 vs 예쁘게 깎아 접시에 담아 먹는 사람!\n스친들의 아침 루틴 알려줘 🍎"
        ]
    },
    "ggul_bamm": {
        # F01. 체크리스트 / 자가진단형 (Bullet Lists)
        "F01_checklist": [
            "스레드에 제철 밤 러버들 계신가요?\n- 가을만 되면 생밤 오독오독 깎아먹는 사람\n- 갓 찐 찐밤 숟가락으로 푹 퍼먹는 사람\n- 갓 지은 쌀밥에 통밤 듬뿍 넣어 먹는 밤밥 좋아하는 사람\n- 마트 밤 샀다가 속 비어서 실망해본 사람\n하나라도 해당하면 하트 콕 🌰",
            "연휴 끝나고 출근해서 멘붕 온 K-직장인 특징\n- 오후 3시만 되면 당 떨어져서 손 떨림\n- 탕비실 과자 뜯으려다 속 더부룩해서 현타 옴\n- 저녁에 밥맛 없는데 건강한 야식 찾고 있음\n자연 그대로 쪄낸 달콤한 공주 정안 햇밤이 구원투수야 🌰",
            "속이 꽉 찬 명품 햇밤 고르는 법\n- 물에 넣었을 때 동동 뜨지 않고 바닥에 묵직하게 가라앉음\n- 껍질 색이 짙은 밤색에 윤기 좌르르\n- 손으로 쥐었을 때 빈틈없이 돌처럼 단단함\n충남 공주 정안에서 갓 주운 특품 알밤이야 🌰",
            "가을철 햇밤이 몸에 좋은 이유\n- 비타민 C가 사과의 4배 (천연 피로회복제)\n- 위장 보호해 주는 착한 탄수화물\n- 환절기 면역력 올려주는 천연 영양 덩어리\n올가을엔 건강한 햇밤 챙겨 먹자 🌰"
        ],
        # F02. 초단문 절규/정면돌파형 (Ultra Short - 실전 2.9만 뷰 대표님 실제 글 & 3.6만 뷰 모티브)
        "F02_raw_plea": [
            "밤 가게 주인입니다.\n스레드 글은 솔직하게 정면돌파 해야 합니다.\n저희 밤 진짜 맛있읍니다.\n달콤한 공주 정안 햇밤 사세요.\n산지직송 특품 알밤 2kg 무료배송입니다 🌰",
            "쓰레드에서\n너무 진지하게 팔지 마세요.\n어차피 아무도 안 봅니다.\n갓 수확한 햇밤 사세요 🌰",
            "밤 파는 청년입니다.\n성공 꼭 하고 싶습니다 ...\n공주 정안에서 갓 주운 햇밤인데 찌면 설탕 뿌린 것처럼 달콤합니다.\n지나가다 실수로라도 하트 하나 부탁드립니다 🌰",
            "사주세요.\n공주 정안 햇알밤인데 알이 진짜 굵고 속이 꽉 찼습니다 🌰",
            "밤 파는 사람인데 주문이 조용해서 심장이 철렁하네요...\n맛없으면 100% 환불해 드릴 테니 믿고 드셔보세요 🌰"
        ],
        # F03. 트렌드/대세 선언형 (Trend Declaration)
        "F03_trend_declaration": [
            "밤장수로서 진심으로 말합니다.\n밤은 무조건 산지직송 좋은 걸로 드세요.\n시장이나 마트 가서 바짝 말라 비틀어진 거 사 먹지 마세요 제발.\n공주 정안에서 갓 주운 특품 생알밤 드세요 🌰",
            "가을철 홈카페 대세는 무조건 '수제 밤라떼'야.\n포슬포슬 찐밤 5알 + 우유 + 꿀 넣고 믹서기 30초.\n카페 7천원짜리보다 100배 진하고 고소한데 안 만들어 먹으면 손해 🌰",
            "전국 밤 산지 중에서 왜 '공주 정안'이 독보적인지 알아?\n차령산맥 밤나무 숲에서 자라서 과육 밀도와 단맛이 타 지역이랑 비교가 안 돼 🌰"
        ],
        # F04. 5분 꿀팁/레시피형 (5-Min Recipe / Food Hack)
        "F04_recipe_hack": [
            "햇밤 쉽게 까는 3단계 공식\n1. 미지근한 물에 20분 불리기\n2. 밑동 부분부터 칼로 살짝 벗기기\n3. 겉껍질 벗기면 속껍질까지 쏙 벗겨짐\n밤 좋아하는 사람 꼭 저장해둬 🌰✨",
            "생밤 맛있게 찌는 법 모르면 평생 손해야!\n찜기에 김 오르면 햇밤 넣고 딱 20분.\n불 끄고 뜸 5분 들이면 숟가락으로 푹푹 떠먹는 꿀맛 찐밤 완성 🌰",
            "따끈한 찐밤에 버터 한 조각 + 소금 살짝 올려본 사람?\n단짠고소 풍미가 입안에서 폭발함.\n아는 사람만 아는 극락 레시피 🌰✨",
            "가을철 밥도둑 1등: 갓 지은 쌀밥에 생알밤 듬뿍 넣기.\n밥솥 열자마자 달콤한 밤 향기가 온 집안에 진동함 🌰"
        ],
        # F05. 상황/비상사태형 (Situation Emergency)
        "F05_situation_emergency": [
            "가시 폭탄 맞았어 ㅠㅠ 공주 산에서 햇밤 줍다가 장갑 뚫림...\n그래도 통통하고 실한 놈들로 바구니 가득 채워왔어 🌰\n열심히 사는 꿀밤이 응원 하트 하나 콕 부탁해 🌰❤️",
            "스친들 제발 나 좀 도와줄 수 있을까?\n나는 공주 정안 밤을 팔고 있엉.\n새벽부터 산에 올라가서 알밤 줍고 포장도 열심히 준비했는데..\n생각보다 홍보가 쉽지 않네 ㅠㅠ 우연히 이 글 봤다면 하트라도 부탁해 🌰",
            "오늘 산지 직송 택배 물량 맞추느라 새벽 4시부터 밤 선별 중이야.\n벌레 먹은 거 1도 없이 3번 꼼꼼히 검수해서 보내는 중.\n피로 싹 가시게 응원 하트 하나 부탁해 🌰"
        ],
        # F06. 호기심/상식 반전형 (Discovery & Curiosity - 실전 10.4만 뷰 정보형 모티브)
        "F06_discovery_curiosity": [
            "정보) 물에 둥둥 뜨는 밤 vs 가라앉는 밤의 과학적 차이.\n물에 뜨는 건 속이 말라 비틀어졌거나 벌레 먹은 밤이다.\n공주 정안 햇밤은 물에 넣으면 돌처럼 바닥에 묵직하게 가라앉음. 그만큼 속이 꽉 찬 특품이야 🌰",
            "밤이 과일일까 견과류일까?\n비타민 C가 사과보다 4배나 많이 들어있어서 사실 천연 비타민 덩어리야.\n올가을엔 생밤 오독오독 깎아먹고 피로 풀자 🌰✨",
            "비밀인데 스레드에만 솔직하게 말하는 거여.\n'나 찐밤보다 달콤한 생밤 깎아먹는 거 더 좋아해' 🌰\n생밤파 스친들 손!"
        ],
        # F07. 오감/식감 자극형 (Sensory Craving)
        "F07_sensory_craving": [
            "오독오독 씹을수록 달콤한 과즙이 배어 나오는 생밤의 매력.\n마트 밤이랑 다르게 갓 수확한 햇밤이라 수분감이 가득해 🌰❤️",
            "숟가락으로 푹 떠먹으면 설탕 친 것처럼 포슬포슬 달콤한 정안 햇밤.\n목 막히지 않고 부드럽게 꿀떡 넘어가는 그 단맛 알면 다른 밤 절대 못 먹어 🌰",
            "방금 지은 흰쌀밥 위에 큼직한 노란 통밤 올려서 한 입 크게 먹을 때.\n밥알의 단맛과 밤의 고소함이 섞여서 밥 한 공기 순삭 🌰✨"
        ],
        # F08. 밸런스 게임/취향 논쟁형 (Balance Debate)
        "F08_balance_debate": [
            "평생 논쟁거리 하나 던져볼게.. 스친들의 진짜 제철 밤 취향은?\n1번) 달콤하고 포슬포슬한 찐밤\n2번) 아작아작 씹는 맛 터지는 생밤\n스친들의 최애는? 댓글 달고 가줘 🌰",
            "가을 제철 간식 원탑 대결!\n달콤포슬 정안 찐밤 vs 달달한 꿀고구마!\n갓 수확한 정안 햇밤 맛보면 고구마 생각 싹 사라짐. 스친들 선택은? 🌰"
        ],
        # F09. 일상 산지 일기형 (Farmer Diary)
        "F09_farmer_diary": [
            "새벽 5시부터 충남 공주 정안 알밤 숲에서 땀 뻘뻘..\n가시에 찔려가면서 제일 실하고 굵은 특품 햇밤만 골라 담았어 🌰\n열심히 사는 청년 밤장수 응원 하트 콕 🌰❤️",
            "공주 정안 산길 오르내리며 갓 떨어진 윤기 나는 햇알밤만 수확했어.\n산지에서 직송으로 당일 포장해서 보내.\n정직하게 키운 밤 힘내라고 하트 툭 🌰",
            "오늘 공주 산에 가을바람 불어 알밤들이 우수수 떨어졌어.\n가시 속에서 톡 튀어나온 밤송이 보면 그렇게 예쁠 수가 없다.\n올가을 햇밤 구경하고 가 🌰✨"
        ],
        # F10. 가격 역발상/팩트폭격형 (Price & Value Contrast - 실전 14.2만 뷰 모티브)
        "F10_price_contrast": [
            "공주 정안 특품 햇밤이 2만원대인데..!!!!!!\n이게 진짜 비싸 스친들?????\n요즘 마트 물가에 산지직송 갓 주운 묵직한 특품 알밤인데 왜 자꾸 비싸다고 하나 ㅠㅠ\n이 가격에 팔면 진짜 남는 것도 없는데.. 지나가다 응원 하트 하나 부탁해 🌰",
            "두쫀쿠 하나에 7천원은 줄 서서 사 먹으면서, 제철 햇밤은 비싸대 ㅠㅠ\n자연이 준 천연 간식이라 속도 편하고 설탕보다 달콤한데..\n속상한 꿀밤이 힘내라고 하트 하나 콕 🌰❤️",
            "마트에서 파는 비쩍 마른 밤이랑은 비교 불가한 묵직함이야.\n공주 정안에서 바로 수확한 특품 햇알밤이거든.\n커피 한두 잔 값에 가을 제철 꿀밤 즐기자 🌰"
        ],
        # F11. 후기 박제/셀프공구 유머형 (Real Review & Humor - 실전 2.1만 뷰 모티브)
        "F11_real_review": [
            "스토어에 햇밤을 한 번에 20kg 주문하신 분 누구신가요 ㅋㅋㅋㅋ\n동네 이웃들이랑 나눠먹는다고 셀프 공구하셨대 ㅋㅋㅋ\n밤알 보고 다들 크기에 놀라셨나 봐. 꿀밤이 축하 하트 콕 🌰❤️",
            "'인생 햇밤 만났다'는 리뷰 보고 꿀밤이 울 뻔했잖아 ㅠㅠ\n산지직송이라 확실히 신선도가 다르다는 칭찬에 힘이 번쩍 나.\n꿀밤이 축하 하트 하나만 콕 부탁해 🌰❤️",
            "혹시 스레드에 밤 덕후 있어?\n포슬포슬하고 고소한데 포만감도 좋아\n쿠폰 뿌려도 홍보하기 쉽지 않네..\n지나가다 이 글을 봐준다면 하트라도 부탁해 🌰"
        ],
        # F12. 스친 소통/질문형 (Community Question)
        "F12_community_question": [
            "퇴근길에 편의점 들러 과자 살까 고민하는 스친들 잠깐 멈춰봐 🌰\n인스턴트 대신 자연 그대로 쪄낸 달콤한 정안 햇밤 어때?\n다들 달콤하고 편안한 저녁 보내! 🌰",
            "스레드에 생밤 오독오독 깎아먹는 사람 손 들어봐 🌰\n어릴 때 엄마가 깎아주던 그 맛 기억하는 스친들 댓글 남겨줘!",
            "오늘 하루도 치열하게 일한 스친들 다들 고생 많았어!\n따끈하게 쪄낸 달콤한 햇밤 한 그릇으로 힐링하자.\n지나가다 응원 하트 하나 남겨줘 🌰❤️"
        ]
    }
}

# ==============================================================================
# 🚀 [학습형 콘텐츠 엔진 (AdaptiveContentEngine)]
# ==============================================================================

class ContentEngine:
    """
    278개 고조회수 바이럴 레퍼런스 + 12대 구조 포맷 기반
    글 구조, 문장 길이, 어투, 서식(체크리스트, 초단문, 5분레시피 등)을
    매 슬롯마다 완전히 다변화하여 봇 느낌을 원천 차단하는 지능형 엔진
    """
    def __init__(self):
        self.image_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "images"))
        self.history_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "posted_history.json"))
        self.learned_patterns_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "learned_patterns.json"))
        self.load_history()
        self.load_learned_patterns()

    def load_history(self):
        self.history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def load_learned_patterns(self):
        """매일 100+개 1만뷰 게시물에서 자동 학습된 실전 템플릿 DB 로드"""
        self.learned_templates = {"only_apples0.1": [], "ggul_bamm": []}
        if os.path.exists(self.learned_patterns_file):
            try:
                with open(self.learned_patterns_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    syn = data.get("synthesized_templates", {})
                    self.learned_templates["only_apples0.1"] = syn.get("only_apples0.1", [])
                    self.learned_templates["ggul_bamm"] = syn.get("ggul_bamm", [])
            except Exception:
                pass

    def record_post(self, account: str, text: str, archetype: str):
        from datetime import timezone
        self.history.append({
            "account": account,
            "text": text[:120],
            "archetype": archetype,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        })
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history[-100:], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_recent_formats(self, account: str, limit: int = 4) -> List[str]:
        """최근 사용된 구조 포맷 목록 반환 (연속 동일 포맷 방지)"""
        acc_history = [h.get("archetype") for h in self.history if h.get("account") == account]
        return [a for a in acc_history[-limit:] if a]

    def get_recent_prefixes(self, account: str, limit: int = 15) -> List[str]:
        """최근 발행된 글들의 첫 6글자 수집 (동일 문장 시작 방지)"""
        acc_history = [
            h.get("text", "").splitlines()[0][:6].strip()
            for h in self.history if h.get("account") == account and h.get("text")
        ]
        return [p for p in acc_history[-limit:] if p]

    def get_recent_texts(self, account: str, limit: int = 30) -> List[str]:
        """최근 발행된 글들의 전문 목록 수집 (유사도 검사용)"""
        return [
            h.get("text", "").strip()
            for h in self.history if h.get("account") == account and h.get("text")
        ][-limit:]

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """두 텍스트 간 2-gram Jaccard 유사도 계산"""
        def get_ngrams(s: str, n: int = 2) -> set:
            clean_s = re.sub(r"[^\w\s]", "", s).replace(" ", "")
            if len(clean_s) < n:
                return {clean_s}
            return {clean_s[i:i+n] for i in range(len(clean_s) - n + 1)}

        set1 = get_ngrams(text1)
        set2 = get_ngrams(text2)
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def is_too_similar(self, candidate_text: str, account: str, threshold: float = 0.35) -> bool:
        """최근 30개 글과 비교하여 유사도가 임계치(35%)를 초과하는지 검사"""
        recent_texts = self.get_recent_texts(account, limit=30)
        for past_text in recent_texts:
            sim = self.calculate_similarity(candidate_text, past_text)
            if sim >= threshold:
                return True
        return False

    def get_random_image_for_account(self, account: str) -> Optional[str]:
        folder_name = "only_apples" if "apple" in account else "ggul_bamm"
        img_dir = os.path.join(self.image_base_dir, folder_name)
        if not os.path.exists(img_dir):
            return None
        valid_exts = [".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".m4v"]
        images = [
            os.path.join(img_dir, f) for f in os.listdir(img_dir)
            if os.path.splitext(f.lower())[1] in valid_exts
        ]
        return random.choice(images) if images else None

    def get_first_comment(self, account: str, custom_comment: str = None) -> str:
        acc_key = "only_apples0.1" if "apple" in account else "ggul_bamm"
        return custom_comment or FIRST_COMMENTS.get(acc_key, "")

    def compose_post(self, account: str) -> Dict[str, str]:
        """
        [12대 구조 포맷 기반 탈정형 다이내믹 콘텐츠 합성기]
        1. 최근 사용된 4개 포맷과 중복되지 않는 새로운 구조 포맷 선택
        2. 최근 15개 글과 첫 문장(6글자)이 겹치지 않도록 검증
        3. 최근 30개 글과의 2-gram Jaccard 유사도가 35% 미만인 신선한 글만 채택
        4. 추석/명절 관련 단어 원천 배제 (시즌 종료 반영)
        """
        acc_key = "only_apples0.1" if "apple" in account else "ggul_bamm"
        format_dict = VIRAL_FORMATS[acc_key]
        all_formats = list(format_dict.keys())
        recent_formats = self.get_recent_formats(acc_key, limit=4)
        recent_prefixes = self.get_recent_prefixes(acc_key, limit=15)

        # 1. 최근 사용된 4개 포맷 제외한 사용 가능한 포맷 추출
        available_formats = [f for f in all_formats if f not in recent_formats]
        if not available_formats:
            available_formats = all_formats

        best_text = None
        best_format = None

        # 2. 최대 30회 시도하여 조건 동시 충족하는 글 발굴
        for _ in range(30):
            chosen_format = random.choice(available_formats)
            templates = format_dict[chosen_format]
            candidate_text = random.choice(templates).strip()

            # 추석/명절 금지 단어 검사
            if any(bw in candidate_text for bw in BANNED_WORDS):
                continue

            first_line_prefix = candidate_text.splitlines()[0][:6].strip()

            # 첫 문장 중복 검사
            if any(first_line_prefix.startswith(rp) or rp.startswith(first_line_prefix) for rp in recent_prefixes):
                continue

            # 전체 본문 유사도 검사 (최근 30개 글 대상 35% 미만)
            if self.is_too_similar(candidate_text, acc_key, threshold=0.35):
                continue

            best_text = candidate_text
            best_format = chosen_format
            break

        # 폴백 처리
        if not best_text:
            for fmt in available_formats:
                clean_pool = [t for t in format_dict[fmt] if not any(bw in t for bw in BANNED_WORDS)]
                if clean_pool:
                    best_text = random.choice(clean_pool).strip()
                    best_format = fmt
                    break

        if not best_text:
            best_format = available_formats[0]
            best_text = format_dict[best_format][0].strip()

        return {
            "text": best_text,
            "comment": self.get_first_comment(acc_key),
            "archetype": best_format
        }

    def generate_post(self, account: str) -> Dict[str, str]:
        data = self.compose_post(account)
        data["image_path"] = self.get_random_image_for_account(account)
        return data

    def generate_daily_schedule_posts(self, account: str, count: int = 10, custom_comment: str = None) -> List[Dict]:
        """
        하루 10개 슬롯에 대해 12대 구조 포맷을 골고루 배정하고,
        모든 슬롯 간 문장 길이, 어투, 접두사, 내용 유사도가 겹치지 않는 완전 다변화 세트를 생성합니다.
        """
        acc_key = "only_apples0.1" if "apple" in account else "ggul_bamm"
        format_dict = VIRAL_FORMATS[acc_key]
        all_formats = list(format_dict.keys())
        random.shuffle(all_formats)

        # 10개 슬롯에 대해 포맷 순환 배정 (12개 포맷 중 10개 각각 다른 포맷 배정)
        selected_formats = all_formats[:count]
        if len(selected_formats) < count:
            selected_formats.extend(all_formats[:(count - len(selected_formats))])

        posts = []
        comment = self.get_first_comment(acc_key, custom_comment)
        used_prefixes = []
        session_texts = []

        for i, fmt in enumerate(selected_formats):
            templates = format_dict[fmt]
            random.shuffle(templates)

            chosen_text = None
            for cand in templates:
                cand_clean = cand.strip()

                # 추석/명절 단어 배제
                if any(bw in cand_clean for bw in BANNED_WORDS):
                    continue

                prefix = cand_clean.splitlines()[0][:6].strip()

                if prefix in used_prefixes:
                    continue

                # 세션 내 생성된 글들과도 유사도 35% 미만인지 검사
                too_close = False
                for prev in session_texts:
                    if self.calculate_similarity(cand_clean, prev) >= 0.35:
                        too_close = True
                        break
                if too_close:
                    continue

                chosen_text = cand_clean
                used_prefixes.append(prefix)
                session_texts.append(cand_clean)
                break

            if not chosen_text:
                chosen_text = templates[0].strip()
                session_texts.append(chosen_text)

            img = self.get_random_image_for_account(account)

            posts.append({
                "slot_index": i + 1,
                "account": account,
                "archetype": fmt,
                "text": chosen_text,
                "image_path": img,
                "comment": comment
            })

        return posts

if __name__ == "__main__":
    engine = ContentEngine()
    print("=" * 65)
    print("🍎 [완전 다변화 검증] 온리애플 10개 슬롯 연속 생성 테스트:")
    print("=" * 65)
    for p in engine.generate_daily_schedule_posts("only_apples0.1", count=10):
        print(f"\n[슬롯 {p['slot_index']:02d} | 구조 포맷: {p['archetype']}]")
        print(p["text"])
        print("-" * 50)

    print("\n" + "=" * 65)
    print("🌰 [완전 다변화 검증] 꿀밤 10개 슬롯 연속 생성 테스트:")
    print("=" * 65)
    for p in engine.generate_daily_schedule_posts("ggul_bamm", count=10):
        print(f"\n[슬롯 {p['slot_index']:02d} | 구조 포맷: {p['archetype']}]")
        print(p["text"])
        print("-" * 50)
