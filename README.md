# YouTube Viewer - Flask приложение

Удобное веб-приложение для поиска и просмотра видео с YouTube через официальный API.

## 🚀 Быстрый старт

### 1. Получите YouTube API ключ
Следуйте инструкциям в файле [API_KEY_SETUP.md](API_KEY_SETUP.md)

### 2. Запустите приложение

```bash
# Простой способ
./run.sh

# Или вручную
export YOUTUBE_API_KEY="ваш_api_ключ"
python app.py
```

Откройте http://localhost:5000 в браузере

## ✨ Возможности

- 🔍 Поиск видео на YouTube
- ▶️ Встроенный плеер для просмотра
- 📊 Статистика: просмотры, лайки, комментарии
- 📱 Адаптивный дизайн

## 📁 Структура проекта

```
.
├── app.py              # Основное Flask-приложение
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
├── run.sh             # Скрипт запуска
├── static/
│   └── style.css      # Стили
└── templates/         # HTML шаблоны
    ├── base.html
    ├── index.html
    ├── results.html
    ├── video.html
    └── error.html
```

## 📖 Документация

- [API_KEY_SETUP.md](API_KEY_SETUP.md) - Настройка YouTube API
- [README_YOUTUBE.md](README_YOUTUBE.md) - Подробная документация

## ⚠️ Важно

- Требуется YouTube API ключ
- Лимит: ~10,000 запросов в день (бесплатно)
- Только для легального использования
- Не скачивайте видео

## 🔧 Технологии

- Flask 3.0.0
- YouTube Data API v3
- Bootstrap 5.3
- Font Awesome 6.4

