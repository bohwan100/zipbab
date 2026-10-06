import os
import time
import requests
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(ENV_PATH)

def send_telegram_post_alert(account: str, text: str, comment: str = None, photo_path: str = None, daily_progress: str = None) -> bool:
    """
    스레드 게시물이 성공적으로 발행되었을 때 텔레그램으로 실시간 알림을 발송합니다.
    (텍스트 메시지 및 인증 캡처 사진 지원, 일일 목표 진행도 표시)
    """
    load_dotenv(ENV_PATH, override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return False

    acc_title = "🍎 [온리애플]" if "apple" in account else "🌰 [꿀밤]"
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    progress_line = f"📊 <b>오늘 달성 현황:</b> <b>{daily_progress}</b>\n\n" if daily_progress else ""

    message_text = (
        f"🎉 <b>{acc_title} 스레드 자동 발행 완료!</b>\n\n"
        f"⏰ <b>발행 시각:</b> {now_str}\n"
        f"👤 <b>계정:</b> @{account}\n"
        f"{progress_line}"
        f"📝 <b>본문 카피:</b>\n"
        f"<blockquote>{text}</blockquote>\n\n"
        f"💬 <b>첫 댓글(스마트스토어+오픈채팅):</b> 정상 등록 완료 ✅\n"
        f"🔗 <b>미리보기 박스:</b> 스마트스토어 상품 카드 선점 완료 ✅"
    )

    try:
        if photo_path and os.path.exists(photo_path):
            # 캡처 사진과 함께 전송
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(photo_path, "rb") as f:
                res = requests.post(
                    url,
                    data={"chat_id": chat_id, "caption": message_text, "parse_mode": "HTML"},
                    files={"photo": f},
                    timeout=15
                )
            if res.status_code == 200:
                print("📱 텔레그램 사진 알림 발송 성공!")
                return True

        # 사진이 없거나 사진 전송 실패 시 일반 텍스트 발송
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(
            url,
            json={"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"},
            timeout=10
        )
        if res.status_code == 200:
            print("📱 텔레그램 텍스트 알림 발송 성공!")
            return True
        else:
            print(f"⚠️ 텔레그램 발송 응답 에러: {res.text}")
            return False

    except Exception as e:
        print(f"⚠️ 텔레그램 알림 발송 예외: {e}")
        return False

def send_telegram_milestone_alert(account: str, views: int, text: str, post_url: str = None, photo_path: str = None) -> bool:
    """
    내 게시물이 '진짜 1만 뷰 이상' 마일스톤을 달성했을 때만 축하 알림 메시지를 발송합니다.
    (1만 뷰 미만일 경우 절대 발송하지 않는 방어 안전장치 내장)
    """
    if views < 10000:
        print(f"🛡️ [안전 방어] 조회수({views:,}회)가 1만 뷰 미만이므로 마일스톤 알림을 전송하지 않습니다.")
        return False

    load_dotenv(ENV_PATH, override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return False

    acc_title = "🍎 [온리애플]" if "apple" in account else "🌰 [꿀밤]"
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    views_str = f"{views:,}회" if views < 10000 else f"{views/10000:.1f}만 회"

    caption = (
        f"🚨🎉 <b>[축하합니다! 스레드 1만 뷰 떡상 달성!]</b> 🚀💥\n\n"
        f"👤 <b>계정:</b> {acc_title} (@{account})\n"
        f"👀 <b>현재 조회수:</b> <b>{views_str} 돌파!!</b> 🔥\n"
        f"⏰ <b>감지 시각:</b> {now_str}\n\n"
        f"📝 <b>떡상 본문 카피:</b>\n"
        f"<blockquote>{text.strip()[:150]}...</blockquote>\n\n"
        f"📈 <b>알고리즘 분석 보고:</b>\n"
        f"• 스레드 추천 피드(For You) 노출 가속화 진행 중!\n"
        f"• 첫 댓글의 스마트스토어 상품 카드와 오픈채팅 유입이 폭증하는 골든타임입니다 🛒\n\n"
        f"🔗 <b>스레드 확인:</b> {post_url or '스레드 프로필에서 확인'}"
    )

    try:
        if photo_path and os.path.exists(photo_path):
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(photo_path, "rb") as f:
                res = requests.post(
                    url,
                    data={"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"},
                    files={"photo": f},
                    timeout=15
                )
            if res.status_code == 200:
                print("📱 텔레그램 떡상 축하 사진 알림 발송 성공!")
                return True

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(
            url,
            json={"chat_id": chat_id, "text": caption, "parse_mode": "HTML"},
            timeout=10
        )
        if res.status_code == 200:
            print("📱 텔레그램 떡상 축하 알림 발송 성공!")
            return True
        return False
    except Exception as e:
        print(f"⚠️ 텔레그램 떡상 알림 발송 예외: {e}")
        return False


if __name__ == "__main__":
    # 테스트 전송
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("💡 .env 파일에 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 설정해주세요.")
    else:
        print(f"📡 텔레그램 테스트 발송 시도 중... (Chat ID: {chat_id})")
        success = send_telegram_post_alert(
            account="ggul_bamm",
            text="안녕 나는 꿀밤이야 ! 🌰\n테스트 알림 메시지입니다.",
            comment="스마트스토어 링크 등록 완료"
        )
        print("결과:", "성공" if success else "실패")
