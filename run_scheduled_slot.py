"""
🚀 [GitHub Actions / 클라우드 전용 실행기] run_scheduled_slot.py
대표님의 핵심 원칙: "시간이 지연되더라도 하루 10개는 꼭 올려줘"
1. 하루 10개 완주 보장 엔진 (Daily Quota: 계정당 10개/일)
2. 계정별 15분 최소 쿨다운 준수 (동일 계정 연속 업로드 방지)
3. 두 계정(온리애플, 꿀밤) 간 1~2분 자연스러운 시차 업로드
4. 매일 다른 분(min)에 올라가도록 20~90초 랜덤 Jitter 적용
5. 심야/새벽(23:00 ~ 07:15 KST) 발행 100% 원천 차단
"""
import os
import sys
import json
import argparse
import time
import random
from datetime import datetime, timezone, timedelta
from content_engine import ContentEngine
from threads_multi_poster import post_to_threads_multi
from view_milestone_monitor import check_and_alert_milestones

# ⏰ 한국 표준시 (KST = UTC + 9)
KST = timezone(timedelta(hours=9))

DAILY_TARGET_POSTS = 10  # 계정당 하루 목표 업로드 개수

# 📌 대표님이 지정해주신 10대 핵심 업로드 슬롯
# (출근 2회, 점심 2회, 늦은오후/퇴근 3회, 저녁/밤 3회)
BASE_TIME_SLOTS = [
    (7, 30),   # 1. 아침 출근길 1
    (8, 0),    # 2. 아침 출근길 2
    (12, 0),   # 3. 점심 시간 1
    (12, 20),  # 4. 점심 시간 2
    (17, 0),   # 5. 늦은 오후 1
    (17, 30),  # 6. 늦은 오후 2
    (18, 0),   # 7. 퇴근/저녁 시간
    (20, 0),   # 8. 저녁 휴식 시간 1
    (21, 0),   # 9. 저녁 휴식 시간 2
    (22, 0),   # 10. 취침 전 밤 시간
]

def get_target_quota_by_now(now_kst: datetime) -> tuple[int, str]:
    """
    현재 시각(KST)까지 도래한 기준 슬롯의 누적 개수와 다음 예정 슬롯 안내를 반환합니다.
    (±5분 자연 오차를 감안하여 슬롯 5분 전부터 해당 슬롯 도래로 인정)
    """
    now_minutes = now_kst.hour * 60 + now_kst.minute
    due_count = 0
    next_slot_str = "내일 07:30"

    for h, m in BASE_TIME_SLOTS:
        slot_minutes = h * 60 + m - 5  # 5분 전부터 진입 허용
        if now_minutes >= slot_minutes:
            due_count += 1
        else:
            if next_slot_str == "내일 07:30":
                next_slot_str = f"오늘 {h:02d}:{m:02d}"

    return min(due_count, DAILY_TARGET_POSTS), next_slot_str

def get_today_post_count(account: str) -> int:
    """오늘(KST 날짜 기준) 해당 계정으로 실제 발행 완료된 게시물 개수 반환"""
    history_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "posted_history.json"))
    if not os.path.exists(history_file):
        return 0
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        today_str = datetime.now(KST).strftime("%Y-%m-%d")
        count = 0
        for p in history:
            if p.get("account") == account:
                try:
                    dt_utc = datetime.strptime(p["created_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    dt_kst = dt_utc.astimezone(KST)
                    if dt_kst.strftime("%Y-%m-%d") == today_str:
                        count += 1
                except Exception:
                    pass
        return count
    except Exception:
        return 0

def is_already_posted_recently(account: str, threshold_minutes: int = 15) -> bool:
    """동일 계정 기준 최근 15분 이내 중복/연속 발행 방지"""
    history_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "posted_history.json"))
    if not os.path.exists(history_file):
        return False
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        acc_posts = [h for h in history if h.get("account") == account]
        if not acc_posts:
            return False
        last_post = acc_posts[-1]
        last_time_str = last_post.get("created_at")
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                dt_utc = datetime.strptime(last_time_str, fmt).replace(tzinfo=timezone.utc)
                diff = (datetime.now(timezone.utc) - dt_utc).total_seconds() / 60.0
                if diff < threshold_minutes:
                    return True
            except Exception:
                pass
    except Exception:
        pass
    return False

