from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, delete_token, get_token


app_name = 'api_users'
router = routers.DefaultRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', get_token, name='token'),
    path('auth/token/logout/', delete_token, name='delete_token')
]
