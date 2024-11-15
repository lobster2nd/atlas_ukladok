# Generated by Django 5.0.7 on 2024-07-31 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название укладки')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/images', verbose_name='Иллюстрация')),
                ('video_link', models.URLField(blank=True, null=True, verbose_name='Видео')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('body_part', models.CharField(blank=True, choices=[('head', 'голова'), ('spine', 'позвоночник'), ('limbs', 'конечности'), ('thorax', 'грудь'), ('abdomen', 'живот')], max_length=7, null=True, verbose_name='часть тела')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Укладка',
                'verbose_name_plural': 'Укладки',
                'ordering': ['title'],
            },
        ),
    ]
