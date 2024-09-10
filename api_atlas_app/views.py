from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status, filters
from rest_framework.parsers import MultiPartParser, FormParser, \
    FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from api_profile_app.models import User
from core.utils import ProjectPagination
from .filters import PlacementFilter
from .models import Placement, Image
from .serializers import PlacementSerializer, ImageSerializer


class PlacementModelViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    """Работа с укладками"""

    queryset = Placement.objects.filter(is_published=True)
    serializer_class = PlacementSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PlacementFilter
    pagination_class = ProjectPagination
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

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
        if self.request.user.is_authenticated:
            author = self.request.user

        elif 'tg_user' in self.request.data:
            author, created = User.objects.get_or_create(
                username=self.request.data["tg_user"]
            )
            if created:
                author.set_password('password')
                author.save()
        else:
            author, created = User.objects.get_or_create(
                username='Неизвестный пользователь')

            if created:
                author.set_password('password')
                author.save()
        return serializer.save(author=author)

    def retrieve(self, request,  *args, **kwargs):
        """
        Получить укладку по id

        Получить укладку по id
        """
        return super().retrieve(request, *args, **kwargs)


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
        photos = request.FILES.getlist('photo')  # Получаем список изображений
        description = request.data.get('description')
        placement_id = request.data.get('placement')

        placement = get_object_or_404(Placement, id=placement_id)

        if not photos:
            return Response({"error": "Нет изображений."},
                            status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        for photo in photos:
            image_instance = Image(photo=photo, description=description,
                                   placement=placement)
            image_instance.save()
            created_images.append(image_instance)

        serializer = self.get_serializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
