from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите Email"
    )

    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="tg chat id",
        help_text="Введите tg chat id",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город",
    )

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
