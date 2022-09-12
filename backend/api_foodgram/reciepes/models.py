from django.db import models
from django.core.validators import RegexValidator
from users.models import User



class Ingredient(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True
    )
    measurement_unit = models.TextField(max_length=20)


class Tag(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
        unique=True
    )
    color = models.TextField(
        max_length=256,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'#?([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})',
                message='mField must contain color HEX-code'
            )
        ]
    )
    slug = models.TextField(
        max_length=256,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Unacceptable symbols'
            )
        ]
    )