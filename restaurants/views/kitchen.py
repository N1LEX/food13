from rest_access_policy import AccessViewSetMixin

from core.viewsets import CustomReadOnlyModelViewSet
from restaurants.models import Kitchen
from restaurants.permissions.kitchen import KitchenManageAccessPolicy
from restaurants.serializers.kitchen import KitchenSerializer, KitchenManageSerializer
from restaurants.views.base import ManageViewSet


class KitchenViewSet(CustomReadOnlyModelViewSet):
    """
    Публичный viewset кухни
    """
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class KitchenManageViewSet(AccessViewSetMixin, ManageViewSet):
    """
    Viewset кухни в административной панели
    """
    queryset = Kitchen.objects.all()
    access_policy = KitchenManageAccessPolicy
    serializer_class = KitchenManageSerializer
