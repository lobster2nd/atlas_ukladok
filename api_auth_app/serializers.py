from datetime import datetime, timedelta

from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api_profile_app.models import User
from .models import UserCodeVerify


def check_attempts_cnt(address: str):
    """Проверка количества попыток входа"""

    obj = UserCodeVerify.objects.filter(address=address)
    if obj and \
        obj.first().attempts_cnt == 0 and \
        obj.first().access_at > (datetime.now() - timedelta(hours=12)):
        raise Exception({'error': 'Количество попыток исчерпано.'
                                  'Попробуйте через 12 часов'})

    elif obj and obj.first().attempts_cnt == 0:
        UserCodeVerify.objects.filter(
            address=address).update(
            attempts_cnt=3, access_at=None)


class CreateCodeSerializer(serializers.Serializer):
    address = serializers.EmailField(required=True,
                                     help_text='куда прислать код')


# class CreateCodeSerializer(ModelSerializer):
#     """Создание кода подтверждения"""
#
#     address = serializers.CharField(help_text='Куда направлен код')
#
#     class Meta:
#         model = UserCodeVerify
#         fields = ('address', )
#
#     def validate(self, attrs):
#         start_period = datetime.now() - timedelta(hours=12)
#         if UserCodeVerify.objects.filter(created_at__gte=start_period,
#                                          address=attrs['address']).count() > 1:
#             raise ValidationError({'error': 'Лимит запросов исчерпан'})
#         return attrs
#
#
# class GetUserTokenSerializer(TokenObtainPairSerializer):
#     """Выдать токен по логину"""
#
#     def __init__(self, username):
#         self.user = User.objects.get(username=username)
#
#     def get(self):
#         data = dict()
#
#         check_attempts_cnt(self.user.username)
#
#         refresh = self.get_token(self.user)
#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)
#
#         update_last_login(None, self.user)
#
#         return data
#
#
# class GetFromCodeTokenSerializer(ModelSerializer):
#     """Выдача токена по подноразовому коду"""
#
#     address = serializers.CharField(help_text='Куда пришел код')
#     code = serializers.CharField(help_text='Код')
#
#     class Meta:
#         model = UserCodeVerify
#         fields = ['address', 'code']
#
#     def validate(self, attrs):
#
#         address = attrs.get('address')
#         user = User.objects.filter(username=address).first()
#         password = f'{address}'
#
#         if not user:
#             user = User.objects.create_user(
#                 username=address,
#                 password=password,
#             )
#             user.save()
#
#         refresh = GetUserTokenSerializer(username=address).get()
#
#         return refresh
