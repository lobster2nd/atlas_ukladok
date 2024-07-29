from django.core.exceptions import ValidationError
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_profile_app.models import User
from api_profile_app.serializers import ProfileUserSerializer


class UserModelViewSet(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    Работа с моделью пользователя

    Работа с моделью пользователя
    """
    queryset = User.objects.all()
    serializer_class = ProfileUserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(pk=self.request.user.pk).first()
        else:
            raise PermissionDenied({'error': 'Необходимо авторизироваться'})

    def get_object(self):
        return self.get_queryset()


    # def create(self, request, *args, **kwargs):
    #     """
    #     Реактирование/получение профиля текущего пользователя
    #
    #     Реактирование/получение профиля текущего пользователя
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     _ = serializer.is_valid(raise_exception=True)
    #     try:
    #         instance = self.get_object()
    #         if instance and kwargs:
    #             return super().update(request, pk=instance.pk, **kwargs)
    #         elif instance:
    #             return super().retrieve(request, pk=request.pk)
    #         else:
    #             return super().create(request, *args, **kwargs)
    #
    #     except ValidationError as e:
    #         return Response({'error': e.messages[0]},
    #                         status=400)
