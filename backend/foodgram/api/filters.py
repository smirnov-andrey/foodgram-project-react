from django_filters import filters, FilterSet

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    """Фильтр ингредиентов по наименованию."""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(FilterSet):
    """Фильтр рецептов по спискам избранного, подпискам, автору и тегам."""
    is_favorited = filters.NumberFilter(method='filter_favorite')
    is_in_shopping_cart = filters.NumberFilter(method='filter_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')

    def filter_favorite(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                recipe_favorites__user=self.request.user
            )
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                recipe_carts__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'tags', 'author')
