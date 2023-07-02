from rest_framework import serializers

from posts.models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    serializers.HyperlinkedRelatedField
    author_info = serializers.SerializerMethodField("get_author_info")
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, slug_field='name')

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'author_info', 'title', 'text',
            'creation_date', 'tags'
        )
        read_only_fields = ('creation_date',)

    def get_author_info(self, obj):
        url = obj.author.get_absolute_url()
        request = self.context.get('request')
        return {
            "name": obj.author.username,
            "url": request.build_absolute_uri(url)
        }


class UserPostSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        fields = (
            'id', 'title', 'text', 'creation_date',
            'is_published', 'is_blocked', 'tags',
        )
