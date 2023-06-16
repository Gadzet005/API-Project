from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Post
from posts.serializers import PostSerializer, UserPostSerializer
from posts.permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_url_kwarg = 'post_id'

    @action(detail=True, url_path='stat')
    def post_statistics(self, request, post_id):
        post = self.get_object()

        letters = dict()
        for let in post.text.upper():
            if let not in letters:
                letters[let] = 0
            letters[let] += 1

        data = {
            'Длина заголовка': len(post.title),
            'Длина текст': len(post.text),
            'Самая частый символ': max(letters, key=lambda let: letters[let]),
            'Самая редкий символ': min(letters, key=lambda let: letters[let]),
        }

        return Response(data)

    @action(detail=False, url_path='my')
    def my_posts(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Вы не авторизованы'}, status=status.HTTP_403_FORBIDDEN)
        return self.user_posts(request, request.user.id)

    @action(detail=False, url_path=r'user-posts/(?P<user_id>\d+)')
    def user_posts(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Такого пользователя не существует'}, status=status.HTTP_404_NOT_FOUND)

        queryset = Post.objects.filter(author=user)
        serializer = UserPostSerializer(queryset, many=True)

        return Response({'user': user.username, 'posts': serializer.data})
