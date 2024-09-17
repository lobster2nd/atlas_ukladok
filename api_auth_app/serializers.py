from rest_framework import serializers


class CreateCodeSerializer(serializers.Serializer):
    address = serializers.EmailField(required=True,
                                     help_text='куда прислать код')


class VerifyCodeSerializer(serializers.Serializer):
    address = serializers.EmailField(required=True,
                                     help_text='куда пришёл код')
    code = serializers.CharField(max_length=4,
                                 help_text='код из сообщения')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, help_text='refresh токен')
