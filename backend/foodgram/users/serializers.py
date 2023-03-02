from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request', None).user
        if current_user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=current_user,
            author=obj
        ).exists()


class SubscriptionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
