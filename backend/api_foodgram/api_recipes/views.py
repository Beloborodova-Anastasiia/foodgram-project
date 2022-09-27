from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api_foodgram.constants import (PASH_SHOPPING_CART,
                                    PATH_DOWNLOAD_SHOPPING_CART, PATH_FAVORITE,
                                    SAVE_AS)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag)

from .filters import IngredientFilter, RecipeFilter
from .mixins import RetriveListViewSet, RetriveListCreateDeleteUpdateViewSet
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortcutRecipeSerializer, TagSerializer)
from .utilits import create_relation, delete_relation


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
        # recipe = get_object_or_404(
        #     Recipe,
        #     id=self.kwargs.get('recipe_id'),
        # )
        context = None
        if request.method == 'POST':
            context, response_status = create_relation(
                request=request,
                model=Recipe,
                relate_model=Favorite,
                serializer=ShortcutRecipeSerializer,
                *args,
                **kwargs
            )
    
        # user = request.user
        
        if request.method == 'DELETE':
            context, response_status = delete_relation(
                request=request,
                model=Recipe,
                relate_model=Favorite,
                serializer=ShortcutRecipeSerializer,
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
        # recipe = get_object_or_404(
        #     Recipe,
        #     id=self.kwargs.get('recipe_id'),
        # )
        # user = request.user
        context = None
        if request.method == 'POST':
            context, response_status = create_relation(
                request=request,
                model=Recipe,
                relate_model=Shopping,
                serializer=ShortcutRecipeSerializer,
                *args,
                **kwargs
            )
            # return Response(context, status=response_status)
        #     if Shopping.objects.filter(user=user, recipe=recipe).exists():
        #         context = {
        #             'errors': 'Рецепт уже есть в списке покупок'
        #         }
        #         return Response(
        #             context,
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        #     Shopping.objects.create(user=user, recipe=recipe)
        #     serializer = ShortcutRecipeSerializer(recipe)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            context, response_status = delete_relation(
                request=request,
                model=Recipe,
                relate_model=Shopping,
                serializer=ShortcutRecipeSerializer,
                *args,
                **kwargs
            )
            # if Shopping.objects.filter(user=user, recipe=recipe).exists():
            #     Shopping.objects.filter(
            #         user=user, recipe=recipe
            #     ).delete()
            #     return Response(status=status.HTTP_204_NO_CONTENT)
            # context = {
            #     'errors': 'Рецепта нет в списке покупок'
            # }
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
