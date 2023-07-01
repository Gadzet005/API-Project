from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from users.models import User
from users.permissions import IsOwnerOrReadOnly
from posts.serializers import UserPostSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=True, url_path='posts')
    def get_posts(self, request, user_id):
        user = self.get_object()
        serializer = UserPostSerializer(user.posts.allowed(), many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='register', serializer_class=RegisterSerializer)
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        auth_token = Token.objects.get(user=serializer.instance)
        data = serializer.data.copy()
        data['auth-token'] = auth_token.key

        return Response(data)

    @action(
        methods=['put'], detail=True, url_path='change-password',
        serializer_class=ChangePasswordSerializer
    )
    def change_password(self, request, user_id):
        serializer = self.serializer_class(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Пароль успешно изменен'})
