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

updates = [
    {
        "id": "3fa58961-82de-80b1-8022-d8cb9ca1596a",
        "name": "우삼겹 200g",
        "url": "https://link.coupang.com/a/hR4fNMaruK"
    },
    {
        "id": "3fa58961-82de-8026-9b90-c825e8006c28",
        "name": "굴소스 15g",
        "url": "https://link.coupang.com/a/hLAEgr2BI4"
    },
    {
        "id": "3fa58961-82de-80bd-b001-ef28dcfc18d4",
        "name": "참치액 15g",
        "url": "https://link.coupang.com/a/hR4fOIUAg0"
    },
    {
        "id": "3fa58961-82de-802a-82f7-db02e80cd8e8",
        "name": "미림 15g",
        "url": "https://link.coupang.com/a/hLA1WfoDM4"
    },
    {
        "id": "3fa58961-82de-80f0-bb71-df04163b6fce",
        "name": "마늘 5g",
        "url": "https://link.coupang.com/a/hLAEP5Zr3s"
    },
    {
        "id": "3fa58961-82de-8060-ac8b-c81b98653201",
        "name": "소금 1/3T",
        "url": "https://link.coupang.com/a/hLB7lAWERE"
    },
    {
        "id": "3fa58961-82de-803f-a3b3-e9f7b70a405d",
        "name": "대파 20g",
        "url": "https://link.coupang.com/a/hLBW0skzSK"
    },
    {
        "id": "3fa58961-82de-80a2-9d09-d2a6325a3f51",
        "name": "넙적당면(좋아하는 만큼)",
        "url": "https://link.coupang.com/a/hR4fPfwZEW"
    },
    {
        "id": "3fa58961-82de-80d6-9315-f53f3edcf75b",
        "name": "후추 살짝",
        "url": "https://link.coupang.com/a/hLAEQE0U0W"
    }
]

print(f"총 {len(updates)}개 재료 링크 업데이트 시작...")
for item in updates:
    block_id = item["id"]
    text_content = item["name"] + " "
    url = item["url"]

    payload = {
        "to_do": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": text_content
                    }
                },
                {
                    "type": "text",
                    "text": {
                        "content": url,
                        "link": {
                            "url": url
                        }
                    }
                }
            ]
        }
    }

    res = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=headers, json=payload)
    print(f"[{item['name']}] Status: {res.status_code}")
    if res.status_code != 200:
        print("Error:", res.text)

print("\n모든 블록 업데이트 완료!")
