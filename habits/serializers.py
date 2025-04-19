from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from habits.models import Habit, Place
from users.models import User


class PlaceSerializer(ModelSerializer):
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
