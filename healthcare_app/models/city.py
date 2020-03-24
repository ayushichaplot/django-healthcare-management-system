import re

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.forms import ModelForm

from .state import State


# Create your models here.
class City(models.Model):
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)
    name_regex = RegexValidator(regex=r'^[a-zA-Z]+$',
                                message="Name should only consist of characters")
    name = models.CharField(validators=[name_regex], max_length=100)
    postalcode = models.IntegerField(unique=True)

    class Meta:
        unique_together = ["state", "name"]

    def clean(self):
        self.clean_fields()
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name
