from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


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