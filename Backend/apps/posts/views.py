from django.utils.translation import gettext as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Post
from posts.serializers import PostSerializer, UserPostSerializer
from posts.permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.allowed(self.request.user)

    @action(detail=False, url_path='my')
    def my_posts(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': _('Вы не авторизованы')}, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(author=request.user)
        serializer = UserPostSerializer(posts, many=True)

        return Response(serializer.data)
