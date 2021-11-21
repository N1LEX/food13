from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.viewsets import CustomModelViewSet
from restaurants.consts import StatusChoices
from restaurants.models import Category
from restaurants.permissions.category import CategoryManageAccessPolicy
from restaurants.serializers.category import CategoryRetrieveSerializer, CategoryManageSerializer


class CategoryRetrieveViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """
    View объекта категории
    """
    queryset = Category.objects.active().filter(restaurant__status=StatusChoices.ACTIVE).prefetch_related('products')
    serializer_class = CategoryRetrieveSerializer


class CategoryManageViewSet(AccessViewSetMixin, CustomModelViewSet):
    """
    Viewset административной панели категории
    """
    access_policy = CategoryManageAccessPolicy
    serializer_class = CategoryManageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'status']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Category.objects.select_related('restaurant')
        user_restaurants = self.request.user.restaurants.all()
        return Category.objects.select_related('restaurant').filter(restaurant__in=user_restaurants)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            serializer.save(status=StatusChoices.CHECK)
        serializer.save()

    @action(detail=True)
    def hide(self, request, pk=None):
        instance = self.get_object()
        if not request.user.is_superuser and instance.status != StatusChoices.ACTIVE:
            return Response(status=400, data={"message": "Возможно отключить только активную категорию"})
        instance.status = StatusChoices.HIDDEN
        instance.save()
        return Response()

    @action(detail=True)
    def activate(self, request, pk=None):
        instance = self.get_object()
        if not request.user.is_superuser and instance.status != StatusChoices.HIDDEN:
            return Response(status=400, data={"message": "Возможно включить только отключенную категорию"})
        instance.status = StatusChoices.ACTIVE
        instance.save()
        return Response()
