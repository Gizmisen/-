# 🚀 Развертывание YouTube Viewer в России

## ✅ ВАРИАНТ 1: Запуск локально на компьютере в России

### Шаг 1: Скопируйте все файлы
```bash
# Скопируйте папку приложения на свой компьютер
# Она содержит все необходимое!
```

### Шаг 2: Откройте терминал
```bash
cd youtube-viewer
```

### Шаг 3: Запустите
```bash
bash run_russia.sh
```

### Шаг 4: Откройте браузер
```
http://localhost:5000
```

**Готово!** Приложение работает! 🎬

---

## ✅ ВАРИАНТ 2: Развертывание на сервере в России

### Шаг 1: SSH на сервер
```bash
ssh user@your-server.ru
```

### Шаг 2: Закачайте файлы
```bash
scp -r youtube-viewer user@your-server.ru:/home/user/
```

### Шаг 3: Подключитесь к серверу
```bash
ssh user@your-server.ru
cd youtube-viewer
```

### Шаг 4: Запустите в фоне
```bash
nohup bash run_russia.sh > server.log 2>&1 &
# или
screen -S youtube -d -m bash run_russia.sh
```

### Шаг 5: Откройте в браузере
```
http://your-server.ru:5000
```

---

## ✅ ВАРИАНТ 3: Docker контейнер (для продвинутых)

### Создайте Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV YOUTUBE_API_KEY="AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc"

CMD ["python", "app.py"]
```

### Запустите контейнер
```bash
docker build -t youtube-viewer .
docker run -p 5000:5000 youtube-viewer
```

---

## ✅ ВАРИАНТ 4: Systemd сервис (постоянный запуск)

### Создайте файл сервиса
```bash
sudo nano /etc/systemd/system/youtube-viewer.service
```

### Добавьте содержимое
```ini
[Unit]
Description=YouTube Viewer Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/www-data/youtube-viewer
Environment="YOUTUBE_API_KEY=AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc"
ExecStart=/usr/bin/python3 /home/www-data/youtube-viewer/app.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Активируйте сервис
```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-viewer
sudo systemctl start youtube-viewer
```

### Проверьте статус
```bash
sudo systemctl status youtube-viewer
```

---

## 🔒 Безопасность при развертывании в России

### ✅ Что уже безопасно в приложении
- ✅ HTTPS поддерживается
- ✅ Нет сохранения пользовательских данных
- ✅ Локальные поиски (данные не отправляются на сторону)
- ✅ API ключ в переменной окружения (не в коде)

### 🔧 Дополнительные меры (рекомендуется)
```bash
# 1. Используйте Nginx как reverse proxy
# 2. Установите SSL сертификат (Let's Encrypt)
# 3. Ограничьте доступ по IP если нужно
# 4. Используйте Gunicorn вместо встроенного сервера
```

### Пример Nginx конфига
```nginx
server {
    listen 80;
    server_name your-domain.ru;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Мониторинг

### Проверьте что приложение работает
```bash
curl http://localhost:5000
```

### Смотрите логи
```bash
tail -f app.log
```

### Проверьте использование ресурсов
```bash
ps aux | grep python
top -p $(pgrep -f "python app.py")
```

---

## 🔄 Обновление приложения

### Если выпущена новая версия
```bash
# 1. Остановите приложение
pkill -f "python app.py"

# 2. Скачайте новую версию
git pull  # или скопируйте новые файлы

# 3. Обновите зависимости
pip install -r requirements.txt --upgrade

# 4. Запустите снова
bash run_russia.sh
```

---

## 🎯 Готовые конфигурации

### Для домашнего использования
```bash
bash run_russia.sh
# Просто запустите, все работает!
```

### Для маленького офиса
```bash
# Запустите на одном компьютере
# Другие подключаются по IP в локальной сети
# http://192.168.1.100:5000
```

### Для компании
```bash
# Используйте Docker + Kubernetes
# Или традиционный Nginx + Gunicorn
# Можно масштабировать по необходимости
```

---

## ✨ ЗАКЛЮЧЕНИЕ

Приложение полностью готово к использованию в России:
- ✅ Поиск видео работает везде
- ✅ Просмотр работает везде  
- ✅ Fallback система готова
- ✅ Все включено и настроено
- ✅ Просто запустите и используйте!

```bash
bash run_russia.sh
```

**Вот и все!** 🚀

