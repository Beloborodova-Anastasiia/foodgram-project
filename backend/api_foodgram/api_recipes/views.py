import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api_foodgram.constants import (PASH_SHOPPING_CART,
                                    PATH_DOWNLOAD_SHOPPING_CART, PATH_FAVORITE,
                                    SAVE_AS)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag)

from .filters import RecipeFilter
from .mixins import RetriveListCreateDeleteUpdateViewSet
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortcutRecipeSerializer, TagSerializer)


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
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            id=self.kwargs.get('recipe_id'),
        )
        user = request.user
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                context = {
                    'errors': 'Рецепт уже есть в избранном'
                }
                return Response(
                    context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = ShortcutRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                Favorite.objects.filter(
                    user=user, recipe=recipe
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            context = {
                'errors': 'Рецепта нет в избранном'
            }
            return Response(
                context,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=PASH_SHOPPING_CART,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            id=self.kwargs.get('recipe_id'),
        )
        user = request.user
        if request.method == 'POST':
            if Shopping.objects.filter(user=user, recipe=recipe).exists():
                context = {
                    'errors': 'Рецепт уже есть в списке покупок'
                }
                return Response(
                    context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            Shopping.objects.create(user=user, recipe=recipe)
            serializer = ShortcutRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Shopping.objects.filter(user=user, recipe=recipe).exists():
                Shopping.objects.filter(
                    user=user, recipe=recipe
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            context = {
                'errors': 'Рецепта нет в списке покупок'
            }
            return Response(
                context,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['get'],
        detail=False,
        url_path=PATH_DOWNLOAD_SHOPPING_CART,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = SAVE_AS
        writer = csv.writer(response)
        shopping = Shopping.objects.filter(user=request.user)
        recipes = Recipe.objects.filter(
            id__in=shopping.values_list('recipe',)
        )
        shopping_cart = {}
        for recipe in recipes:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                amount = get_object_or_404(
                    IngredientRecipe,
                    recipe=recipe,
                    ingredient=ingredient
                ).amount
                if ingredient.name in shopping_cart:
                    shopping_cart[ingredient.name] += amount
                else:
                    shopping_cart[ingredient.name] = amount
        for ingredient in shopping_cart:
            writer.writerow([ingredient, shopping_cart[ingredient]])
        return response
