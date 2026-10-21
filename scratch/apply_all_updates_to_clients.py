#!/usr/bin/env python3
"""
모든 고객 최신 시스템 일괄 적용 스크립트
(규칙: 사용자가 '김태영거는 바꾸지마. 내가 요청했을 때만'이라고 지정한 '김태영_23'은 철저히 보호/제외하고 나머지 전원 리빌드)
"""

import os
import sys
import json
import subprocess

ROOT = "/Users/bohwanlee/Desktop/antigravity 폴더"
sys.path.insert(0, os.path.join(ROOT, "generator"))

import build_client as builder

clients_dir = os.path.join(ROOT, "clients")
clients = sorted(os.listdir(clients_dir))

updated_clients = []
skipped_clients = []

for c in clients:
    c_path = os.path.join(clients_dir, c)
    if not os.path.isdir(c_path):
        continue
    
    # [사용자 규칙 엄수] 김태영 고객은 사용자가 직접 지목 요청하기 전까지 절대 수정하지 않고 보존
    if "김태영" in c:
        print(f"🔒 [보호 대상 제외] {c} - 사용자 특별 지시('내가 요청했을 때만')에 따라 원본 100% 유지")
        skipped_clients.append(c)
        continue

    info_path = os.path.join(c_path, "client_info.json")
    if not os.path.exists(info_path):
        print(f"⚠️ [건너뜀] {c} - client_info.json 없음")
        continue

    with open(info_path, "r", encoding="utf-8") as f:
        d = json.load(f)

    cid = d.get("client_id", c)
    name = d.get("client_name", c.split("_")[0])
    age = d.get("client_age", "30대")
    household = d.get("household_size", "1명")
    budget = d.get("budget", 300000)
    freq = d.get("meal_frequency", "하루 한 끼 (퇴근 후 저녁 30끼)")
    goal = d.get("goal", "일반식")
    cuisine = d.get("cuisine", "한식, 일식")
    exclude = d.get("excluded_foods", "없음")
    pantry = d.get("pantry_items", "아무것도 없음")
    goal_notes = d.get("goal_notes", "")

    print(f"\n🚀 [최신 업데이트 적용 중] {cid} ({name}님 / {household} / {budget:,}원 / {cuisine} / 목표: {goal})")
    try:
        builder.build_client(
            client_id=cid,
            name=name,
            age=age,
            household=household,
            budget=budget,
            frequency=freq,
            goal=goal,
            cuisine=cuisine,
            exclude=exclude,
            pantry=pantry,
            goal_notes=goal_notes
        )
        updated_clients.append(cid)
    except Exception as e:
        print(f"❌ Error rebuilding {cid}: {e}")

print("\n" + "="*70)
print(f"✅ 업데이트 완료: 총 {len(updated_clients)}명 고객 파일 갱신")
print(f"🔒 안전 보호: 총 {len(skipped_clients)}명 ({', '.join(skipped_clients)})")
print("="*70)

print("\n--- 3. Regenerating clients.html ---")
subprocess.run([sys.executable, os.path.join(ROOT, "scratch", "generate_clients_dashboard.py")], check=True)
print("All clients dashboard updated with cache-busting URLs!")
