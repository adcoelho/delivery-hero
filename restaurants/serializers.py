from rest_framework import serializers
from restaurants.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    """
    This class provides a way of serializing and deserializing the restaurant instances into representations such as json.
    """
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'opens_at', 'closes_at')
