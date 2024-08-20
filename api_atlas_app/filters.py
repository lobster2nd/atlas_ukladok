import django_filters

from .models import Placement

class PlacementFilter(django_filters.FilterSet):
    class Meta:
        model = Placement
        fields = {
            'body_part': ['exact']
        }
