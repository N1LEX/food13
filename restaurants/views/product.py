from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin

from core.viewsets import CustomRetrieveViewSet
from restaurants.consts import StatusChoices
from restaurants.filters.product import ProductFilter
from restaurants.models import Product, ProductPortion
from restaurants.permissions.product import ProductManageAccessPolicy
from restaurants.serializers.product import ProductSerializer, ProductManageSerializer
from restaurants.views.base import ManageViewSet


class ProductReadOnlyViewSet(CustomRetrieveViewSet):
    """
    Публичный viewset продукта
    """
    queryset = Product.objects.active()\
        .select_related('category')\
        .prefetch_related(
            Prefetch('portions', queryset=ProductPortion.objects.active())
        ).filter(category__status=StatusChoices.ACTIVE, category__restaurant__status=StatusChoices.ACTIVE)
    serializer_class = ProductSerializer


class ProductManageViewSet(AccessViewSetMixin, ManageViewSet):
    access_policy = ProductManageAccessPolicy
    serializer_class = ProductManageSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter

    def get_queryset(self):
        """
        Вывод только продуктов ресторана пользователя
        """
        products = Product.objects.all()
        if self.request.user.is_superuser:
            return products
        return products.select_related('category')\
            .filter(category__restaurant__in=self.request.user.restaurants.all())
