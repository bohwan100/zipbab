import json
from pathlib import Path

cache_path = Path("data/partners_links_cache.json")
cache = {}
if cache_path.exists():
    with open(cache_path, "r", encoding="utf-8") as f:
        cache = json.load(f)

new_entries = {
    "우삼겹 200g": {
        "query": "우삼겹 200g",
        "productName": "대패 우삼겹 (냉동) 600g",
        "shortenUrl": "https://link.coupang.com/a/hR4fNMaruK"
    },
    "참치액 15g": {
        "query": "참치액 15g",
        "productName": "한라식품 참치액 500ml",
        "shortenUrl": "https://link.coupang.com/a/hR4fOIUAg0"
    },
    "넙적당면": {
        "query": "넙적당면",
        "productName": "백설 대왕 납작당면 300g",
        "shortenUrl": "https://link.coupang.com/a/hR4fPfwZEW"
    }
}

cache.update(new_entries)
with open(cache_path, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print("캐시 파일 업데이트 완료!")
