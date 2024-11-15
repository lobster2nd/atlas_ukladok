from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_profile_app.models import User
from core.utils import TimestampField


class ProfileUserSerializer(ModelSerializer):
    """Сериализатор профиля пользователя"""

    uid = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=False,
                                     help_text='пароль')
    username = serializers.CharField(required=False, help_text='логин',)
    first_name = serializers.CharField(required=False, help_text='имя')
    last_name = serializers.CharField(required=False, help_text='фамилия')
    gender_label = serializers.CharField(source='get_gender_display',
                                         required=False, read_only=True,
                                         help_text="пол")
    birthday = TimestampField(required=False, help_text='дата рождения')
    email = serializers.EmailField(required=False, help_text='e-mail',)
    avatar = serializers.ImageField(read_only=True,
                                    help_text='аватар',
                                    use_url=False)
    avatar_url = serializers.ImageField(source='avatar', read_only=True,
                                        help_text='url-ссылка на аватар',
                                        use_url=True)
    telegram = serializers.CharField(required=False,
                                     help_text='профиль telegram')

    class Meta:
        model = User
        fields = (
            'uid',
            'password',
            'username',
            'first_name',
            'last_name',
            'birthday',
            'email',
            'gender',
            'gender_label',
            'email',
            'telegram',
            'avatar',
            'avatar_url',
        )