def get_minutes_since_last_post(account: str) -> float:
    """해당 계정의 직전 발행 이후 경과한 시간(분) 반환. 발행 기록 없으면 9999.0 반환"""
    history_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "posted_history.json"))
    if not os.path.exists(history_file):
        return 9999.0
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        acc_posts = [h for h in history if h.get("account") == account]
        if not acc_posts:
            return 9999.0
        last_post = acc_posts[-1]
        last_time_str = last_post.get("created_at")
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                dt_utc = datetime.strptime(last_time_str, fmt).replace(tzinfo=timezone.utc)
                diff = (datetime.now(timezone.utc) - dt_utc).total_seconds() / 60.0
                return max(0.0, diff)
            except Exception:
                pass
    except Exception:
        pass
    return 9999.0

def check_can_post_now(account: str, force: bool = False) -> tuple[bool, str, int]:
    """
    대표님의 핵심 지시:
    "시간대는 참고하되 네가 못올릴 것 같으면 그냥 시간 상관없이 하루에 10개만 채워주면 돼"

    1. 수동 강제 실행(--force) 시 즉시 승인
    2. 심야/새벽(23:00 ~ 07:15 KST) 취침 시간 절대 보호 (피드 도배/스팸 신고 방지)
    3. 오늘 목표 10개 완주 완료 시 당일 자동 대기
    4. 최소 15분 안전 쿨다운 준수 (동일 계정 연타 업로드 방지)
    5. 지능형 완주 보장 판정:
       a. [지연 슬롯 보정] 현재 시각 기준 도래한 슬롯보다 부족하면 즉시 발행
       b. [슬롯 부족 위기] 남은 정규 슬롯 수 < 남은 목표 개수이면 시간 불문 즉시 발행
       c. [동적 페이싱 분산] 마감(23:00)까지 남은 시간 / 남은 개수 기준 적정 간격(최소 25분~최대 75분) 이상 지났으면 즉시 발행
    """
    today_count = get_today_post_count(account)

    if force:
        return True, f"🚀 [수동 강제 실행] 시간/슬롯 제한 없이 즉시 발행 (현재 {today_count}개 완료)", today_count

    now_kst = datetime.now(KST)
    now_total_minutes = now_kst.hour * 60 + now_kst.minute

    # 1. 심야/새벽(23:00 ~ 07:15 KST) 절대 차단 (취침 시간 피드 오염 방지)
    if now_total_minutes > (23 * 60) or now_total_minutes < (7 * 60 + 15):
        return False, f"⛔ [심야/새벽 차단] 현재 한국 시각 {now_kst.strftime('%H:%M')} (23:00~07:15 취침 보호)", today_count

    # 2. 오늘 목표 10개 완주 여부 확인
    if today_count >= DAILY_TARGET_POSTS:
        return False, f"🎉 [{account}] 오늘 목표 10개 완주 완료! ({today_count}/{DAILY_TARGET_POSTS}개). 내일 07:30까지 대기합니다.", today_count

    # 3. 최소 15분 안전 쿨다운 확인 (동일 계정 초고속 연타 방지)
    mins_since_last = get_minutes_since_last_post(account)
    if mins_since_last < 15.0:
        remain_wait = int(15.0 - mins_since_last) + 1
        return False, f"⏳ [{account}] 직전 발행 후 {mins_since_last:.1f}분 경과 (안전 쿨다운 {remain_wait}분 대기 중, 현재 {today_count}/{DAILY_TARGET_POSTS}개)", today_count

    # 4. 남은 목표 및 남은 정규 슬롯 계산
    remaining_posts = DAILY_TARGET_POSTS - today_count
    future_slots = sum(1 for h, m in BASE_TIME_SLOTS if (h * 60 + m - 5) > now_total_minutes)
    due_target, next_slot = get_target_quota_by_now(now_kst)

    # 5. [대표님 핵심 원칙] 시간대는 참고하되, 10개 완주에 위험이 생기면 시간 상관없이 발행
    # (a) 이미 지나간 정규 슬롯이 밀려있는 경우
    if today_count < due_target:
        return True, f"⚡ [{account}] 지연 슬롯 자동 복구 발행 (목표 누적 {due_target}개 중 현재 {today_count}개 ➔ 이번이 {today_count+1}번째 업로드)", today_count

    # (b) 오늘 남은 정규 슬롯 개수만으로는 남은 목표(10개)를 채울 수 없는 경우 (슬롯 부족 비상)
    if future_slots < remaining_posts:
        return True, f"🚨 [{account}] 일일 10개 완주 비상 가동 (남은 정규 슬롯 {future_slots}개 < 남은 목표 {remaining_posts}개 ➔ 시간 불문 즉시 {today_count+1}번째 발행)", today_count

    # (c) 동적 페이싱: 23:00 마감까지 남은 시간을 고려하여 적정 간격이 경과한 경우
    minutes_left_today = max(0, (23 * 60) - now_total_minutes)
    ideal_interval = max(25.0, min(75.0, minutes_left_today / max(1, remaining_posts)))
    if mins_since_last >= ideal_interval:
        return True, f"🎯 [{account}] 동적 페이싱 자동 발행 (남은 {remaining_posts}개 완주 위해 {mins_since_last:.0f}분 만에 {today_count+1}번째 업로드)", today_count

    # 위 조건에 해당하지 않고 정상 페이스라면 다음 정규 슬롯까지 대기
    return False, f"⏳ [{account}] 현재 페이스 안정적 ({today_count}/{DAILY_TARGET_POSTS}개 완료, 남은 슬롯 {future_slots}개 충분). 다음 슬롯({next_slot}) 또는 약 {ideal_interval - mins_since_last:.0f}분 뒤 자동 발행됩니다.", today_count

