from rest_framework import serializers
import base64
from django.core.files.base import ContentFile


class ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        print(imgstr, ext)
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return data
