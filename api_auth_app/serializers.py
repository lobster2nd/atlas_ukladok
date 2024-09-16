from rest_framework import serializers


class CreateCodeSerializer(serializers.Serializer):
    address = serializers.EmailField(required=True,
                                     help_text='куда прислать код')


class VerifyCodeSerializer(serializers.Serializer):
    address = serializers.EmailField(required=True,
                                     help_text='куда пришёл код')
    code = serializers.CharField(max_length=4)
