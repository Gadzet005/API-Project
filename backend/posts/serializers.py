from rest_framework import serializers

from posts.models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.username")
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, slug_field="name")

    class Meta:
        model = Post
        fields = (
            "id", "author", "author_name", "title", "text",
            "creation_date", "tags"
        )
        read_only_fields = ("creation_date",)


class UserPostSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        fields = ("id", "title", "text", "creation_date", "tags")
