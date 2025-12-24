# 🚀 БЫСТРЫЙ СТАРТ ДЛЯ ДРУГА ИЗ РОССИИ

## Если сайт совсем не открывается

### Шаг 1: Запустить приложение

**Linux/Mac:**
```bash
bash start.sh
```

**Windows (PowerShell):**
```powershell
python app.py
```

**Windows (CMD):**
```cmd
python app.py
```

### Шаг 2: Открыть браузер

```
http://localhost:5000
```

---

## Если выдаёт ошибку

### ❌ "ModuleNotFoundError: No module named..."

Установите зависимости:
```bash
pip install -r requirements.txt
```

### ❌ "YOUTUBE_API_KEY not found"

Отредактируйте `config.py`:
```python
class Config:
    YOUTUBE_API_KEY = 'AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'
```

Или установите переменную окружения:
```bash
export YOUTUBE_API_KEY='AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'
bash start.sh
```

### ❌ "Порт 5000 занят"

```bash
PORT=8000 python3 app.py
```

Откройте: `http://localhost:8000`

---

## Проверка что всё работает

### Способ 1: Через браузер
```
http://localhost:5000/status
```

Должно показать:
```json
{
  "app_running": true,
  "youtube_api": true,
  "yt_dlp_available": true
}
```

### Способ 2: Тестовый поиск
```bash
curl "http://localhost:5000/api/search?q=тест&max=3"
```

### Способ 3: Диагностика
```bash
bash diagnose.sh
```

---

## 🎯 Чит-коды для быстрого запуска

| Ситуация | Команда |
|----------|---------|
| Обычный запуск | `bash start.sh` |
| Безопасный запуск | `bash run_safe.sh` |
| Диагностика | `bash diagnose.sh` |
| Запуск на другом порту | `PORT=8000 python3 app.py` |
| Запуск с логами | `python3 app.py` |

---

## 💡 Если всё ещё не работает

1. **Проверьте логи:**
   ```bash
   tail -50 app.log
   ```

2. **Переустановите всё с нуля:**
   ```bash
   pip install --upgrade flask google-api-python-client python-dotenv yt-dlp
   python3 app.py
   ```

3. **Проверьте Python версию:**
   ```bash
   python3 --version  # должна быть 3.7+
   ```

4. **Убедитесь что нет старых процессов:**
   ```bash
   # Linux/Mac
   pkill -f "python.*app.py"
   
   # Windows
   taskkill /im python.exe /f
   ```

---

## ✨ Что уже реализовано в коде

✅ Поиск видео по запросу  
✅ Просмотр видео (YouTube Player API)  
✅ Информация о видео (просмотры, лайки, комментарии)  
✅ **4-метод обход блокировки для России**  
✅ HTML5 fallback плеер  
✅ Мобильная версия  
✅ Обработка ошибок  
✅ API для разработчиков  

---

## 📞 Нужна помощь?

1. Запустите диагностику: `bash diagnose.sh`
2. Проверьте логи: `tail app.log`
3. Убедитесь что установлены зависимости: `pip install -r requirements.txt`
4. Проверьте что есть API ключ в `config.py`

**ВСЁ РЕШАЕМО! 🎉**
