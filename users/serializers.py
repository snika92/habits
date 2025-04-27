from rest_framework.serializers import ModelSerializer

from habits.serializers import HabitSerializer

from .models import User


class UserSerializer(ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "password",
            "email",
            "phone_number",
            "tg_chat_id",
            "avatar",
            "city",
            "habits",
        ]


class UserDetailSerializer(ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "tg_chat_id",
            "avatar",
            "city",
            "habits",
        ]
