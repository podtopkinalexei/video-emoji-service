# Video Emoji Service

Сервис для добавления эмодзи в центр видео. Доступен через веб-интерфейс и Telegram бота.

## Функциональность

- Загрузка видео через веб-интерфейс
- Добавление эмодзи "😊" по центру видео
- Просмотр и скачивание результата
- Обработка видео через Telegram бота

## Технологии

- **Backend**: FastAPI, FFmpeg, Python
- **Frontend**: Vue.js, Vite
- **Telegram Bot**: python-telegram-bot
- **Infrastructure**: Docker, Docker Compose, Nginx

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd video-emoji-service
```

2. Настройте переменные окружения:
```bash
cp .env.example .env
```
Отредактируйте `.env` файл, добавив ваш Telegram Bot Token.

3. Запустите проект:
```bash
docker compose up -d
```

4. Откройте в браузере: http://localhost

## Использование

### Веб-интерфейс
1. Перейдите на http://localhost
2. Загрузите MP4 видеофайл
3. Нажмите "Добавить 😊"
4. Просмотрите и скачайте результат

### Telegram бот
1. Найдите бота в Telegram
2. Отправьте видеофайл
3. Получите обработанное видео с эмодзи

## Лицензия
MIT