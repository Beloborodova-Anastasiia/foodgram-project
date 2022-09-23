# from django.shortcuts import get_object_or_404
import imp
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.response import Response
from rest_framework.decorators import action, api_view

# from rest_framework.permissions import SAFE_METHODS

from recipes.models import Ingredient, Recipe, Shoping, Tag, IngredientRecipe, Favorite
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, IngredientRecipeSerializer,
                          )
from .permissions import AuthorOrAdmin
from users.models import User
from .filters import RecipeFilter

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


class RecipeViewSet(RetriveListCreateDeleteUpdateViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter


class Favorited(CreateDeleteViewSet):
    queryset = Favorite.objects.all()
    permission_classes = [IsAuthenticated]
                                                                                                                


