#!/bin/bash

# Скрипт для быстрого запуска YouTube Viewer

echo "🚀 Запуск YouTube Viewer..."
echo ""

# Проверка наличия API ключа
if [ -z "$YOUTUBE_API_KEY" ] && [ ! -f .env ]; then
    echo "⚠️  ВНИМАНИЕ: YouTube API ключ не найден!"
    echo ""
    echo "📝 Установите ключ одним из способов:"
    echo "   1. export YOUTUBE_API_KEY='ваш_ключ'"
    echo "   2. Создайте файл .env с содержимым: YOUTUBE_API_KEY=ваш_ключ"
    echo "   3. Измените config.py напрямую"
    echo ""
    echo "📖 Подробнее: см. API_KEY_SETUP.md"
    echo ""
    read -p "Продолжить запуск без ключа? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Проверка зависимостей
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Установка зависимостей..."
    pip install -r requirements.txt
    echo ""
fi

# Запуск приложения
echo "✅ Запуск приложения на http://localhost:5000"
echo "Press CTRL+C to quit"
echo ""

python app.py
