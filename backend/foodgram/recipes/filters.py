import django_filters

from .models import Favorite, Recipe, Shopping


class RecipeFilter(django_filters.FilterSet):
    FILTER_FAVORITE_OR_SHOPPING = 1

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
        if value == self.FILTER_FAVORITE_OR_SHOPPING:
            user = self.request.user
            query_relate = Favorite.objects.filter(user=user)
        return queryset.filter(id__in=query_relate.values_list('recipe',))

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value == self.FILTER_FAVORITE_OR_SHOPPING:
            user = self.request.user
            query_relate = Shopping.objects.filter(user=user)
        return queryset.filter(id__in=query_relate.values_list('recipe',))


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        method='name_filter',
    )

    def name_filter(self, queryset, name, value):
        value = value.lower()
        return queryset.filter(name__istartswith=value)
