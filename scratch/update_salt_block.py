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

# 소금 10g block ID: 3f658961-82de-81a9-ad9c-c2d4be713f51
block_id = "3f658961-82de-81a9-ad9c-c2d4be713f51"
text_content = "소금 10g "
url = "https://link.coupang.com/a/hLB7lAWERE"

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
print(f"Status: {res.status_code}")
if res.status_code == 200:
    print("성공적으로 소금 10g 블록에 쿠팡 파트너스 링크를 등록했습니다!")
else:
    print("Error:", res.text)
