from django.db.models import Prefetch, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import (
    CustomReadOnlyModelViewSet,
    CustomModelViewSet,
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


class RestaurantReadOnlyViewSet(CustomReadOnlyModelViewSet):
    """
    Read only viewset ресторана
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
            .annotate(weight=Subquery(standard_portion.values('weight')[:1]))
        category_qs = Category.objects.active().prefetch_related(
            Prefetch('products', queryset=product_qs.distinct())
        )

        return Restaurant.objects.active().prefetch_related(
            Prefetch('categories', queryset=category_qs)
        )


class RestaurantManageViewSet(AccessViewSetMixin, CustomModelViewSet):
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

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            serializer.save(status=StatusChoices.CHECK)
        serializer.save()

    @action(detail=True)
    def hide(self, request, pk=None):
        instance = self.get_object()
        if not request.user.is_superuser and instance.status != StatusChoices.ACTIVE:
            return Response(status=400, data={"message": "Возможно отключить только активный ресторан"})
        instance.status = StatusChoices.HIDDEN
        instance.save()
        return Response()

    @action(detail=True)
    def activate(self, request, pk=None):
        instance = self.get_object()
        if not request.user.is_superuser and instance.status != StatusChoices.HIDDEN:
            return Response(status=400, data={"message": "Возможно включить только отключенный ресторан"})
        instance.status = StatusChoices.ACTIVE
        instance.save()
        return Response()
