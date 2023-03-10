from django_filters import filters, FilterSet

from recipes.models import Ingredient


class IngredientFilter(FilterSet):
    """Фильтр ингредиентов по наименованию."""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', )
