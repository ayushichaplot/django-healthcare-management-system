from django.core.validators import RegexValidator
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework import status
from ..models import State
from ..serilaizers import StateSerializer


@api_view(['GET', 'DELETE', 'PATCH', 'PUT'])
def state_detail(request, id):
    # get details of a single state
    if request.method == 'GET':
        try:
            state = State.objects.get(id=id)
        except State.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StateSerializer(state)
        return Response(serializer.data)

    # delete a single state
    elif request.method == 'DELETE':
        try:
            state = State.objects.get(id=id)
        except State.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # update details of a single state
    elif request.method == 'PATCH':
        try:
            state = State.objects.get(id=id)
        except State.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StateSerializer(state, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            if e.detail.get('name') == ['state with this name already exists.']:
                raise Custom409()
            elif e.detail.get('name') == ['Name should only consist of characters']:
                raise Custom422()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            state = State.objects.get(id=id)
        except State.DoesNotExist:
            serializer = StateSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if e.detail.get('name') == ['state with this name already exists.']:
                    raise Custom409()
                elif e.detail.get('name') == ['Name should only consist of characters']:
                    raise Custom422()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = StateSerializer(state, data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            if e.detail.get('name') == ['state with this name already exists.']:
                raise Custom409()
            elif e.detail.get('name') == ['Name should only consist of characters']:
                raise Custom422()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def state_list(request):
    # get all state
    if request.method == 'GET':
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)
        return Response({})
    # insert a new record for a state
    elif request.method == 'POST':
        serializer = StateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            if e.detail.get('name') == ['state with this name already exists.']:
                raise Custom409()
            elif e.detail.get('name') == ['Name should only consist of characters']:
                raise Custom422()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Custom409(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "State already there."


class Custom422(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "State name should have characters only."
