# 🚀 Быстрый старт - YouTube Viewer

## 1️⃣ Получите YouTube API ключ (5 минут)

### Кратко:
1. Откройте: **https://console.cloud.google.com/**
2. Создайте проект
3. Включите **YouTube Data API v3** в Library
4. Создайте **API Key** в Credentials
5. Скопируйте ключ

📖 **Подробная инструкция**: [HOW_TO_GET_API_KEY.md](HOW_TO_GET_API_KEY.md)

---

## 2️⃣ Установите API ключ

```bash
export YOUTUBE_API_KEY="ваш_api_ключ_здесь"
```

Или создайте файл `.env`:
```bash
echo "YOUTUBE_API_KEY=ваш_ключ" > .env
```

---

## 3️⃣ Проверьте ключ (опционально)

```bash
./check_api_key.sh
```

Этот скрипт проверит:
- ✅ Установлен ли ключ
- ✅ Работает ли ключ
- ✅ Включен ли YouTube API
- ✅ Есть ли доступ

---

## 4️⃣ Запустите приложение

```bash
python app.py
```

Откройте браузер: **http://localhost:5000**

---

## 🎯 Что вы получите:

- 🔍 **Поиск видео** - находите любые видео на YouTube
- ▶️ **Просмотр** - встроенный YouTube плеер
- 📊 **Статистика** - просмотры, лайки, комментарии
- 📱 **Адаптивный дизайн** - работает на всех устройствах

---

## ❓ Проблемы?

### Ключ не работает
```bash
./check_api_key.sh  # Диагностика проблемы
```

### "Access Not Configured"
- YouTube Data API v3 не включен
- Зайдите: https://console.cloud.google.com/apis/library
- Найдите и включите "YouTube Data API v3"

### "Quota exceeded"
- Превышен дневной лимит (10,000 единиц)
- Подождите до следующего дня

---

## 📚 Документация

- [HOW_TO_GET_API_KEY.md](HOW_TO_GET_API_KEY.md) - Как получить API ключ
- [README_YOUTUBE.md](README_YOUTUBE.md) - Полное описание проекта
- [API_KEY_SETUP.md](API_KEY_SETUP.md) - Настройка ключа

---

## 🆘 Нужна помощь?

1. Проверьте скриптом: `./check_api_key.sh`
2. Прочитайте: [HOW_TO_GET_API_KEY.md](HOW_TO_GET_API_KEY.md)
3. Посмотрите логи: `tail -f app.log`

**Все работает легально через официальный YouTube API!** 🎉
