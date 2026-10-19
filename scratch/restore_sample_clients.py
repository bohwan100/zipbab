#!/usr/bin/env python3
"""
Restore the 9 sample test clients that were present yesterday.
"""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "generator"))
import build_client as builder

SAMPLE_CLIENTS = [
    {
        "id": "김홍현_25세", "name": "김홍현", "age": "25세", "household": "1명",
        "budget": 300000, "frequency": "저녁만 (30끼)", "goal": "일반식",
        "cuisine": "한식, 일식, 양식", "exclude": "없음", "pantry": "아무것도 없음",
        "goal_notes": "배달 음식을 줄이고 건강한 자취 요리를 직접 해먹고 싶어요."
    },
    {
        "id": "이보환_30일집밥", "name": "이보환", "age": "30대", "household": "1명",
        "budget": 300000, "frequency": "저녁만 (30끼)", "goal": "다이어트",
        "cuisine": "한식, 일식", "exclude": "없음", "pantry": "기본 양념만 있음",
        "goal_notes": "체중 감량과 식비 절약을 동시에 달성하는 건강한 집밥."
    },
    {
        "id": "김민수_31세", "name": "김민수", "age": "31세", "household": "1명",
        "budget": 300000, "frequency": "저녁만 (30끼)", "goal": "일반식",
        "cuisine": "한식, 일식, 양식, 중식", "exclude": "오이", "pantry": "쌀, 간장",
        "goal_notes": "퇴근 후 15분 만에 맛있게 먹을 수 있는 가성비 식단."
    },
    {
        "id": "최다이어트_25세", "name": "최다이어트", "age": "25세", "household": "1명",
        "budget": 200000, "frequency": "저녁만 (30끼)", "goal": "다이어트",
        "cuisine": "한식", "exclude": "밀가루", "pantry": "아무것도 없음",
        "goal_notes": "단백질 위주의 가성비 20만원 한식 다이어트."
    },
    {
        "id": "강프리미엄_35세", "name": "강프리미엄", "age": "35세", "household": "3명",
        "budget": 500000, "frequency": "저녁만 (30끼)", "goal": "고단백·근육 증가",
        "cuisine": "한식, 일식, 양식", "exclude": "없음", "pantry": "쌀, 기본 조미료",
        "goal_notes": "가족 3인이 함께 먹는 푸짐하고 든든한 고단백 맞춤 식단."
    },
    {
        "id": "김민수_40세", "name": "김민수", "age": "40세", "household": "2명",
        "budget": 500000, "frequency": "저녁만 (30끼)", "goal": "다이어트",
        "cuisine": "한식", "exclude": "없음", "pantry": "아무것도 없음",
        "goal_notes": "부부가 함께 실천하는 건강한 저염식 식단."
    },
    {
        "id": "앙기모_31세", "name": "앙기모", "age": "31세", "household": "1명",
        "budget": 300000, "frequency": "저녁만 (30끼)", "goal": "벌크업",
        "cuisine": "한식, 일식", "exclude": "없음", "pantry": "간장, 참기름",
        "goal_notes": "운동 후 근육 성장을 위한 탄단지 균형 식단."
    },
    {
        "id": "김민수_31세_2", "name": "김민수", "age": "31세", "household": "1명",
        "budget": 300000, "frequency": "저녁만 (30끼)", "goal": "일반식",
        "cuisine": "한식, 일식, 양식, 중식", "exclude": "없음", "pantry": "아무것도 없음",
        "goal_notes": "다양한 4개국 요리를 골고루 즐기는 집밥 플랜."
    },
    {
        "id": "김민수_40세_2", "name": "김민수", "age": "40세", "household": "2명",
        "budget": 500000, "frequency": "저녁만 (30끼)", "goal": "다이어트",
        "cuisine": "한식", "exclude": "돼지고기", "pantry": "기본 양념",
        "goal_notes": "소고기와 닭고기 위주의 깔끔한 식단."
    }
]

def restore_all():
    print("🚀 Restoring sample clients...")
    for sc in SAMPLE_CLIENTS:
        print(f"Creating [{sc['id']}]...")
        builder.build_client(
            client_id=sc["id"],
            name=sc["name"],
            age=sc["age"],
            household=sc["household"],
            budget=sc["budget"],
            frequency=sc["frequency"],
            goal=sc["goal"],
            cuisine=sc["cuisine"],
            exclude=sc["exclude"],
            pantry=sc["pantry"],
            goal_notes=sc["goal_notes"]
        )
    
    # Regenerate clients dashboard
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT_DIR, "scratch", "generate_clients_dashboard.py")], check=True)
    print("✅ All 9 clients restored and clients.html updated!")

if __name__ == "__main__":
    restore_all()
