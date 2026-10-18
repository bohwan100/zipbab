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

# Blocks to update:
# 1. 설탕 50g -> 3f658961-82de-8168-9f91-e51c47b7b1fd
#    Link: https://link.coupang.com/a/hLBWZHVZgi (백설 하얀설탕 1kg 1개 로켓배송)
# 2. 양파 1/2개 (110g) -> 3f658961-82de-819c-b2d7-c919107718f7
#    Link: https://link.coupang.com/a/hLBWZ568HY (국내산 양파 로켓프레시)
# 3. 대파 3개 (80g) -> 3f658961-82de-8127-8d7a-cc76c4e92960
#    Link: https://link.coupang.com/a/hLBW0skzSK (흙대파 1단 로켓프레시)

updates = [
    {
        "id": "3f658961-82de-8168-9f91-e51c47b7b1fd",
        "name": "설탕 50g",
        "url": "https://link.coupang.com/a/hLBWZHVZgi"
    },
    {
        "id": "3f658961-82de-819c-b2d7-c919107718f7",
        "name": "양파 1/2개 (110g)",
        "url": "https://link.coupang.com/a/hLBWZ568HY"
    },
    {
        "id": "3f658961-82de-8127-8d7a-cc76c4e92960",
        "name": "대파 3개 (80g)",
        "url": "https://link.coupang.com/a/hLBW0skzSK"
    }
]

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
