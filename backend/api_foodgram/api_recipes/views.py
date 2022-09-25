from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404
import csv
from django.http import HttpResponse
# from rest_framework.permissions import SAFE_METHODS

from recipes.models import Ingredient, Recipe, Shopping, Tag, IngredientRecipe, Favorite
from .serializers import (IngredientSerializer, RecipeSerializer, ShortcutRecipeSerializer,
                          TagSerializer, IngredientRecipeSerializer,
                          )
from .permissions import AuthorOrAdmin
from users.models import User
from .filters import RecipeFilter
from api_foodgram.constants import (PATH_FAVORITE, PATH_DOWNLOAD_SHOPPING_CART,
                                    PASH_SHOPPING_CART)
from .utilits import create_relation
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
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        
        shopping = Shopping.objects.filter(user=request.user)
        recipes = Recipe.objects.filter(
            id__in=shopping.values_list('recipe',)
        )
        shopping_cart = {}
        for recipe in recipes:
            # ingredients = Ingredient.objects.filter(
            #     id__in=recipe.values_list('ingredients',)
            # )
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
