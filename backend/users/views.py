from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer
from users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
