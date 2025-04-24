from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Place
from habits.serializers import HabitSerializer
from habits.validators import (is_pleasant_habit_validator,
                               related_habit_is_pleasant_habit_validator,
                               related_habit_or_reward_validator)
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@mail.ru")
        self.place = Place.objects.create(title="Дом", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_habits_list(self):
        """Тестирование вывода списка привычек пользователя"""
        Habit.objects.create(
            action="Habit 1",
            owner=self.user,
            last_execution_time="2025-04-23",
            place=self.place,
            is_public=True,
        )
        Habit.objects.create(
            action="Habit 2",
            owner=self.user,
            last_execution_time="2025-04-22",
            place=self.place,
            is_public=False,
        )
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 2)

    def test_habits_public_list(self):
        """Тестирование вывода списка публичных привычек"""
        Habit.objects.create(
            action="Habit 1",
            owner=self.user,
            last_execution_time="2025-04-23",
            place=self.place,
            is_public=True,
        )
        Habit.objects.create(
            action="Habit 2",
            owner=self.user,
            last_execution_time="2025-04-22",
            place=self.place,
            is_public=False,
        )
        url = reverse("habits:public_habits_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 1)
        self.assertEqual(response.json().get("results")[0].get("action"), "Habit 1")

    def test_create_habit(self):
        """Тестирование создания полезной привычки"""
        data = {
            "action": "Habit 3",
            "owner": self.user,
            "last_execution_time": "2025-04-22",
            "place": self.place.pk,
            "is_public": False,
        }
        url = reverse("habits:habit_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 1)
        habit = Habit.objects.get(action="Habit 3")
        self.assertEqual(habit.action, "Habit 3")

    def test_delete_habit(self):
        """Тестирование удаления полезной привычки"""
        habit = Habit.objects.create(
            action="Habit 4",
            owner=self.user,
            last_execution_time="2025-04-23",
            place=self.place,
            is_public=True,
        )
        url = reverse("habits:habit_delete", args=(habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_retrieve_habit(self):
        """Тестирование вывода информации по полезной привычке"""
        habit = Habit.objects.create(
            action="Habit 5",
            owner=self.user,
            last_execution_time="2025-04-23",
            place=self.place,
            is_public=True,
        )
        url = reverse("habits:habit_retrieve", args=(habit.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("action"), "Habit 5")

    class HabitSerializerTest(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(email="test@mail.ru", password="test")
            self.place = Place.objects.create(title="Дом", owner=self.user)

        def test_valid_data(self):
            """Тестирование сериализатора на валидацию корректных данных"""
            data = {
                "action": "Habit 6",
                "owner": self.user,
                "last_execution_time": "2025-04-22",
                "place": self.place.pk,
                "is_public": False,
            }
            serializer = HabitSerializer(data=data)
            self.assertTrue(serializer.is_valid())

        def test_invalid_data(self):
            """Тестирование сериализатора на отклонения некорректных данных"""
            data = {
                "action": "Habit 7",
                "owner": self.user,
                "last_execution_time": "2025-04-22",
                "place": self.place.pk,
                "is_public": False,
                "duration_time": 200,
                "period": 8,
            }
            serializer = HabitSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("last_execution_time", serializer.errors)
            self.assertIn("duration_time", serializer.errors)
            self.assertIn("period", serializer.errors)


class RewardAndAssociatedValidatorTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@mail.ru", password="test", username="test"
        )
        self.place = Place.objects.create(title="Дом", owner=self.user)

    def test_related_habit_or_reward_validator(self):
        """Тестирование проверки валидатора одновременного указания связанной привычки и вознагражения"""
        data = {"reward": "Приз", "related_habit": 1}
        with self.assertRaisesMessage(
            Exception,
            "Нельзя одновременно указывать связанную привычку и вознаграждение. Выберите что-то одно.",
        ):
            related_habit_or_reward_validator(data)

    def test_only_reward(self):
        """Тестирование корректной обработки валидатора при указании только вознаграждения"""
        data = {"reward": "Приз", "related_habit": None}
        try:
            related_habit_or_reward_validator(data)
        except Exception as e:
            self.fail(f"Validator raised exception unexpectedly: {e}")

    def test_related_habit_is_pleasant_habit_validator(self):
        """Тестирование проверки валидатора связанной привычки, если не указано, что это приятная привычка"""
        data = {"is_pleasant_habit": False, "related_habit": 1}
        with self.assertRaisesMessage(
            Exception,
            "В связанные привычки могут попадать только привычки с признаком приятной привычки",
        ):
            related_habit_is_pleasant_habit_validator(data)

    def test_is_pleasant_habit_validator(self):
        """Тестирование проверки валидатора, который проверяет, что у приятной привычки нет ни вознаграждения,
        ни связанной привычки"""
        data = {"is_pleasant_habit": True, "reward": "Reward", "related_habit": 1}
        with self.assertRaisesMessage(
            Exception,
            "У приятной привычки не может быть вознаграждения или связанной привычки",
        ):
            is_pleasant_habit_validator(data)
