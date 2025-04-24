from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_info_about_habit():
    date_now = timezone.now().date()
    time_now = timezone.now() + timedelta(minutes=5)
    time = time_now.time().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(
        is_pleasant_habit=False, planned_time=time, last_execution_time=date_now
    )

    for habit in habits:
        days = habit.period
        habit.last_execution_time = date_now + timedelta(days=days)
        habit.save()

        message = (
            f"Привет {habit.user}! Время {habit.planned_time}. Пора идти в {habit.place} и {habit.action}."
            f"Это займет {habit.duration_time} минут! После сможете себя порадовать "
            f"{habit.related_habit if habit.related_habit else habit.reward}"
        )
        print(message)

        if habit.owner.tg_chat_id:
            send_telegram_message(habit.owner.tg_chat_id, message)
