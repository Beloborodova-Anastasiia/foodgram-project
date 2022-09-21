# from django.shortcuts import get_object_or_404
import imp
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.response import Response
from rest_framework.decorators import action, api_view

# from rest_framework.permissions import SAFE_METHODS

from recipes.models import Ingredient, Recipe, Tag, IngredientRecipe, Favorite
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, IngredientRecipeSerializer,
                          )
from .permissions import AuthorOrAdmin
from users.models import User

class RetriveListCreateDeleteUpdateViewSet(mixins.RetrieveModelMixin,
                                           mixins.ListModelMixin,
                                           mixins.CreateModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.DestroyModelMixin,
                                           viewsets.GenericViewSet):
    pass


class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer


class FavoriteFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user=request.user
        querys = Favorite.objects.filter(user=user)
        # groups = groups.objects.filter(item__in=items).distinct().values_list('name', flat=True)

        recipes = Recipe.objects.filter(id__in=querys.values_list('recipe',))
        # rec = user.favorite.all()
        print(user, querys.values_list('recipe',))
        print(recipes)
        # posts = Post.objects.filter(author__following__user=request.user)

        # return request.user.favorite.all()
        return recipes

class RecipeViewSet(RetriveListCreateDeleteUpdateViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrAdmin]
    serializer_class = RecipeSerializer
    # filter_backends = (DjangoFilterBackend, FavoriteFilterBackend)
    filterset_fields = ('author', 'tags', 'favorite')

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     print(self.kwargs)
    #     if 'favorite' in self.kwargs:
    #         queryset = queryset.favoreted.all()
    #     if 'shopping_cart' in self.kwargs:
    #         queryset = queryset.shopping.all()
    #     return queryset
    # def get_filter_backends

class Favorited(CreateDeleteViewSet):
    queryset = Favorite.objects.all()
    permission_classes = [IsAuthenticated]
                                                                                                                


