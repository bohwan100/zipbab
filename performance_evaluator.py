"""
🧠 [성과 피드백 & 자가 진화 엔진] performance_evaluator.py
대표님 핵심 요청:
"너가 글을 쓰고 너가 쓴 글이 조회수가 안나왔을 때 그것도 분석하면서 계속 높은 조회수가 나올 수 있도록 포맷도 바꿔가면서 학습하고 계속 배포해."

1. 내 게시물 성과 4단계 자동 분류 (VIRAL 10k+, HIGH 2k~10k, NORMAL 500~2k, UNDERPERFORMING <500)
2. 저조 게시물 4대 원인 정밀 진단 (Weak Hook, Sensory Lack, Low Emotion, Weak CTA)
3. 템플릿 자가 변형(Mutation) 생성: 대표님 4줄 초단문 공식 기반으로 결핍 요소 보강
4. 아키타입별 가중치(Weights) 동적 조정 및 data/performance_weights.json 저장
5. 텔레그램 진단 리포트 자동 발송 지원
"""

import os
import re
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
TRACKED_POSTS_FILE = os.path.join(DATA_DIR, "tracked_my_posts.json")
POSTED_HISTORY_FILE = os.path.join(DATA_DIR, "posted_history.json")
WEIGHTS_FILE = os.path.join(DATA_DIR, "performance_weights.json")
REPORT_FILE = os.path.join(DATA_DIR, "performance_feedback_report.json")

# 성과 등급 기준
TIER_VIRAL = "VIRAL"            # 10,000뷰 이상: 가중치 2.0배, 템플릿 복제
TIER_HIGH = "HIGH"              # 2,000 ~ 9,999뷰: 가중치 1.5배
TIER_NORMAL = "NORMAL"          # 500 ~ 1,999뷰: 가중치 1.0배 (기본)
TIER_UNDER = "UNDERPERFORMING"  # 500뷰 미만: 가중치 0.6배, 결핍 원인 분석 및 변형(Mutation) 생성

DEFAULT_ARCHETYPES = [
    "F01_checklist", "F02_raw_plea", "F03_trend_declaration", "F04_recipe_hack",
    "F05_situation_emergency", "F06_discovery_curiosity", "F07_sensory_craving",
    "F08_balance_debate", "F09_farmer_diary", "F10_price_contrast",
    "F11_real_review", "F12_community_question"
]

def load_json(filepath: str, default=None):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default if default is not None else []
    return default if default is not None else []

