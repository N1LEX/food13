from rest_access_policy import AccessViewSetMixin

from restaurants.models import ProductPortion
from restaurants.permissions.product_portion import ProductPortionManageAccessPolicy
from restaurants.serializers.product_portion import ProductPortionManageSerializer
from restaurants.views.base import ManageViewSet


class ProductPortionManageViewSet(AccessViewSetMixin, ManageViewSet):
    access_policy = ProductPortionManageAccessPolicy
    serializer_class = ProductPortionManageSerializer

    def get_queryset(self):
        """
        Вывод только порций ресторана пользователя
        """
        product_portions = ProductPortion.objects.all()
        if self.request.user.is_superuser:
            return product_portions
        return product_portions.select_related('product', 'product__category')\
            .filter(product__category__restaurant__in=self.request.user.restaurants.all())
