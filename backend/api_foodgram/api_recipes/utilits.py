from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import RecipeSerializer, ShortcutRecipeSerializer
from api_foodgram.constants import ERROR_MESSAGES


def create_relation(*args, **kwargs):
    model = kwargs.get('model')
    object_id = kwargs.get((str(model.__name__).lower() + '_id'))
    object = get_object_or_404(
        model,
        id=object_id,
    )
    user = kwargs.get('request').user
    relate_model = kwargs.get('relate_model')
    query_relate = relate_model.objects.filter(user=user)
    queryset = model.objects.filter(
        id__in=query_relate.values_list((str(model.__name__).lower()),)
    )
    if object in queryset:
        message = ERROR_MESSAGES['exists']
        context = {
            'errors': (
                f'{model._meta.verbose_name} '
                f'{message} {relate_model._meta.verbose_name}'
            )
        }
        return context, status.HTTP_400_BAD_REQUEST
    data = {
        'user': user,
        str(model.__name__).lower(): object
    }
    relate_model.objects.create(**data)
    serializer = kwargs.get('serializer')
    context = {'request': kwargs.get('request')}
    serializer = serializer(object)
    return serializer.data, status.HTTP_201_CREATED


def delete_relation(**kwargs):
    model = kwargs.get('model')
    object_id = kwargs.get((str(model.__name__).lower() + '_id'))
    object = get_object_or_404(
        model,
        id=object_id,
    )
    user = kwargs.get('request').user
    relate_model = kwargs.get('relate_model')
    query_relate = relate_model.objects.filter(user=user)
    queryset = model.objects.filter(
        id__in=query_relate.values_list((str(model.__name__).lower()),)
    )
    if object not in queryset:
        message = ERROR_MESSAGES['non_exists']
        context = {
            'errors': (
                f'{model._meta.verbose_name} '
                f'{message} {relate_model._meta.verbose_name}'
            )
        }
        return context, status.HTTP_400_BAD_REQUEST
    data = {
        'user': user,
        str(model.__name__).lower(): object
    }
    relate_model.objects.filter(**data).delete()
    return None, status.HTTP_204_NO_CONTENT