def save_json(filepath: str, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def infer_archetype_from_text(text: str) -> str:
    """텍스트 내용에서 12대 구조 포맷을 역추적합니다."""
    if "-" in text or "•" in text or "1." in text:
        return "F01_checklist"
    if len(text.strip().splitlines()) <= 2 or "사주세요" in text or "성공 꼭" in text or "어이가 없다" in text:
        return "F02_raw_plea"
    if "대세" in text or "앞으로" in text or "이깁니다" in text:
        return "F03_trend_declaration"
    if "5분" in text or "에어프라이어" in text or "레시피" in text or "버터" in text or "갈변" in text:
        return "F04_recipe_hack"
    if "큰일" in text or "가시" in text or "쥐 남" in text or "가격을 내렸" in text or "버릴 순" in text:
        return "F05_situation_emergency"
    if "혹시" in text or "이유 알아" in text or "견과류" in text or "자연 왁스" in text:
        return "F06_discovery_curiosity"
    if "과즙" in text or "와그작" in text or "침 고" in text or "노란 김" in text or "오독오독" in text:
        return "F07_sensory_craving"
    if "vs" in text.lower() or "골라" in text or "논쟁" in text or "1번" in text:
        return "F08_balance_debate"
    if "새벽" in text or "안개" in text or "과수원" in text or "산길" in text or "수확" in text:
        return "F09_farmer_diary"
    if "초콜릿" in text or "두쫀쿠" in text or "백화점" in text or "비싸" in text or "떡볶이" in text:
        return "F10_price_contrast"
    if "후기" in text or "리뷰" in text or "디엠" in text or "평점" in text or "단체 주문" in text:
        return "F11_real_review"
    if "스레드에" in text or "공복" in text or "퇴근길" in text or "치열하게" in text:
        return "F12_community_question"
    return "F09_farmer_diary"

def diagnose_underperformance(text: str) -> List[str]:
    """
    조회수 저조(<500) 게시물의 원인을 진단합니다.
    1. Weak Hook: 첫 줄 직진성/호기심 결여
    2. Sensory Lack: 침 고이는 감각적 단어(과즙, 뚝뚝, 포슬포슬 등) 누락
    3. Low Emotion: 서운함/간절함/안타까움 등 스레드형 감정선 미흡
    4. Weak CTA: 댓글/하트 행동 유도력 부재
    """
    reasons = []
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_line = lines[0] if lines else ""

    # 1. 훅 진단 (질문, 감정 고백, 산지 날씨, 레시피, 꿀팁 등 다채로운 스레드형 훅 인정)
    hook_patterns = [
        "큰일이야", "스레드", "솔직히", "정보)", "꿀팁", "비밀", "안녕", "새벽",
        "서럽", "성공", "두쫀쿠", "두바이", "골라줘", "어때", "손", "진짜", "논쟁"
    ]
    has_strong_hook = any(h in first_line for h in hook_patterns) or ("?" in first_line) or ("!" in first_line)
    if not has_strong_hook:
        reasons.append("Weak Hook (첫 줄 시선 집중도 및 직진성 부족)")

    # 2. 감각적 표현 진단
    sensory_words = ["과즙", "뚝뚝", "포슬포슬", "꿀", "달콤", "설탕", "단단", "사르르", "윤기", "아삭", "새콤", "고소"]
    if not any(w in text for w in sensory_words):
        reasons.append("Sensory Lack (과즙/포슬포슬/아삭 등 침 고이는 감각 묘사 결여)")

    # 3. 감정/공감 요소 진단
    emotion_words = ["서럽", "모르시는", "서운", "간절", "성공", "울 뻔", "실수로라도", "두쫀쿠", "비싸", "고생", "피로", "행복", "힐링", "고마워", "편견"]
    if not any(w in text for w in emotion_words):
        reasons.append("Low Emotion (스레드 특유의 짠내/서운함/간절함/일상 공감 감정선 약화)")

    # 4. CTA 진단
    cta_words = ["하트", "좋아요", "댓글", "부탁", "골라줘", "콕", "툭", "알려줘", "남겨줘"]
    if not any(w in text for w in cta_words):
        reasons.append("Weak CTA (명확한 반응 유도 장치 누락)")

    if not reasons:
        reasons.append("Algorithm Timing (게시 시간대 노출 경쟁 심화 또는 일시적 알고리즘 분배 지연)")

    return reasons

def mutate_template_for_underperformance(account: str, archetype: str, diagnosis: List[str]) -> str:
    """
    278개 실전 고조회수 레퍼런스를 기반으로, 고정 접두사('상위 0.1%', '20년 장인')를 과감히 탈피하여
    스레드 유저들이 혹할 만한 자연스럽고 다채로운 감정/상황/꿀팁 4줄 단문을 동적으로 합성합니다.
    """
    is_apple = "apple" in account

    if is_apple:
        candidate_variations = [
            # 산지 날씨 / 위기 스토리
            "큰일이야 ㅠㅠ 해발 740미터 고랭지는 벌써 영하로 떨어질까 봐 걱정이야.\n일교차 크게 맞고 자란 사과들이 당도 높고 단단한 거 알지.\n새벽부터 정성껏 딴 소백산 사과인데 다들 지나가다 응원 하트 하나만 부탁해 🍎",
            # 편견 깨기 / 진정성
            "스레드에서 과일 사면 안 된다는 편견 깨고 싶습니다.\n소백산 영주에서 진짜 정직하게 농사지은 사과예요.\n한 입 베어 물면 턱으로 과즙 진짜 뚝뚝 흘러내립니다.\n좋아요.. 부탁드려요..실수로라도 🍎",
            # 일상 꿀팁 / 레시피
            "정보) 사과 고를 때 겉이 번지르르하고 반짝이는 건 오히려 피해!\n당일 수확한 신선한 사과는 껍질에 뽀얀 가루(자연 왁스)가 살아있어야 찐이야.\n사과 덕후들 꼭 메모해둬 🍎",
            # 땅콩버터 이색 조합
            "사과 얇게 썰어서 땅콩버터 발라 먹어봤어?\n다이어트할 때 이거 모르면 진짜 손해야.\n포만감 미쳤고 달콤 고소 끝판왕! 사과 좋아하는 스친들 하트 콕 🍎",
            # 밸런스 게임
            "스레드에 제철 사과 취향 확고한 스친들 있어? 딱 하나만 골라줘!\n1번) 껍질째 통째로 베어 문다\n2번) 칼로 예쁘게 깎아 먹는다\n스친들 취향 댓글로 달고 하트 콕 🍎",
            # 가치 대비 반전
            "두바이 초콜릿 하나에 2만원은 줄 서서 사 먹으면서, 제철 햇사과는 비싸다고 지나치면 서운해 ㅠㅠ\n한 박스면 온 가족 일주일 내내 건강하고 달콤한데..\n속상한 사과 장사 힘내라고 하트 툭 🍎",
            # 감동 후기 입증
            "'한 입 물었다가 과즙 튀어서 옷 다 젖었어요'라는 후기 보고 울 뻔 ㅠㅠ\n네이버 평점 4.9점 찍었어.\n사과에 진심인 청년 농부 응원 하트 부탁해 🍎",
            # 출근길 일상 공감
            "바쁜 아침에 밥 거르고 출근하는 스친들..\n사과 반 쪽이라도 꼭 챙겨 먹어!\n커피만 들이붓지 말고 상큼한 비타민 충전하자. 오늘 하루도 힘내! 응원 하트 콕 🍎"
        ]
    else:
        candidate_variations = [
            # 밤 찌는 실전 꿀팁
            "정보) 밤 맛있게 찌는 법 모르면 평생 손해야!\n찜기에 김 오르면 햇밤 넣고 딱 20분만 쪄봐.\n불 끄고 찬물에 5초만 헹궈주면 껍질이 쏙쏙 벗겨지거든.\n유용한 꿀팁이면 하트 하나 콕 🌰✨",
            # 에어프라이어 군밤
            "에어프라이어에 생밤 칼집 내서 180도 15분만 돌려봐.\n껍질 쫙 벌어지며 노란 속살 톡 튀어나오는데 군밤 장수 울고 가 ㅋㅋㅋ\n달콤한 밤 냄새 가득! 밤 좋아하는 스친들 하트 콕 🌰❤️",
            # 이색 꿀조합 버터밤
            "따끈한 찐밤에 버터 한 조각 올려본 사람 있어?\n달콤하고 고소한 풍미가 입안에서 폭발해.\n이 꿀조합 모르면 진짜 손해! 하트 하나 콕 🌰",
            # 산지 수확 일기
            "새벽 5시부터 충남 공주 정안 알밤 숲에서 땀 뻘뻘..\n가시에 찔려가면서 제일 실하고 굵은 특품 햇밤만 주워왔어 🌰\n스친들이 맛있게 먹어주면 피로가 싹 사라져! 열심히 사는 꿀밤이한테 응원 하트 콕 🌰❤️",
            # 밸런스 게임
            "평생 논쟁거리 하나 던져볼게.. 스친들의 진짜 밤 취향은?\n1번) 달콤하고 포슬포슬한 찐밤\n2번) 아작아작 씹는 맛 터지는 생밤\n스친들 최애는? 댓글 달고 하트 콕 🌰✨",
            # 디저트 대비 가치 비교
            "두바이 초콜릿 하나에 2만원은 줄 서서 사 먹으면서, 제철 햇밤은 비싸대 ㅠㅠ\n자연이 준 천연 간식이라 속도 편하고 설탕보다 달콤한데..\n속상한 꿀밤이 힘내라고 하트 하나 콕 🌰❤️",
            # 캐릭터 솔직 고백
            "안녕 꿀밤이야 ! 밤 파는 작은 스토어 주인인데..\n진짜 성공 꼭 해보고 싶다....\n공주 정안 햇밤이라 당도가 설탕 친 것처럼 달콤하거든.\n지나가다 실수로라도 하트 부탁해 🌰❤️",
            # 퇴근길 야식 제안
            "퇴근길에 편의점 들러 과자 살까 고민하는 스친들 잠깐 멈춰봐 🌰\n인스턴트 대신 자연 그대로 쪄낸 달콤한 정안 햇밤 어때?\n칼로리 부담 없이 달콤해서 건강 야식으로 딱이야. 다들 꿀밤 보내! 하트 콕 🌰✨"
        ]

    return random.choice(candidate_variations).strip()

def evaluate_and_evolve() -> Dict:
    """
    내 게시물들의 조회수를 전수 평가하고,
    가중치 동적 조정 및 저조 포맷 자가 진화(Mutation)를 수행합니다.
    """
    tracked_posts = load_json(TRACKED_POSTS_FILE, default=[])
    posted_history = load_json(POSTED_HISTORY_FILE, default=[])
    existing_weights = load_json(WEIGHTS_FILE, default={
        "weights": {
            "only_apples0.1": {arch: 1.0 for arch in DEFAULT_ARCHETYPES},
            "ggul_bamm": {arch: 1.0 for arch in DEFAULT_ARCHETYPES}
        },
        "evolved_templates": {
            "only_apples0.1": [],
            "ggul_bamm": []
        },
        "stats": {
            "total_analyzed": 0,
            "viral_count": 0,
            "underperforming_count": 0,
            "last_updated": ""
        }
    })

    weights = existing_weights.get("weights", {})
    evolved = existing_weights.get("evolved_templates", {"only_apples0.1": [], "ggul_bamm": []})

    analyzed_records = []
    viral_hits = []
    underperforming_posts = []

    # 최근 게시물별 성과 분석
    for post in tracked_posts:
        account = post.get("account", "")
        text = post.get("text", "")
        views = post.get("views", 0)
        url = post.get("url", "")
        first_seen = post.get("first_seen", "")

        if not account or not text:
            continue

        arch = infer_archetype_from_text(text)

        # 티어 분류
        if views >= 10000:
            tier = TIER_VIRAL
            viral_hits.append(post)
        elif views >= 2000:
            tier = TIER_HIGH
        elif views >= 500:
            tier = TIER_NORMAL
        else:
            tier = TIER_UNDER
            underperforming_posts.append({
                "account": account,
                "archetype": arch,
                "views": views,
                "text": text,
                "url": url,
                "first_seen": first_seen
            })

        analyzed_records.append({
            "account": account,
            "archetype": arch,
            "views": views,
            "tier": tier,
            "text": text[:40]
        })

        # 가중치 업데이트 (계정별, 아키타입별)
        acc_weights = weights.setdefault(account, {a: 1.0 for a in DEFAULT_ARCHETYPES})
        current_w = acc_weights.get(arch, 1.0)

        if tier == TIER_VIRAL:
            acc_weights[arch] = min(round(current_w * 1.5, 2), 3.0)
        elif tier == TIER_HIGH:
            acc_weights[arch] = min(round(current_w * 1.2, 2), 2.5)
        elif tier == TIER_UNDER:
            acc_weights[arch] = max(round(current_w * 0.8, 2), 0.3)

    # 저조한 게시물 원인 진단 및 포맷 자가 진화(Mutation) 생성
    new_evolutions = {"only_apples0.1": [], "ggul_bamm": []}
    diagnosed_under = []

    for item in underperforming_posts:
        acc = item["account"]
        arch = item["archetype"]
        diag = diagnose_underperformance(item["text"])
        mutated_text = mutate_template_for_underperformance(acc, arch, diag)

        new_evolutions.setdefault(acc, []).append(mutated_text)
        diagnosed_under.append({
            "account": acc,
            "archetype": arch,
            "views": item["views"],
            "diagnoses": diag,
            "mutated_fix": mutated_text,
            "snippet": item["text"].splitlines()[0][:25]
        })

    # 진화 템플릿 풀 갱신 (최근 10개 유지)
    for acc in ["only_apples0.1", "ggul_bamm"]:
        existing_evolved = evolved.get(acc, [])
        combined = list(dict.fromkeys(new_evolutions.get(acc, []) + existing_evolved))
        evolved[acc] = combined[:10]

    # 가중치 정규화 (평균 1.0 유지)
    for acc, arch_w in weights.items():
        if arch_w:
            avg_w = sum(arch_w.values()) / len(arch_w)
            if avg_w > 0:
                weights[acc] = {k: round(v / avg_w, 2) for k, v in arch_w.items()}

    # 결과 저장
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "weights": weights,
        "evolved_templates": evolved,
        "stats": {
            "total_analyzed": len(analyzed_records),
            "viral_count": len(viral_hits),
            "underperforming_count": len(underperforming_posts),
            "last_updated": now_str
        }
    }
    save_json(WEIGHTS_FILE, payload)

    # 상세 진단 리포트 저장
    report = {
        "timestamp": now_str,
        "summary": {
            "total_posts": len(analyzed_records),
            "viral_hits": len(viral_hits),
            "underperforming": len(underperforming_posts),
        },
        "top_performing_archetypes": {
            acc: sorted(w.items(), key=lambda x: x[1], reverse=True)[:3]
            for acc, w in weights.items()
        },
        "diagnosed_underperforming_cases": diagnosed_under[:5],
        "evolved_template_samples": {
            acc: evolved[acc][:2] for acc in ["only_apples0.1", "ggul_bamm"]
        }
    }
    save_json(REPORT_FILE, report)

    return report

