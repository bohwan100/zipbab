import os
import sys
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENTS_DIR = os.path.join(ROOT_DIR, "clients")
GENERATOR_DIR = os.path.join(ROOT_DIR, "generator")

sys.path.insert(0, GENERATOR_DIR)
import build_client as builder

# 1. Remove unwanted mock clients
mock_dirs = [
    '강프리미엄_35세',
    '김민수_31세',
    '김민수_31세_2',
    '김민수_40세',
    '김민수_40세_2',
    '김홍현_25세',
    '앙기모_31세',
    '이보환_30일집밥',
    '최다이어트_25세'
]

for md in mock_dirs:
    target = os.path.join(CLIENTS_DIR, md)
    if os.path.exists(target):
        print(f"Removing old mock: {md}")
        shutil.rmtree(target, ignore_errors=True)

# 2. Define the exact 8-9 clients from last night starting with 정유진
clients_to_restore = [
    {
        "client_id": "정유진_37",
        "name": "정유진",
        "age": "37세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식, 중식, 양식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": "퇴근 후 간편하고 맛있는 건강 집밥"
    },
    {
        "client_id": "최민석_26",
        "name": "최민석",
        "age": "26세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식, 중식, 양식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": "배달음식 줄이고 1인 자취 식비 절약"
    },
    {
        "client_id": "차민홍_34",
        "name": "차민홍",
        "age": "34세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식, 양식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": "건강하고 균형 잡힌 저녁 식단"
    },
    {
        "client_id": "정진향_41",
        "name": "정진향",
        "age": "41세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식, 중식, 양식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": "퇴근 후 간편하고 따뜻한 집밥"
    },
    {
        "client_id": "노한석_30",
        "name": "노한석",
        "age": "30세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식, 중식, 양식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": "식비 20만원으로 알뜰하게 즐기는 집밥"
    },
    {
        "client_id": "정수원_21세",
        "name": "정수원",
        "age": "21세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": "자취생 첫 집밥 도전"
    },
    {
        "client_id": "테스트_22",
        "name": "테스트",
        "age": "22세",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": ""
    },
    {
        "client_id": "테스트_30대",
        "name": "테스트",
        "age": "30대",
        "household": "1명",
        "budget": 200000,
        "frequency": "하루 한 끼 (퇴근 후 저녁 30끼)",
        "goal": "일반식",
        "cuisine": "한식, 일식",
        "exclude": "없음",
        "pantry": "아무것도 없음",
        "goal_notes": ""
    }
]

print("Generating clients...")
for c in clients_to_restore:
    cid = c["client_id"]
    print(f"-> Building client: {cid}")
    builder.build_client(
        client_id=cid,
        name=c["name"],
        age=c["age"],
        household=c["household"],
        budget=c["budget"],
        frequency=c["frequency"],
        goal=c["goal"],
        cuisine=c["cuisine"],
        exclude=c["exclude"],
        pantry=c["pantry"],
        goal_notes=c["goal_notes"]
    )

print("All target clients built successfully!")
