from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PlacementModelViewSet, ImageModelViewSet

router = DefaultRouter()

router.register('placement', PlacementModelViewSet, basename='placement')
router.register('image', ImageModelViewSet, basename='image')

urlpatterns = [
    path('v1/atlas/', include(router.urls)),
]
