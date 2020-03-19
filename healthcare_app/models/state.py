from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class State(models.Model):
    name_regex = RegexValidator(regex=r'^[a-zA-Z]+$',
                                message="Name should only consist of characters")
    name = models.CharField(validators=[name_regex], max_length=100)

    def __str__(self):
        return self.name
