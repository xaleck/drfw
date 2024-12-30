import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    currency = django_filters.CharFilter(field_name='currency', lookup_expr='iexact')  # Case-insensitive exact match
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')  # Case-insensitive exact match

    class Meta:
        model = Event
        fields = ['currency', 'type']
