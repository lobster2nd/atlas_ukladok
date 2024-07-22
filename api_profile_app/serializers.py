from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_profile_app.models import User


class ProfileUserSerializer(ModelSerializer):

    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(required=False,
                                     help_text='логин',
                                     read_only=True)
    first_name = serializers.CharField(required=False, help_text='имя')
    last_name = serializers.CharField(required=False, help_text='фамилия')
    gender_label = serializers.CharField(source='get_gender_display',
                                         required=False, read_only=True,
                                         help_text="пол")
    birthday = serializers.DateTimeField(required=False,
                                         help_text='дата рождения')
    email = serializers.EmailField(required=False, help_text='e-mail')
    avatar = serializers.ImageField(read_only=True,
                                    help_text='аватар',
                                    use_url=False)
    avatar_url = serializers.ImageField(source='avatar', read_only=True,
                                        help_text='url-ссылка на аватар',
                                        use_url=True)

    class Meta:
        model = User
        fields = (
            'uid',
            'username',
            'nickname',
            'first_name',
            'last_name',
            'birthday',
            'email',
            'gender',
            'gender_label',
            'email',
            'avatar',
            'avatar_url',
        )
