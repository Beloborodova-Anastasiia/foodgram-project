from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response

from .serializers import UserSerializer, GetTokenSerializer
from users.models import User


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


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
