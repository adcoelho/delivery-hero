from rest_framework import serializers
from restaurants.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    """
    This class provides a way of serializing and deserializing the restaurant instances into representations such as json.
    """
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'opens_at', 'closes_at')


    def validate(self, data):
        """
        Check that the opening time is before the closing time.
        """
        if data['opens_at'] > data['closes_at']:
            raise serializers.ValidationError("The restaurant must open before it closes.")
        return data