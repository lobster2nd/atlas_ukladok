from datetime import datetime, timedelta
from random import randint

from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_profile_app.models import User
from core import settings
from .models import UserCodeVerify
from .serializers import CreateCodeSerializer, VerifyCodeSerializer, \
    RefreshTokenSerializer


def send_confirmation_code(user_address, confirmation_code):
    """Отправка кода подтверждения"""
    subject = 'Код подтверждения'
    message = f'Для входа на сайт введите код {confirmation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_address]

    send_mail(subject, message, from_email, recipient_list)


class CreateCodeViewSet(mixins.CreateModelMixin, GenericViewSet):

    permission_classes = (AllowAny, )
    serializer_class = CreateCodeSerializer
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        """
        Получить код подтверждения


        Получить код подтверждения
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.validated_data.get('address')

        code = randint(1000, 9999)

        # Обновляем старую запись если есть
        UserCodeVerify.objects.filter(address=address).update(code=code)
        # Обновляем новую запись если есть для контроля
        UserCodeVerify.objects.create(address=address, code=code)

        try:
            send_confirmation_code(address, code)
            return Response(
                {"message": f"Код подтверждения отправлен на {address}"},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyCodeViewSet(mixins.CreateModelMixin, GenericViewSet):
    """Проверка кода подтверждения"""
    permission_classes = (AllowAny, )
    serializer_class = VerifyCodeSerializer
    http_method_names = ('post', )

    def create(self, request, *args, **kwargs):
        """
        Получение токенов

        Получение токенов
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.validated_data['address']
        code = serializer.validated_data['code']

        user_address = UserCodeVerify.objects.filter(address=address).first()

        if not user_address:
            return Response({'error': 'Запросите код ещё раз'},
                            status=status.HTTP_404_NOT_FOUND)

        elif user_address.attempts_cnt == 0 or \
                user_address.access_at and timezone.now() - user_address.access_at > timedelta(hours=12):
            return Response({'error': 'Количество попыток исчерпано. '
                                            'Попробуйте через 12 часов'},
                            status=status.HTTP_403_FORBIDDEN)

        elif user_address.code != code:
            user_address.attempts_cnt -= 1
            user_address.access_at = datetime.now()
            user_address.save()
            if user_address.attempts_cnt == 0:
                return Response({'error': 'Количество попыток исчерпано. '
                                          'Попробуйте через 12 часов'},
                                status=status.HTTP_403_FORBIDDEN)
            return Response({'error': f'Неверный код. '
                             f'Попыток осталось: {user_address.attempts_cnt}'},
                            status=status.HTTP_403_FORBIDDEN)

        elif user_address.code == code:
            user, created = User.objects.get_or_create(email=address)
            user_address.delete()
            user.is_active = True
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Что-то не так. Всё сломалось'},
                            status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    """Получение access токена по refresh токену"""
    permission_classes = (AllowAny, )
    serializer_class = RefreshTokenSerializer
    http_method_names = ('post', )

    def create(self, request, *args, **kwargs):
        """
        Получить новый access токен

        Получить новый access токен
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            return Response({'access': new_access_token},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
