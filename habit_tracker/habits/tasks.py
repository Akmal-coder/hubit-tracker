from celery import shared_task


@shared_task
def send_habit_reminders():
    print("Celery задача работает!")
    return "OK"
