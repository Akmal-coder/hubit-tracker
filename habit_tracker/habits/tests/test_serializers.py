import pytest
from django.contrib.auth import get_user_model

from habits.models import Habit
from habits.serializers import HabitSerializer

User = get_user_model()


@pytest.mark.django_db
class TestHabitSerializer:

    def test_serializer_valid_data(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='12345')
        data = {
            'user': user.id,
            'place': 'Спортзал',
            'time': '09:00:00',
            'action': 'Тренировка',
            'duration': 90,
            'periodicity': 1
        }
        serializer = HabitSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_invalid_duration(self):
        user = User.objects.create_user(username='testuser2', email='test2@test.com', password='12345')
        data = {
            'user': user.id,
            'place': 'Спортзал',
            'time': '09:00:00',
            'action': 'Тренировка',
            'duration': 121,
            'periodicity': 1
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Время выполнения не должно превышать 120 секунд' in str(serializer.errors)

    def test_serializer_invalid_periodicity(self):
        user = User.objects.create_user(username='testuser3', email='test3@test.com', password='12345')
        data = {
            'user': user.id,
            'place': 'Спортзал',
            'time': '09:00:00',
            'action': 'Тренировка',
            'duration': 60,
            'periodicity': 8
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()

    def test_serializer_reward_and_related_together(self):
        user = User.objects.create_user(username='testuser4', email='test4@test.com', password='12345')
        pleasant = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Приятная',
            duration=60,
            periodicity=1,
            is_pleasant=True
        )
        data = {
            'user': user.id,
            'place': 'Спортзал',
            'time': '09:00:00',
            'action': 'Тренировка',
            'duration': 60,
            'periodicity': 1,
            'reward': 'Награда',
            'related_habit': pleasant.id
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()

    def test_serializer_pleasant_habit_cannot_have_reward(self):
        user = User.objects.create_user(username='testuser5', email='test5@test.com', password='12345')
        data = {
            'user': user.id,
            'place': 'Дом',
            'time': '10:00:00',
            'action': 'Приятная привычка',
            'duration': 60,
            'periodicity': 1,
            'is_pleasant': True,
            'reward': 'Награда'
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()
        assert 'приятной привычки не может быть вознаграждения' in str(serializer.errors)

    def test_serializer_related_habit_not_pleasant(self):
        user = User.objects.create_user(username='testuser6', email='test6@test.com', password='12345')
        not_pleasant = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Не приятная привычка',
            duration=60,
            periodicity=1,
            is_pleasant=False
        )
        data = {
            'user': user.id,
            'place': 'Спортзал',
            'time': '09:00:00',
            'action': 'Полезная привычка',
            'duration': 60,
            'periodicity': 1,
            'related_habit': not_pleasant.id
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Связанная привычка должна быть приятной' in str(serializer.errors)