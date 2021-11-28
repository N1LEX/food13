from rest_framework import serializers

from restaurants.models import Category, Product
from restaurants.serializers.product_portion import ProductPortionSerializer


class CategoryPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Получаем кверисет доступных категорий ресторанов пользователя при создании продукта.
    Необходимо для избежания добавления в категории ресторанов, которые недоступны пользователю для редактирования.
    """
    def get_queryset(self):
        categories = Category.objects.all()
        if self.context['request'].user.is_superuser:
            return categories
        return categories.filter(restaurant__in=self.context['request'].user.restaurants.all())


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер продукта
    """
    category_name = serializers.StringRelatedField(source='category.name', read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    portions = ProductPortionSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'created_by',
            'is_available',
            'portions'
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер продуктов категории
    """
    price = serializers.IntegerField()
    weight = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'logo',
            'is_available',
            'price',
            'weight',
        )
