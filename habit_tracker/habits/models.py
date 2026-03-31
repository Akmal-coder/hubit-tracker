from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (дней)'
    )
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вознаграждение')
    duration = models.PositiveSmallIntegerField(verbose_name='Время на выполнение (сек)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']

    def __str__(self):
        return f"{self.user} - {self.action} в {self.time}"

    def clean(self):
        # 1. Нельзя одновременно заполнять reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя одновременно указывать вознаграждение и связанную привычку')

        # 2. Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError('Время выполнения не должно превышать 120 секунд')

        # 3. В связанные привычки могут попадать только привычки с is_pleasant = True
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной')

        # 4. У приятной привычки не может быть reward или related_habit
        if self.is_pleasant:
            if self.reward:
                raise ValidationError('У приятной привычки не может быть вознаграждения')
            if self.related_habit:
                raise ValidationError('У приятной привычки не может быть связанной привычки')

        # 5. Периодичность не реже 1 раза в 7 дней (1-7 дней)
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError('Периодичность должна быть от 1 до 7 дней')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    telegram_chat_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Telegram chat ID'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль {self.user.username}"


# Сигналы для автоматического создания профиля
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
