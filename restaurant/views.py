from rest_framework.decorators import action
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from restaurant.models import Restaurant, Category, Product
from restaurant.serializers import RestaurantSerializer, CategorySerializer, ProductSerializer


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=True)
    def categories(self, request, pk=None):
        instance = self.get_object()
        return CategorySerializer(instance.categories.all(), many=True).data

    @action(detail=True)
    def products(self, request, pk=None):
        return ProductSerializer(
            Product.objects.select_related('category').filter(category__restaurant__pk=pk), many=True
        ).data


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True)
    def products(self, request, pk=None):
        instance = self.get_object()
        return ProductSerializer(instance.products.all(), many=True).data


class ProductViewSet(ModelSerializer):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

