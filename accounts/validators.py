from django.core import validators
from django.utils.translation import gettext_lazy as _


class UsernameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z]+[\w.-]{3,}\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'digits, and ./-/_ only which starts with letters and has at least 4 characters.'
    )


class PhoneValidator(validators.RegexValidator):
    regex = r'^09[0-9]{9}\Z'
    message = _(
        'Enter a valid phone number. This value must have 11 digits'
        ' which starts with the number 09.'
    )
