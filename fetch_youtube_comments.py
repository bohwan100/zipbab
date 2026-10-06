import os
import sys
import time
from datetime import datetime
from itertools import islice
from yt_dlp import YoutubeDL
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

def search_youtube_videos(keyword, max_results=5):
    """
    yt-dlp를 이용해 키워드로 유튜브 최신/인기 영상을 검색합니다.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    
    search_query = f"ytsearch{max_results}:{keyword}"
    print(f"[*] 유튜브에서 '{keyword}' 검색 중... (영상 {max_results}개)")
    
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
    """
    youtube-comment-downloader를 이용해 영상의 댓글을 수집합니다.
    """
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
        print(f"[-] 댓글 수집 중 오류 ({video_url}): {e}")
        
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
            text = c['text'].replace('\n', '\n> ')
            
            md.append(f"**{c_idx}. {author}** (👍 {votes} · 🕒 {time_str})")
            md.append(f"> {text}\n")
            
        md.append("\n")
        
    return "\n".join(md)

def main():
    keyword = "배달음식"
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_time = datetime.now().strftime("%H:%M")
    
    videos = search_youtube_videos(keyword, max_results=5)
    video_comments_map = {}
    
    for idx, v in enumerate(videos, 1):
        print(f"[{idx}/{len(videos)}] 수집 중: {v['title']}")
        comments = fetch_comments_for_video(v['url'], max_comments=50)
        video_comments_map[v['url']] = comments
        time.sleep(1)

    md_content = generate_markdown_report(videos, video_comments_map, keyword, today_date, today_time)
    
    md_filename = f"배달음식_유튜브댓글_{datetime.now().strftime('%Y%m%d')}.md"
    latest_md = "배달음식_유튜브댓글_최신.md"
    
    for path in [md_filename, latest_md]:
        with open(path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
    print(f"\n[+] 마크다운 보고서 저장 완료!")
    print(f" - 일자별: {md_filename}")
    print(f" - 최신본: {latest_md}")

if __name__ == '__main__':
    main()
