# 유튜브 댓글 수집기 (fetch_youtube_comments.py)

`yt-dlp` 및 `youtube-comment-downloader` 라이브러리를 사용하여 유튜브에서 특정 키워드로 영상을 검색하고, 각 영상의 인기 댓글을 수집하여 Excel 및 CSV 파일로 저장하는 Python 스크립트입니다.

---

## 📌 주요 기능
1. **유튜브 영상 검색**: 지정된 키워드로 유튜브 영상 검색 (`yt-dlp` 기반)
2. **댓글 수집**: 검색된 각 영상의 인기순 댓글 수집 (`youtube-comment-downloader` 기반)
3. **데이터 내보내기**:
   - **Excel (`.xlsx`)**: '수집영상목록' 및 '댓글목록' 시트로 분리 저장
   - **CSV (`.csv`)**: 엑셀 호환 UTF-8-SIG 인코딩으로 댓글 데이터 저장

---

## 📦 필요 라이브러리 설치

```bash
pip install yt-dlp youtube-comment-downloader pandas openpyxl
```

---

## 💻 전체 소스 코드

```python
import json
import time
import pandas as pd
from itertools import islice
from yt_dlp import YoutubeDL
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR, SORT_BY_RECENT

def search_youtube_videos(keyword, max_results=5):
    """
    yt-dlp를 이용해 키워드로 유튜브 영상을 검색합니다.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    
    search_query = f"ytsearch{max_results}:{keyword}"
    print(f"[*] 유튜브에서 '{keyword}' 검색 중... (최대 {max_results}개 영상)")
    
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
    youtube-comment-downloader를 이용해 특정 영상의 댓글을 수집합니다.
    """
    downloader = YoutubeCommentDownloader()
    comments = []
    try:
        # 인기순 (SORT_BY_POPULAR = 0)
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

def main():
    keyword = "배달음식"
    # 상위 5개 영상에서 각각 최대 50개 댓글 수집
    videos = search_youtube_videos(keyword, max_results=5)
    
    all_comments_data = []
    video_summary = []
    
    for idx, v in enumerate(videos, 1):
        print(f"\n[{idx}/{len(videos)}] 영상: {v['title']} ({v['url']})")
        comments = fetch_comments_for_video(v['url'], max_comments=50)
        print(f" -> 수집된 댓글 수: {len(comments)}개")
        
        v['collected_comments_count'] = len(comments)
        video_summary.append(v)
        
        for c in comments:
            all_comments_data.append({
                '영상 제목': v['title'],
                '영상 URL': v['url'],
                '채널명': v['uploader'],
                '댓글 작성자': c['author'],
                '댓글 내용': c['text'],
                '좋아요 수': c['votes'],
                '작성 시점': c['time'],
                '하트 여부': 'O' if c['heart'] else 'X',
                '답글 여부': '답글' if c['reply'] else '일반댓글'
            })
        time.sleep(1)

    # DataFrame 생성 및 저장
    df_comments = pd.DataFrame(all_comments_data)
    df_videos = pd.DataFrame(video_summary)
    
    excel_filename = "배달음식_유튜브댓글_수집결과.xlsx"
    csv_filename = "배달음식_유튜브댓글_수집결과.csv"
    
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df_videos.to_excel(writer, sheet_name='수집영상목록', index=False)
        df_comments.to_excel(writer, sheet_name='댓글목록', index=False)
        
    df_comments.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n[+] 수집 완료! 총 {len(all_comments_data)}개의 댓글이 저장되었습니다.")
    print(f" - 엑셀 파일: {excel_filename}")
    print(f" - CSV 파일: {csv_filename}")

if __name__ == '__main__':
    main()
```

---

## 📊 수집 데이터 구조

### 1. 영상 목록 (`수집영상목록`)
| 필드명 | 설명 |
| :--- | :--- |
| `video_id` | 유튜브 영상 ID |
| `title` | 영상 제목 |
| `url` | 영상 재생 URL |
| `uploader` | 채널/업로더 이름 |
| `view_count` | 조회수 |
| `duration` | 영상 길이 (초) |
| `collected_comments_count` | 수집된 댓글 수 |

### 2. 댓글 목록 (`댓글목록`)
| 필드명 | 설명 |
| :--- | :--- |
| `영상 제목` | 해당 댓글이 작성된 영상의 제목 |
| `영상 URL` | 영상 URL |
| `채널명` | 채널 이름 |
| `댓글 작성자` | 댓글 작성자 닉네임 |
| `댓글 내용` | 작성된 댓글 텍스트 |
| `좋아요 수` | 해당 댓글의 좋아요 수 |
| `작성 시점` | 작성 시기 (예: '2일 전', '3개월 전') |
| `하트 여부` | 채널 게시자의 하트 수락 여부 (`O` / `X`) |
| `답글 여부` | 대댓글 여부 (`답글` / `일반댓글`) |

---

## 🚀 실행 방법

```bash
python fetch_youtube_comments.py
```