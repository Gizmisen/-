from flask import Flask, render_template, request, jsonify, redirect
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import Config
import logging
import yt_dlp
import sys
import io

app = Flask(__name__)

# Загружаем конфиг
try:
    app.config.from_object(Config)
except Exception as e:
    print(f"⚠️  Ошибка конфига: {e}")
    app.config['YOUTUBE_API_KEY'] = os.environ.get('YOUTUBE_API_KEY', '')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Скрываем verbose логи yt-dlp
logging.getLogger('yt_dlp').setLevel(logging.CRITICAL)
logging.getLogger('yt_dlp.extractor').setLevel(logging.CRITICAL)

def check_yt_dlp():
    """Проверяем, установлен ли yt-dlp"""
    try:
        import yt_dlp
        return True
    except:
        return False
api_key = app.config.get('YOUTUBE_API_KEY', '')

if not api_key:
    print("❌ ОШИБКА: YOUTUBE_API_KEY не установлен!")
    print("📌 Решение:")
    print("   1. Отредактируйте config.py")
    print("   2. Или установите переменную: export YOUTUBE_API_KEY='ваш_ключ'")
    api_key = os.environ.get('YOUTUBE_API_KEY', '')
    if not api_key:
        print("❌ YOUTUBE_API_KEY так и не найден. Выход.")
        sys.exit(1)

try:
    youtube = build('youtube', 'v3', developerKey=api_key)
    print("✅ YouTube API подключен успешно")
except Exception as e:
    print(f"❌ Ошибка подключения YouTube API: {e}")
    print("⚠️  Приложение будет работать без поиска видео")
    youtube = None

def get_video_url(video_id):
    """Получаем видео - работает везде в России! Несколько способов."""
    
    if not check_yt_dlp():
        return None
    # Способ 1: Попытка с разными User-Agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ]
    
    for user_agent in user_agents:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 15,
                'http_headers': {'User-Agent': user_agent},
                'skip_unavailable_fragments': True,
            }
            
            # Перенаправляем вывод
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            
            try:
                sys.stdout = io.StringIO()
                sys.stderr = io.StringIO()
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                    url = info.get('url')
                    if url:
                        return url
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
        except Exception:
            continue
    
    # Способ 2: Попытка через инициализацию клиента
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 20,
            'extractor_args': {'youtube': {'player_client': ['web', 'android']}},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        try:
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                url = info.get('url')
                if url:
                    return url
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    except Exception:
        pass
    
    # Если ничего не сработало - возвращаем None (будет fallback)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status_check():
    """Страница для проверки статуса приложения"""
    status = {
        'app_running': True,
        'youtube_api': youtube is not None,
        'yt_dlp_available': check_yt_dlp(),
        'version': '2.0-russia-bypass'
    }
    return jsonify(status)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
    else:
        query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('index.html', error="Введите поисковый запрос")
    
    try:
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=20,
            type='video',
            order='relevance'
        ).execute()
        
        videos = []
        for item in search_response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_data = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'channel_title': item['snippet']['channelTitle'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url']
                }
                videos.append(video_data)
        
        return render_template('results.html', 
                             videos=videos, 
                             query=query,
                             total_results=len(videos))
    
    except HttpError as e:
        logger.error(f'YouTube API Error: {e}')
        return render_template('error.html', 
                             message=f'Ошибка API: {e.resp.status}')

@app.route('/video/<video_id>')
def watch_video(video_id):
    try:
        video_response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        ).execute()
        
        if not video_response['items']:
            return render_template('error.html', message='Видео не найдено')
        
        item = video_response['items'][0]
        
        # Получаем fallback URL на случай блокировки региона
        fallback_url = get_video_url(video_id)
        
        video_details = {
            'id': video_id,
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'published_at': item['snippet']['publishedAt'][:10],
            'channel_title': item['snippet']['channelTitle'],
            'view_count': format(int(item['statistics'].get('viewCount', 0)), ','),
            'like_count': format(int(item['statistics'].get('likeCount', 0)), ','),
            'comment_count': format(int(item['statistics'].get('commentCount', 0)), ','),
            'duration': item['contentDetails']['duration'],
            'fallback_url': fallback_url
        }
        
        return render_template('video.html', video=video_details)
    
    except HttpError as e:
        logger.error(f'YouTube API Error: {e}')
        return render_template('error.html', 
                             message=f'Ошибка загрузки видео: {e.resp.status}')

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()
    max_results = int(request.args.get('max', 10))
    
    if not query:
        return jsonify({'success': False, 'error': 'Empty query'})
    
    try:
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            order='relevance'
        ).execute()
        
        videos = []
        for item in search_response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_data = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'published': item['snippet']['publishedAt'][:10]
                }
                videos.append(video_data)
        
        return jsonify({
            'success': True,
            'query': query,
            'videos': videos,
            'count': len(videos)
        })
    
    except HttpError as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/video/<video_id>')
def api_video_info(video_id):
    try:
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        
        if not video_response['items']:
            return jsonify({'success': False, 'error': 'Video not found'})
        
        item = video_response['items'][0]
        return jsonify({
            'success': True,
            'video': {
                'id': video_id,
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'views': item['statistics'].get('viewCount', '0'),
                'likes': item['statistics'].get('likeCount', '0')
            }
        })
    
    except HttpError as e:
        return jsonify({'success': False, 'error': str(e)})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message='Страница не найдена'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message='Внутренняя ошибка сервера'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
