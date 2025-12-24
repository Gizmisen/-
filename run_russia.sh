#!/bin/bash

# 🚀 YouTube Viewer для России - Быстрый запуск

echo "=========================================="
echo "   🎬 YouTube Viewer - Запуск в России"
echo "=========================================="
echo ""

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен"
    echo "   Установите Python 3.8+ и попробуйте снова"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Проверяем требуемые файлы
if [ ! -f "config.py" ]; then
    echo "❌ Ошибка: config.py не найден"
    exit 1
fi

if [ ! -f "app.py" ]; then
    echo "❌ Ошибка: app.py не найден"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"
echo ""

# Устанавливаем зависимости если нужно
echo "📦 Проверяем зависимости..."
pip install -q -r requirements.txt 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Зависимости установлены"
else
    echo "⚠️  Ошибка при установке зависимостей, но пытаемся запустить..."
fi

echo ""
echo "=========================================="
echo "   🎬 Запуск YouTube Viewer"
echo "=========================================="
echo ""

# Запускаем приложение
export YOUTUBE_API_KEY="AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc"

echo "🌐 Приложение запускается на:"
echo "   • http://localhost:5000"
echo "   • http://127.0.0.1:5000"
echo ""
echo "💡 Откройте ссылку в браузере и ищите видео!"
echo "📝 Для остановки нажмите Ctrl+C"
echo ""
echo "=========================================="
echo ""

python3 app.py

