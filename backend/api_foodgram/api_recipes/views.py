from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, TagSerializer


class RetriveListViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    pass

class IngredientViewSet(RetriveListViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TagViewSet(RetriveListViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
