from django.urls import include, path
from rest_framework import routers
from .views import CustomUserViewSet

app_name = 'api_users'
router = routers.DefaultRouter()
router.register(
    'users',
    CustomUserViewSet,
    basename='users'
)
urlpatterns = [
    # path('users/', CustomUserViewSet.as_view({'get': 'subscribtions'})),

    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
