from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet,
                    SubscriptionActionViewSet, SubscriptionViewSet, TagViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('ingredients',
                   IngredientViewSet,
                   basename='ingredients')
router_v1.register('tags',
                   TagViewSet,
                   basename='tags')
router_v1.register('recipes',
                   RecipeViewSet,
                   basename='recipes')
router_v1.register('users/subscriptions',
                   SubscriptionViewSet,
                   basename='users_subscriptions')
router_v1.register('users',
                   SubscriptionActionViewSet,
                   basename='users_subscribe_action')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
