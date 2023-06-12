from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="автор")
    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст", max_length=10000)
    creation_date = models.DateTimeField("Дата создания", auto_now_add=True)
