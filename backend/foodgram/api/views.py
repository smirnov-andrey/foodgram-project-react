from django.db.models import Sum
from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated

from .filters import IngredientFilter
from .mixins import AddRemoveListMixin
from .permissions import AllowAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeSerializer, SubscriptionListSerializer,
                          TagSerializer)
from recipes.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCarts,
                            Tag, User)
from users.models import Subscription


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Возвращает имеющиеся в базе ингредиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    permission_classes = (AllowAny,)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Возвращает имеющиеся в базе теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet, AddRemoveListMixin):
    """Обрабатывает запоросы по работе с рецептами GET, POST, PATCH, DELETE."""
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (AllowAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def get_queryset(self):
        tags = self.request.query_params.getlist('tags')
        user = self.request.user
        queryset = Recipe.objects
        if tags:
            queryset = queryset.filtered_by_tags(tags)
        queryset = queryset.add_user_annotations(user.pk)
        if self.request.query_params.get('is_favorited'):
            queryset = queryset.filter(is_favorited=True)
        if self.request.query_params.get('is_in_shopping_cart'):
            queryset = queryset.filter(is_in_shopping_cart=True)
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author=author)
        return queryset

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<requested_id>\d+)/favorite',
        url_name='recipe_favorite')
    def favorite(self, request, requested_id=None):
        return self.add_remove_to_list(
            requested_id=requested_id,
            field_name='recipe',
            target_model=FavoriteRecipes,
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<requested_id>\d+)/shopping_cart',
        url_name='recipe_favorite')
    def shopping_cart(self, request, requested_id=None):
        return self.add_remove_to_list(
            requested_id=requested_id,
            field_name='recipe',
            target_model=ShoppingCarts,
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'download_shopping_cart',
        url_name='download_shopping_cart')
    def download_shopping_cart(self, request):
        """Возвращает список покупок рецептам в корзине пользователя."""
        queryset = (
            Ingredient.objects
            .prefetch_related('ingredient_in_recipes__recipe__recipe_carts')
            .filter(
                ingredient_in_recipes__recipe__recipe_carts__user=request.user)
            .annotate(amount=Sum('ingredient_in_recipes__amount'))
            .values('name', 'measurement_unit', 'amount')
            .order_by('name')
        )
        response = HttpResponse(content_type='text/plain')
        for data in queryset:
            response.write(
                f'''{data['name']} - {data['amount']} '''
                f'''{data['measurement_unit']}\n'''
            )
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping-list.txt"')
        return response


class SubscriptionViewSet(viewsets.ModelViewSet, AddRemoveListMixin):
    """Возвращает список текщих подпискок пользователя."""
    serializer_class = SubscriptionListSerializer
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(subscribers__user=self.request.user)


class SubscriptionActionViewSet(viewsets.ViewSet, AddRemoveListMixin):
    """Обрабатывает действия с подписками"""
    http_method_names = ('post', 'delete')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return SubscriptionListSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<requested_id>\d+)/subscribe',
        url_name='user_subscribe')
    def subscribe(self, request, requested_id=None):
        return self.add_remove_to_list(
            requested_id=requested_id,
            field_name='author',
            target_model=Subscription,
        )
