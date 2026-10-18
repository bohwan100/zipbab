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

# Search Notion for "우삼겹" or "갈비탕"
search_res = requests.post(
    "https://api.notion.com/v1/search",
    headers=headers,
    json={"query": "우삼겹", "page_size": 20}
)
print("Search status:", search_res.status_code)
for item in search_res.json().get("results", []):
    obj = item.get("object")
    iid = item.get("id")
    if obj == "page":
        props = item.get("properties", {})
        title_list = props.get("title", {}).get("title", [])
        title = "".join([t.get("plain_text", "") for t in title_list])
        print(f"[Page] {iid}: {title}")
    elif obj == "block":
        btype = item.get("type")
        rt = item.get(btype, {}).get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in rt])
        print(f"[Block] {iid} ({btype}): {text}")

# Also list children of master page
url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
resp = requests.get(url, headers=headers)
results = resp.json().get("results", [])
print(f"\nMaster page child count: {len(results)}")
for b in results:
    btype = b.get("type")
    rt = b.get(btype, {}).get("rich_text", [])
    text = "".join([t.get("plain_text", "") for t in rt])
    if "우삼겹" in text or "갈비탕" in text:
        print(f"[Master child match] {b.get('id')} ({btype}): {text}")
    elif any(num in text for num in ["20.", "21.", "22.", "23.", "24."]):
        print(f"[Master child recipe] {b.get('id')} ({btype}): {text}")
