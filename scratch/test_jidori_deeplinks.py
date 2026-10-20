import sys
from pathlib import Path
sys.path.insert(0, str(Path("scratch").resolve().parent))
import coupang_partners

candidates = [
    # 우동면
    ("면사랑 사누끼우동면 5개입 4980원", "https://www.coupang.com/vp/products/8341377794?itemId=24089887162"),
    ("풀무원 수타식 우동사리면 1인분", "https://www.coupang.com/vp/products/7790479797?itemId=28993445565"),
    # 닭다리살
    ("마니커 닭다리살 정육 냉장 500g", "https://www.coupang.com/vp/products/1478827813"),
    ("곰곰 순살 닭다리살 냉동", "https://www.coupang.com/vp/products/9608009961"),
    # 혼쯔유
    ("기꼬만 혼쯔유 코이다시 500ml", "https://www.coupang.com/vp/products/193942663"),
]

for label, url in candidates:
    res = coupang_partners.generate_deeplinks([url])
    print(f"[{label}] -> {res}")
