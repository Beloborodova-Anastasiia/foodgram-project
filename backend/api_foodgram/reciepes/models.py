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
    slug = models.TextField(
        max_length=256,
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
        validators=MinValueValidator(1),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    