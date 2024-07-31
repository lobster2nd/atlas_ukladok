from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PlacementModelViewSet

router = DefaultRouter()

router.register('placement', PlacementModelViewSet, basename='placement')

urlpatterns = [
    path('v1/atlas/placement/', PlacementModelViewSet.as_view(
        {'get': 'list'}),
         name='placement-list'),
]
