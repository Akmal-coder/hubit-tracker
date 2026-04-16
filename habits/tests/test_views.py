import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
class TestHabitViews:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_list_habits(self):
        Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            duration=60,
            periodicity=1
        )
        response = self.client.get('/api/habits/')
        assert response.status_code == 200

    def test_create_habit(self):
        data = {
            'place': 'Офис',
            'time': '10:00:00',
            'action': 'Прогулка',
            'duration': 30,
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        assert response.status_code == 201

    def test_cannot_edit_other_user_habit(self):
        other_user = User.objects.create_user(username='other', email='other@test.com', password='12345')
        habit = Habit.objects.create(
            user=other_user,
            place='Дом',
            time='08:00:00',
            action='Чужая привычка',
            duration=60,
            periodicity=1
        )
        response = self.client.put(f'/api/habits/{habit.id}/', {'action': 'Попытка изменить'})
        assert response.status_code == 404

    def test_public_habits_list(self):
        self.client.logout()
        Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Публичная',
            duration=60,
            periodicity=1,
            is_public=True
        )
        response = self.client.get('/api/public/')
        assert response.status_code == 200