from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.username")
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("id", "author", "author_name", "title", "text", "creation_date")
        read_only_fields = ("creation_date",)


class MyPostSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ("id", "author", "title", "text", "creation_date")
        read_only_fields = ("creation_date",)
