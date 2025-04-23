from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.validators import (related_habit_is_pleasant_habit_validator,
                               related_habit_or_reward_validator)
from users.models import User


class UserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", password="test")
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        data = {
            "username": "new",
            "email": "new@mail.ru",
            "password": "new",
        }
        url = reverse("users:register")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
