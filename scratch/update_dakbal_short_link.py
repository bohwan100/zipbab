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

# The user provided Coupang product link
raw_target_url = "https://www.coupang.com/vp/products/7708926691?itemId=20659241166&vendorItemId=87707484634"
short_url = "https://tinyurl.com/28jjcw7a"

block_id = "3f658961-82de-81c3-915a-ea531a94a2ee"
payload = {
    "to_do": {
        "rich_text": [
            {
                "type": "text",
                "text": {
                    "content": "닭발 1kg "
                }
            },
            {
                "type": "text",
                "text": {
                    "content": short_url,
                    "link": {
                        "url": raw_target_url
                    }
                }
            }
        ]
    }
}

res = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=headers, json=payload)
print("Status:", res.status_code)
if res.status_code == 200:
    print("성공적으로 노션 닭발 1kg에 단축 링크를 업데이트했습니다!")
else:
    print("에러:", res.text)
