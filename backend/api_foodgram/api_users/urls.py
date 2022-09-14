from django.urls import include, path
# from api_users.views import UserApiViewSet, get_token, signup
from rest_framework import routers
from .views import UserApiViewSet, delete_token, get_token


app_name = 'api_users'
router = routers.DefaultRouter()
router.register(
    'users',
    UserApiViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
    # path('v1/auth/signup/', signup, name='signup'),
    path('auth/token/login/', get_token, name='token'),
    # path('auth/token/login/', views.obtain_auth_token),
    path('auth/token/logout/', delete_token, name='delete_token')

]
