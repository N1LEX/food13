from rest_framework.serializers import ModelSerializer

from restaurant.models import Restaurant, Category, Product


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('average_check',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        models = Product
        fields = '__all__'
