from django.core.validators import RegexValidator
from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .serializer_state import StateSerializer
from ..models import City, State


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityGetSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = '__all__'


class CityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['state'] = StateSerializer(instance.state).data
        return response
