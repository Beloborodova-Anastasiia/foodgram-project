from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response

from api_foodgram.constants import KEYWORD_ME, KEYWORD_SET_PASSWORD
from .permissions import UserOwner
from .serializers import (UserSerializer, GetTokenSerializer,
                          SetPasswordSerializer)
from users.models import User


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateRetrieveListViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path=KEYWORD_ME,
        permission_classes=[UserOwner]
    )
    def user_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=False,
        url_path=KEYWORD_SET_PASSWORD,
        permission_classes=[UserOwner],
    )
    def set_password(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_password = serializer.data['current_password']
        if not user.check_password(current_password):
            content = {
                "detail": "Authentication credentials were not provided."
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        new_password = serializer.data['new_password']
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    user = get_object_or_404(User, email=email)
    token, created = Token.objects.get_or_create(user=user)
    content = {
        'auth_token': token.key,
    }
    return Response(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_token(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
