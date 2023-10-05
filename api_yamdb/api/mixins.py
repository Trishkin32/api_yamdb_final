from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import MethodNotAllowed


class GetListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для методов Get, List, Create, Delete."""

    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GetPatchCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для запросов GET, PATCH, POST, DELETE."""

    def update(self, *args, **kwargs):
        raise MethodNotAllowed('POST', detail='Use PATCH')

    def partial_update(self, *args, **kwargs):
        return super().update(*args, **kwargs, partial=True)
