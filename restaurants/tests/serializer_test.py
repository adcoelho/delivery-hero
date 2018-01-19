from django.test import TestCase

from rest_framework import serializers
from restaurants.serializers import RestaurantSerializer

class RestaurantSerializerTest(TestCase):
    def test_validate_restaurant(self):
        invalid_restaurant = {
            'name': 'New Mirazur that closes later',
            'opens_at': '14:15:00',
            'closes_at': '12:16:00'
        }
        invalid_restaurant_serializer = RestaurantSerializer()
        with self.assertRaisesMessage(serializers.ValidationError, 'The restaurant must open before it closes.'):
            invalid_restaurant_serializer.validate(data=invalid_restaurant)
