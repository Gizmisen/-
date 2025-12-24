# YouTube Viewer - Flask приложение для просмотра YouTube видео

Это Flask-приложение позволяет искать и смотреть видео с YouTube через официальный API.

## 🚀 Быстрый старт

### 1. Получите YouTube API ключ

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите **YouTube Data API v3**:
   - Перейдите в "APIs & Services" → "Library"
   - Найдите "YouTube Data API v3"
   - Нажмите "Enable"
4. Создайте учетные данные (API ключ):
   - Перейдите в "APIs & Services" → "Credentials"
   - Нажмите "Create Credentials" → "API Key"
   - Скопируйте созданный ключ

### 2. Настройте приложение

Установите YouTube API ключ одним из способов:

**Способ 1: Переменная окружения (рекомендуется)**
```bash
export YOUTUBE_API_KEY="ваш_api_ключ_здесь"
```

**Способ 2: Файл .env**
```bash
echo "YOUTUBE_API_KEY=ваш_api_ключ_здесь" > .env
echo "SECRET_KEY=ваш_секретный_ключ" >> .env
```

**Способ 3: Прямая замена в config.py**
Откройте `config.py` и замените `YOUR_YOUTUBE_API_KEY` на ваш ключ.

### 3. Запустите приложение

```bash
# Убедитесь, что зависимости установлены
pip install -r requirements.txt

# Запустите приложение
python app.py
```

Приложение запустится на `http://localhost:5000`

## 📁 Структура проекта

```
youtube_viewer_flask/
├── app.py                 # Основное Flask-приложение
├── config.py              # Конфигурация и API-ключ
├── requirements.txt       # Зависимости Python
├── README_YOUTUBE.md      # Эта инструкция
├── static/
│   └── style.css          # CSS стили
└── templates/
    ├── base.html          # Базовый шаблон
    ├── index.html         # Главная страница
    ├── results.html       # Результаты поиска
    ├── video.html         # Страница просмотра видео
    └── error.html         # Страница ошибок
```

## ✨ Возможности

- 🔍 **Поиск видео** - Ищите любые видео на YouTube
- ▶️ **Просмотр** - Встроенный YouTube плеер
- 📊 **Статистика** - Количество просмотров, лайков, комментариев
- 📱 **Адаптивный дизайн** - Работает на всех устройствах
- 🎨 **Современный UI** - Чистый и понятный интерфейс

## 🔧 API Endpoints

### Web Routes
- `GET /` - Главная страница
- `GET /search?q=запрос` - Страница результатов поиска
- `GET /video/<video_id>` - Страница просмотра видео

### JSON API
- `GET /api/search?q=запрос&max=10` - JSON поиск видео
- `GET /api/video/<video_id>` - JSON информация о видео

## ⚠️ Важные ограничения

1. **API квоты**: Бесплатный тариф YouTube API имеет лимит ~10,000 запросов в день
2. **Легальность**: Используйте только в образовательных целях
3. **Авторские права**: Не скачивайте видео - это нарушает условия YouTube
4. **Только просмотр**: Это приложение только для просмотра через официальный плеер

## 🐛 Решение проблем

### Ошибка "API key not valid"
- Убедитесь, что YouTube Data API v3 включен в Google Cloud Console
- Проверьте, что API ключ правильно установлен в переменных окружения

### Ошибка "Quota exceeded"
- Вы превысили дневной лимит запросов API
- Подождите до следующего дня или увеличьте квоту в Google Cloud Console

### Видео не загружаются
- Проверьте интернет-соединение
- Убедитесь, что видео доступно в вашей стране
- Проверьте логи приложения

## 📝 Лицензия

Этот проект предназначен только для образовательных целей. Соблюдайте условия использования YouTube API.

## 🔗 Полезные ссылки

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
