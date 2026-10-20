#!/usr/bin/env python3
import os
import sys
import json

ROOT = "/Users/bohwanlee/Desktop/antigravity 폴더"
sys.path.insert(0, os.path.join(ROOT, "generator"))
sys.path.insert(0, os.path.join(ROOT, "scratch"))

import build_client as builder

print("--- 1. Rebuilding 김태영_23 with 한식, 일식, 양식 ---")
builder.build_client(
    client_id="김태영_23",
    name="김태영",
    age="23",
    household="1명",
    budget=300000,
    frequency="저녁만 (30끼)",
    goal="일반식",
    cuisine="한식, 일식, 양식",
    exclude="어류",
    pantry="진간장, 식용유, 설탕, 고춧가루, 쌀",
    goal_notes=""
)

print("\n--- 2. Rebuilding 최종본_100세_2 with 한식, 일식, 양식, 중식 ---")
builder.build_client(
    client_id="최종본_100세_2",
    name="최종본 !!!",
    age="100",
    household="1명",
    budget=300000,
    frequency="저녁만 (30끼)",
    goal="일반식",
    cuisine="한식, 일식, 양식, 중식",
    exclude="없음",
    pantry="아무것도 없음",
    goal_notes=""
)

print("\n--- 3. Regenerating clients.html ---")
import subprocess
subprocess.run([sys.executable, os.path.join(ROOT, "scratch", "generate_clients_dashboard.py")], check=True)

print("\nAll done!")
