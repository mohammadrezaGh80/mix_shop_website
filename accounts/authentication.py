from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models.base import Q

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        User can authenticate with username or email
        """
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
            if user.check_password(password):
                if not self.user_can_authenticate(user):
                    messages.error(request, _("Your account is not active."))
                else:
                    return user
            else:
                messages.error(request, _("User with entered info was not found."))
        except User.DoesNotExist:
            messages.error(request, _("User with entered info was not found."))
