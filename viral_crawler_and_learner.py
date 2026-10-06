"""
🧠 [스레드 타 카테고리 구조 치환 자가진화 엔진] viral_crawler_and_learner.py
대표님의 핵심 원칙 (Cross-Category Structure Transfer):
1. 내 카테고리(과일)가 아닌 '완전히 다른 카테고리(꽃, 화장품/향수, 자기개발, 운동, 살림, 공방 등)' 탐색
2. 1만 뷰 이상 터진 글의 핵심 성공 요인인 '글의 구조(Hook ➔ 감정호소/반전 ➔ USP ➔ CTA)' 추출
3. 그 구조를 우리가 판매하는 영주 사과(온리애플)와 공주 정안알밤(꿀밤)으로 1:1 완벽 치환
4. 4~6줄 황금 비율, 모바일 화면 더보기 없는 즉각 완독형 고전환 글 매일 합성
"""

import os
import re
import json
import time
import random
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from viral_radar import parse_view_count

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(ENV_PATH)

SESSION_ID = os.getenv("ONLY_APPLES_SESSION_ID") or os.getenv("GGUL_BAMM_SESSION_ID")
USER_ID = os.getenv("ONLY_APPLES_USER_ID") or os.getenv("GGUL_BAMM_USER_ID")

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
VIRAL_DB_FILE = os.path.join(DATA_DIR, "viral_posts_db.json")
LEARNED_PATTERNS_FILE = os.path.join(DATA_DIR, "learned_patterns.json")

# 📌 타 카테고리(과일 외) 탐색 카테고리 & 키워드 풀
# 꽃, 화장품/향수, 자기개발, 공방/패션, 운동/헬스, 인테리어/살림 등에서
# 1만 뷰 이상 터진 글의 문장 구조(Hook -> 공감/결핍 -> USP -> CTA)를 수집하여 사과/밤으로 치환 학습
CATEGORIES = {
    "beauty_cosmetics": {
        "name": "화장품/뷰티/향수",
        "keywords": ["조향사", "향수", "스킨케어", "화장품", "피부과", "선크림", "앰플", "립스틱"]
    },
    "flower_plants": {
        "name": "꽃/플라워/식물",
        "keywords": ["플로리스트", "꽃집", "화훼", "식물집사", "생화", "꽃다발", "가드닝"]
    },
    "self_growth_career": {
        "name": "자기계발/커리어/공부",
        "keywords": ["자기계발", "이직", "공부법", "직장인", "퇴사", "독서", "루틴", "자격증"]
    },
    "craft_fashion": {
        "name": "공방/핸드메이드/패션",
        "keywords": ["공방", "가죽공예", "도자기", "주얼리", "목공", "핸드메이드", "디자이너"]
    },
    "fitness_health": {
        "name": "운동/피트니스/다이어트",
        "keywords": ["필라테스", "헬스", "PT", "다이어트", "바디프로필", "식단관리", "오운완"]
    },
    "living_interior": {
        "name": "살림/인테리어/리빙",
        "keywords": ["인테리어", "살림꿀팁", "자취템", "청소법", "주방꿀팁", "살림", "가구"]
    }
}

def clean_thread_text(raw_text: str) -> str:
    """스레드 UI 텍스트(시간, 좋아요, 버튼, 조회수 등) 및 OCR 아티팩트를 정밀 제거하고 순수 본문만 추출"""
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    filtered = []
    for l in lines:
        if re.match(r'^(<|〈|\^|v)?\s*(뒤로|스레드|활동|검색|알림|홈|프로필|팔로우|고정됨|Pinned|활동 보기)', l):
            continue
        if re.search(r'(\d+(\.\d+)?\s*(만|천|K|k)?\s*조회|\d+회\s*조회|조회\s*[\d,]+)', l):
            continue
        if re.match(r'^[a-zA-Z0-9._\-]{3,}\s+\d+\s*(시간|일|분|초|h|d|m)', l):
            continue
        if re.match(r'^\d+/\d+$', l):
            continue
        if re.match(r'^[_~^]?\s*[\d,]+\s*$', l):
            continue
        if re.match(r'^[A-Za-z]\s*\d+$', l):
            continue
        if any(w in l for w in ['좋아요', '답글', '공유', '리포스트', '팔로우']):
            if len(l) < 15:
                continue
        filtered.append(l)
    return "\n".join(filtered)

