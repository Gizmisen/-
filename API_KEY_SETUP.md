# ⚠️ ВАЖНО: Настройте YouTube API ключ перед использованием!

## Быстрая настройка API ключа

Приложение работает, но **требуется YouTube API ключ** для поиска и просмотра видео.

### Шаг 1: Получите API ключ

1. Откройте [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте проект
3. Включите **YouTube Data API v3**
4. Создайте **API Key**

### Шаг 2: Установите ключ

Выполните в терминале:

```bash
export YOUTUBE_API_KEY="ВАШ_API_КЛЮЧ_ЗДЕСЬ"
```

Или создайте файл `.env`:

```bash
echo "YOUTUBE_API_KEY=ваш_ключ" > .env
```

### Шаг 3: Перезапустите приложение

```bash
python app.py
```

---

Приложение доступно на: http://localhost:5000

📖 Полная инструкция в файле [README_YOUTUBE.md](README_YOUTUBE.md)
