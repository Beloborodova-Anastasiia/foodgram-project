from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import TokenProxy

from recipes.models import Favorite, Shopping

from .models import Subscribe, User


class SubscribeInline(admin.TabularInline):
    model = Subscribe
    extra = 1
    fk_name = 'user'


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1
    fk_name = 'user'


class ShoppingInline(admin.TabularInline):
    model = Shopping
    extra = 1
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    list_filter = ('username', 'email')
    inlines = (SubscribeInline, FavoriteInline, ShoppingInline,)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(TokenProxy)
