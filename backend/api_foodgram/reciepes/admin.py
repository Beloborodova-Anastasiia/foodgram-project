from django.contrib import admin

from .models import Ingredient, IngredientReciepe, Reciepe, Tag, TagReciepe


class IngredientsInline(admin.TabularInline):
    model = IngredientReciepe
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagReciepe
    extra = 1

    
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk','name','measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk','name','color', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-empty-'

class ReciepeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'in_favorite',
        'text',
        'cooking_time',
    )
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-empty-'
    date_hierarchy = 'pub_date'
    inlines = (IngredientsInline, TagsInline,)

    def in_favorite(self, obj):
        return obj.favorite.count()



admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Reciepe, ReciepeAdmin)
