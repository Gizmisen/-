#!/bin/bash

# Скрипт для проверки YouTube API ключа

echo "🔑 Проверка YouTube API ключа"
echo "================================"
echo ""

# Проверка наличия ключа
if [ -z "$YOUTUBE_API_KEY" ]; then
    echo "❌ Переменная окружения YOUTUBE_API_KEY не установлена"
    echo ""
    echo "📝 Установите ключ одним из способов:"
    echo ""
    echo "1️⃣  Временно (только для текущей сессии):"
    echo "   export YOUTUBE_API_KEY='ваш_ключ_здесь'"
    echo ""
    echo "2️⃣  Постоянно через .env файл:"
    echo "   echo 'YOUTUBE_API_KEY=ваш_ключ_здесь' > .env"
    echo ""
    echo "3️⃣  Ввести сейчас:"
    read -p "   Введите ваш YouTube API ключ: " api_key
    if [ -n "$api_key" ]; then
        export YOUTUBE_API_KEY="$api_key"
        echo "   ✅ Ключ установлен временно"
    else
        echo "   ❌ Ключ не введен. Выход."
        exit 1
    fi
    echo ""
fi

# Показываем первые символы ключа для безопасности
key_preview="${YOUTUBE_API_KEY:0:10}...${YOUTUBE_API_KEY: -4}"
echo "🔍 Найден ключ: $key_preview"
echo ""

# Проверяем, установлены ли зависимости
echo "📦 Проверка зависимостей..."
if ! python3 -c "import googleapiclient" 2>/dev/null; then
    echo "❌ google-api-python-client не установлен"
    echo "📥 Установка зависимостей..."
    pip install -q -r requirements.txt
    echo "✅ Зависимости установлены"
else
    echo "✅ Все зависимости установлены"
fi
echo ""

# Тестируем API ключ
echo "🧪 Тестирование API ключа..."
echo ""

python3 << EOF
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

api_key = os.environ.get('YOUTUBE_API_KEY')
if not api_key:
    print("❌ API ключ не найден")
    sys.exit(1)

try:
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Простой тестовый запрос
    request = youtube.search().list(
        part='snippet',
        q='test',
        maxResults=1,
        type='video'
    )
    response = request.execute()
    
    if response.get('items'):
        print("✅ API ключ работает корректно!")
        print(f"✅ Найдено видео: {response['items'][0]['snippet']['title']}")
        print("")
        print("🎉 Все готово! Можете запускать приложение:")
        print("   python app.py")
        sys.exit(0)
    else:
        print("⚠️  API ключ работает, но поиск не вернул результатов")
        sys.exit(0)
        
except HttpError as e:
    error_reason = e.error_details[0]['reason'] if e.error_details else 'unknown'
    
    if e.resp.status == 400:
        if 'keyInvalid' in str(e) or 'badRequest' in str(e):
            print("❌ API ключ недействителен")
            print("   Проверьте правильность ключа")
        else:
            print(f"❌ Ошибка запроса: {error_reason}")
    elif e.resp.status == 403:
        if 'quotaExceeded' in str(e):
            print("❌ Квота API исчерпана")
            print("   Подождите до следующего дня или увеличьте квоту")
        elif 'accessNotConfigured' in str(e):
            print("❌ YouTube Data API v3 не включен для этого ключа")
            print("   Перейдите: https://console.cloud.google.com/apis/library")
            print("   Найдите 'YouTube Data API v3' и нажмите 'Enable'")
        else:
            print(f"❌ Доступ запрещен: {error_reason}")
    else:
        print(f"❌ Ошибка API: {e.resp.status} - {error_reason}")
    
    print("")
    print("📖 Инструкция по получению ключа: HOW_TO_GET_API_KEY.md")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Неожиданная ошибка: {str(e)}")
    sys.exit(1)
EOF

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "================================"
    echo "✅ Проверка успешно завершена!"
    echo "================================"
else
    echo "================================"
    echo "❌ Проверка не пройдена"
    echo "================================"
    echo ""
    echo "📖 Подробная инструкция: HOW_TO_GET_API_KEY.md"
    echo "🌐 Получить ключ: https://console.cloud.google.com/"
fi

exit $exit_code
