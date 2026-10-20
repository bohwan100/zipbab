import json
from pathlib import Path

cache_path = Path("data/partners_links_cache.json")
cache = {}
if cache_path.exists():
    with open(cache_path, "r", encoding="utf-8") as f:
        cache = json.load(f)

new_entries = {
    "우동면 1개 (200g)": {
        "query": "우동면 1개 (200g)",
        "productName": "면사랑 사누끼 우동면 (냉동) 250g x 5개입",
        "shortenUrl": "https://link.coupang.com/a/h0jpCimcX6"
    },
    "닭다리살 150g": {
        "query": "닭다리살 150g",
        "productName": "마니커 무항생제 인증 닭다리살 정육 (냉장) 500g",
        "shortenUrl": "https://link.coupang.com/a/h0jpDchbAO"
    },
    "혼쯔유 40ml": {
        "query": "혼쯔유 40ml",
        "productName": "기꼬만 혼쯔유 코이다시 500ml",
        "shortenUrl": "https://link.coupang.com/a/h0jpEx2xoa"
    }
}

cache.update(new_entries)
with open(cache_path, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print("캐시 업데이트 완료!")
