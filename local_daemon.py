#!/usr/bin/env python3
"""
🚀 24/7 지속 실행 감시 데몬 (Continuous Auto-Poster Daemon)
대표님 핵심 지시: "계속 실행해줘" / "시간대는 참고하되 못올릴 것 같으면 그냥 시간 상관없이 하루에 10개만 채워줘"

역할:
1. 3~5분 간격으로 깨어나 오늘자 발행 현황(목표: 10개) 및 슬롯/쿨다운 상태를 실시간 감시합니다.
2. 계정 보호 쿨다운(15분)이 지났고 다음 슬롯 발행 조건이 충족되면 GitHub Actions를 즉각 원격 트리거합니다.
3. 깃허브 크론이 지연되거나 누락되더라도 이 데몬이 쉬지 않고 감시하여 하루 10개를 100% 무조건 채워 넣습니다.
4. 오늘 목표 10개 완주 시 또는 심야(23:00~07:15)에는 안전하게 대기합니다.
"""
import os
import sys
import time
import json
import subprocess
from datetime import datetime, timezone, timedelta

# KST 표준시 설정
KST = timezone(timedelta(hours=9))

REPO_NAME = "bohwan100/zipbabbot"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "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")
WORKFLOW_ID = "354810326"

def log(msg: str):
    now_str = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now_str} KST] {msg}", flush=True)

def git_pull():
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    except Exception as e:
        log(f"⚠️ git pull 오류 (무시 후 계속): {e}")

def get_active_github_run() -> bool:
    """현재 깃허브 액션에서 발행 워크플로우가 실행 중인지 확인"""
    cmd = [
        "curl", "-s",
        "-H", f"Authorization: token {GITHUB_TOKEN}",
        f"https://api.github.com/repos/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}/runs?status=in_progress"
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
        if res.returncode == 0:
            data = json.loads(res.stdout)
            runs = data.get("workflow_runs", [])
            return len(runs) > 0
    except Exception as e:
        log(f"⚠️ GitHub Actions 상태 조회 오류: {e}")
    return False

def trigger_github_action():
    """GitHub Actions 수동 트리거 (workflow_dispatch)"""
    log("🚀 [데몬] 슬롯 발행 조건 충족! GitHub Actions 발행 워크플로우를 즉시 트리거합니다...")
    cmd = [
        "curl", "-s", "-X", "POST",
        "-H", f"Authorization: token {GITHUB_TOKEN}",
        "-H", "Accept: application/vnd.github.v3+json",
        f"https://api.github.com/repos/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}/dispatches",
        "-d", '{"ref":"main","inputs":{"account":"both"}}'
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
        log("✅ [데몬] GitHub Actions 트리거 요청 전송 완료.")
    except Exception as e:
        log(f"❌ [데몬] 트리거 전송 실패: {e}")

def main():
    log("=================================================================")
    log("🚀 [24/7 지속 실행 감시 데몬] 백그라운드 무한 가동 시작")
    log("   목표: 온리애플(@only_apples0.1) & 꿀밤(@ggul_bamm) 하루 각 10개 완주")
    log("=================================================================")

    last_trigger_timestamp = 0.0

    while True:
        try:
            # 1. 최신 커밋 및 발행 이력 동기화
            git_pull()

            # 2. 동적으로 run_scheduled_slot 로드하여 발행 자격 검사
            import run_scheduled_slot
            import importlib
            importlib.reload(run_scheduled_slot)

            now_kst = datetime.now(KST)
            apples_ready, apples_msg, apples_count = run_scheduled_slot.check_can_post_now("only_apples0.1")
            bamm_ready, bamm_msg, bamm_count = run_scheduled_slot.check_can_post_now("ggul_bamm")

            log(f"📊 [진행 현황] 온리애플: {apples_count}/10개 | 꿀밤: {bamm_count}/10개")

            # 두 계정 모두 10개 완주한 경우
            if apples_count >= 10 and bamm_count >= 10:
                log("🎉🎉 [오늘 목표 완주] 두 계정 모두 10개 업로드 완료! 내일 아침까지 편안히 휴식합니다.")
                time.sleep(300)
                continue

            # 심야/새벽 시간대 (23:00 ~ 07:15)
            now_total_minutes = now_kst.hour * 60 + now_kst.minute
            if now_total_minutes > (23 * 60) or now_total_minutes < (7 * 60 + 15):
                log(f"🌙 [취침 보호] 현재 시각 {now_kst.strftime('%H:%M')} (23:00~07:15 야간 피드 보호 중, 10분 후 재확인)")
                time.sleep(600)
                continue

            # 발행 가능한 계정이 있는 경우
            if apples_ready or bamm_ready:
                # 이미 깃허브 액션이 돌고 있는지 확인 (중복 실행 방지)
                if get_active_github_run():
                    log("⏳ [대기] 현재 GitHub Actions 러너가 이미 업로드 작업 수행 중입니다. 완료될 때까지 대기...")
                    time.sleep(45)
                    continue

                # 직전 트리거로부터 최소 15분(안전 쿨다운) 경과 여부 확인
                time_since_trigger = time.time() - last_trigger_timestamp
                if time_since_trigger < 900:
                    wait_remaining = int(900 - time_since_trigger)
                    log(f"⏳ [안전 쿨다운] 직전 트리거 후 {int(time_since_trigger/60)}분 경과. 다음 트리거까지 {wait_remaining}초 대기...")
                    time.sleep(min(60, wait_remaining))
                    continue

                log(f"👉 발행 필요 사유: {apples_msg if apples_ready else bamm_msg}")
                trigger_github_action()
                last_trigger_timestamp = time.time()
                
                # 발행 작업이 시작되었으므로 120초간 대기 후 다시 모니터링
                log("⏳ 발행 작업 수행 중... (2분간 대기)")
                time.sleep(120)
            else:
                log(f"⏳ [쿨다운/안정 페이스 대기 중]")
                log(f"   - 온리애플: {apples_msg}")
                log(f"   - 꿀밤: {bamm_msg}")
                # 3분 대기 후 다음 주기 검사
                time.sleep(180)

        except Exception as e:
            log(f"⚠️ 데몬 루프 예외 발생 (자동 복구 후 재시도): {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
