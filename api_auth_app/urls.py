from django.urls import path

from .views import CreateCodeViewSet, VerifyCodeViewSet, RefreshTokenViewSet

urlpatterns = [
    path('send_code/', CreateCodeViewSet.as_view(
        {'post': 'create'}), name='send_code'),
    path('token/get_tokens/', VerifyCodeViewSet.as_view(
        {'post': 'create'}), name='get_tokens'),
    path('token/refresh/', RefreshTokenViewSet.as_view(
        {'post': 'create'}), name='refresh'),
]
