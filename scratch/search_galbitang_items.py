import sys
from pathlib import Path
sys.path.insert(0, str(Path("scratch").resolve().parent))
import coupang_partners
import requests, time, hmac, hashlib, urllib.parse

def search_products(kw, limit=5):
    url_path = "/v2/providers/affiliate_open_api/apis/openapi/v1/products/search"
    query_str = f"keyword={urllib.parse.quote(kw)}&limit={limit}"
    datetime_str = time.strftime("%y%m%d", time.gmtime()) + "T" + time.strftime("%H%M%S", time.gmtime()) + "Z"
    message = datetime_str + "GET" + url_path + query_str
    sig = hmac.new(coupang_partners.SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {
        "Authorization": f"CEA algorithm=HmacSHA256, access-key={coupang_partners.ACCESS_KEY}, signed-date={datetime_str}, signature={sig}",
        "Content-Type": "application/json"
    }
    r = requests.get(f"{coupang_partners.GATEWAY_HOST}{url_path}?{query_str}", headers=headers)
    items = r.json().get("data", {}).get("productData", [])
    print(f"\n=== Results for: {kw} ===")
    for it in items:
        pid = it.get('productId')
        name = it.get('productName')
        price = it.get('productPrice')
        rocket = it.get('isRocket')
        url = it.get('productUrl')
        print(f"ID: {pid} | {name} | {price}원 | Rocket: {rocket} | URL: {url}")

search_products("곰곰 우삼겹 바로구이")
search_products("우삼겹 로켓프레시")
search_products("한라 참치액 500ml")
search_products("오뚜기 납작당면")
search_products("넓적당면 로켓배송")
