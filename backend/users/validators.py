import re

from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator:
    def __call__(self, username):
        if len(username) < 3:
            raise ValidationError(
                _("Имя пользователя должно содержать более 2 символов.")
            )

        if len(username) <= 1000 and re.fullmatch(r"(?:[^\W_]| )+", username) is None:
            raise ValidationError(
                _("Имя пользователя может содержать только буквы, цифры и пробел.")
            )
