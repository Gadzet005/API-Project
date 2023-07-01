import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator:
    def __call__(self, username):
        if len(username) < 3:
            raise ValidationError(
                "Имя пользователя должно содержать более 2 символов"
            )

        if len(username) <= 1000 and re.fullmatch(r"(?:[^\W_]| )+", username) is None:
            raise ValidationError(
                "Имя пользователя может содержать только буквы, цифры и пробел."
            )
