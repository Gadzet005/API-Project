from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        default_related_name = "tags"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="автор")
    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст", max_length=10000)
    creation_date = models.DateTimeField("Дата создания", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    is_blocked = models.BooleanField("Заблокировано", default=False)
    tags = models.ManyToManyField(Tag, verbose_name="Тэг")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        default_related_name = "posts"

    def __str__(self):
        return self.title
