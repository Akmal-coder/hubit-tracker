import pytest

from habits.tasks import send_habit_reminders


@pytest.mark.django_db
class TestTasks:

    def test_send_habit_reminders(self):
        result = send_habit_reminders()
        assert result == "OK"