from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name", "phone", "birth_date")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "phone", "birth_date", "is_active", "is_admin", )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Password"))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email) > 255:
            raise ValidationError(_("Your email is not valid!"), code="invalid_email")
        return email
