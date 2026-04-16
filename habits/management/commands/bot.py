import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from habits.models import Profile

User = get_user_model()
TOKEN = settings.TELEGRAM_BOT_TOKEN
URL = f"https://api.telegram.org/bot{TOKEN}"


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def send_message(self, chat_id, text):
        """Отправка сообщения в Telegram"""
        try:
            requests.post(f"{URL}/sendMessage", json={'chat_id': chat_id, 'text': text})
        except Exception as e:
            self.stdout.write(f'Ошибка отправки: {e}')

    def handle(self, *args, **options):
        self.stdout.write('Бот запущен...')
        last_update_id = 0

        while True:
            try:
                response = requests.get(f"{URL}/getUpdates", params={'offset': last_update_id + 1, 'timeout': 30})
                data = response.json()

                if not data.get('ok'):
                    continue

                updates = data.get('result', [])

                for update in updates:
                    last_update_id = update['update_id']
                    self.process_update(update)

            except Exception as e:
                self.stdout.write(f'Ошибка: {e}')

    def process_update(self, update):
        message = update.get('message')
        if not message:
            return

        chat_id = message['chat']['id']
        text = message.get('text', '')

        # Проверяем, есть ли уже chat_id в профиле
        try:
            profile = Profile.objects.get(telegram_chat_id=str(chat_id))
            self.send_message(chat_id, f"Вы уже привязаны! Ваш email: {profile.user.email}")
            return
        except Profile.DoesNotExist:
            pass

        # Если пользователь ввел email (содержит @)
        if '@' in text and '.' in text:
            try:
                user = User.objects.get(email=text)
                profile = Profile.objects.get(user=user)
                profile.telegram_chat_id = str(chat_id)
                profile.save()
                self.send_message(chat_id,
                                  f"Успешно! Ваш email {text} привязан. Теперь вы будете получать напоминания о привычках.")
            except User.DoesNotExist:
                self.send_message(chat_id,
                                  "Пользователь с таким email не найден." 
                                       "Зарегистрируйтесь сначала в веб-приложении.")
            except Profile.DoesNotExist:
                self.send_message(chat_id, "Профиль не найден. Обратитесь к администратору.")
        else:
            # Просим ввести email
            self.send_message(chat_id, "Привет! Пожалуйста, введите ваш email, указанный при регистрации:")
