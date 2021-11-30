from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin

from restaurants.models import Category
from restaurants.permissions.category import CategoryManageAccessPolicy
from restaurants.serializers.category import CategoryManageSerializer
from restaurants.views.base import ManageViewSet


class CategoryManageViewSet(AccessViewSetMixin, ManageViewSet):
    """
    Viewset административной панели категории
    """
    access_policy = CategoryManageAccessPolicy
    serializer_class = CategoryManageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'status']

    def get_queryset(self):
        """
        Вывод категорий ресторанов пользователя
        """
        categories = Category.objects.select_related('restaurant')
        if self.request.user.is_superuser:
            return categories
        user_restaurants = self.request.user.restaurants.all()
        return categories.filter(restaurant__in=user_restaurants)
