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

page_id = os.environ.get("NOTION_PAGE_ID", "").replace("-", "")

url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
resp = requests.get(url, headers=headers)
results = resp.json().get("results", [])

print("총 블록 수:", len(results))
for b in results:
    btype = b.get("type")
    rt = b.get(btype, {}).get("rich_text", [])
    text = "".join([t.get("plain_text", "") for t in rt])
    if any(k in text for k in ["24", "지도리", "우동", "23", "22"]):
        print(f"[{b.get('id')}] {btype}: {text}")
