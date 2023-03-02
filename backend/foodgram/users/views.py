from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Subscription, User
from .serializers import SubscriptionListSerializer


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer
    permission_classes = [IsAuthenticated]

class SubscriptionList(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer