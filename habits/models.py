from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from config import settings


class Place(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Название места выполнения привычки"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание места выполнения привычки"
    )
    image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="Превью"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец места",
        related_name="places",
        help_text="Укажите владельца места",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ["title"]


class Habit(models.Model):

    action = models.CharField(max_length=200, verbose_name="Название привычки")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец привычки",
        related_name="habits",
        help_text="Укажите владельца привычки",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    place = models.ForeignKey(
        Place,
        verbose_name="Место выполнения привычки",
        related_name="habits",
        help_text="Укажите место выполнения привычки",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    planned_time = models.TimeField(
        verbose_name="Время",
        help_text="Укажите, в какое время планируете выполнять привычку",
        null=True,
        blank=True,
    )
    last_execution_time = models.DateField(
        null=True,
        blank=True,
        verbose_name="Время последнего выполнения привычки",
        help_text="Укажите время последнего выполнения привычки",
    )

    # У приятной привычки не может быть вознаграждения или связанной привычки.
    is_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Укажите является ли привычка приятной, а не полезной",
    )

    # Можно указывать только для полезных привычек, но не для приятных
    # Либо приятная связанная привычка, либо вознаграждение
    # В связанные привычки могут попадать только привычки с признаком приятной привычки.
    related_habit = models.ForeignKey(
        "self",
        verbose_name="Связанная привычка",
        related_name="habits",
        help_text="Укажите связанную привычку",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    period = models.PositiveIntegerField(
        validators=[MaxValueValidator(7), MinValueValidator(1)],
        default=1,
        verbose_name="Периодичность привычки",
        help_text="Укажите периодичность привычки",
    )

    # Либо приятная связанная привычка, либо вознаграждение
    reward = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение за выполнение привычки",
    )

    # Время выполнения должно быть не больше 120 секунд
    duration_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        null=True,
        blank=True,
        verbose_name="Время на выполнение привычки",
        help_text="Укажите время, необходимое для выполнения привычки",
    )

    is_public = models.BooleanField(
        verbose_name="Признак публичности",
        default=False,
        help_text="Укажите, можно ли публиковать привычку в общий доступ",
    )

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action"]
