from rest_framework import viewsets, mixins, status

from .models import Placement
from .serializers import PlacementSerializer


class PlacementModelViewSet(
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    """Работа с укладками"""

    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer

    def list(self, request, *args, **kwargs):
        """
        Получить список укладок

        Получить список укладок
        """
        return super().list(request, args, kwargs)
