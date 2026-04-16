# Habit Tracker

Бэкенд-часть SPA веб-приложения для трекера полезных привычек с Telegram-уведомлениями.

## Ссылка на сервер
http://89.169.162.73

## Технологии

- Python 3.13
- Django + DRF + JWT
- PostgreSQL + Redis
- Celery + Celery Beat
- Telegram Bot API
- Docker + Docker Compose
- GitHub Actions (CI/CD)

## Локальный запуск

Клонировать репозиторий
git clone https://github.com/Akmal-coder/hubit-tracker.git
cd hubit-tracker

## Создать .env файл
bash
cp .env.example .env
Заполнить переменные (SECRET_KEY, DB_*, TELEGRAM_BOT_TOKEN)

## Запустить через Docker Compose
bash
docker-compose up -d --build

## API эндпоинты
Метод	    Эндпоинт	            Описание
POST	    /api/register/	        Регистрация пользователя
POST	    /api/login/	            Авторизация (JWT токен)
GET	        /api/habits/	        Список привычек (пагинация 5)
POST	    /api/habits/	        Создание привычки
PUT        /DELETE/api/habits/{id}/	Редактирование/удаление
GET	        /api/public/	        Публичные привычки


## Настройка CI/CD
В GitHub Secrets необходимо добавить:

Secret:	                Описание:
SSH_PRIVATE_KEY	        Приватный SSH-ключ для доступа к серверу
SERVER_IP	            IP адрес сервера
SERVER_USER	            Имя пользователя на сервере


**Скопируй, замени содержимое `README.md`, затем:**

git add README.md
git commit -m "Update README: add server URL and CI/CD instructions"
git push origin feature/final_task