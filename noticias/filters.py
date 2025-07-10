import django_filters
from .models import Noticia

class NoticiaFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(field_name='data_publicacao', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data_publicacao', lookup_expr='lte')
    categoria = django_filters.CharFilter(field_name='categoria__nome', lookup_expr='iexact')
    subcategoria = django_filters.CharFilter(field_name='subcategoria__nome', lookup_expr='iexact')
    urgente = django_filters.BooleanFilter(field_name='urgente')
    tags = django_filters.CharFilter(method='filter_tags')

    class Meta:
        model = Noticia
        fields = ['categoria', 'subcategoria', 'urgente', 'data_inicio', 'data_fim', 'tags']

    def filter_tags(self, queryset, name, value):
        tags = [tag.strip() for tag in value.split(',')]
        return queryset.filter(tags__nome__in=tags).distinct()
