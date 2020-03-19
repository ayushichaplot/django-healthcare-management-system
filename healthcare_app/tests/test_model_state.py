from django.core.exceptions import ValidationError
from django.test import TestCase
from .. import models
from ..models import State


class StateTestCase(TestCase):
    def setUp(self):
        State.objects.create(name='Rajasthan')
        State.objects.create(name='Gujarat')

    def test_state_count(self):
        state = State.objects.all()
        self.assertEqual(state.count(), 2)

    def test_name_max_length(self):
        state = State.objects.get(id=1)
        max_length = state._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_name_validation(self):
        name = State(name="123")
        with self.assertRaises(ValidationError):
            name.full_clean()









