from django.core.validators import RegexValidator
from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from ..models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

