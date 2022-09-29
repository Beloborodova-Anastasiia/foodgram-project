from api_foodgram.constants import (FAVORITE_OR_SHOPPING, PASH_SHOPPING_CART,
                                    PATH_DOWNLOAD_SHOPPING_CART, PATH_FAVORITE,
                                    SAVE_AS)
from api_foodgram.utilits import create_relation, delete_relation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag)
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .mixins import RetriveListCreateDeleteUpdateViewSet, RetriveListViewSet
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortcutRecipeSerializer, TagSerializer)


class IngredientViewSet(RetriveListViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(RetriveListViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(RetriveListCreateDeleteUpdateViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self, *args, **kwargs):
        for key in FAVORITE_OR_SHOPPING:
            if key in self.request.path:
                return ShortcutRecipeSerializer
        return RecipeSerializer

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=PATH_FAVORITE,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        if request.method == 'POST':
            context, response_status = create_relation(
                request=request,
                model=Recipe,
                relate_model=Favorite,
                serializer=self.get_serializer(),
                *args,
                **kwargs
            )
        if request.method == 'DELETE':
            context, response_status = delete_relation(
                request=request,
                model=Recipe,
                relate_model=Favorite,
                *args,
                **kwargs
            )
        return Response(context, status=response_status)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=PASH_SHOPPING_CART,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, *args, **kwargs):
        if request.method == 'POST':
            context, response_status = create_relation(
                request=request,
                model=Recipe,
                relate_model=Shopping,
                serializer=self.get_serializer(),
                *args,
                **kwargs
            )
        if request.method == 'DELETE':
            context, response_status = delete_relation(
                request=request,
                model=Recipe,
                relate_model=Shopping,
                serializer=ShortcutRecipeSerializer,
                *args,
                **kwargs
            )
        return Response(context, response_status)

    @action(
        methods=['get'],
        detail=False,
        url_path=PATH_DOWNLOAD_SHOPPING_CART,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        file_response = HttpResponse(content_type='text/plain')
        file_response['Content-Disposition'] = SAVE_AS
        shopping_obj = Shopping.objects.filter(user=request.user)
        recipes = Recipe.objects.filter(
            id__in=shopping_obj.values_list('recipe',)
        )
        shopping_list = {}
        for recipe in recipes:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                amount = get_object_or_404(
                    IngredientRecipe,
                    recipe=recipe,
                    ingredient=ingredient
                ).amount
                if ingredient in shopping_list:
                    shopping_list[ingredient] += amount
                else:
                    shopping_list[ingredient] = amount
        for ingredient in shopping_list:
            line = (str(ingredient) + '  ' + str(shopping_list[ingredient])
                    + str(ingredient.measurement_unit) + '\n')
            file_response.write(line)
        return file_response
