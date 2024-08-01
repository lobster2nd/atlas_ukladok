from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Placement, Image
from api_profile_app.serializers import ProfileUserSerializer
from api_profile_app.models import User


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'photo', 'description', 'placement']


class PlacementSerializer(ModelSerializer):
    author = type('AuthorSerializer', (serializers.SerializerMethodField,
                                       ProfileUserSerializer), dict())(
        read_only=True,
        help_text='Автор')
    images = type('ImagesSerializer', (serializers.SerializerMethodField,
                                       ImageSerializer), dict())(
        read_only=True,
        help_text='Иллюстраци')

    class Meta:
        model = Placement
        fields = [
            'id',
            'title',
            'body_part',
            'content',
            'video_link',
            'is_published',
            'author',
            'images',
        ]

    @staticmethod
    def get_author(instance):
        author = User.objects.filter(placements=instance).first()
        return ProfileUserSerializer(author).data if author else []

    @staticmethod
    def get_images(instance):
        image = Image.objects.filter(placement=instance)
        return ImageSerializer(image, many=True).data if image else []
