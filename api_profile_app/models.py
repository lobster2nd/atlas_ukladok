from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователя """

    class Meta:
        verbose_name_plural = 'пользователи'
        verbose_name = 'пользователь'

    class Gender(models.TextChoices):
        MALE = ('male', 'Мужчина')
        FEMALE = ('female', 'Женщина')

    uid = models.UUIDField(verbose_name='ид', primary_key=True, default=uuid4)
    username = models.CharField(verbose_name='имя пользователя',
                                help_text='имя пользователя',
                                max_length=250, unique=True)
    avatar = models.ImageField(upload_to='media/users_avatar', blank=True,
                               verbose_name='аватар', null=True,
                               help_text='аватар')
    gender = models.CharField(verbose_name='пол',
                              help_text='пол (male: мужской, female: женский)',
                              max_length=6, choices=Gender.choices, null=True,
                              blank=True)
    birthday = models.DateField(
        verbose_name='дата рождения',
        help_text="дата рождения в формате временной метки",
        null=True, blank=True)
    telegram = models.CharField(verbose_name='профиль telegram',
                                help_text='профиль telegram',
                                max_length=250, blank=True, null=True,
                                unique=True)
    additional_information = models.TextField(
        verbose_name='дополнительная информация',
        blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='время создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='время обновления')

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Используем email в качестве username
        super().save(*args, **kwargs)