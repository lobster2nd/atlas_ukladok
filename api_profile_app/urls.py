from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserModelViewSet

router = DefaultRouter()

router.register('profile', UserModelViewSet, basename='profile')

urlpatterns = [
    path('profile/', UserModelViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update'}), name='profile-detail'),
    path('register/', UserModelViewSet.as_view({'post': 'create'}),
         name='profile-register')
]
