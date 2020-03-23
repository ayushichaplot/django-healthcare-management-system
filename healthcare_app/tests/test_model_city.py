from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import City, State

class CityTestCase(TestCase):
    def setUp(self):
        state1 = State.objects.create(name='Rajasthan')
        City.objects.create(state=state1, name='Udaipur', postalcode=313001)
        state2 = State.objects.create(name='Gujarat')
        City.objects.create(state=state2, name='Gandhinagar', postalcode=123456)

    def test_total_city_count(self):
        count = City.objects.all()
        self.assertEqual(count.count(), 2)

    def test_name_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_name_validation(self):
        name = City(name="123")
        with self.assertRaises(ValidationError):
            name.full_clean()

    def test_name_single_entry(self):
        self.assertEqual(1, len(City.objects.filter(name='Udaipur')))
        self.assertEqual(1, len(City.objects.filter(postalcode= 313001)))