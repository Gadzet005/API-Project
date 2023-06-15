from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', unique=True)
    username = models.CharField(
        'Имя пользователя', max_length=100, unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    is_active = models.BooleanField('Активен', default=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_staff = models.BooleanField(
        "Статус персонала", default=False,
        help_text="Определяет, есть ли у пользователя доступ к админ панели",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
