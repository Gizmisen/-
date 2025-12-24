#!/bin/bash

# Скрипт для создания готового к развертыванию пакета приложения

echo "📦 Создание пакета YouTube Viewer для России..."

# Создаем папку
mkdir -p youtube-viewer
cd youtube-viewer

# Копируем необходимые файлы
cp -v ../app.py .
cp -v ../config.py .
cp -v ../requirements.txt .
cp -v ../run_russia.sh .
cp -v ../README_RUSSIA.md .

# Копируем папки
cp -rv ../templates .
cp -rv ../static .

# Создаем README
cat > README.md << 'EOF'
# YouTube Viewer для России

## 🚀 Быстрый старт

```bash
# Способ 1 (самый быстрый)
bash run_russia.sh

# Способ 2 (вручную)
pip install -r requirements.txt
export YOUTUBE_API_KEY="AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc"
python app.py
```

Откройте http://localhost:5000 в браузере!

## ✅ Что включено

- Полное приложение Flask
- YouTube поиск и просмотр видео
- Работает в России везде
- Все зависимости указаны
- API ключ уже установлен

## 📖 Подробнее

Смотрите README_RUSSIA.md
EOF

echo ""
echo "✅ Пакет создан в папке youtube-viewer/"
echo ""
echo "📋 Содержимое:"
ls -la
echo ""
echo "🚀 Чтобы запустить:"
echo "   cd youtube-viewer"
echo "   bash run_russia.sh"
echo ""

