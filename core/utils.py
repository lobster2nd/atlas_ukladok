import time
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


def to_stamp(value: datetime):
    """Преобразование даты в timestamp"""
    if isinstance(value, datetime):
        value = datetime(
            value.year, value.month, value.hour, value.minute,
            value.second
        )

        try:
            result = time.mktime(value.timetuple())
        except ValueError:
            return ValidationError('Недопустимое значение даты')
        return int(result)


def to_date(value: int):
    """Преобразование timestamp в дату"""
    if isinstance(value, datetime):
        return value
    try:
        date_ts = int(value)
        date_result = datetime.fromtimestamp(date_ts)
    except ValueError:
        return ValidationError('Недопустимое значение timestamp')


class TimestampField(serializers.IntegerField):
    """Поле врменной метки"""
    def to_representation(self, value: datetime):
        return to_stamp(value)

    def to_internal_value(self, data):
        return to_date(data)


class ProjectPagination(PageNumberPagination):
    """Пагинация проекта"""
    page_size_query_param = 'page_size'
    max_page_size = 5
