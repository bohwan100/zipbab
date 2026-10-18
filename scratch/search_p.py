import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import coupang_partners
import requests, time, hmac, hashlib, urllib.parse

def search_products(kw, limit=10):
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
    print(f"=== Results for: {kw} ===")
    for it in items:
        pid = it.get('productId')
        name = it.get('productName')
        price = it.get('productPrice')
        rocket = it.get('isRocket')
        url = it.get('productUrl')
        print(f"ID: {pid} | {name} | {price}원 | Rocket: {rocket} | URL: {url}")

search_products("백설 하얀설탕 1kg")
search_products("국내산 양파 1.5kg")
search_products("국내산 흙대파")
