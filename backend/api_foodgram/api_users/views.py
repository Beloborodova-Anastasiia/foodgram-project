from rest_framework import viewsets

from .serializers import UserSerializer
from users.models import User


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = (AdminOnly,)
    serializer_class = UserSerializer


