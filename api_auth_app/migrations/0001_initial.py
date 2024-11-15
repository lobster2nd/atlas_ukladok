# Generated by Django 5.0.7 on 2024-07-30 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCodeVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=256, verbose_name='адрес')),
                ('code', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('access_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время последней неудачной попытки')),
                ('attempts_cnt', models.IntegerField(default=3, verbose_name='Количество попыток')),
            ],
            options={
                'verbose_name': 'Код подтверждения',
                'verbose_name_plural': 'Коды подтверждения',
            },
        ),
    ]
