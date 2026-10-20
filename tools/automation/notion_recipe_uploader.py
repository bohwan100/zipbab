import os
import sys
import json
import urllib.parse
import requests
from pathlib import Path

# Coupang Partners helper
import coupang_partners

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

def load_env():
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("'").strip('"')

load_env()

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_PAGE_ID = os.environ.get("NOTION_PAGE_ID", "").replace("-", "")
NOTION_VERSION = "2022-06-28"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}


def test_connection():
    """Checks if Notion API token is valid and target page is accessible."""
    if not NOTION_API_KEY:
        return False, "NOTION_API_KEY가 .env에 설정되지 않았습니다."
    
    # 1. Check user/bot info
    me_resp = requests.get("https://api.notion.com/v1/users/me", headers=NOTION_HEADERS)
    if me_resp.status_code != 200:
        return False, f"Notion API 인증 실패 ({me_resp.status_code}): {me_resp.text}"
    bot_name = me_resp.json().get("name", "Notion Bot")

    # 2. Check access to NOTION_PAGE_ID
    url = f"https://api.notion.com/v1/pages/{NOTION_PAGE_ID}"
    resp = requests.get(url, headers=NOTION_HEADERS)
    if resp.status_code == 200:
        page_title = "Untitled"
        props = resp.json().get("properties", {})
        title_prop = props.get("title", {}).get("title", [])
        if title_prop:
            page_title = title_prop[0].get("plain_text", page_title)
        return True, f"'{bot_name}' 봇으로 '{page_title}' 페이지에 정상 연결되었습니다."
    elif resp.status_code == 404:
        # Check if it's a database
        db_url = f"https://api.notion.com/v1/databases/{NOTION_PAGE_ID}"
        db_resp = requests.get(db_url, headers=NOTION_HEADERS)
        if db_resp.status_code == 200:
            db_title = "Database"
            title_list = db_resp.json().get("title", [])
            if title_list:
                db_title = title_list[0].get("plain_text", db_title)
            return True, f"'{bot_name}' 봇으로 '{db_title}' 데이터베이스에 정상 연결되었습니다."
        return False, f"페이지 ID({NOTION_PAGE_ID})를 찾을 수 없습니다. 노션 페이지 우측 상단 [···] -> [연결(Connections)]에서 '{bot_name}'을 추가했는지 확인해 주세요."
    else:
        return False, f"오류 발생 ({resp.status_code}): {resp.text}"


