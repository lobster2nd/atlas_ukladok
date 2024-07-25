from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

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


class CreateCodeSerializer(ModelSerializer):
    """Создание кода подтверждения"""

    address = serializers.CharField(help_text='Куда направлен код')

    class Meta:
        model = UserCodeVerify
        fields = ('address', )

    def validate(self, attrs):
        start_period = datetime.now() - timedelta(hours=12)
        if UserCodeVerify.objects.filter(created_at__gte=start_period,
                                         address=attrs['address']).count() > 1:
            raise ValidationError({'error': 'Лимит запросов исчерпан'})
        return attrs
