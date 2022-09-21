from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
# from recipes.models import Recipe


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
    # shoping_cart = models.ManyToManyField(
    #     Recipe,
    #     through='Shoping',
    #     verbose_name='Список покупок'
    # )
    # favorites = models.ManyToManyField(
    #     Recipe,
    #     through='Favorite',
    #     verbose_name='Избранное'
    # )
    # subscribes = 


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='followings'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscription',
            )
        ]


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='favorite',
#         verbose_name='Пользователь',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='favorite',
#         verbose_name='Рецепт',
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'recipe'],
#                 name='unique_favorite_recipe',
#             )
#         ]


# class Shoping(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='user'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipes'
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'recipe'],
#                 name='unique_shoping_recipe',
#             )
#         ]
