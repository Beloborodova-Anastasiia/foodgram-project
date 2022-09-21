from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from djoser.views import UserViewSet
from rest_framework.response import Response

from api_foodgram.constants import KEYWORD_ME, KEYWORD_SET_PASSWORD
from .permissions import UserOwner
from .serializers import (CustomUserSerializer, SetPasswordSerializer)
from users.models import User

