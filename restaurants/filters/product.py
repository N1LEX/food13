from django_filters import FilterSet

from core.filters import NumberInFilter
from restaurants.models import Product


class ProductFilter(FilterSet):
    category = NumberInFilter(field_name='category', lookup_expr='in')

    def filter_category(self, queryset, name, value):
        return super().filter_category(queryset, name, value).select_related('category')

    class Meta:
        model = Product
        fields = ['category', 'is_available']
