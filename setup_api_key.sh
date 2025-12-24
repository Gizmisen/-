#!/bin/bash

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       🔑 УСТАНОВКА YOUTUBE API КЛЮЧА                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "БЫСТРЫЙ СПОСОБ (30 СЕКУНД):"
echo "─────────────────────────────────────────────────────────────"
echo ""
echo "1️⃣ Откройте эту ссылку в браузере:"
echo ""
echo "   https://console.cloud.google.com/apis/library/youtube.googleapis.com"
echo ""
echo "2️⃣ Нажмите кнопку 'ENABLE'"
echo ""
echo "3️⃣ Перейдите в Credentials (слева) и нажмите '+ CREATE CREDENTIALS'"
echo ""
echo "4️⃣ Выберите 'API key' - скопируйте ключ"
echo ""
echo "─────────────────────────────────────────────────────────────"
echo ""

read -p "📝 Введите полученный API ключ: " api_key

if [ -z "$api_key" ]; then
    echo "❌ Ошибка: ключ не введен"
    exit 1
fi

echo ""
echo "💾 Выберите как сохранить ключ:"
echo "1) В переменной окружения (временно)"
echo "2) В файле .env (рекомендуется)"
echo ""
read -p "Выбор (1 или 2): " choice

if [ "$choice" = "1" ]; then
    export YOUTUBE_API_KEY="$api_key"
    echo "✅ Ключ установлен! Запустите приложение:"
    echo "   python app.py"
elif [ "$choice" = "2" ]; then
    echo "YOUTUBE_API_KEY=$api_key" > .env
    export YOUTUBE_API_KEY="$api_key"
    echo "✅ Ключ сохранен в .env и установлен в переменную окружения"
    echo "   Запустите приложение:"
    echo "   python app.py"
else
    echo "❌ Неверный выбор"
    exit 1
fi

echo ""