def apply_random_jitter():
    """매일 똑같은 초/분에 올라가지 않도록 자연스러운 20~90초 랜덤 시차 적용"""
    jitter_sec = random.randint(20, 90)
    print(f"🎲 [스텔스 봇 방지] 자연스러운 분(min) 분산을 위해 {jitter_sec}초 대기...")
    time.sleep(jitter_sec)

def run_slot(target: str = "both", force: bool = False):
    now_kst = datetime.now(KST)
    print("=" * 65)
    print("⏰ [스레드 24/7 일일 10개 완주 보장 엔진]")
    print(f"   현재 시각 (KST): {now_kst.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    engine = ContentEngine()
    accounts = []
    if target == "both":
        accounts = ["only_apples0.1", "ggul_bamm"]
    elif target in ["only_apples0.1", "ggul_bamm"]:
        accounts = [target]
    else:
        print(f"⚠️ 알 수 없는 계정: {target}")
        sys.exit(1)

    posted_any = False

    for idx, account in enumerate(accounts):
        can_post, reason, current_count = check_can_post_now(account, force=force)
        print(f"\n{reason}")

        if not can_post:
            continue

        # 수동 강제가 아닌 정규 실행일 경우 매일 다른 초/분에 올리도록 20~90초 랜덤 시차 적용
        if not force and not posted_any:
            apply_random_jitter()

        next_count = current_count + 1
        progress_str = f"{next_count} / {DAILY_TARGET_POSTS}개 달성 중 🚀"

        print(f"\n==================================================")
        print(f"🚀 [{account}] 오늘 제 {next_count}번째 포스팅 시작 (KST {datetime.now(KST).strftime('%H:%M:%S')})")
        print(f"==================================================")
        post_data = engine.generate_post(account)
        
        success = post_to_threads_multi(
            account=account,
            text=post_data["text"],
            image_path=post_data["image_path"],
            comment=post_data.get("comment"),
            headless=True,
            enable_stealth=True,
            daily_progress=progress_str
        )
        
        if success:
            posted_any = True
            engine.record_post(account, post_data["text"], post_data["archetype"])
            print(f"✅ [{account}] 오늘 ({next_count}/{DAILY_TARGET_POSTS}개) 포스팅 성공 완료!")
        else:
            print(f"❌ [{account}] 포스팅 실패")
            
        # 두 계정 사이 1~2분 가벼운 시차 (계정이 다르므로 15분 대기 불필요!)
        if idx < len(accounts) - 1:
            inter_account_gap_sec = random.randint(60, 110) # 1분 ~ 1분 50초
            print(f"\n⏳ [계정 전환] 다음 계정({accounts[idx+1]}) 발행 전 자연스러운 {inter_account_gap_sec}초 시차 대기...")
            time.sleep(inter_account_gap_sec)

    # 1만 조회수 마일스톤 검사 및 성과 피드백 루프
    if posted_any:
        print("\n🔍 1만 조회수 돌파 마일스톤 스캔 중...")
        try:
            check_and_alert_milestones(headless=True)
        except Exception as e:
            print(f"⚠️ 조회수 감시 중 경고: {e}")
    else:
        print("\n🛡️ [안전 조치 완료] 이번 회차는 업로드 조건이 아니므로 피드백 가중치만 최신화합니다.")
        try:
            from performance_evaluator import evaluate_and_evolve
            evaluate_and_evolve()
        except Exception as e:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Actions Threads Poster")
    parser.add_argument("--account", choices=["only_apples0.1", "ggul_bamm", "both"], default="both")
    parser.add_argument("--force", action="store_true", help="시간 및 횟수 검증 건너뛰고 강제 실행")
    args = parser.parse_args()
    run_slot(args.account, force=args.force)
