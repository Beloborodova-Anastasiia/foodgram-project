from django.urls import include, path
from rest_framework import routers
from .views import IngredientViewSet, TagViewSet, RecipeViewSet


app_name = 'api_recipes'
router = routers.DefaultRouter()
router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router.register(
    'tags',
    TagViewSet,
    basename='tags'
)
router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)
# r'titles/(?P<title_id>[0-9]+)/reviews',
    # path('v1/auth/signup/', signup, name='signup'),

urlpatterns = [
    path('', include(router.urls)),
]
