from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related('restaurant').filter(is_active=True)
    serializer_class = UserSerializer
