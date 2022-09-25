from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from recipes.models import Recipe


def create_relation(**kwargs):
    model = kwargs['model']
    object = get_object_or_404(
        model,
        id=kwargs['object_id'],
    )
    model_relate = kwargs['model_relate']
    user = kwargs['user']
    if model_relate.objects.filter(user=user, object=object).exists():
        message = kwargs['message']
        context = {
            'errors': f'Рецепт уже есть в {message}'
        }
        return Response(
            context,
            status=status.HTTsP_400_BAD_REQUEST
        )
    model_relate.objects.create(user=user, object=object)
    serializer = kwargs['serializer'](object)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_relation(**kwargs):
    model_relate = kwargs['model_relate']
    model = kwargs['model']
    recipe = get_object_or_404(
        model,
        id=kwargs['model_id'],
    )
    if model_relate.objects.filter(recipe=recipe).exists():
        model_relate.objects.filter(
            user=kwargs['user'], recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    message = kwargs['message']
    context = {
        'errors': f'Рецепта нет в {message}'
    }
    return Response(
        context,
        status=status.HTTP_400_BAD_REQUEST
    )