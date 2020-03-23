import re

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class State(models.Model):
    #regex = re.compile(r'^[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', re.IGNORECASE)
    name_regex = RegexValidator(regex=r'^[a-zA-Z]+$',
                                message="Name should only consist of characters")
    name = models.CharField(validators=[name_regex], max_length=100, unique=True)

    def clean(self):
        self.clean_fields()
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name
