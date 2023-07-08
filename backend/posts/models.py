from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

from posts.managers import PostManager


class Post(models.Model):
    author = models.ForeignKey(verbose_name=_('автор'), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('заголовок'), max_length=100)
    text = models.TextField(_('текст'), max_length=10000)
    creation_date = models.DateTimeField(_('дата создания'), auto_now_add=True)
    is_published = models.BooleanField(_('опубликовано'), default=True)
    is_blocked = models.BooleanField(_('заблокировано'), default=False)
    tags = models.ManyToManyField(verbose_name=_('тэги'), to='Tag')

    objects = PostManager()

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(_('название'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('тэг')
        verbose_name_plural = _('тэги')
        default_related_name = 'tags'

    def __str__(self):
        return self.name
