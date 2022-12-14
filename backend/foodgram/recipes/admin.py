from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


class IngredientsInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1


class TagsInline(admin.TabularInline):
    model = TagRecipe
    extra = 1
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
    search_fields = ('name',)
    sortable_by = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
    search_fields = ('name', 'slug',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = '-empty-'
    date_hierarchy = 'pub_date'
    inlines = (IngredientsInline, TagsInline,)
    fields = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'is_favorite',
    )
    readonly_fields = ('is_favorite',)

    def is_favorite(self, obj):
        return obj.favorite.count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
