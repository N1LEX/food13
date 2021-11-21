from rest_framework import serializers

from restaurants.models import Restaurant
from restaurants.serializers.category import CategoryRestaurantSerializer


class RestaurantListSerializer(serializers.ModelSerializer):
    """
    Сериалайзер списка ресторанов
    """
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'logo',
            'delivery_min',
            'delivery_time',
            'opens_in',
            'closes_in',
            'self_pickup_discount',
        )


class RestaurantInstanceSerializer(serializers.ModelSerializer):
    """
    Сериалайзер объекта ресторана
    """
    kitchen = serializers.StringRelatedField(many=True, read_only=True)
    categories = CategoryRestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'logo',
            'description',
            'kitchen',
            'delivery_min',
            'delivery_time',
            'opens_in',
            'closes_in',
            'self_pickup_discount',
            'phone',
            'address',
            'vk',
            'instagram',
            'telegram',
            'website',
            'categories',
        )


class RestaurantManageSerializer(serializers.ModelSerializer):
    """
    Сериалайзер ресторанов в административной панели
    """
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'logo',
            'description',
            'delivery_min',
            'delivery_time',
            'opens_in',
            'closes_in',
            'self_pickup_discount',
            'kitchen',
            'phone',
            'address',
            'vk',
            'instagram',
            'telegram',
            'website',
            'status',
        )
        read_only_fields = ('status',)
