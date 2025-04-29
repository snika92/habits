from rest_framework import serializers


def related_habit_or_reward_validator(value):
    """Валидатор для проверки, что нельзя указывать одновременно связанную привычку и вознаграждение."""

    related_habit = dict(value).get("related_habit")
    reward = dict(value).get("reward")

    if related_habit and reward:
        raise serializers.ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение. Выберите что-то одно."
        )


def related_habit_is_pleasant_habit_validator(value):
    """
    Валидатор для проверки, что в связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    related_habit = dict(value).get("related_habit")
    is_pleasant_habit = dict(value).get("is_pleasant_habit")

    if related_habit and not is_pleasant_habit:
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки"
        )


def is_pleasant_habit_validator(value):
    """Валидатор для проверки, что у приятной привычки не может быть вознаграждения или связанной привычки."""

    is_pleasant_habit = dict(value).get("is_pleasant_habit")
    reward = dict(value).get("reward")
    related_habit = dict(value).get("related_habit")

    if is_pleasant_habit and reward or related_habit:
        raise serializers.ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки"
        )
