import os
import requests
import json
from pathlib import Path

env_path = Path(".env")
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'").strip('"')

headers = {
    "Authorization": f"Bearer {os.environ.get('NOTION_API_KEY')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

toggle_id = "3ff58961-82de-8078-9857-efb1b8413784"

# 1. Update toggle title to match existing emoji style
title_payload = {
    "toggle": {
        "rich_text": [
            {
                "type": "text",
                "text": {"content": "24. 🍜지도리우동🍜"}
            }
        ]
    }
}
r_title = requests.patch(f"https://api.notion.com/v1/blocks/{toggle_id}", headers=headers, json=title_payload)
print("Title update status:", r_title.status_code)

# 2. Get existing child blocks and delete empty placeholder blocks
r_children = requests.get(f"https://api.notion.com/v1/blocks/{toggle_id}/children", headers=headers)
existing_children = r_children.json().get("results", [])
print(f"기존 자식 블록 {len(existing_children)}개 삭제 진행...")
for b in existing_children:
    bid = b.get("id")
    requests.delete(f"https://api.notion.com/v1/blocks/{bid}", headers=headers)

# 3. Create full structured blocks
new_children = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": []}
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "<관련 영상>"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": []}
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "[주재료]"}}]
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {"type": "text", "text": {"content": "우동면 1개 (200g) "}},
                {
                    "type": "text",
                    "text": {
                        "content": "https://link.coupang.com/a/h0jpCimcX6",
                        "link": {"url": "https://link.coupang.com/a/h0jpCimcX6"}
                    }
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {"type": "text", "text": {"content": "닭다리살 150g "}},
                {
                    "type": "text",
                    "text": {
                        "content": "https://link.coupang.com/a/h0jpDchbAO",
                        "link": {"url": "https://link.coupang.com/a/h0jpDchbAO"}
                    }
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "[부재료 및 양념]"}}]
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {"type": "text", "text": {"content": "대파 80g (55g + 25g) "}},
                {
                    "type": "text",
                    "text": {
                        "content": "https://link.coupang.com/a/hLBW0skzSK",
                        "link": {"url": "https://link.coupang.com/a/hLBW0skzSK"}
                    }
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "물 400ml"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {"type": "text", "text": {"content": "혼쯔유 40ml "}},
                {
                    "type": "text",
                    "text": {
                        "content": "https://link.coupang.com/a/h0jpEx2xoa",
                        "link": {"url": "https://link.coupang.com/a/h0jpEx2xoa"}
                    }
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {"type": "text", "text": {"content": "소금 약간 (닭 밑간용) "}},
                {
                    "type": "text",
                    "text": {
                        "content": "https://link.coupang.com/a/hLB7lAWERE",
                        "link": {"url": "https://link.coupang.com/a/hLB7lAWERE"}
                    }
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {"type": "text", "text": {"content": "후추 약간 (닭 밑간용) "}},
                {
                    "type": "text",
                    "text": {
                        "content": "https://link.coupang.com/a/hLAEQE0U0W",
                        "link": {"url": "https://link.coupang.com/a/hLAEQE0U0W"}
                    }
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "만드는 방법"}}]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "닭다리살(150g)은 한입 크기로 썰고 소금과 후추를 살짝 뿌려 밑간해둡니다."}}]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "대파 80g 중 55g은 3~4cm 길이로 큼직하게 썰고, 남은 25g은 송송 썰어 고명용으로 준비합니다."}}]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "달군 팬이나 냄비에 기름 없이 닭다리살(껍질 쪽부터)과 큼직하게 썬 대파(55g)를 넣고, 겉면이 노릇노릇 그을리듯 구워 닭기름과 불맛을 냅니다."}}]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "닭고기와 대파가 노릇하게 익으면 물 400ml와 혼쯔유 40ml를 붓고 센 불에서 끓입니다."}}]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "국물이 끓어오르면 우동면(200g)을 넣고 2~3분간 면을 살살 풀어가며 끓여줍니다."}}]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "그릇에 면과 진한 국물, 구운 닭고기·대파를 담고 송송 썬 대파(25g)를 고명으로 올려 마무리합니다."}}]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "팁 (Tip)"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "닭다리살 껍질과 대파를 팬에 노릇하고 살짝 거뭇하게 구워야 국물에 진한 불향(지도리 풍미)과 감칠맛이 폭발합니다."}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "취향에 따라 시치미(七味)나 고춧가루를 톡톡 뿌려 드시면 국물이 한층 더 개운하고 칼칼해집니다."}}]
        }
    }
]

# Append new children
r_append = requests.patch(
    f"https://api.notion.com/v1/blocks/{toggle_id}/children",
    headers=headers,
    json={"children": new_children}
)
print("Append status:", r_append.status_code)
if r_append.status_code == 200:
    print("성공적으로 24번 지도리우동 레시피를 노션에 정리했습니다!")
else:
    print("Error:", r_append.text)
