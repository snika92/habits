from rest_framework.serializers import ModelSerializer

from habits.serializers import HabitSerializer
from .models import User


class UserSerializer(ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "tg_nick", "avatar", "city", "payments"]
