import requests

from config import settings


def send_telegram_message(chat_id, message):
    """Функция отправки уведомления в телеграмм"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }

    response = requests.get(
        f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage", params=params
    )
