from django.core.management.base import BaseCommand

from habits.models import Profile


class Command(BaseCommand):
    help = 'Привязка chat_id к пользователю'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя')
        parser.add_argument('chat_id', type=str, help='Telegram chat_id')

    def handle(self, *args, **options):
        email = options['email']
        chat_id = options['chat_id']

        try:
            profile = Profile.objects.get(user__email=email)
            profile.telegram_chat_id = chat_id
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Chat_id {chat_id} привязан к {email}'))
        except Profile.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Пользователь с email {email} не найден'))
