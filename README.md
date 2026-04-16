# Habit Tracker

Бэкенд-часть SPA веб-приложения для трекера полезных привычек с Telegram-уведомлениями.

## Технологии

- Python 3.13
- Django + DRF
- PostgreSQL (SQLite для разработки)
- Celery + Redis
- Telegram Bot API
- Docker (опционально)

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone git@github.com:ТВОЙ_НИК/habit-tracker.git
cd habit-tracker
2. Установить зависимости
bash
poetry install
3. Настроить переменные окружения
Скопировать .env.example в .env и заполнить:

bash
cp .env.example .env
4. Выполнить миграции
bash
poetry run python manage.py migrate
5. Создать суперпользователя
bash
poetry run python manage.py createsuperuser
6. Запустить сервер
bash
poetry run python manage.py runserver 8080
7. Запустить Redis и Celery
bash
redis-server
poetry run celery -A config worker -l info --pool=solo
poetry run celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
8. Запустить Telegram бота
bash
poetry run python manage.py bot
Эндпоинты API
GET /api/habits/ — список привычек пользователя (пагинация 5)

GET /api/public/ — список публичных привычек

POST /api/habits/ — создание привычки

PUT /api/habits/{id}/ — редактирование

DELETE /api/habits/{id}/ — удаление

Тесты
bash
poetry run pytest --cov=habits
/