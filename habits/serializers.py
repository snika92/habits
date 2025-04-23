from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from habits.models import Habit, Place
from habits.validators import (is_pleasant_habit_validator,
                               related_habit_is_pleasant_habit_validator,
                               related_habit_or_reward_validator)
from users.models import User


class PlaceSerializer(ModelSerializer):
    owner = SerializerMethodField()

    def get_owner(self, place):
        return [owner.email for owner in User.objects.filter(places=place)]

    class Meta:
        model = Place
        fields = "__all__"


class HabitSerializer(ModelSerializer):
    owner = SerializerMethodField()

    def get_owner(self, habit):
        return [owner.email for owner in User.objects.filter(habits=habit)]

    class Meta:
        model = Habit
        fields = "__all__"
        validators = (
            related_habit_is_pleasant_habit_validator,
            related_habit_or_reward_validator,
            is_pleasant_habit_validator,
        )
