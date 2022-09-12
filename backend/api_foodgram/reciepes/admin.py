from django.contrib import admin

from .models import Ingredient, Reciepe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk','name','measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk','name','color', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class ReciepeAdmin(admin.ModelAdmin):
    # list_display = (
    #     'pk',
    #     'author',
    #     'name',
    #     'image',
    #     # 'ingredients','tags',
    #     'text',
    #     'cooking_time',
    # )
    # filter_horizontal = ('ingredients','tags',)
    # list_filter = ('name', 'author', 'tags')
    # empty_value_display = '-empty-'
    pass

# class TagReciepe(admin.ModelAdmin):


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Reciepe, ReciepeAdmin)
