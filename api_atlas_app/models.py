from django.db import models

from api_profile_app.models import User


class Placement(models.Model):
    """Модель укладки"""

    class Meta:
        verbose_name = 'Укладка'
        verbose_name_plural = 'Укладки'
        ordering = ['title']

    class BodyPart(models.TextChoices):
        HEAD = ('head', 'голова')
        SPINE = ('spine', 'позвоночник')
        LIMBS = ('limbs', 'конечности')
        THORAX = ('thorax', 'грудь')
        ABDOMEN = ('abdomen', 'живот')

    title = models.CharField(max_length=255, verbose_name='Название укладки')
    content = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to="media/images", blank=True, null=True,
                              verbose_name='Иллюстрация')
    video_link = models.URLField(blank=True, null=True, verbose_name='Видео')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='время создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='время обновления')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.PROTECT)
    body_part = models.CharField(choices=BodyPart.choices, blank=True,
                                 null=True, verbose_name='часть тела')

    def __str__(self):
        return self.title
