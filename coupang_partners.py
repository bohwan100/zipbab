import os
import sys
import json
import time
import hmac
import hashlib
import urllib.parse
import requests
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
CACHE_PATH = BASE_DIR / "data" / "partners_links_cache.json"

def load_env():
    """Loads environment variables from .env if present."""
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip("'").strip('"')
                    os.environ[key.strip()] = val

load_env()

ACCESS_KEY = os.environ.get("COUPANG_PARTNERS_ACCESS_KEY", "676d3de9-7f03-469a-9001-1264226f2647")
SECRET_KEY = os.environ.get("COUPANG_PARTNERS_SECRET_KEY", "31fc336eb4798c0dc115c0874584789dbfb5967d")
TRACKING_ID = os.environ.get("COUPANG_PARTNERS_TRACKING_ID", "AF9148506")

GATEWAY_HOST = "https://api-gateway.coupang.com"
DEEPLINK_PATH = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"


def _generate_auth_header(method: str, path: str) -> tuple[str, str]:
    """Generates the HMAC-SHA256 authorization header for Coupang Partners Open API."""
    datetime_gmt = time.strftime('%y%m%d', time.gmtime()) + 'T' + time.strftime('%H%M%S', time.gmtime()) + 'Z'
    message = datetime_gmt + method + path
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    auth_header = f"CEA algorithm=HmacSHA256, access-key={ACCESS_KEY}, signed-date={datetime_gmt}, signature={signature}"
    return auth_header, datetime_gmt


def load_cache() -> dict:
    """Loads cached deeplinks."""
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Coupang Partners] Cache load warning: {e}")
    return {}


def save_cache(cache: dict):
    """Saves deeplinks cache to file."""
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def generate_deeplinks(urls: list[str]) -> list[dict]:
    """
    Calls Coupang Partners Open API to convert raw Coupang URLs to affiliate short links.
    Supports batching up to 20 URLs at a time.
    """
    if not urls:
        return []

    results = []
    chunk_size = 20
    
    for i in range(0, len(urls), chunk_size):
        chunk = urls[i:i + chunk_size]
        auth_header, _ = _generate_auth_header("POST", DEEPLINK_PATH)
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": auth_header
        }
        payload = {"coupangUrls": chunk}

        try:
            resp = requests.post(
                f"{GATEWAY_HOST}{DEEPLINK_PATH}",
                headers=headers,
                json=payload,
                timeout=12
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("rCode") == "0" and "data" in data:
                    results.extend(data["data"])
                else:
                    print(f"[Coupang Partners] API Error: {data.get('rMessage')}")
            else:
                print(f"[Coupang Partners] HTTP Error {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[Coupang Partners] Request Exception: {e}")

    return results


def get_deeplink_for_query(query: str) -> str:
    """
    Returns an affiliate shortened URL for a search query.
    Checks cache first, generates on-demand if missing.
    """
    cache = load_cache()
    if query in cache:
        return cache[query].get("shortenUrl", "")

    raw_url = f"https://www.coupang.com/np/search?q={urllib.parse.quote(query)}&channel=user"
    api_res = generate_deeplinks([raw_url])
    
    if api_res and len(api_res) > 0:
        item = api_res[0]
        cache[query] = {
            "query": query,
            "originalUrl": raw_url,
            "shortenUrl": item.get("shortenUrl", raw_url),
            "landingUrl": item.get("landingUrl", ""),
            "updatedAt": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        save_cache(cache)
        return cache[query]["shortenUrl"]

    return raw_url


def warm_up_product_links(queries: list[str]) -> dict:
    """
    Batches link creation for all product queries to optimize speed and cache everything.
    """
    cache = load_cache()
    missing_queries = [q for q in queries if q not in cache]

    if missing_queries:
        print(f"[Coupang Partners] Generating affiliate links for {len(missing_queries)} new items...")
        url_map = {}
        for q in missing_queries:
            raw_url = f"https://www.coupang.com/np/search?q={urllib.parse.quote(q)}&channel=user"
            url_map[raw_url] = q

        api_results = generate_deeplinks(list(url_map.keys()))
        for res in api_results:
            orig = res.get("originalUrl", "")
            q = url_map.get(orig)
            if q:
                cache[q] = {
                    "query": q,
                    "originalUrl": orig,
                    "shortenUrl": res.get("shortenUrl", orig),
                    "landingUrl": res.get("landingUrl", ""),
                    "updatedAt": time.strftime("%Y-%m-%d %H:%M:%S")
                }
        save_cache(cache)
        print(f"[Coupang Partners] Successfully cached {len(api_results)} affiliate links!")
    else:
        print(f"[Coupang Partners] All {len(queries)} items already cached.")

    return {q: cache.get(q, {}).get("shortenUrl", "") for q in queries}


def get_all_cached_links() -> dict:
    """Returns mapping of query -> {shortenUrl, landingUrl, etc.}."""
    return load_cache()


def get_account_status() -> dict:
    """Returns current Coupang Partners connection status."""
    cache = load_cache()
    return {
        "connected": bool(ACCESS_KEY and SECRET_KEY),
        "trackingId": TRACKING_ID,
        "accessKey": f"{ACCESS_KEY[:8]}...{ACCESS_KEY[-4:]}" if ACCESS_KEY else "",
        "cachedLinksCount": len(cache),
        "lastUpdated": time.strftime("%Y-%m-%d %H:%M:%S")
    }


if __name__ == "__main__":
    print("Testing Coupang Partners Module...")
    status = get_account_status()
    print("Status:", json.dumps(status, indent=2, ensure_ascii=False))
    
    test_q = "쌀 4kg"
    link = get_deeplink_for_query(test_q)
    print(f"Affiliate link for '{test_q}': {link}")
