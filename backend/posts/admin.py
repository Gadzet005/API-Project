from django.contrib import admin

from posts.models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = (
        'author', 'title', 'text', 'creation_date',
        'is_published', 'is_blocked', 'tags'
    )
    readonly_fields = ('author', 'creation_date')
    list_display = ('title', 'author', 'creation_date', 'is_published', 'is_blocked')
    filter_horizontal = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
