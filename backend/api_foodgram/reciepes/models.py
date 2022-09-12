from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

from users.models import User



class Ingredient(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
    )
    measurement_unit = models.TextField(max_length=20)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
        unique=True,
    )
    color = models.TextField(
        max_length=256,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'#?([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})',
                message='mField must contain color HEX-code'
            )
        ],
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Unacceptable symbols'
            )
        ],
    )

    def __str__(self):
        return self.name


class Reciepe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reciepes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientReciepe',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagReciepe',
    )
    image = models.ImageField(
        upload_to='reciepes/',
    ) 
    name = models.TextField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=(MinValueValidator(1),),
        default=1,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.name

class IngredientReciepe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        # related_name='ingredient',
    )
    reciepe = models.ForeignKey(
        Reciepe,
        on_delete=models.CASCADE,
        # related_name='reciepe'
    )
    amount = models.FloatField(
        validators=(MinValueValidator(0),),
        default=0,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'reciepe'],
                name='unique_ingredient_reciepe',
            )
        ]


class TagReciepe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        # related_name='tag',
    )
    reciepe = models.ForeignKey(
        Reciepe,
        on_delete=models.CASCADE,
        # related_name='reciepe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'reciepe'],
                name='unique_tag_reciepe',
            )
        ]


class Favorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='user'
    )
    reciepe = models.ForeignKey(
        Reciepe,
        on_delete=models.CASCADE,
        # related_name='favorite'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'reciepe'],
                name='unique_favorite_reciepe',
            )
        ]


class Shoping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='user'
    )
    reciepe = models.ForeignKey(
        Reciepe,
        on_delete=models.CASCADE,
        # related_name='shopping'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'reciepe'],
                name='unique_shoping_reciepe',
            )
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscription',
            )
        ]