def create_recipe_page(recipe_data: dict) -> dict:
    """
    Takes a structured recipe dict, attaches Coupang Partners links to ingredients,
    and creates a new Notion child page.
    """
    title = recipe_data.get("title", "맛있는 요리 레시피")
    desc = recipe_data.get("description", "사진에서 추출된 레시피입니다.")
    servings = recipe_data.get("servings", "")
    cooking_time = recipe_data.get("cooking_time", "")
    ingredients = recipe_data.get("ingredients", [])
    seasonings = recipe_data.get("seasonings", [])
    steps = recipe_data.get("steps", [])
    tips = recipe_data.get("tips", [])

    print(f"[Notion Recipe] '{title}' 레시피 등록 시작...")

    # Blocks to append into Notion page
    children_blocks = []

    # 1. Summary Callout
    meta_info = []
    if servings:
        meta_info.append(f"👥 {servings}")
    if cooking_time:
        meta_info.append(f"⏱️ {cooking_time}")
    meta_str = f" ({' | '.join(meta_info)})" if meta_info else ""

    children_blocks.append({
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{
                "type": "text",
                "text": {"content": f"{desc}{meta_str}"}
            }],
            "icon": {"emoji": "💡"},
            "color": "orange_background"
        }
    })

    children_blocks.append({"object": "block", "type": "divider", "divider": {}})

    # 2. Ingredients Section with Coupang Partners Links
    children_blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🛒 필수 재료 & 쿠팡 최저가 구매"}}]
        }
    })

    print(f"[Notion Recipe] 재료 {len(ingredients)}개 쿠팡 파트너스 단품 직링크 매칭 중...")
    for item in ingredients:
        name = item.get("name", "")
        amount = item.get("amount", "")
        search_query = item.get("query", f"{name} {amount}".strip())

        # Generate Coupang Partners direct product link (only if valid earning single-product short link exists)
        coupang_url = item.get("url", "")
        if not coupang_url:
            coupang_url, _ = coupang_partners.get_direct_product_deeplink(search_query, allow_search_fallback=False)

        text_content = f"{name} {amount}".strip()
        if coupang_url and "link.coupang.com/a/" in coupang_url:
            rich_text = [
                {"type": "text", "text": {"content": f"{text_content}  —  "}},
                {
                    "type": "text",
                    "text": {
                        "content": "쿠팡에서 구매하기 🔗",
                        "link": {"url": coupang_url}
                    },
                    "annotations": {"bold": True, "color": "blue"}
                }
            ]
        else:
            rich_text = [{"type": "text", "text": {"content": text_content}}]

        children_blocks.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": rich_text,
                "checked": False
            }
        })

    # 3. Seasonings Section (if exists)
    if seasonings:
        children_blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "🧂 양념 및 소스"}}]
            }
        })
        for item in seasonings:
            name = item.get("name", "")
            amount = item.get("amount", "")
            search_query = item.get("query", f"{name} {amount}".strip())
            
            coupang_url = item.get("url", "")
            if not coupang_url:
                coupang_url, _ = coupang_partners.get_direct_product_deeplink(search_query, allow_search_fallback=False)

            text_content = f"{name} {amount}".strip()
            if coupang_url and "link.coupang.com/a/" in coupang_url:
                rich_text = [
                    {"type": "text", "text": {"content": f"{text_content}  —  "}},
                    {
                        "type": "text",
                        "text": {
                            "content": "구매 🔗",
                            "link": {"url": coupang_url}
                        },
                        "annotations": {"color": "blue"}
                    }
                ]
            else:
                rich_text = [{"type": "text", "text": {"content": text_content}}]

            children_blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": rich_text,
                    "checked": False
                }
            })

    children_blocks.append({"object": "block", "type": "divider", "divider": {}})

    # 4. Cooking Steps
    children_blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "👩‍🍳 조리 순서"}}]
        }
    })

    for step_text in steps:
        children_blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": step_text}}]
            }
        })

    # 5. Tips
    if tips:
        children_blocks.append({"object": "block", "type": "divider", "divider": {}})
        children_blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "✨ 쉐프의 꿀팁"}}]
            }
        })
        for tip in tips:
            children_blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": tip}}]
                }
            })

    # 6. Legal Coupang Disclaimer
    children_blocks.append({"object": "block", "type": "divider", "divider": {}})
    children_blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "📢 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
                },
                "annotations": {"italic": True, "color": "gray"}
            }]
        }
    })

    # Notion Page Payload
    payload = {
        "parent": {"page_id": NOTION_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🍳"},
        "properties": {
            "title": [
                {
                    "type": "text",
                    "text": {"content": title}
                }
            ]
        },
        "children": children_blocks
    }

    resp = requests.post("https://api.notion.com/v1/pages", headers=NOTION_HEADERS, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        page_url = data.get("url", "")
        print(f"[Notion Recipe] 성공! 등록된 페이지: {page_url}")
        return {"success": True, "url": page_url, "id": data.get("id")}
    else:
        print(f"[Notion Recipe] 등록 실패 ({resp.status_code}): {resp.text}")
        return {"success": False, "error": resp.text, "status_code": resp.status_code}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        ok, msg = test_connection()
        print(f"[{'OK' if ok else 'FAIL'}] {msg}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        recipe_data = json.loads(sys.argv[2])
        res = create_recipe_page(recipe_data)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--file":
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            recipe_data = json.load(f)
        res = create_recipe_page(recipe_data)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--sample":
        sample_recipe = {
            "title": "초간단 묵은지 돼지고기 김치찌개",
            "description": "묵은지와 쫄깃한 돼지고기로 국물 맛이 깊고 진한 한국인의 소울푸드 김치찌개",
            "servings": "2~3인분",
            "cooking_time": "25분",
            "ingredients": [
                {"name": "신김치", "amount": "1/4포기 (300g)", "query": "신김치 포기김치"},
                {"name": "찌개용 돼지 앞다리살", "amount": "200g", "query": "찌개용 돼지고기 앞다리살"},
                {"name": "두부", "amount": "반모 (150g)", "query": "찌개용 두부"},
                {"name": "대파", "amount": "1대", "query": "대파 1단"},
                {"name": "청양고추", "amount": "1개", "query": "청양고추"}
            ],
            "seasonings": [
                {"name": "고춧가루", "amount": "1.5 큰술", "query": "고춧가루"},
                {"name": "다진 마늘", "amount": "1 큰술", "query": "국산 다진마늘"},
                {"name": "국간장", "amount": "1 큰술", "query": "국간장"},
                {"name": "들기름", "amount": "1 큰술", "query": "들기름"}
            ],
            "steps": [
                "냄비에 들기름 1큰술을 두르고 찌개용 돼지고기를 넣어 겉면이 하얗게 변할 때까지 볶아줍니다.",
                "먹기 좋게 썬 신김치를 넣고 함께 달달 볶아 김치가 나른해질 때까지 3분 정도 볶습니다.",
                "물 또는 멸치 다시마 육수 600ml를 붓고 고춧가루, 다진 마늘, 국간장을 넣고 센 불로 끓입니다.",
                "국물이 끓어오르면 중약불로 줄이고 10분간 푹 끓여 깊은 맛을 냅니다.",
                "두부와 숭숭 썬 대파, 청양고추를 넣고 3분간 더 끓여 마무리합니다."
            ],
            "tips": [
                "신김치가 너무 시다면 설탕 1/2 작은술을 넣어 산미를 잡아주세요.",
                "돼지고기 기름과 김치가 들기름에 충분히 볶아져야 국물에 진한 풍미가 우러납니다."
            ]
        }
        res = create_recipe_page(sample_recipe)
        print(json.dumps(res, ensure_ascii=False, indent=2))
