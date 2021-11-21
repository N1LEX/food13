from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import CustomReadOnlyModelViewSet, CustomModelViewSet
from restaurants.consts import StatusChoices
from restaurants.models import Restaurant
from restaurants.permissions.restaurant import RestaurantManageAccessPolicy
from restaurants.serializers.restaurant import RestaurantListSerializer, RestaurantInstanceSerializer, \
    RestaurantManageSerializer


class RestaurantReadOnlyViewSet(CustomReadOnlyModelViewSet):
    """
    Read only viewset ресторана
    """
    queryset = Restaurant.object.active()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kitchen']
    serializer_classes = {
        'List': RestaurantListSerializer,
        'Instance': RestaurantInstanceSerializer,
    }


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
            return Restaurant.object.prefetch_related('kitchen')
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
