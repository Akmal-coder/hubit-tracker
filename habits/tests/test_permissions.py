import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly

User = get_user_model()


@pytest.mark.django_db
class TestIsOwnerOrReadOnly:

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='owner', email='owner@test.com', password='12345')
        self.other_user = User.objects.create_user(username='other', email='other@test.com', password='12345')
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Тестовая',
            duration=60,
            periodicity=1
        )
        self.permission = IsOwnerOrReadOnly()

    def test_owner_can_edit(self):
        request = self.factory.put('/api/habits/1/')
        request.user = self.user
        assert self.permission.has_object_permission(request, None, self.habit) is True

    def test_other_user_cannot_edit(self):
        request = self.factory.put('/api/habits/1/')
        request.user = self.other_user
        assert self.permission.has_object_permission(request, None, self.habit) is False

    def test_other_user_can_read(self):
        request = self.factory.get('/api/habits/1/')
        request.user = self.other_user
        assert self.permission.has_object_permission(request, None, self.habit) is True