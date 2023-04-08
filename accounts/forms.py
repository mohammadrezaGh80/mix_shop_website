from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name", "phone", "birth_date")
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": _("email...")}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": _("username...")}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("first name...")}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("last name...")}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": _("phone number...")}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "placeholder": _("birth date..."), "type": "date"}
            ),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        current_date = timezone.now().date()
        if birth_date and birth_date > current_date:
            self.add_error(
                "birth_date",
                _("Your birth date is invalid,date of today: %(current_date)s") % {"current_date": current_date}
            )
        return birth_date

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _('password...')})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _('password confirmation...')})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "phone", "birth_date", "is_active", "is_admin",)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("Email or Username"))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Password"))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) > 255:
            raise ValidationError(_("Your username is not valid!"), code="invalid_username")
        return username


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=255,
                             widget=forms.TextInput(attrs={"placeholder": _("email..."), "class": "form-control"}),
                             error_messages={"invalid_email": _("Enter a valid email address.")})


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("password...")}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("password confirmation...")}),
    )
