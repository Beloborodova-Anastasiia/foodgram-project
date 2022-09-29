from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


class SubscribeInline(admin.TabularInline):
    model = Subscribe
    extra = 1
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    list_filter = ('username', 'email')
    inlines = (SubscribeInline,)


admin.site.register(User, CustomUserAdmin)
