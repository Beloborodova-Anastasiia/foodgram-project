import imp
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404

# from rest_framework.permissions import SAFE_METHODS

from recipes.models import Ingredient, Recipe, Shoping, Tag, IngredientRecipe, Favorite
from .serializers import (IngredientSerializer, RecipeSerializer, ShortcutRecipe,
                          TagSerializer, IngredientRecipeSerializer,
                          )
from .permissions import AuthorOrAdmin
from users.models import User
from .filters import RecipeFilter
from api_foodgram.constants import PATH_FAVORITE

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

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=PATH_FAVORITE,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, recipe_id):
        recipe = get_object_or_404(
            Recipe,
            id=self.kwargs.get('recipe_id'),
        )
        if request.method == 'POST':
            if Favorite.objects.filter(recipe=recipe).exists():
                context = {
                    'errors': 'Рецепт уже есть в избранном'
                }
                return Response(
                    context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=self.request.user, recipe=recipe)
            serializer = ShortcutRecipe(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if Favorite.objects.filter(recipe=recipe).exists():
            Favorite.objects.filter(
                user=self.request.user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        context = {
            'errors': 'Рецепта нет в избранном'
        }
        return Response(
            context,
            status=status.HTTP_400_BAD_REQUEST
        )



class FavoriteViewSet(RetriveListCreateDeleteUpdateViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ShortcutRecipe
    
    # @action(
    #     methods=['post'],
    #     detail=False,
    # )
    def perform_create(self):
        # recipe = get_object_or_404(
        #     Recipe,
        #     id=self.kwargs.get('recipe_id'),
        # )
        # print(recipe)
        # if Favorite.objects.filter(recipe=recipe).exists():
        #     return Response(
        #         'Рецепт уже есть в избранном',
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # Favorite.objects.create(user=self.request.user, recipe=recipe)
        # serializer.data(
        #     recipe=recipe
        # )
        return Response('oK', status=status.HTTP_201_CREATED)
