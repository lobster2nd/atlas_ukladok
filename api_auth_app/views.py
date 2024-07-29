from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from core import settings
from .serializers import CreateCodeSerializer


# class CreateCodeModelViewSet(mixins.CreateModelMixin, GenericViewSet):
#     """
#     Получить код подтверждения
#
#     Получить код подтверждения
#     """
#     permission_classes = [AllowAny, ]
#     serializer_class = CreateCodeSerializer
#     http_method_names = ('post',)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         _ = serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(serializer)
#
#         headers = self.get_success_headers(serializer.validated_data)
#         address = serializer.validated_data['address']
#
#         code = settings.DEFAULT_CODE
