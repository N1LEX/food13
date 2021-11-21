from rest_access_policy import AccessViewSetMixin

from core.viewsets import CustomModelViewSet
from restaurants.models import Kitchen
from restaurants.permissions.kitchen import KitchenAccessPolicy
from restaurants.serializers.kitchen import KitchenSerializer


class KitchenViewSet(AccessViewSetMixin, CustomModelViewSet):
    """
    Viewset кухни
    """
    queryset = Kitchen.objects.all()
    access_policy = KitchenAccessPolicy
    serializer_class = KitchenSerializer
