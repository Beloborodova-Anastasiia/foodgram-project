from rest_framework import serializers
from users.models import User, Subscribe
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(author=obj, user=user).exists()


class GetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        if 'email' in data and 'password' in data:
            if User.objects.filter(email=data['email']).exists():
                user = get_object_or_404(User, email=data['email'])
                username = user.username
                user = authenticate(
                    username=username,
                    password=data['password']
                )
                if user:
                    if not user.is_active:
                        message = 'User account is disabled.'
                        raise serializers.ValidationError(message)
                else:
                    message = 'Invalid password.'
                    raise serializers.ValidationError(message)
            else:
                message = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(message)
        else:
            message = 'Must include "email and "password".'
            raise serializers.ValidationError(message)
        return data


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