def extract_viral_dna(text: str, views: int, category: str, keyword: str) -> Optional[Dict]:
    """1만 뷰 외부 카테고리 게시물의 문장 구조 DNA를 정밀 분해"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) < 3:
        return None

    hook = "\n".join(lines[:2]) if len(lines) >= 4 else lines[0]
    cta = lines[-1]
    body = "\n".join(lines[2:-1]) if len(lines) >= 4 else lines[1]
    t_full = text.lower()

    # 1. 조향사/전문성 서러움 호소형 (perfumer_yun 1.9만뷰 구조: 소개/권위 -> 감정호소 -> USP -> 실수로라도 좋아요 CTA)
    if any(k in t_full for k in ["조향사", "년째", "서럽게도", "실수로라도", "모르시는 분이 많은데", "파는 조향사", "파는 사장"]):
        hook_type = "artisan_sympathy"
    # 2. 꽃집/가치 폄훼 반박형 (꽃은 금방 시드는데 -> 피로가 싹 가시는)
    elif any(k in t_full for k in ["시드는데", "돈 아깝다", "서운한 말", "꽃집", "플로리스트", "화병"]):
        hook_type = "flower_value_defense"
    # 3. 자기계발/이직 깨달음 역발상형 (N년/실패 끝에 깨달은 진실 -> 핵심은 한 문장)
    elif any(k in t_full for k in ["깨달은 진실", "실패하고", "이직", "자기계발", "면접", "스펙", "핵심은"]):
        hook_type = "career_truth_revelation"
    # 4. 헬스/다이어트 실패 원인 반전형 (살 안 빠지는 공통점 -> 가짜 식욕 -> 살 안 찌는 간식)
    elif any(k in t_full for k in ["살 안 빠지는", "트레이너", "헬스", "다이어터", "식욕", "살 안 찌는"]):
        hook_type = "fitness_trainer_hack"
    # 5. 살림/인테리어 삶의 질 수직상승형 (살림 N년차 모르는 사람 많아 -> 비싼 것 살 필요 없어 -> 삶의 질 수직상승)
    elif any(k in t_full for k in ["삶의 질", "살림", "수직 상승", "주부", "청소 세제", "과탄산소다"]):
        hook_type = "lifestyle_upgrade_tip"
    # 6. 공방/디자이너 마진 솔직 고백형 (로고 떼면 마진 -> 손바느질 -> 버티고 있습니다)
    elif any(k in t_full for k in ["공방", "솔직히 고백", "마진", "로고 떼면", "가죽", "도자기", "핸드메이드"]):
        hook_type = "craftsman_raw_truth"
    # 7. 취향 논쟁/밸런스형
    elif any(k in t_full for k in ["vs", "몇 번", "골라", "호불호", "대결", "최애", "1번", "2번", "당신의 선택"]):
        hook_type = "debate_polarizing"
    elif any(k in t_full for k in ["간절", "성공 꼭", "성공하고 싶", "주인 입니다", "애가 셋", "버티고"]):
        hook_type = "artisan_sympathy"
    else:
        hook_type = "artisan_sympathy"

    triggers = []
    trigger_dict = [
        "과즙", "꿀맛", "아삭", "달콤", "포슬포슬", "설탕", "산지직송",
        "무료배송", "평점", "백화점", "마진", "손편지", "10분", "20분"
    ]
    for trig in trigger_dict:
        if trig in text:
            triggers.append(trig)

    return {
        "views": views,
        "category": category,
        "keyword": keyword,
        "hook_type": hook_type,
        "line_count": len(lines),
        "char_count": len(text),
        "hook": hook,
        "body": body,
        "cta": cta,
        "triggers": triggers,
        "raw_text": text
    }

def synthesize_product_templates(dna_list: List[Dict]) -> Dict[str, List[str]]:
    """
    [타 카테고리 구조 치환 학습법 (Cross-Category Structure Transfer)]
    꽃, 화장품/향수, 자기개발, 헬스, 살림 등에서 1만~100만 뷰를 기록한 글의
    '문장 구조(권위/소개 -> 감정호소/반전 -> 감각 USP -> CTA)'를 그대로 흡수하여
    영주 풍기 사과(온리애플)와 공주 정안알밤(꿀밤)으로 1:1 완벽 치환 합성합니다.
    """
    apples_templates = []
    bamm_templates = []

    for dna in dna_list:
        ht = dna.get("hook_type", "artisan_sympathy")

        # 1. 🌟 [대표님 제시 조향사 1.9만뷰 구조 완벽 치환] 초단문 펀치라인
        if ht == "artisan_sympathy":
            apples_templates.append(
                "상위 0.1% 사과인데\n서럽게도... 아직 모르시는 분이 많은데ㅠㅠ\n한 입 물면 과즙 진짜 뚝뚝 흘러요,,,\n좋아요.. 부탁드려요..실수로라도 🍎"
            )
            apples_templates.append(
                "상위 0.1% 사과인데\n스레드에서 성공 진짜 하고 싶다 ....\n한 입 베어 물면 턱으로 과즙 뚝뚝 떨어져.\n지나가다 하트라도 툭 부탁해 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤.\n서럽게도... 아직 모르시는 분이 많은데ㅠㅠ\n저희 밤 정말로 포슬포슬하니 맛있어요,,,\n좋아요.. 부탁드려요..실수로라도 🌰"
            )
            bamm_templates.append(
                "20년 장인의 밤.\n스레드에서 성공 진짜 꼭 해보고 싶다 ....\n따끈하게 푹 찌면 껍질 쏙 벗겨지고 꿀맛이야.\n지나가다 하트라도 툭 부탁해 🌰❤️"
            )

        # 2. 🌸 [꽃집 1만뷰 구조 치환] 가치 폄훼 반박
        elif ht == "flower_value_defense":
            apples_templates.append(
                "상위 0.1% 사과인데\n두쫀쿠 7천원은 쿨하게 먹으면서 비싸대 ㅠㅠ\n한 입 물면 과즙 뚝뚝 피로가 싹 가시거든.\n사과 좋아하는 스친들 하트 하나만.. 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤.\n밤 까기 귀찮아서 과자 먹는다는 말 서운해 ㅠㅠ\n따끈하게 푹 찌면 포슬포슬 극락이거든.\n밤 좋아하는 스친들 하트 하나만.. 🌰"
            )

        # 3. 📚 [자기계발 3만뷰 구조 치환] 역발상 진실
        elif ht == "career_truth_revelation":
            apples_templates.append(
                "상위 0.1% 사과의 진실.\n빨갛다고 다 달콤한 사과가 아니래.\n소백산 일교차에서 꿀이 꽉 차야 찐이거든.\n맛있는 사과 찾는 스친들 하트 툭 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤. 그 진실.\n알만 크다고 다 맛있는 밤이 아니래.\n공주 정안에서 갓 딴 햇밤이어야 꿀맛이거든.\n달콤한 햇밤 찾는 스친들 하트 툭 🌰"
            )

        # 4. 🏋️ [헬스/다이어트 5만뷰 구조 치환] 꿀팁 해결
        elif ht == "fitness_trainer_hack":
            apples_templates.append(
                "상위 0.1% 사과 고르는 법!\n빨간 색깔만 보고 고르면 100% 실패해.\n엉덩이 노랗고 껍질 거친 게 찐 꿀사과야.\n사과 덕후들 까먹기 전에 하트 콕 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤 꿀팁!\n생밤 껍질 깔 때 손 다치지 마.\n뜨거운 물에 10분이면 껍질 슥슥 다 벗겨져.\n유용한 꿀팁이면 꿀밤이 하트 콕 🌰"
            )

        # 5. 🏡 [살림 10만뷰 구조 치환] 삶의 질 수직상승
        elif ht == "lifestyle_upgrade_tip":
            apples_templates.append(
                "상위 0.1% 사과인데\n비싼 백화점 선물세트 살 필요 전혀 없어.\n산지직송 영주 사과면 과즙 뚝뚝 꿀맛 보장이야.\n사과 좋아하는 사람 하트 꾹 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤.\n비싼 마트 밤 살 필요 전혀 없어.\n공주 정안 갓 수확한 햇알밤이라 꿀맛이야.\n알밤 좋아하는 스친들 하트 꾹 🌰"
            )

        # 6. 🧵 [공방 4만뷰 구조 치환] 솔직 고백
        elif ht == "craftsman_raw_truth":
            apples_templates.append(
                "상위 0.1% 사과인데 솔직히 고백할게.\n백화점 가면 유통 마진만 3배 붙어.\n소백산 산지직송 영주 사과가 진짜인데..\n사과 장사 응원 하트 부탁해 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤인데 솔직히 고백할게.\n길거리 군밤이나 마트는 마진만 3배야.\n공주 정안 갓 딴 특품 햇알밤이 진짜야.\n꿀밤이 응원 하트 부탁해 🌰"
            )

        # 7. ⚖️ [논쟁/선택형 7만뷰 구조 치환] 밸런스 게임
        elif ht == "debate_polarizing":
            apples_templates.append(
                "상위 0.1% 사과인데 딱 하나만 골라줘!\n1번) 껍질째 통째로 과즙 뚝뚝\n2번) 예쁘게 깎아서 달콤하게\n스친들 최애는? 댓글 달고 하트 콕 🍎"
            )
            bamm_templates.append(
                "20년 장인의 밤인데 딱 하나만 골라줘!\n1번) 따끈하게 푹 찐 달콤 포슬포슬 찐밤\n2번) 아작아작 달달한 생밤\n스친들 최애는? 댓글 달고 하트 콕 🌰"
            )

    # 중복 제거
    apples_unique = list(dict.fromkeys(apples_templates))
    bamm_unique = list(dict.fromkeys(bamm_templates))

    return {
        "only_apples0.1": apples_unique,
        "ggul_bamm": bamm_unique
    }

def bootstrap_from_reference_posts() -> List[Dict]:
    """
    기존 278개 고조회수 레퍼런스 DB(reference_posts.json) 중
    1만 뷰 이상 게시물을 전수 추출/분석하여 기초 DNA 풀을 구축합니다.
    """
    ref_file = os.path.join(DATA_DIR, "reference_posts.json")
    if not os.path.exists(ref_file):
        return []

    try:
        with open(ref_file, "r", encoding="utf-8") as f:
            refs = json.load(f)
    except Exception:
        return []

    bootstrapped_dna = []
    seen = set()

    for item in refs:
        raw_text = item.get("rawText", "")
        if not raw_text:
            continue
        views = parse_view_count(raw_text)
        if views < 10000:
            continue

        clean_text = clean_thread_text(raw_text)
        sig = clean_text[:30]
        if not sig or sig in seen:
            continue
        seen.add(sig)

        cat_key = "beauty_cosmetics"
        for ck, cinfo in CATEGORIES.items():
            if any(kw in clean_text for kw in cinfo["keywords"]):
                cat_key = ck
                break

        dna = extract_viral_dna(clean_text, views, cat_key, "reference")
        if dna:
            bootstrapped_dna.append(dna)

    return bootstrapped_dna

def run_daily_viral_learning(target_posts: int = 100, headless: bool = True) -> Dict:
    """
    매일 꽃, 화장품, 자기개발, 운동, 살림, 공방 등 타 카테고리를 순회하며
    1만 뷰 이상 게시물 100여 개를 수집하고, 그 문장 구조를 사과/밤 실전 템플릿으로 변환합니다.
    """
    print("=" * 65)
    print("🧠 [스레드 타 카테고리 구조 치환 자가진화 엔진 가동]")
    print(f"   시작 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   목표 수집: 1만 뷰 이상 {target_posts}개 (꽃, 화장품, 자기개발 등)")
    print("=" * 65)

    existing_db = []
    if os.path.exists(VIRAL_DB_FILE):
        try:
            with open(VIRAL_DB_FILE, "r", encoding="utf-8") as f:
                existing_db = json.load(f)
        except Exception:
            existing_db = []

    base_dna = bootstrap_from_reference_posts()
    print(f"📚 [기존 1만뷰 레퍼런스 DNA 로드]: {len(base_dna)}개 패턴 확보")

    seen_signatures = set(p.get("text", "")[:30] for p in existing_db if p.get("text"))
    collected_this_run = []
    dna_this_run = list(base_dna)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 850},
            locale="ko-KR",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        if SESSION_ID:
            cookie_val = urllib.parse.unquote(SESSION_ID)
            for domain in [".threads.com", ".threads.net", ".instagram.com"]:
                context.add_cookies([
                    {"name": "sessionid", "value": cookie_val, "domain": domain, "path": "/", "secure": True, "httpOnly": True},
                    {"name": "ds_user_id", "value": USER_ID or "", "domain": domain, "path": "/", "secure": True, "httpOnly": False}
                ])

        page = context.new_page()

        cat_items = list(CATEGORIES.items())
        random.shuffle(cat_items)

        for cat_key, cat_info in cat_items:
            if len(collected_this_run) >= target_posts:
                break

            keywords = cat_info["keywords"].copy()
            random.shuffle(keywords)
            selected_keywords = keywords[:3]

            print(f"\n📂 [{cat_info['name']}] 카테고리 구조 탐색 시작...")

            for kw in selected_keywords:
                if len(collected_this_run) >= target_posts:
                    break

                try:
                    search_url = f"https://www.threads.com/search?q={urllib.parse.quote(kw)}&serp_type=default"
                    page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
                    time.sleep(2.5)

                    for step in range(3):
                        page.mouse.wheel(0, 900)
                        time.sleep(1.2)

                        cards = page.locator("div[data-pressable-container='true'], article").all()
                        for card in cards:
                            try:
                                raw_text = card.inner_text().strip()
                                if not raw_text:
                                    continue

                                views = parse_view_count(raw_text)
                                if views >= 10000:
                                    clean_text = clean_thread_text(raw_text)
                                    sig = clean_text[:30]
                                    if sig and sig not in seen_signatures:
                                        seen_signatures.add(sig)

                                        post_item = {
                                            "category": cat_key,
                                            "category_name": cat_info["name"],
                                            "keyword": kw,
                                            "views": views,
                                            "text": clean_text,
                                            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        }
                                        collected_this_run.append(post_item)

                                        dna = extract_viral_dna(clean_text, views, cat_key, kw)
                                        if dna:
                                            dna_this_run.append(dna)

                                        print(f"   🎯 [1만뷰 발견!] {views:,}회 | [{cat_info['name']}] '{kw}': {clean_text.splitlines()[0][:25]}...")

                                        if len(collected_this_run) >= target_posts:
                                            break
                            except Exception:
                                continue

                        if len(collected_this_run) >= target_posts:
                            break

                except Exception as e:
                    print(f"   ⚠️ 키워드 '{kw}' 탐색 중 일시 오류: {e}")
                    continue

        browser.close()

    # 1. DB 저장
    all_posts = existing_db + collected_this_run
    all_posts = all_posts[-500:]
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VIRAL_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    # 2. 브랜드 맞춤형 템플릿 치환 합성
    synthesized = synthesize_product_templates(dna_this_run)

    # 3. 학습 패턴 저장
    learning_result = {
        "last_learned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_viral_in_db": len(all_posts),
        "newly_collected_today": len(collected_this_run),
        "dna_analyzed_count": len(dna_this_run),
        "synthesized_templates": synthesized,
        "dna_samples": dna_this_run[:20]
    }

    with open(LEARNED_PATTERNS_FILE, "w", encoding="utf-8") as f:
        json.dump(learning_result, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 65)
    print("✨ [타 카테고리 구조 치환 학습 완료 리포트]")
    print(f"   • 금일 신규 수집 1만 뷰 글: {len(collected_this_run)}개")
    print(f"   • 구조 DNA 분석 완료: {len(dna_this_run)}개")
    print(f"   • 온리애플 맞춤 템플릿 생성: {len(synthesized.get('only_apples0.1', []))}개")
    print(f"   • 꿀밤 맞춤 템플릿 생성: {len(synthesized.get('ggul_bamm', []))}개")
    print(f"   • 영구 보존 DB 총량: {len(all_posts)}개")
    print("=" * 65)

    return learning_result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Daily 100+ Cross-Category Viral Structure Learner")
    parser.add_argument("--count", type=int, default=15, help="수집할 1만뷰 게시물 목표 개수")
    parser.add_argument("--headless", action="store_true", default=True)
    parser.add_argument("--bootstrap-only", action="store_true", help="크롤링 없이 기존 1만뷰 레퍼런스 DNA 기반 즉시 합성")
    args = parser.parse_args()

    if args.bootstrap_only:
        print("⚡ [타 카테고리 구조 즉시 치환 합성 모드 실행]")
        base_dna = bootstrap_from_reference_posts()
        synthesized = synthesize_product_templates(base_dna)
        learning_result = {
            "last_learned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_viral_in_db": len(base_dna),
            "newly_collected_today": len(base_dna),
            "dna_analyzed_count": len(base_dna),
            "synthesized_templates": synthesized,
            "dna_samples": base_dna[:20]
        }
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(LEARNED_PATTERNS_FILE, "w", encoding="utf-8") as f:
            json.dump(learning_result, f, ensure_ascii=False, indent=2)
        print(f"✅ 타 카테고리 레퍼런스 {len(base_dna)}개 기반 구조 치환 완료!")
        print(f"   • 온리애플 치환 템플릿: {len(synthesized.get('only_apples0.1', []))}개")
        print(f"   • 꿀밤 치환 템플릿: {len(synthesized.get('ggul_bamm', []))}개")
    else:
        run_daily_viral_learning(target_posts=args.count, headless=args.headless)
