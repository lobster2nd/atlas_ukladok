import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Placement, Image
from api_profile_app.serializers import ProfileUserSerializer
from api_profile_app.models import User


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo', 'description', 'placement']



class PlacementSerializer(ModelSerializer):
    author = type('AuthorSerializer', (serializers.SerializerMethodField,
                                       ProfileUserSerializer), dict())(
                                       read_only=True,
                                       help_text='Автор')
    images = type('ImagesSerializer', (serializers.SerializerMethodField,
                                       ImageSerializer), dict())(
                                        read_only=True,
                                        help_text='Иллюстрация'
    )

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

    def validate(self, data):
        photo = data.get('photo')
        if photo:
            ext = os.path.splitext(photo.name)[1].lower()
            valid_extensions = ['.jpeg', 'jpg', '.pdf', '.png']
            if ext not in valid_extensions:
                raise ValidationError(
                    {'error': 'Допустимые форматы: jpg, jpeg, pdf, png'},
                    400)

        return data

    @staticmethod
    def get_author(instance):
        author = User.objects.filter(placements=instance).first()
        if author:
            return ProfileUserSerializer(author).data
        return None

    @staticmethod
    def get_images(instance):
        images = Image.objects.filter(placement=instance)
        return  ImageSerializer(images, many=True).data

