import django_filters
from api_foodgram.constants import FILTER_FAVORITE_OR_SHOPPING
from recipes.models import Favorite, Ingredient, Recipe, Shopping


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = django_filters.CharFilter(
        field_name='author__id',
        lookup_expr='iexact'
    )
    is_favorite = django_filters.NumberFilter(
        method='is_favorite_filter',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='is_in_shopping_cart_filter',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def is_favorite_filter(self, queryset, name, value):
        if value == FILTER_FAVORITE_OR_SHOPPING:
            user = self.request.user
            query_relate = Favorite.objects.filter(user=user)
            queryset = queryset.filter(
                id__in=query_relate.values_list('recipe',)
            )
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value == FILTER_FAVORITE_OR_SHOPPING:
            user = self.request.user
            query_relate = Shopping.objects.filter(user=user)
            queryset = queryset.filter(
                id__in=query_relate.values_list('recipe',)
            )
        return queryset


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = {
            'name',
        }
