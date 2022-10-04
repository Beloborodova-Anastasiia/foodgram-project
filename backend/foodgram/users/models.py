from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscription',
            )
        ]
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписки'


class CustomToken(Token):
    class Meta:
        verbose_name_plural = 'Токены'
        verbose_name = 'Токен'
