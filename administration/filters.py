import django_filters
from projects.models import Case


class CaseFilter(django_filters.FilterSet):
    class Meta:
        model = Case
        fields = ['type']