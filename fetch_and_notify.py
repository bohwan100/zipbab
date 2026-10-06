import os
import sys
import time
from datetime import datetime
import pandas as pd
import requests
from itertools import islice
from yt_dlp import YoutubeDL
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

# 환경변수에서 텔레그램 설정값 불러오기
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """텔레그램으로 텍스트 메시지 발송"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[!] 텔레그램 환경변수가 설정되지 않았습니다.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        print("[+] 텔레그램 메시지 발송 완료")
    except Exception as e:
        print(f"[-] 텔레그램 메시지 발송 실패: {e}")

def send_telegram_file(file_path, caption=""):
    """텔레그램으로 마크다운(.md) 파일 발송"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            res = requests.post(url, files=files, data=data, timeout=30)
            res.raise_for_status()
        print(f"[+] 텔레그램 파일 발송 완료: {file_path}")
    except Exception as e:
        print(f"[-] 텔레그램 파일 발송 실패: {e}")

def search_youtube_videos(keyword, max_results=5):
    """유튜브에서 키워드로 최신/인기 영상을 검색"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    search_query = f"ytsearch{max_results}:{keyword}"
    print(f"[*] 유튜브에서 '{keyword}' 검색 중... ({max_results}개 영상)")
    
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_query, download=False)
        
    videos = []
    if 'entries' in result:
        for entry in result['entries']:
            if entry:
                video_info = {
                    'video_id': entry.get('id'),
                    'title': entry.get('title'),
                    'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    'uploader': entry.get('uploader') or entry.get('channel'),
                    'view_count': entry.get('view_count'),
                    'duration': entry.get('duration'),
                }
                videos.append(video_info)
    return videos

def fetch_comments_for_video(video_url, max_comments=50):
    """유튜브 영상에서 댓글 수집"""
    downloader = YoutubeCommentDownloader()
    comments = []
    try:
        generator = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
        for comment in islice(generator, max_comments):
            comments.append({
                'comment_id': comment.get('cid'),
                'author': comment.get('author'),
                'text': comment.get('text'),
                'votes': comment.get('votes'),
                'time': comment.get('time'),
                'heart': comment.get('heart', False),
                'reply': comment.get('reply', False)
            })
    except Exception as e:
        print(f"[-] 댓글 수집 오류 ({video_url}): {e}")
        
    return comments

def generate_markdown_report(videos, video_comments_map, keyword, today_date, today_time):
    """마크다운(.md) 포맷의 보고서 생성"""
    total_comments = sum(len(c_list) for c_list in video_comments_map.values())
    
    md = []
    md.append(f"# 🍳 '{keyword}' 유튜브 댓글 일일 수집 리포트\n")
    md.append(f"- **수집 일시**: {today_date} {today_time}")
    md.append(f"- **수집 대상 영상**: 총 {len(videos)}개")
    md.append(f"- **총 수집 댓글 수**: {total_comments}개\n")
    md.append("---\n")
    
    md.append("## 🎥 수집 영상 목록\n")
    md.append("| 번호 | 채널명 | 영상 제목 | 수집 댓글 | 링크 |")
    md.append("| :---: | :--- | :--- | :---: | :---: |")
    for idx, v in enumerate(videos, 1):
        v_url = v['url']
        c_count = len(video_comments_map.get(v_url, []))
        md.append(f"| {idx} | **{v['uploader']}** | {v['title']} | {c_count}개 | [영상 바로가기]({v_url}) |")
    md.append("\n---\n")
    
    md.append("## 💬 영상별 댓글 상세 목록\n")
    for idx, v in enumerate(videos, 1):
        v_url = v['url']
        comments = video_comments_map.get(v_url, [])
        md.append(f"### {idx}. [{v['uploader']}] {v['title']}")
        md.append(f"- **영상 링크**: {v_url}")
        md.append(f"- **수집된 댓글 수**: {len(comments)}개\n")
        
        if not comments:
            md.append("> *수집된 댓글이 없습니다.*\n")
            continue
            
        for c_idx, c in enumerate(comments, 1):
            author = c['author']
            votes = c['votes'] or 0
            time_str = c['time'] or ""
            # 줄바꿈 처리
            text = c['text'].replace('\n', '\n> ')
            
            md.append(f"**{c_idx}. {author}** (👍 {votes} · 🕒 {time_str})")
            md.append(f"> {text}\n")
            
        md.append("\n")
        
    return "\n".join(md)

def main():
    keyword = "배달음식"
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_time = datetime.now().strftime("%H:%M")
    
    print(f"[{today_date} {today_time}] 유튜브 댓글 자동 수집 시작...")
    
    videos = search_youtube_videos(keyword, max_results=5)
    video_comments_map = {}
    
    for idx, v in enumerate(videos, 1):
        print(f"[{idx}/{len(videos)}] 수집 중: {v['title']}")
        comments = fetch_comments_for_video(v['url'], max_comments=50)
        v['collected_comments_count'] = len(comments)
        video_comments_map[v['url']] = comments
        time.sleep(1)

    # 마크다운(.md) 보고서 생성 및 파일 저장
    md_content = generate_markdown_report(videos, video_comments_map, keyword, today_date, today_time)
    md_filename = f"배달음식_유튜브댓글_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"[+] 마크다운 보고서 저장 완료: {md_filename}")

    # 텔레그램 요약 메시지 생성
    total_comments = sum(len(c) for c in video_comments_map.values())
    msg = f"🌅 <b>[배달음식 유튜브 댓글 일일 브리핑]</b> ({today_date})\n\n"
    msg += f"✅ <b>수집된 영상:</b> {len(videos)}개\n"
    msg += f"✅ <b>총 수집 댓글:</b> {total_comments}개\n\n"
    msg += "📌 <b>수집 영상 목록:</b>\n"
    for idx, v in enumerate(videos, 1):
        msg += f"{idx}. <a href='{v['url']}'>{v['title'][:25]}...</a> ({len(video_comments_map.get(v['url'], []))}개)\n"
    
    msg += "\n📝 상세 댓글 리포트는 첨부된 <b>.md (마크다운) 파일</b>을 확인해주세요!"
    
    # 텔레그램 발송
    send_telegram_message(msg)
    send_telegram_file(md_filename, caption=f"📝 {today_date} 배달음식 유튜브 댓글 리포트 (.md)")

if __name__ == '__main__':
    main()
