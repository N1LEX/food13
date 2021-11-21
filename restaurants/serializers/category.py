from rest_framework import serializers

from restaurants.models import Category, Restaurant
from restaurants.serializers.product import ProductCategorySerializer


class RestaurantPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Получаем кверисет доступных ресторанов пользователя при создании категории.
    Необходимо для избежания добавления в рестораны, которые недоступны пользователю для редактирования.
    """
    def get_queryset(self):
        if self.context['request'].user.is_superuser:
            return Restaurant.objects.all()
        return self.context['request'].user.restaurants.all()


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериалайзер категории
    """
    products = ProductCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'restaurant', 'products')


class CategoryRestaurantSerializer(serializers.ModelSerializer):
    """
    Сериалайзер категорий ресторана
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryManageSerializer(serializers.ModelSerializer):
    """
    Сериалайзер категорий в административной панели
    """
    restaurant = RestaurantPrimaryKeyRelatedField(label='Ресторан')
    restaurant_name = serializers.StringRelatedField(source='restaurant.name', read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'restaurant',
            'restaurant_name',
            'created_by',
            'status',
        )
        read_only_fields = ('status',)