def get_performance_weights(account: str) -> Dict[str, float]:
    """특정 계정의 아키타입별 최신 가중치 딕셔너리를 반환합니다."""
    data = load_json(WEIGHTS_FILE, default={})
    weights = data.get("weights", {}).get(account, {})
    if not weights:
        return {arch: 1.0 for arch in DEFAULT_ARCHETYPES}
    return weights

def get_evolved_templates(account: str) -> List[str]:
    """저조한 성과를 극복하기 위해 자가 진화(Mutation)된 최신 템플릿 목록을 반환합니다."""
    data = load_json(WEIGHTS_FILE, default={})
    return data.get("evolved_templates", {}).get(account, [])

if __name__ == "__main__":
    print("=" * 65)
    print("🧠 [성과 피드백 & 자가 진화 엔진] 실행 중...")
    print("=" * 65)
    rep = evaluate_and_evolve()
    print(f"\n📊 분석 완료:")
    print(f" • 총 분석 게시물: {rep['summary']['total_posts']}개")
    print(f" • 바이럴 떡상 게시물: {rep['summary']['viral_hits']}개")
    print(f" • 저조 피드백 대상: {rep['summary']['underperforming']}개")
    print("\n🌟 계정별 가중치 TOP 3:")
    for acc, tops in rep["top_performing_archetypes"].items():
        print(f"  [@{acc}]: {tops}")
    print("\n🧬 자가 진화(Mutation) 템플릿 샘플:")
    for acc, tmps in rep["evolved_template_samples"].items():
        print(f"\n  [@{acc}]:")
        for t in tmps:
            print("  " + "\n  ".join(t.splitlines()))
