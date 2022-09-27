from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api_foodgram.constants import PATH_SUBSCRIBE, PATH_SUBSCRIPTIONS
from api_recipes.serializers import SubscribtionSerializer
from users.models import Subscribe, User

from .serializers import CustomUserSerializer


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if PATH_SUBSCRIPTIONS in self.request.path:
            user = self.request.user
            subscriptions = Subscribe.objects.filter(user=user)
            return User.objects.filter(
                id__in=subscriptions.values_list('author',)
            )
        return User.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if (PATH_SUBSCRIPTIONS in self.request.path
                or PATH_SUBSCRIBE in self.request.path):
            return SubscribtionSerializer
        return CustomUserSerializer

    @action(
        methods=['get', ],
        detail=False,
        url_path='subscriptions',
        permission_classes=[IsAuthenticated]
    )
    def subsctiptions(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=PATH_SUBSCRIBE,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        author = get_object_or_404(
            User,
            id=self.kwargs.get('author_id'),
        )
        user = request.user
        if request.method == 'POST':
            if Subscribe.objects.filter(user=user, author=author).exists():
                context = {
                    'errors': 'Вы уже подписаны на этого автора'
                }
                return Response(
                    context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user == author:
                context = {
                    'errors': 'Вы не можете подписаться на самого себя'
                }
                return Response(
                    context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscribe.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Subscribe.objects.filter(user=user, author=author).exists():
                Subscribe.objects.filter(
                    user=user, author=author
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            context = {
                'errors': 'Вы не подписаны на этого автора'
            }
            return Response(
                context,
                status=status.HTTP_400_BAD_REQUEST
            )
