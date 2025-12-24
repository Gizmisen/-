#!/bin/bash

# 🚀 БЕЗОПАСНЫЙ ЗАПУСК ДЛЯ РОССИИ
# Убивает старые процессы, проверяет зависимости, запускает приложение

echo "🔧 Подготовка к запуску..."

# 1️⃣ Убиваем старые процессы
pkill -9 -f "python.*app.py" 2>/dev/null
sleep 1

# 2️⃣ Проверяем зависимости
echo "📦 Проверка зависимостей..."
pip install -q flask google-api-python-client python-dotenv yt-dlp 2>/dev/null

# 3️⃣ Проверяем API ключ
if [ -z "$YOUTUBE_API_KEY" ]; then
    echo "❌ YOUTUBE_API_KEY не установлен!"
    echo "📌 Добавьте в config.py или установите переменную:"
    echo "   export YOUTUBE_API_KEY='ваш_ключ'"
    exit 1
fi

# 4️⃣ Проверяем наличие файлов
if [ ! -f "app.py" ]; then
    echo "❌ app.py не найден!"
    exit 1
fi

if [ ! -d "templates" ]; then
    echo "❌ Папка templates не найдена!"
    exit 1
fi

# 5️⃣ Очищаем порт
echo "🧹 Очистка порта 5000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null
sleep 2

# 6️⃣ Запускаем приложение
echo ""
echo "✅ Всё готово! Запускаю приложение..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")"

# Запускаем с выводом ошибок
python3 app.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "❌ Приложение остановлено"
