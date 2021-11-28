from rest_framework import serializers

from restaurants.models import ProductPortion


class ProductPortionSerializer(serializers.ModelSerializer):
    """
    Сериалайзер порции продукта
    """
    class Meta:
        model = ProductPortion
        fields = (
            'id',
            'weight',
            'price',
        )
