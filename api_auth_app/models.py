from django.db import models


class UserCodeVerify(models.Model):
    """Код подтверждения"""
    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    address = models.CharField(max_length=256, verbose_name='адрес')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания')
    access_at = models.DateTimeField(
        verbose_name='Время последней неудачной попытки',
        default=None, null=True, blank=True)
    attempts_cnt = models.IntegerField(
        default=3, verbose_name='Количество попыток')

    def __str__(self):
        return f'{self.address}'
