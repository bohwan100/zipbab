"""
🚀 [스레드 단독 즉시 포스팅 도구] run_post.py
24시간 자동 스케줄러와 별개로, 지금 즉시 특정 계정으로 글을 테스트 발행할 때 사용합니다.

사용법:
  python3 run_post.py only_apples0.1   # 사과 계정으로 1회 즉시 발행
  python3 run_post.py ggul_bamm        # 밤 계정으로 1회 즉시 발행
"""
import sys
from content_engine import ContentEngine
from threads_multi_poster import post_to_threads_multi

def run_single_post(account: str = "only_apples0.1", headless: bool = False):
    print("=" * 65)
    print(f"🚀 [{account}] AI 학습 기반 즉시 포스팅 시작")
    print("=" * 65)
    
    engine = ContentEngine()
    post_data = engine.generate_post(account)
    
    print(f"📝 생성된 본문:\n{post_data['text']}\n")
    print("-" * 65)
    print(f"💬 첨부될 첫 댓글:\n{post_data.get('comment', '')}\n")
    print("=" * 65)
    
    success = post_to_threads_multi(
        account=account,
        text=post_data["text"],
        image_path=post_data["image_path"],
        comment=post_data.get("comment"),
        headless=headless,
        enable_stealth=True
    )
    
    if success:
        print(f"🎉 [{account}] 즉시 포스팅 성공 완료!")
    else:
        print(f"❌ [{account}] 즉시 포스팅 실패")
    return success

if __name__ == "__main__":
    target_account = sys.argv[1] if len(sys.argv) > 1 else "only_apples0.1"
    if target_account not in ["only_apples0.1", "ggul_bamm"]:
        print("⚠️ 사용 가능한 계정: only_apples0.1 또는 ggul_bamm")
        sys.exit(1)
    run_single_post(target_account, headless=False)
