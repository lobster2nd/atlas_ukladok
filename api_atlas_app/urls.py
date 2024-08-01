from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PlacementModelViewSet, ImageModelViewSet

router = DefaultRouter()

router.register('placement', PlacementModelViewSet, basename='placement')

urlpatterns = [
    path('v1/atlas/placement/', PlacementModelViewSet.as_view(
        {'get': 'list', 'post': 'create'}),
         name='placement-list'),
    path('v1/atlas/image/', ImageModelViewSet.as_view(
        {'post': 'create'}, name='image-detail'
    ))
]
