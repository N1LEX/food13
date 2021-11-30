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
            'open_time',
            'close_time',
            'self_pickup_discount',
        )
        read_only_fields = fields


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
            'open_time',
            'close_time',
            'self_pickup_discount',
            'phone',
            'address',
            'vk',
            'instagram',
            'telegram',
            'website',
            'categories',
        )
        read_only_fields = fields


class KitchenRestaurantSerializer(serializers.ModelSerializer):
    """
    Сериалайзер ресторана кухни.
    """
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'logo',
            'delivery_min',
            'delivery_time',
            'open_time',
            'close_time',
        )
        read_only_fields = fields


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
            'open_time',
            'close_time',
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
