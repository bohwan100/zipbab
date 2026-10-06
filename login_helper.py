import os
import sys
import time
import base64
import requests
from playwright.sync_api import sync_playwright
from dotenv import set_key, load_dotenv
from nacl import public, encoding

load_dotenv()

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "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")
REPO_NAME = "bohwan100/zipbabbot"

def update_github_secret(name: str, value: str):
    """GitHub Actions Secret에 암호화하여 즉시 반영"""
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        r = requests.get(f"https://api.github.com/repos/{REPO_NAME}/actions/secrets/public-key", headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"⚠️ GitHub public key 조회 실패: {r.status_code}")
            return False
        key_data = r.json()
        pub_key = public.PublicKey(key_data["key"].encode("utf-8"), encoding.Base64Encoder())
        box = public.SealedBox(pub_key)
        encrypted = box.encrypt(value.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

        payload = {"encrypted_value": encrypted_b64, "key_id": key_data["key_id"]}
        put_res = requests.put(f"https://api.github.com/repos/{REPO_NAME}/actions/secrets/{name}", headers=headers, json=payload, timeout=10)
        if put_res.status_code in [201, 204]:
            print(f"✅ GitHub Actions Secret '{name}' 자동 동기화 성공!")
            return True
        else:
            print(f"⚠️ GitHub Actions Secret 업데이트 실패: {put_res.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ GitHub Secret 동기화 중 오류: {e}")
        return False

def login_and_save_cookie(account: str = "auto"):
    print("=" * 60)
    print("🔑 스레드 로그인 헬퍼 가동 (화면에 브라우저 창이 열립니다)")
    print("=" * 60)
    print("화면에 열리는 브라우저에서 인스타그램/스레드 로그인을 완료해주세요.")
    print("로그인 완료 시 계정(@only_apples0.1 또는 @ggul_bamm)을 자동 감지하여")
    print(".env 및 GitHub Actions Secrets에 자동으로 즉시 동기화합니다.\n")

    with sync_playwright() as p:
        # 화면에 보이는 Chromium 브라우저 실행
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale="ko-KR")
        page = context.new_page()
        page.goto("https://www.threads.com/login")

        captured = False
        for i in range(150): # 최대 5분 대기
            time.sleep(2)
            try:
                cookies = context.cookies()
            except Exception:
                # 브라우저를 사용자가 수동으로 닫았을 때 예외 방지
                print("\n⚠️ 브라우저 창이 닫혔습니다.")
                break

            session_cookie = next((c for c in cookies if c["name"] == "sessionid"), None)
            ds_user_id = next((c for c in cookies if c["name"] == "ds_user_id"), None)

            if session_cookie and "login" not in page.url:
                sess_val = session_cookie["value"]
                uid_val = ds_user_id["value"] if ds_user_id else ""

                # 프로필 페이지 확인하여 어떤 계정인지 자동 판별
                detected_account = account
                try:
                    print("🔍 로그인된 계정 핸들 자동 확인 중...")
                    page.goto("https://www.threads.com/@me", wait_until="networkidle", timeout=8000)
                    time.sleep(2)
                    final_url = page.url.lower()
                    print(f"📍 로그인 완료 후 리다이렉트 URL: {final_url}")
                    if "only_apples" in final_url or "apple" in final_url:
                        detected_account = "only_apples"
                    elif "ggul_bamm" in final_url or "bamm" in final_url:
                        detected_account = "ggul_bamm"
                except Exception as e:
                    print(f"URL 확인 중 오류(기본 설정 적용): {e}")

                if detected_account == "auto":
                    # 기본 폴백: 전달된 인자나 bamm
                    detected_account = sys.argv[1] if len(sys.argv) > 1 else "ggul_bamm"

                prefix = "ONLY_APPLES" if "apple" in detected_account else "GGUL_BAMM"
                set_key(ENV_PATH, f"{prefix}_SESSION_ID", sess_val)
                if uid_val:
                    set_key(ENV_PATH, f"{prefix}_USER_ID", uid_val)

                print(f"\n🎉 [{prefix}] 새 세션 쿠키 .env 저장 완료!")
                print(f" • SESSION_ID: {sess_val[:20]}...")
                if uid_val:
                    print(f" • USER_ID: {uid_val}")

                # GitHub Actions Secrets 자동 동기화
                update_github_secret(f"{prefix}_SESSION_ID", sess_val)
                if uid_val:
                    update_github_secret(f"{prefix}_USER_ID", uid_val)

                captured = True
                break

        time.sleep(3)
        try:
            browser.close()
        except Exception:
            pass
        return captured

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "auto"
    login_and_save_cookie(target)


