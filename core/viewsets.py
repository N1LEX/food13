from rest_framework import viewsets, mixins
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class CustomGenericViewSet(viewsets.GenericViewSet):
    serializer_classes = None

    def get_serializer_class(self):
        """
            Return the class to use for the serializer.
            Defaults to using `self.serializer_class`.

            You may want to override this if you need to provide different
            serializations depending on the incoming request.

            (Eg. admins get full serialization, others get basic serialization)
        """
        serializer_class = self.serializer_class

        if self.serializer_classes:
            serializer_class = self.serializer_classes.get(self.suffix, self.serializer_classes['List'])

        assert serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute or `serializer_classes`"
                % self.__class__.__name__
        )
        return serializer_class


class CustomModelViewSet(ModelViewSet, CustomGenericViewSet):
    pass


class CustomReadOnlyModelViewSet(ReadOnlyModelViewSet, CustomGenericViewSet):
    pass


class CustomRetrieveViewSet(mixins.RetrieveModelMixin, CustomGenericViewSet):
    pass
