from random import randint

from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from core import settings
from .models import UserCodeVerify
from .serializers import CreateCodeSerializer


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
