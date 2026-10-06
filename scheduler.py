import os
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict
from content_engine import ContentEngine
from threads_multi_poster import post_to_threads_multi

# 기준 시간표 (10개 슬롯)
BASE_TIME_SLOTS = [
    (7, 30),   # 07:30
    (8, 0),    # 08:00
    (12, 0),   # 12:00
    (12, 20),  # 12:20
    (17, 0),   # 17:00
    (17, 30),  # 17:30
    (18, 0),   # 18:00
    (20, 0),   # 20:00
    (21, 0),   # 21:00
    (22, 0),   # 22:00
]

def generate_safe_schedule_for_account(account: str, base_date: datetime = None) -> List[datetime]:
    """
    지정된 10개 시간대에 ±10분 오차를 부여하되,
    어떤 경우에도 게시물 간격이 15분 미만으로 좁혀지지 않도록 안전 보정한 시간표를 생성합니다.
    """
    now = base_date or datetime.now()
    scheduled_times = []

    for h, m in BASE_TIME_SLOTS:
        # ±10분 랜덤 오차 생성 (ex: -9 ~ +9분)
        jitter_minutes = random.randint(-8, 8)
        slot_dt = now.replace(hour=h, minute=m, second=random.randint(5, 55), microsecond=0) + timedelta(minutes=jitter_minutes)
        scheduled_times.append(slot_dt)

    # 15분 간격 제약조건 강제 보정 (앞뒤 시간 충돌 방지)
    for i in range(1, len(scheduled_times)):
        diff_minutes = (scheduled_times[i] - scheduled_times[i-1]).total_seconds() / 60.0
        if diff_minutes < 15.0:
            # 15분이 안 되면 최소 16분 뒤로 강제 보정
            needed_shift = 16.0 - diff_minutes
            scheduled_times[i] += timedelta(minutes=needed_shift)

    return scheduled_times

def build_daily_timetable(custom_link_apples: str = None, custom_link_bamm: str = None) -> List[Dict]:
    """
    ggul_bamm (10개) + only_apples0.1 (10개) = 총 20개 게시물 일정표 생성
    두 계정이 동시에 올라가지 않도록 계정 간에도 5~8분 시차 배치
    """
    engine = ContentEngine()
    today = datetime.now()

    apples_times = generate_safe_schedule_for_account("only_apples0.1", today)
    bamm_times = generate_safe_schedule_for_account("ggul_bamm", today)

    # 두 계정이 같은 분에 겹치지 않도록 bamm 계정은 5~7분 분산
    bamm_times = [t + timedelta(minutes=random.randint(5, 8)) for t in bamm_times]

    apples_posts = engine.generate_daily_schedule_posts("only_apples0.1", count=10, custom_comment=custom_link_apples)
    bamm_posts = engine.generate_daily_schedule_posts("ggul_bamm", count=10, custom_comment=custom_link_bamm)

    timetable = []

    for i in range(10):
        timetable.append({
            "slot_index": i + 1,
            "scheduled_time": apples_times[i],
            "account": "only_apples0.1",
            "text": apples_posts[i]["text"],
            "image_path": apples_posts[i]["image_path"],
            "comment": apples_posts[i].get("comment"),
            "is_done": False
        })
        timetable.append({
            "slot_index": i + 1,
            "scheduled_time": bamm_times[i],
            "account": "ggul_bamm",
            "text": bamm_posts[i]["text"],
            "image_path": bamm_posts[i]["image_path"],
            "comment": bamm_posts[i].get("comment"),
            "is_done": False
        })

    # 시간순으로 정렬
    timetable.sort(key=lambda x: x["scheduled_time"])
    return timetable

def run_scheduler_daemon(headless: bool = True):
    """
    하루 종일 켜두고 정해진 시간표에 맞춰 자동으로 글을 쏘아 올리는 메인 실행 루프
    """
    print("=" * 65)
    print("⏰ [스레드 24시간 스마트 스케줄러 가동]")
    print("=" * 65)

    current_day = datetime.now().date()
    timetable = build_daily_timetable()
    
    # 이미 지난 오늘 이전 시간대 슬롯은 자동 완료 처리
    now_init = datetime.now()
    for item in timetable:
        if item["scheduled_time"] < now_init:
            item["is_done"] = True

    upcoming = [item for item in timetable if not item["is_done"]]
    print(f"\n📅 오늘({current_day}) 총 {len(timetable)}개 슬롯 중 앞으로 발행 예정: {len(upcoming)}개")
    for item in upcoming:
        print(f" • {item['scheduled_time'].strftime('%H:%M:%S')} | [{item['account']:<14}] {item['text'][:25]}...")

    print("\n⏳ 예약 감시를 시작합니다. (24시간 백그라운드 상시 가동 중)")
    last_view_check = datetime.now()

    while True:
        now = datetime.now()

        # 자정 이후 날짜 변경 시 다음 날 20개 타임테이블 새로 생성
        if now.date() != current_day:
            current_day = now.date()
            print(f"\n🔄 [자정 갱신] 새로운 날짜({current_day})의 일일 타임테이블(20개 슬롯)을 생성합니다.")
            timetable = build_daily_timetable()
            for item in timetable:
                print(f" • {item['scheduled_time'].strftime('%H:%M:%S')} | [{item['account']:<14}] {item['text'][:25]}...")

        for item in timetable:
            if not item["is_done"]:
                # 예정 시간 도달 시 (예정 시간 ~ 10분 이내)
                if item["scheduled_time"] <= now <= item["scheduled_time"] + timedelta(minutes=10):
                    print(f"\n⏰ [예약 시간 도달!] {now.strftime('%H:%M:%S')} ➔ 계정: {item['account']}")
                    try:
                        post_to_threads_multi(
                            account=item["account"],
                            text=item["text"],
                            image_path=item["image_path"],
                            comment=item.get("comment"),
                            headless=headless,
                            enable_stealth=True
                        )
                        item["is_done"] = True
                        print(f"✅ [{item['account']}] {now.strftime('%H:%M:%S')} 슬롯 포스팅 완료!")
                    except Exception as e:
                        print(f"❌ 포스팅 실패: {e}")
                        item["is_done"] = True # 무한 재시도 방지
        time.sleep(30) # 30초마다 시간 체크

        # 30분마다 내 게시물 조회수 체크 및 1만 뷰 돌파 축하 알림 발송
        if (now - last_view_check).total_seconds() >= 1800:
            last_view_check = now
            try:
                from view_milestone_monitor import check_and_alert_milestones
                check_and_alert_milestones(headless=headless)
            except Exception as e:
                print(f"⚠️ 조회수 모니터링 예외: {e}")

if __name__ == "__main__":
    import sys
    # 실행 시 데몬 가동 (기본 headless=True)
    headless_mode = "--show-browser" not in sys.argv
    run_scheduler_daemon(headless=headless_mode)


