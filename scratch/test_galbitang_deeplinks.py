import sys
from pathlib import Path
sys.path.insert(0, str(Path("scratch").resolve().parent))
import coupang_partners

test_items = [
    # 우삼겹
    ("우삼겹1", "https://www.coupang.com/vp/products/6976599392?itemId=17030258185"),
    ("우삼겹_곰곰", "https://www.coupang.com/vp/products/8336308869"),
    # 참치액
    ("참치액_한라", "https://www.coupang.com/vp/products/6596111"),
    # 납작당면
    ("납작당면_백설", "https://www.coupang.com/vp/products/6659186715?itemId=15281504396"),
    ("납작당면_오뚜기", "https://www.coupang.com/vp/products/7510828279?itemId=19679439777"),
]

for name, u in test_items:
    res = coupang_partners.generate_deeplinks([u])
    print(f"[{name}] {u} -> {res}")
