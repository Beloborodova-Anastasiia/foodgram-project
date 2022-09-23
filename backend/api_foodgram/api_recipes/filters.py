import django_filters
from recipes.models import Recipe, Favorite, Shoping
from api_foodgram.constants import FILTER_FAVORITE_OR_SHOPPING


class RecipeFilter(django_filters.FilterSet):
    # is_favorite = django_filters.BooleanFilter(
    #     field_name='is_favorite',
    #     # lookup_expr='iexact'
    # )
    # is_in_shopping_cart = django_filters.BooleanFilter(
    #     field_name='is_in_shopping_cart',
    #     # lookup_expr='iexact'
    # )
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )
    author = django_filters.CharFilter(
        field_name='author__id',
        lookup_expr='icontains'
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
            queryset = Recipe.objects.filter(
                id__in=query_relate.values_list('recipe',)
            )
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value == FILTER_FAVORITE_OR_SHOPPING:
            user = self.request.user
            query_relate = Shoping.objects.filter(user=user)
            queryset = Recipe.objects.filter(
                id__in=query_relate.values_list('recipe',)
            )
        return queryset
