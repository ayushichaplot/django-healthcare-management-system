import re

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .city import City
from .state import State


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        name_regex = RegexValidator(regex=r'^\d*[a-zA-Z][#.0-9a-zA-Z\s,-]+$',
                                    message="Name should consist of characters")
        kwargs['validators'] = [name_regex]
        kwargs['max_length'] = 100
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()
    


class Facility(models.Model):
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    name = models.NameField()
    address_regex = RegexValidator(regex=r'^\d*[a-zA-Z][#.0-9a-zA-Z\s,-]+$',
                                   message="Address should be in proper format")
    address = models.CharField(validators=[address_regex], max_length=100)
    medicare_ccn = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


