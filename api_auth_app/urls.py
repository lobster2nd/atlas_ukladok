from django.urls import path

from .views import CreateCodeViewSet, VerifyCodeViewSet

urlpatterns = [
    path('send_code/', CreateCodeViewSet.as_view(
        {'post': 'create'}), name='send_code'),
    path('get_token/', VerifyCodeViewSet.as_view(
        {'post': 'create'}), name='get_token'
         )
]
