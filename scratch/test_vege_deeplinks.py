import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import coupang_partners

test_pids = [
    # 설탕: 백설 하얀설탕 1kg
    ("설탕", "https://www.coupang.com/vp/products/7143767691?itemId=3889146067"),
    ("설탕2", "https://www.coupang.com/vp/products/9498948789"),
    # 양파: 국내산 양파
    ("양파", "https://www.coupang.com/vp/products/1074470755"),
    # 대파: 흙대파
    ("대파", "https://www.coupang.com/vp/products/6528172171?itemId=5911958170"),
]

for name, u in test_pids:
    res = coupang_partners.generate_deeplinks([u])
    print(f"[{name}] {u} -> {res}")
