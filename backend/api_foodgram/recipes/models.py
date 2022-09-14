from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

from users.models import User


class Ingredient(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
    )
    measurement_unit = models.CharField(max_length=20)

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


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
    )
    image = models.ImageField(
        upload_to='recipes/',
    )
    name = models.CharField(max_length=200)
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


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        validators=(MinValueValidator(0),),
        default=0,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe',
            )
        ]


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_recipe',
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            )
        ]


class Shoping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoping_recipe',
            )
        ]
