from django.core.exceptions import ValidationError
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.test import TestCase
from ..models import State, City
from ..serilaizers import StateSerializer, CityPostSerializer, CityGetSerializer

client = Client()


class GetAllCitiesTest(TestCase):
    """ Test module for GET all cities API """

    def setUp(self):
        state1 = State.objects.create(name='Rajasthan')
        City.objects.create(state=state1, name='Udaipur', postalcode=313001)
        state2 = State.objects.create(name='Gujarat')
        City.objects.create(state=state2, name='Gandhinagar', postalcode=123456)

    def test_get_all_cities(self):
        # get API response from urls.py
        response = client.get(reverse('city_list'))
        # get data from db
        cities = City.objects.all()
        serializer = CityGetSerializer(cities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCityTest(TestCase):
    """ Test module for GET single city API """

    def setUp(self):
        state1 = State.objects.create(name='Rajasthan')
        self.city1 = City.objects.create(state=state1, name='Udaipur', postalcode=313001)
        state2 = State.objects.create(name='Gujarat')
        self.city2 = City.objects.create(state=state2, name='Gandhinagar', postalcode=123456)

    def test_get_valid_single_city(self):
        response = client.get(reverse('city_detail', kwargs={'id': self.city1.id}))
        city = City.objects.get(id=self.city1.id)
        serializer = CityGetSerializer(city)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_city(self):
        response = client.get(reverse('city_detail', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCityTest(TestCase):
    """ Test module for inserting a new city """

    def setUp(self):
        state1 = State.objects.create(name='Rajasthan')
        self.valid_payload = {
            'state': state1.id,
            'name': 'Udaipur',
            'postalcode': 313001
        }
        self.invalid_payload = {
            'state': ' ',
            'name': '',
            'postalcode': ''
        }
        self.invalid_payload1 = {
            'state': state1.id,
            'name': '123',
            'postalcode': 313001
        }
        self.invalid_payload2 = {
            'state': state1.id,
            'name': 'Udaipur',
            'postalcode': 313001
        }

    def test_create_valid_city(self):
        response = client.post(reverse('city_list'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_city(self):
        response = client.post(reverse('city_list'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_city_name(self):
        response = client.post(reverse('city_list'),
                               data=json.dumps(self.invalid_payload1),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_if_multiple_city_name(self):
        state2 = State.objects.create(name='Gujarat')
        create_city = self.client.post(reverse('city_list'),
                                       data={'state': state2.id, 'name': 'Gandhinagar', 'postalcode': 313000},
                                       format='application/json')
        self.assertEqual(create_city.status_code, 201)
        create_city = self.client.post(reverse('city_list'),
                                       data={'state': state2.id, 'name': 'Gandhinagar', 'postalcode': 313009},
                                       format='application/json')

        self.assertEqual(create_city.status_code, status.HTTP_409_CONFLICT)

    def test_if_multiple_postalcode(self):
        state2 = State.objects.create(name='Gujarat')
        create_city = self.client.post(reverse('city_list'),
                                       data={'state': state2.id, 'name': 'Gandhinagar', 'postalcode': 313000},
                                       format='application/json')
        self.assertEqual(create_city.status_code, 201)
        create_city = self.client.post(reverse('city_list'),
                                       data={'state': state2.id, 'name': 'Ahmedabad', 'postalcode': 313000},
                                       format='application/json')

        self.assertEqual(create_city.status_code, status.HTTP_409_CONFLICT)


class UpdateSingleCityTest(TestCase):
    """ Test module for updating an existing city record """

    def setUp(self):
        state1 = State.objects.create(name='Rajasthan')
        self.city1 = City.objects.create(state=state1, name='Udaipur', postalcode=313001)
        state2 = State.objects.create(name='Gujarat')
        self.city2 = City.objects.create(state=state2, name='Gandhinagar', postalcode=123456)
        state3 = State.objects.create(name='Maharashtra')
        self.city3 = City.objects.create(state=state3, name='Mumbai', postalcode=123457)
        self.valid_payload = {
            'state': state1.id,
            'name': 'Udaipur',
            'postalcode': 313001
        }
        self.invalid_payload = {
            'state': ' ',
            'name': '',
            'postalcode': ''
        }
        self.invalid_payload1 = {
            'state': state1.id,
            'name': '123',
            'postalcode': 123457
        }
        self.invalid_payload2 = {
            'state': state1.id,
            'name': 'Udaipur',
            'postalcode': 313001
        }
        self.invalid_payload2 = {
            'state': state3.id,
            'name': 'Pune',
            'postalcode': 313001
        }

    def test_valid_update_city(self):
        response = client.put(
            reverse('city_detail', kwargs={'id': self.city1.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_city(self):
        response = client.put(
            reverse('city_detail', kwargs={'id': self.city2.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_city_name(self):
        response = client.put(reverse('city_detail', kwargs={'id': self.city3.id}),
                              data=json.dumps(self.invalid_payload1),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_if_multiple_city_name(self):
        response = client.put(reverse('city_detail', kwargs={'id': self.city3.id}),
                              data=json.dumps(self.invalid_payload2),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_if_multiple_postalcode(self):
        response = client.put(reverse('city_detail', kwargs={'id': self.city3.id}),
                              data=json.dumps(self.invalid_payload2),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class DeleteSingleCityTest(TestCase):
    """ Test module for deleting an existing city record """

    def setUp(self):
        state1 = State.objects.create(name='Rajasthan')
        self.city1 = City.objects.create(state=state1, name='Udaipur', postalcode=313001)
        state2 = State.objects.create(name='Gujarat')
        self.city2 = City.objects.create(state=state2, name='Gandhinagar', postalcode=123456)

    def test_valid_delete_state(self):
        response = client.delete(
            reverse('city_detail', kwargs={'id': self.city1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_state(self):
        response = client.delete(
            reverse('state_detail', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
