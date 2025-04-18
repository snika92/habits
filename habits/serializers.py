from rest_framework.serializers import ModelSerializer

from habits.models import Habit, Place


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
