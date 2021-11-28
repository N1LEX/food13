from django_filters.rest_framework import DjangoFilterBackend

from core.viewsets import CustomReadOnlyModelViewSet
from restaurants.consts import StatusChoices
from restaurants.filters.product import ProductFilter
from restaurants.models import Product
from restaurants.serializers.product import ProductSerializer


class ProductReadOnlyViewSet(CustomReadOnlyModelViewSet):
    """
    Read only viewset продукта
    """
    queryset = Product.objects.active().select_related('category', 'category__restaurant').filter(
        category__status=StatusChoices.ACTIVE, category__restaurant__status=StatusChoices.ACTIVE,
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter
