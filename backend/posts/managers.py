from django.db import models
from django.db.models import Q


class PostManager(models.Manager):
    def allowed(self, user=None):
        if user and user.is_authenticated:
            queryset = (
                self.get_queryset()
                .filter(
                    Q(is_published=True, is_blocked=False) | Q(author=user)
                )
            )
        else:
            queryset = self.get_queryset().filter(is_published=True, is_blocked=False)

        return queryset.prefetch_related('tags').select_related('author')
