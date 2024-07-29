from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserModelViewSet

router = DefaultRouter()

router.register('profile', UserModelViewSet, basename='profile')

urlpatterns = [
    path('v1/auth/profile/', UserModelViewSet.as_view({'get': 'retrieve'}),
         name='profile-detail'),
]
