from django.core.exceptions import ValidationError
from django.test import TestCase
from .. import models
from ..models import State


class StateTestCase(TestCase):
    def setUp(self):
        State.objects.create(name='Rajasthan')
        State.objects.create(name='Gujarat')

    def test_state_count(self):
        count = State.objects.all()
        self.assertEqual(count.count(), 2)

    def test_name_max_length(self):
        state = State.objects.get(id=1)
        max_length = state._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_name_validation(self):
        name = State(name="123")
        with self.assertRaises(ValidationError):
            name.full_clean()

    def test_name_single_entry(self):
        self.assertEqual(1, len(State.objects.filter(name='Gujarat')))
