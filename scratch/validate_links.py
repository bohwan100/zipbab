import requests

links = {
    "우삼겹": "https://link.coupang.com/a/hR4fNMaruK",
    "굴소스": "https://link.coupang.com/a/hLAEgr2BI4",
    "참치액": "https://link.coupang.com/a/hR4fOIUAg0",
    "미림": "https://link.coupang.com/a/hLA1WfoDM4",
    "마늘": "https://link.coupang.com/a/hLAEP5Zr3s",
    "소금": "https://link.coupang.com/a/hLB7lAWERE",
    "대파": "https://link.coupang.com/a/hLBW0skzSK",
    "넙적당면": "https://link.coupang.com/a/hR4fPfwZEW",
    "후추": "https://link.coupang.com/a/hLAEQE0U0W"
}

headers = {"User-Agent": "Mozilla/5.0"}
for name, url in links.items():
    try:
        r = requests.head(url, headers=headers, allow_redirects=False, timeout=5)
        loc = r.headers.get("Location", "")[:60]
        print(f"[{name}] {url} -> status {r.status_code}, redirect: {loc}")
    except Exception as e:
        print(f"[{name}] error: {e}")
