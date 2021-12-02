from rest_framework import serializers

from restaurants.models import ProductPortion, Product


class ProductPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Получаем кверисет доступных продуктов ресторанов пользователя при создании порции.
    Необходимо для избежания добавления в продукты ресторанов, которые недоступны пользователю для редактирования.
    """
    def get_queryset(self):
        products = Product.objects.select_related('category', 'category__restaurant')
        if self.context['request'].user.is_superuser:
            return products
        return products.filter(category__restaurant__in=self.context['request'].user.restaurants.all())


class ProductPortionSerializer(serializers.ModelSerializer):
    """
    Сериалайзер порции продукта
    """
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductPortion
        fields = (
            'id',
            'weight',
            'price',
            'discount',
            'total_price',
        )


class ProductPortionManageSerializer(serializers.ModelSerializer):
    """
    Сериалайзер порции продукта в административной панели
    """
    product = ProductPrimaryKeyRelatedField(label='Продукт')
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductPortion
        fields = (
            'id',
            'product',
            'weight',
            'price',
            'discount',
            'created_by',
        )
