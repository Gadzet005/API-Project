from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

from users.managers import UserManager
from users.validators import UsernameValidator


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('почта'), unique=True)
    username = models.CharField(
        _('имя пользователя'), max_length=30, unique=True,
        validators=[UsernameValidator()],
    )
    is_active = models.BooleanField(_('активен'), default=True)
    date_joined = models.DateTimeField(_('дата регистрации'), auto_now_add=True)
    is_staff = models.BooleanField(
        _('статус персонала'), default=False,
        help_text=_('Определяет, есть ли у пользователя доступ к админ панели.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'user_id': self.id})


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
