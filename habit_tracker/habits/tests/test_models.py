import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from habits.models import Habit, Profile


User = get_user_model()


@pytest.mark.django_db
class TestHabitModel:

    def test_create_habit(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='12345')
        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            duration=60,
            periodicity=1
        )
        assert habit.action == 'Зарядка'
        assert habit.user == user

    def test_duration_validation(self):
        user = User.objects.create_user(username='testuser2', email='test2@test.com', password='12345')
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Бег',
            duration=121,
            periodicity=1
        )
        with pytest.raises(ValidationError):
            habit.full_clean()

    def test_periodicity_validation(self):
        user = User.objects.create_user(username='testuser3', email='test3@test.com', password='12345')
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Чтение',
            duration=60,
            periodicity=8
        )
        with pytest.raises(ValidationError):
            habit.full_clean()

    def test_reward_and_related_habit_cannot_together(self):
        user = User.objects.create_user(username='testuser5', email='test5@test.com', password='12345')
        pleasant = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Приятная',
            duration=60,
            periodicity=1,
            is_pleasant=True
        )
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Полезная',
            duration=60,
            periodicity=1,
            reward='Шоколадка',
            related_habit=pleasant
        )
        with pytest.raises(ValidationError):
            habit.full_clean()

    def test_related_habit_must_be_pleasant(self):
        user = User.objects.create_user(username='testuser6', email='test6@test.com', password='12345')
        not_pleasant = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Не приятная',
            duration=60,
            periodicity=1,
            is_pleasant=False
        )
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Полезная',
            duration=60,
            periodicity=1,
            related_habit=not_pleasant
        )
        with pytest.raises(ValidationError):
            habit.full_clean()


    def test_pleasant_habit_cannot_have_reward(self):
        user = User.objects.create_user(username='testuser7', email='test7@test.com', password='12345')
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Приятная',
            duration=60,
            periodicity=1,
            is_pleasant=True,
            reward='Награда'
        )
        with pytest.raises(ValidationError):
            habit.full_clean()

    def test_str_method(self):
        user = User.objects.create_user(username='testuser8', email='test8@test.com', password='12345')
        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Тестовая привычка',
            duration=60,
            periodicity=1
        )
        expected_str = f"{user} - Тестовая привычка в 08:00:00"
        assert str(habit) == expected_str

    def test_pleasant_habit_cannot_have_related(self):
        user = User.objects.create_user(username='testuser9', email='test9@test.com', password='12345')
        other_habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Другая',
            duration=60,
            periodicity=1
        )
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Приятная',
            duration=60,
            periodicity=1,
            is_pleasant=True,
            related_habit=other_habit
        )
        with pytest.raises(ValidationError):
            habit.full_clean()

    def test_save_triggers_full_clean(self):
        user = User.objects.create_user(username='testuser10', email='test10@test.com', password='12345')
        habit = Habit(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Неправильная',
            duration=121,
            periodicity=1
        )
        with pytest.raises(ValidationError):
            habit.save()


@pytest.mark.django_db
class TestProfileModel:

    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser4', email='test4@test.com', password='12345')
        assert Profile.objects.filter(user=user).exists()

    def test_related_habit_none_validation(self):
        """Тест: связанная привычка может быть None"""
        user = User.objects.create_user(username='testuser11', email='test11@test.com', password='12345')
        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Привычка без связи',
            duration=60,
            periodicity=1,
            related_habit=None
        )
        assert habit.related_habit is None

    def test_periodicity_boundary_values(self):
        """Тест: граничные значения периодичности 1 и 7"""
        user = User.objects.create_user(username='testuser12', email='test12@test.com', password='12345')
        habit_min = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Ежедневная',
            duration=60,
            periodicity=1
        )
        habit_max = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Еженедельная',
            duration=60,
            periodicity=7
        )
        assert habit_min.periodicity == 1
        assert habit_max.periodicity == 7