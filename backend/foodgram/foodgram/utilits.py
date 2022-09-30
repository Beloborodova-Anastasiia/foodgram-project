from django.shortcuts import get_object_or_404
from rest_framework import status


def create_relation(ban_himself=False, *args, **kwargs):
    error_messages = {
        'exists': 'уже есть в',
        'ban_himself': 'Вы не можете добавить себя в',
    }
    for key in kwargs.keys():
        if key.__contains__('id'):
            object_id = kwargs.get(key)
    model = kwargs.get('model')
    object = get_object_or_404(
        model,
        id=object_id,
    )
    user = kwargs.get('request').user
    relate_model = kwargs.get('relate_model')
    if ban_himself and user == object:
        message = error_messages['ban_himself']
        context = {
            'errors': (
                f'{message} {relate_model._meta.verbose_name}'
            )
        }
        return context, status.HTTP_400_BAD_REQUEST
    query_relate = relate_model.objects.filter(user=user)
    key = key.replace('_id', '')
    queryset = model.objects.filter(
        id__in=query_relate.values_list(key)
    )

    if object in queryset:
        message = error_messages['exists']
        context = {
            'errors': (
                f'{model._meta.verbose_name} '
                f'{message} {relate_model._meta.verbose_name}'
            )
        }
        return context, status.HTTP_400_BAD_REQUEST
    data = {
        'user': user,
        key: object
    }
    relate_model.objects.create(**data)
    serializer = kwargs.get('serializer')
    serializer.instance = object
    return serializer.data, status.HTTP_201_CREATED


def delete_relation(**kwargs):
    error_message = 'нет в'
    for key in kwargs.keys():
        if key.__contains__('id'):
            object_id = kwargs.get(key)
    model = kwargs.get('model')
    object = get_object_or_404(
        model,
        id=object_id,
    )
    user = kwargs.get('request').user
    relate_model = kwargs.get('relate_model')
    query_relate = relate_model.objects.filter(user=user)
    key = key.replace('_id', '')
    queryset = model.objects.filter(
        id__in=query_relate.values_list(key)
    )
    if object not in queryset:
        message = error_message['non_exists']
        context = {
            'errors': (
                f'{model._meta.verbose_name} '
                f'{message} {relate_model._meta.verbose_name}'
            )
        }
        return context, status.HTTP_400_BAD_REQUEST
    data = {
        'user': user,
        key: object
    }
    relate_model.objects.filter(**data).delete()
    return None, status.HTTP_204_NO_CONTENT
