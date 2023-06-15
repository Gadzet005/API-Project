from datetime import datetime

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


class AuthBackend(ModelBackend):
    """
    Авторизация по username или по email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return

        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return

        if user.check_password(password) and self.user_can_authenticate(user):
            user.last_login = datetime.now()
            return user
