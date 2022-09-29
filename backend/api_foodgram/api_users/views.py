from api_foodgram.constants import (PATH_SUBSCRIBE, PATH_SUBSCRIPTIONS,
                                    SUBSCRIB_IN_PATH)
from api_foodgram.utilits import create_relation, delete_relation
from api_recipes.serializers import SubscribtionSerializer
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import Subscribe, User


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class CustomUserViewSet(UserViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        if PATH_SUBSCRIPTIONS in self.request.path:
            user = self.request.user
            subscriptions = Subscribe.objects.filter(user=user)
            return User.objects.filter(
                id__in=subscriptions.values_list('author',)
            )
        return User.objects.all()

    def get_serializer_class(self):
        if SUBSCRIB_IN_PATH in self.request.path:
            return SubscribtionSerializer
        return super().get_serializer_class()

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
        if request.method == 'POST':
            context, response_status = create_relation(
                request=request,
                model=User,
                relate_model=Subscribe,
                serializer=self.get_serializer(),
                ban_himself=True,
                *args,
                **kwargs
            )
        if request.method == 'DELETE':
            context, response_status = delete_relation(
                request=request,
                model=User,
                relate_model=Subscribe,
                *args,
                **kwargs
            )
        return Response(context, status=response_status)
