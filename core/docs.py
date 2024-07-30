from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Атлас укладок Кишковского",
        default_version='v1',
        description="Методы для работы с API",
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

# Добавляем параметры безопасности для JWT токена
schema_view._security = [{'Bearer': []}]
schema_view._manual_parameters = [
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING)
]

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
