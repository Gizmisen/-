#!/bin/bash

echo ""
echo "🔍 ДИАГНОСТИКА YOUTUBE VIEWER"
echo "════════════════════════════════════════════"
echo ""

# 1. Проверяем Python
echo "1️⃣  Python:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python не установлен"
fi

# 2. Проверяем Flask
echo ""
echo "2️⃣  Flask:"
if python3 -c "import flask" 2>/dev/null; then
    FLASK_VERSION=$(python3 -c "import flask; print(flask.__version__)")
    echo "   ✅ Flask $FLASK_VERSION"
else
    echo "   ❌ Flask не установлен"
fi

# 3. Проверяем YouTube API
echo ""
echo "3️⃣  Google API:"
if python3 -c "import googleapiclient" 2>/dev/null; then
    echo "   ✅ google-api-python-client установлен"
else
    echo "   ❌ google-api-python-client не установлен"
fi

# 4. Проверяем yt-dlp
echo ""
echo "4️⃣  yt-dlp:"
if python3 -c "import yt_dlp" 2>/dev/null; then
    YTDLP_VERSION=$(python3 -c "import yt_dlp; print(yt_dlp.__version__)")
    echo "   ✅ yt-dlp $YTDLP_VERSION"
else
    echo "   ❌ yt-dlp не установлен"
fi

# 5. Проверяем файлы проекта
echo ""
echo "5️⃣  Файлы проекта:"
[[ -f app.py ]] && echo "   ✅ app.py" || echo "   ❌ app.py"
[[ -f config.py ]] && echo "   ✅ config.py" || echo "   ❌ config.py"
[[ -f requirements.txt ]] && echo "   ✅ requirements.txt" || echo "   ❌ requirements.txt"
[[ -d templates ]] && echo "   ✅ templates/" || echo "   ❌ templates/"
[[ -d static ]] && echo "   ✅ static/" || echo "   ❌ static/"

# 6. Проверяем API ключ
echo ""
echo "6️⃣  YouTube API ключ:"
if grep -q "YOUTUBE_API_KEY = 'AIzaSy" config.py 2>/dev/null; then
    echo "   ✅ Ключ найден в config.py"
elif [[ ! -z "$YOUTUBE_API_KEY" ]]; then
    echo "   ✅ Ключ установлен в переменной окружения"
else
    echo "   ❌ API ключ не найден"
    echo "      Решение: отредактируйте config.py"
fi

# 7. Проверяем порт
echo ""
echo "7️⃣  Порт 5000:"
if lsof -i :5000 2>/dev/null | grep -q LISTEN; then
    echo "   ✅ Приложение уже работает на порту 5000"
elif netstat -tuln 2>/dev/null | grep -q ":5000"; then
    echo "   ✅ Приложение уже работает на порту 5000"
else
    echo "   ℹ️  Порт 5000 свободен (приложение не запущено)"
fi

echo ""
echo "════════════════════════════════════════════"
echo "📋 РЕКОМЕНДАЦИИ:"
echo ""

# Проверяем что отсутствует
ISSUES=0

if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Установите зависимости: pip install -r requirements.txt"
    ISSUES=$((ISSUES+1))
fi

if ! grep -q "YOUTUBE_API_KEY = 'AIzaSy" config.py 2>/dev/null && [[ -z "$YOUTUBE_API_KEY" ]]; then
    echo "⚠️  Добавьте YOUTUBE_API_KEY в config.py"
    ISSUES=$((ISSUES+1))
fi

if [[ $ISSUES -eq 0 ]]; then
    echo "✅ Всё в порядке! Запустите: python3 app.py"
fi

echo ""
