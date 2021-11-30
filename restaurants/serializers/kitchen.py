from rest_framework import serializers

from restaurants.models import Kitchen
from restaurants.serializers.restaurant import KitchenRestaurantSerializer


class KitchenSerializer(serializers.ModelSerializer):
    restaurants = KitchenRestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = Kitchen
        fields = (
            'id',
            'name',
            'restaurants',
        )


class KitchenManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kitchen
        fields = (
            'id',
            'name',
        )
