from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import CustomModelViewSet
from restaurants.consts import StatusChoices


class ManageViewSet(CustomModelViewSet):
    """
    Общий viewset для моделей ресторана в административной панели
    """
    @action(detail=True)
    def hide(self, request, pk=None):
        instance = self.get_object()
        if not request.user.is_superuser and instance.status != StatusChoices.ACTIVE:
            return Response(status=400, data={"message": "Возможно отключить только активный объект"})
        instance.status = StatusChoices.HIDDEN
        instance.save()
        return Response()

    @action(detail=True)
    def activate(self, request, pk=None):
        instance = self.get_object()
        if not request.user.is_superuser and instance.status != StatusChoices.HIDDEN:
            return Response(status=400, data={"message": "Возможно активировать только отключенный объект"})
        instance.status = StatusChoices.ACTIVE
        instance.save()
        return Response()

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            serializer.save(status=StatusChoices.CHECK)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == StatusChoices.HIDDEN:
            return super().destroy(request, args, kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Возможно удалить только скрытый объект'})
