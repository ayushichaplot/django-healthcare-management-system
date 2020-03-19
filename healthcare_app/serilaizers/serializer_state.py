from django.core.validators import RegexValidator
from rest_framework import serializers, status
from rest_framework.response import Response

from ..models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

    def validate(self, data):
        name_regex = RegexValidator(regex=r'^[a-zA-Z]+$',
                                    message="Name should only consist of characters")
        if data['name'] not in format(name_regex):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return data