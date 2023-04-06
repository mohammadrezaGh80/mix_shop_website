from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View, generic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView

from .forms import LoginForm, CustomUserCreationForm, CustomPasswordResetForm, CustomSetPasswordForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request, username=cleaned_data["username"], password=cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("pages:home")
            else:
                messages.error(request, _("Username and Password is incorrect!"))

        return render(request, "registration/login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("pages:home")


class RegisterCreateView(generic.CreateView):
    model = get_user_model()
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")
        messages.info(request, _("Enter your email and a mail will be sent with instructions to reset password"))
        password_reset_form = CustomPasswordResetForm()
        return render(request, "registration/password_reset.html", context={"form": password_reset_form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data.get("email")
            user = get_user_model().objects.filter(email=email)
            if user.exists():
                user = user.first()
                subject = "Password Reset Request"
                email_template_name = 'registration/password_reset_message.txt'
                parameters = {
                    'email': user.email,
                    'domain': f'{request.get_host()}',
                    'site_name': 'MixShop',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http'
                }
                email = render_to_string(email_template_name, context=parameters)
                try:
                    send_mail(subject=subject, message=email, from_email='', recipient_list=[user.email])
                except BadHeaderError:
                    return HttpResponse(_("Invalid Header"))
                return redirect("accounts:password_reset_done")
            else:
                password_reset_form.add_error("email", _("There isn't an email with this address"))
        return render(request, "registration/password_reset.html", context={"form": password_reset_form})


class PasswordResetDoneView(View):
    def get(self, request, *args, **kwargs):
        messages.info(request, _("An email with password reset instructions has been sent to your email address"))
        return render(request, "registration/password_reset_done.html")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(View):
    def get(self, request, *args, **kwargs):
        messages.info(request, _("Your password has been successfully reset."))
        return render(request, "registration/password_reset_complete.html")
