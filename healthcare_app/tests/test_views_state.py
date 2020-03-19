from django.core.exceptions import ValidationError
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.test import TestCase
from ..models import State
from ..serilaizers import StateSerializer

client = Client()


class GetAllStatesTest(TestCase):
    """ Test module for GET all states API """

    def setUp(self):
        State.objects.create(name='Rajasthan')
        State.objects.create(name='Gujarat')

    def test_get_all_states(self):
        # get API response from urls.py
        response = client.get(reverse('state_list'))
        # get data from db
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleStateTest(TestCase):
    """ Test module for GET single state API """

    def setUp(self):
        self.state1 = State.objects.create(name='Rajasthan')
        self.state2 = State.objects.create(name='Punjab')

    def test_get_valid_single_patient(self):
        response = client.get(reverse('state_detail', kwargs={'pk': self.state1.pk}))
        state = State.objects.get(pk=self.state1.pk)
        serializer = StateSerializer(state)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_state(self):
        response = client.get(reverse('state_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewStateTest(TestCase):
    """ Test module for inserting a new state """

    def setUp(self):
        self.valid_payload = {
            'name': 'Rajasthan'
        }
        self.invalid_payload = {
            'name': '',
        }
        self.invalid_payload1 = {
            'name': "123",
        }
        self.valid_payload = {
            'name': 'Rajasthan'
        }

    def test_create_valid_state(self):
        response = client.post(reverse('state_list'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_state(self):
        response = client.post(reverse('state_list'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_state_name(self):
        response = client.post(reverse('state_list'),
                               data=json.dumps(self.invalid_payload1),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_if_multiple_state_name(self):
        create_state = self.client.post(reverse('state_list'),
                                        data={'name': 'ABC'},
                                        format='application/json')
        self.assertEqual(create_state.status_code, 201)
        create_state = self.client.post(reverse('state_list'),
                                        data={'name': 'ABC'},
                                        format='application/json')

        self.assertEqual(create_state.status_code, status.HTTP_409_CONFLICT)


class UpdateSingleStateTest(TestCase):
    """ Test module for updating an existing state record """

    def setUp(self):
        self.state1 = State.objects.create(name='Rajasthan')
        self.state2 = State.objects.create(name='Punjab')
        self.state3 = State.objects.create(name='Bihar')
        self.valid_payload = {
            'name': 'Rajasthan'
        }
        self.invalid_payload = {
            'name': '',
        }
        self.invalid_payload1 = {
            'name': "123",
        }
        self.invalid_payload2 = {
            'name': 'Punjab'
        }

    def test_valid_update_state(self):
        response = client.put(
            reverse('state_detail', kwargs={'pk': self.state1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_state(self):
        response = client.put(
            reverse('state_detail', kwargs={'pk': self.state2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_state_name(self):
        response = client.put(reverse('state_detail', kwargs={'pk': self.state3.pk}),
                              data=json.dumps(self.invalid_payload1),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_if_multiple_state_name(self):
        response = client.put(reverse('state_detail', kwargs={'pk': self.state3.pk}),
                              data=json.dumps(self.invalid_payload2),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class DeleteSingleStateTest(TestCase):
    """ Test module for deleting an existing state record """

    def setUp(self):
        self.state1 = State.objects.create(name='Rajasthan')
        self.state2 = State.objects.create(name='Punjab')

    def test_valid_delete_state(self):
        response = client.delete(
            reverse('state_detail', kwargs={'pk': self.state1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_state(self):
        response = client.delete(
            reverse('state_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
