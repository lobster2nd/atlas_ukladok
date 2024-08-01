from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Placement, Image
from api_profile_app.serializers import ProfileUserSerializer
from api_profile_app.models import User


class PlacementSerializer(ModelSerializer):
    author = type('AuthorSerializer', (serializers.SerializerMethodField,
                                       ProfileUserSerializer), dict())(
                                       read_only=True,
                                       help_text='Автор')

    class Meta:
        model = Placement
        fields = [
            'id',
            'title',
            'content',
            'video_link',
            'is_published',
            'author',
            'images',
        ]

    @staticmethod
    def get_author(instance):
        author = User.objects.filter(placements=instance).first()
        if author:
            return ProfileUserSerializer(author).data
        return None


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
