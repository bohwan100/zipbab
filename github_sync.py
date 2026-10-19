#!/usr/bin/env python3
"""
집밥봇 (ZipbabBot) - GitHub 자동 영구 보존 (Auto-Sync) 모듈
고객 등록/삭제 시 자동으로 GitHub에 커밋 & 푸시하여 Render 절전 모드 롤백을 100% 방지합니다.
"""

import os
import sys
import subprocess
import threading
import datetime

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(DIRECTORY, "scratch", "git_sync.log")

def _log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [GitSync] {msg}"
    print(formatted)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def _run_cmd(cmd, cwd=DIRECTORY, timeout=30):
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def perform_git_sync(commit_message="feat: auto-sync clients data"):
    """
    clients/ 폴더와 clients.html의 변경 사항을 GitHub으로 커밋 및 푸시합니다.
    """
    _log(f"Starting Git auto-sync: {commit_message}")

    git_dir = os.path.join(DIRECTORY, ".git")
    if not os.path.exists(git_dir):
        _log("⚠️ .git directory not found. Skipping git sync.")
        return False, "Not a git repository"

    # 1. Git 작성자 정보 및 safe.directory 설정 (컨테이너/원격 환경 대비)
    _run_cmd(["git", "config", "--global", "--add", "safe.directory", "*"])
    _run_cmd(["git", "config", "user.name", "ZipbabBot AutoSync"])
    _run_cmd(["git", "config", "user.email", "bot@zipbab.com"])

    # 2. Render 또는 원격 환경에서 GITHUB_TOKEN이 있을 경우 remote URL 갱신
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    auth_target = "origin"
    if token and token.strip():
        token = token.strip()
        auth_url = f"https://x-access-token:{token}@github.com/bohwan100/zipbab.git"
        auth_target = auth_url

        ok, remotes, _ = _run_cmd(["git", "remote"])
        remote_list = [r.strip() for r in remotes.split() if r.strip()]
        if "origin" in remote_list:
            _run_cmd(["git", "remote", "set-url", "origin", auth_url])
        else:
            _run_cmd(["git", "remote", "add", "origin", auth_url])
        _log("Configured authenticated remote URL using GITHUB_TOKEN.")

    # 3. 변경 사항 스테이징
    _run_cmd(["git", "add", "-A", "clients/", "clients.html"])

    # 4. 변경 사항 있는지 확인
    ok, status_out, _ = _run_cmd(["git", "status", "--porcelain"])
    if not status_out.strip():
        _log("No local file changes to commit. Verifying remote repository access...")
        ok, out, err = _run_cmd(["git", "ls-remote", auth_target, "main"])
        if ok:
            _log("✅ Remote repository access verified successfully with GitHub token!")
            return True, "GitHub connection verified & repository up to date"
        else:
            _log(f"❌ Failed to connect to remote: {err or out}")
            return False, err or out

    # 5. 커밋
    ok, out, err = _run_cmd(["git", "commit", "-m", commit_message])
    if not ok:
        _log(f"Commit warning/failed: {err or out}")

    # 6. 원격 최신 변경사항 rebase
    _run_cmd(["git", "pull", "--rebase", auth_target, "main"])

    # 7. 푸시 실행
    ok, out, err = _run_cmd(["git", "push", auth_target, "HEAD:main"])
    if ok:
        _log("✅ Successfully pushed clients data to GitHub origin/main!")
        return True, "Successfully synced to GitHub"
    else:
        _log(f"❌ Failed to push to GitHub: {err or out}")
        return False, err or out

def trigger_async_sync(commit_message="feat: auto-sync clients data"):
    """
    웹 서버 응답 속도를 저하시키지 않도록 백그라운드 스레드에서 비동기로 실행합니다.
    """
    t = threading.Thread(target=perform_git_sync, args=(commit_message,), daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    success, msg = perform_git_sync("test: manual sync verification")
    print(f"Result: success={success}, msg={msg}")
