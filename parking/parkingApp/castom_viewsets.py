from rest_framework import viewsets, mixins


class NonReadableViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    pass

class CreateOnlyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
