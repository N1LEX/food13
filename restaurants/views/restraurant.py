from django.db.models import Prefetch, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin

from core.viewsets import (
    CustomReadOnlyModelViewSet,
)
from restaurants.consts import StatusChoices
from restaurants.models import (
    Restaurant,
    Category,
    Product,
    ProductPortion,
)
from restaurants.permissions.restaurant import RestaurantManageAccessPolicy
from restaurants.serializers.restaurant import (
    RestaurantListSerializer,
    RestaurantInstanceSerializer,
    RestaurantManageSerializer,
)
from restaurants.views.base import ManageViewSet


class RestaurantReadOnlyViewSet(CustomReadOnlyModelViewSet):
    """
    Публичный viewset ресторана
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kitchen']
    serializer_classes = {
        'List': RestaurantListSerializer,
        'Instance': RestaurantInstanceSerializer,
    }

    def get_queryset(self):
        standard_portion = ProductPortion.objects.active().filter(product=OuterRef('pk')).order_by('price')
        product_qs = Product.objects.active()\
            .filter(portions__isnull=False, portions__status=StatusChoices.ACTIVE)\
            .annotate(price=Subquery(standard_portion.values('price')[:1]))\
            .annotate(weight=Subquery(standard_portion.values('weight')[:1]))\
            .distinct()
        category_qs = Category.objects.active().prefetch_related(
            Prefetch('products', queryset=product_qs)
        ).filter(products__isnull=False)
        return Restaurant.objects.active().prefetch_related(
            Prefetch('categories', queryset=category_qs)
        )


class RestaurantManageViewSet(AccessViewSetMixin, ManageViewSet):
    """
    Viewset административной панели ресторана
    """
    access_policy = RestaurantManageAccessPolicy
    serializer_class = RestaurantManageSerializer

    def get_queryset(self):
        """
        Вывод только ресторанов пользователя
        """
        if self.request.user.is_superuser:
            return Restaurant.objects.prefetch_related('kitchen')
        return self.request.user.restaurants.prefetch_related('kitchen')
