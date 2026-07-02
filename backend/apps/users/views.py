from rest_framework import viewsets
from apps.users.models import User
from apps.users.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
