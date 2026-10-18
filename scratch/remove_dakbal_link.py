import os
import requests
import json
from pathlib import Path

env_path = Path(".env")
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'").strip('"')

headers = {
    "Authorization": f"Bearer {os.environ.get('NOTION_API_KEY')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Update block 3f658961-82de-81c3-915a-ea531a94a2ee to plain text without link
block_id = "3f658961-82de-81c3-915a-ea531a94a2ee"
payload = {
    "to_do": {
        "rich_text": [
            {
                "type": "text",
                "text": {
                    "content": "닭발 1kg"
                }
            }
        ]
    }
}

res = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=headers, json=payload)
print("Status:", res.status_code)
if res.status_code == 200:
    print("성공: 닭발 1kg의 비수익 파트너스 링크를 완전히 제거하고 깔끔한 텍스트로 복원했습니다.")
else:
    print("오류:", res.text)
