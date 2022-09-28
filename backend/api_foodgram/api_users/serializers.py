from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import Subscribe, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        print(self.context)
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(author=obj, user=user).exists()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )
