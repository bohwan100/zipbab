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

block_id = "3fa58961-82de-80ae-a014-f892bf28066e"
res = requests.get(f"https://api.notion.com/v1/blocks/{block_id}/children", headers=headers)
print("Status:", res.status_code)
for b in res.json().get("results", []):
    btype = b.get("type")
    rt = b.get(btype, {}).get("rich_text", [])
    text = "".join([t.get("plain_text", "") for t in rt])
    print(f"[{b.get('id')}] {btype}: {text}")
