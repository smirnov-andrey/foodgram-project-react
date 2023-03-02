from django.urls import include, path

from .views import SubscriptionList, SubscriptionViewSet


app_name = 'users'

urlpatterns = [
    path('users/subscriptions/', SubscriptionList.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('users/subscriptions/', SubscriptionList.as_view())
         # SubscriptionViewSet.as_view({'get': 'list'}),
         # name='subscription-list'
         # ),


]