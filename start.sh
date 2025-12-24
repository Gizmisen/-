#!/bin/bash

# 🇷🇺 СУПЕР-ПРОСТОЙ ЗАПУСК YOUTUBE VIEWER
# Для друга из России который говорит "не работает"

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║  🎬 YOUTUBE VIEWER - ЗАПУСК ДЛЯ РОССИИ     ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1️⃣  Убиваем старые процессы
echo "🧹 Очистка..."
pkill -9 -f "python.*app.py" 2>/dev/null
sleep 1

# 2️⃣  Проверяем зависимости
echo "📦 Установка зависимостей..."
pip install -q flask google-api-python-client python-dotenv yt-dlp requests 2>/dev/null

# 3️⃣  Проверяем файлы
if [ ! -f "app.py" ] || [ ! -d "templates" ]; then
    echo -e "${RED}❌ ОШИБКА: app.py или папка templates не найдены!${NC}"
    echo "📌 Убедитесь, что файлы в папке с приложением"
    exit 1
fi

# 4️⃣  Проверяем API ключ
if ! grep -q "YOUTUBE_API_KEY = 'AIzaSy" config.py 2>/dev/null && [[ -z "$YOUTUBE_API_KEY" ]]; then
    echo -e "${YELLOW}⚠️  YOUTUBE_API_KEY не найден${NC}"
    echo ""
    echo "📌 РЕШЕНИЕ: Отредактируйте config.py и добавьте:"
    echo ""
    echo "class Config:"
    echo "    YOUTUBE_API_KEY = 'AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'"
    echo ""
    echo "Или установите переменную:"
    echo "export YOUTUBE_API_KEY='AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'"
    echo ""
    read -p "Нажмите Enter если готовы..."
fi

# 5️⃣  Очищаем порт
echo "🧹 Очистка порта 5000..."
if command -v lsof &> /dev/null; then
    lsof -ti:5000 | xargs kill -9 2>/dev/null
elif command -v netstat &> /dev/null; then
    netstat -tuln 2>/dev/null | grep ":5000" | awk '{print $NF}' | cut -d'/' -f1 | xargs kill -9 2>/dev/null
fi
sleep 2

# 6️⃣  Запускаем приложение
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅ ЗАПУСК ПРИЛОЖЕНИЯ${NC}"
echo ""
echo "📱 Откройте в браузере:"
echo ""
echo -e "  ${GREEN}http://localhost:5000${NC}"
echo ""
echo "🔍 Проверка статуса:"
echo ""
echo -e "  ${GREEN}http://localhost:5000/status${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Запускаем с выводом ошибок (не в фоне, чтобы видны были любые проблемы)
export FLASK_APP=app.py
export FLASK_ENV=development

python3 app.py

# Если приложение упало - показываем помощь
echo ""
echo -e "${RED}❌ ПРИЛОЖЕНИЕ УПАЛО${NC}"
echo ""
echo "📋 Проверьте:"
echo "  1. Есть ли YOUTUBE_API_KEY в config.py?"
echo "  2. Установлены ли зависимости? (pip install -r requirements.txt)"
echo "  3. Смотрите логи: tail -50 app.log"
echo ""
