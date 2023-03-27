from django.core import validators
from django.utils.translation import gettext_lazy as _


class UsernameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z]+[\w.-]{3,}\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'digits, and ./-/_ only which starts with letters and has at least 4 characters.'
    )
