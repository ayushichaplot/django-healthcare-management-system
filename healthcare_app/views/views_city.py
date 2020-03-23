from django.core.validators import RegexValidator
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework import status
from ..models import City
from ..serilaizers import CityGetSerializer, CityPostSerializer


class Custom409(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "City already there."


class Custom422(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "City name should have characters only."


@api_view(['GET', 'POST'])
def city_list(request):
    if request.method == 'GET':
        cities = City.objects.all()
        city_serializer = CityGetSerializer(cities, many=True)
        return Response(city_serializer.data)
        return Response({})
        # insert a new record for a city
    elif request.method == 'POST':
        serializer = CityPostSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            if e.detail.get('name') == ['city with this name already exists.']:
                raise Custom409()
            elif e.detail.get('name') == ['Name should only consist of characters']:
                raise Custom422()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PATCH', 'PUT'])
def city_detail(request, id):
    # get details of a single city
    if request.method == 'GET':
        try:
            city = City.objects.get(id=id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CityGetSerializer(city)
        return Response(serializer.data)

    # delete a single city
    elif request.method == 'DELETE':
        try:
            city = City.objects.get(id=id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # update details of a single city
    elif request.method == 'PATCH':
        try:
            city = City.objects.get(id=id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CityPostSerializer(city, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            if e.detail.get('name') == ['city with this name already exists.']:
                raise Custom409()
            elif e.detail.get('name') == ['Name should only consist of characters']:
                raise Custom422()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            city = City.objects.get(id=id)
        except City.DoesNotExist:
            serializer = CityPostSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if e.detail.get('name') == ['city with this name already exists.']:
                    raise Custom409()
                elif e.detail.get('name') == ['Name should only consist of characters']:
                    raise Custom422()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = CityPostSerializer(city, data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            if e.detail.get('name') == ['city with this name already exists.']:
                raise Custom409()
            if e.detail.get('postalcode') == ['city with this postalcode already exists.']:
                raise Custom409()
            elif e.detail.get('name') == ['Name should only consist of characters']:
                raise Custom422()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
