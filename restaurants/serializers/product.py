from rest_framework import serializers

from restaurants.models import Category, Product


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

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'created_by',
            'weight',
            'price',
            'is_available',
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер продуктов категории
    """
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'logo',
            'description',
            'weight',
            'price',
            'is_available',
        )
