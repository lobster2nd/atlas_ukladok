from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_profile_app.models import User
from api_profile_app.serializers import ProfileUserSerializer


class UserModelViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """Работа с моделью пользователя"""
    queryset = User.objects.all()
    serializer_class = ProfileUserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(pk=self.request.user.pk).first()
        else:
            raise PermissionDenied({'error': 'Необходимо авторизироваться'})

    def get_object(self):
        return self.get_queryset()

    def retrieve(self, request, *args, **kwargs):
        """
        Информация о текущем пользователе

        Информация о текущем пользователе
        """
        return super().retrieve(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """
        Зарегистрировать нового пользователя

        Зарегистрировать нового пользователя
        """
        username = request.data.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            # serializer = self.get_serializer(user)
            return Response(
                {'error': 'Такой пользователь уже существует'}, 400)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

            try:
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Редактировать профиль

        Редактировать профиль
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'password' in request.data:
            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
