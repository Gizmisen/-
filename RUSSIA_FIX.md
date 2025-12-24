# 🇷🇺 ИНСТРУКЦИЯ ДЛЯ ЗАПУСКА ИЗ РОССИИ

## ❌ Если сайт не открывается

### Шаг 1: Проверяем, запущено ли приложение
```bash
# Убиваем старые процессы
pkill -9 -f "python.*app.py"

# Устанавливаем зависимости
pip install -q flask google-api-python-client python-dotenv yt-dlp

# Запускаем приложение
python3 app.py
```

### Шаг 2: Открываем в браузере
```
http://localhost:5000
```

## ❌ Если выдаёт "YOUTUBE_API_KEY не установлен"

### Вариант 1: Через config.py (РЕКОМЕНДУЕТСЯ)

Отредактируйте файл `config.py`:
```python
class Config:
    YOUTUBE_API_KEY = 'AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'
```

### Вариант 2: Через переменную окружения

**Для Linux/Mac:**
```bash
export YOUTUBE_API_KEY='AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'
python3 app.py
```

**Для Windows (PowerShell):**
```powershell
$env:YOUTUBE_API_KEY='AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'
python app.py
```

**Для Windows (CMD):**
```cmd
set YOUTUBE_API_KEY=AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc
python app.py
```

## ✅ Проверяем что всё работает

### Способ 1: Через браузер
Откройте: `http://localhost:5000/status`

Должно показать:
```json
{
  "app_running": true,
  "youtube_api": true,
  "yt_dlp_available": true,
  "version": "2.0-russia-bypass"
}
```

### Способ 2: Тестируем поиск
```bash
curl "http://localhost:5000/api/search?q=тест&max=3"
```

### Способ 3: Тестируем видео
```bash
curl "http://localhost:5000/api/video/dQw4w9WgXcQ"
```

## 🚀 Быстрый запуск (проверенный способ)

### Linux/Mac:
```bash
bash run_safe.sh
```

### Windows:
```cmd
python app.py
```

## 🔧 Если всё ещё не работает

### Проверьте порт
Может быть, порт 5000 уже занят:
```bash
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### Если занят, измените порт
```bash
# Запуск на порт 8000
PORT=8000 python3 app.py
```

### Проверьте логи
```bash
tail -50 app.log
```

### Переустановите зависимости
```bash
pip install --upgrade flask google-api-python-client python-dotenv yt-dlp
```

## 📱 Если нужно открыть с другого компьютера

### Linux/Mac - запуск на всех интерфейсах:
```bash
python3 app.py
```
Потом откройте: `http://ВАШ_IP:5000` (замените ВАШ_IP на IP вашего компьютера)

### Узнать свой IP:
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

## 🎯 Типичные проблемы и решения

| Проблема | Решение |
|----------|---------|
| "Порт 5000 занят" | `PORT=8000 python3 app.py` |
| "ModuleNotFoundError" | `pip install -r requirements.txt` |
| "YOUTUBE_API_KEY not found" | Отредактируйте config.py |
| "Video not available" | Это нормально для блокированных видео - работает fallback система |
| "Очень медленно загружается" | yt-dlp может искать URL до 20 сек - это норма |

## ✨ Что работает в системе обхода

1. **User-Agent rotation** - попытка с разными браузерами
2. **Alternative clients** - попытка через разные YouTube API
3. **HTML5 fallback** - встроенный плеер YouTube
4. **Graceful degradation** - даже если всё заблокировано, видно видео информацию

## 💡 Pro tips для России

Если даже обход не помогает, попробуйте:
- **Перезагрузить браузер** (очистить кэш)
- **Использовать другой браузер** (Chrome, Firefox, Safari)
- **Обновить yt-dlp**: `pip install --upgrade yt-dlp`
- **Проверить VPN** (если используется)

---

**Если ничего не помогает - обратитесь с логом ошибки из `app.log`**
