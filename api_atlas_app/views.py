from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, FormParser, \
    FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


from core.utils import ProjectPagination
from .models import Placement, Image
from .serializers import PlacementSerializer, ImageSerializer


class PlacementModelViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    """Работа с укладками"""

    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer
    pagination_class = ProjectPagination

    def list(self, request, *args, **kwargs):
        """
        Получить список укладок

        Получить список укладок
        """
        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """
        Добавить укладку

        Добавить укладку
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        author = self.request.user
        return serializer.save(author=author)


class ImageModelViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Работа с иллюстрациями"""

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    pagination_class = ProjectPagination

    def create(self, request, *args, **kwargs):
        """
        Добавить новую иллюстрацию

        Добавить новую иллюстрацию
        """
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удалить иллюстрацию по ID

        Удалить иллюстрацию по ID
        """
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Объект не найден'})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
