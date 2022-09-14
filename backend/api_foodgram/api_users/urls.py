from django.urls import include, path
# from api_users.views import UserApiViewSet, get_token, signup
from rest_framework import routers
from .views import UserApiViewSet


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
    # path('v1/auth/token/', get_token, name='token'),
]
