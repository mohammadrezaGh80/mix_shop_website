from django.shortcuts import render, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetConfirmView

from mail_templated import EmailMessage

from .forms import LoginForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm, \
    CreateAccountForm, PersonalDetailsForm, ActivationAccountResendForm
from .tokens import custom_token_generator
from .utils import EmailThread

User = get_user_model()


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
                return redirect(self.request.GET.get("next", "pages:home"))

        return render(request, "registration/login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("pages:home")


class RegisterStepOneView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")

        info_user = request.session.get("info_user")
        if info_user and "password" in info_user.keys():
            info_user.pop("password")
            request.session.modified = True

        form = CreateAccountForm(initial=info_user)
        return render(request, "registration/register_step_1.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home")

        form = CreateAccountForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            request.session["info_user"] = {
                "email": cleaned_data["email"], "password": cleaned_data["password2"]
            }
            return redirect("accounts:register_step_two")
        return render(request, "registration/register_step_1.html", context={"form": form})


class RegisterStepTwoView(View):
    def get(self, request, *args, **kwargs):
        info_user = request.session.get("info_user")
        if not info_user or (info_user and "email" not in info_user.keys() or "password" not in info_user.keys()):
            return redirect("accounts:register_step_one")
        form = PersonalDetailsForm()
        return render(request, "registration/register_step_2.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = PersonalDetailsForm(request.POST)
        if form.is_valid():
            info_user = request.session["info_user"]
            user = form.save(commit=False)
            user.email = info_user["email"]
            user.set_password(info_user["password"])
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            email_obj = EmailMessage('email/activation_account.tpl',
                                     context={'email_name': user.email[:user.email.find("@")],
                                              'domain': f'{request.get_host()}',
                                              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                              'token': custom_token_generator.make_token(user),
                                              'protocol': 'http'}, to=[user.email])

            messages.success(request, _("Account created successfully,check your email to activate your account."))
            EmailThread(email_obj).start()
            return redirect("pages:home")
        return render(request, "registration/register_step_2.html", context={"form": form})


class ActivationAccountView(View):

    def get(self, request, uid, token, *args, **kwargs):
        user_id = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, pk=user_id)
        is_valid_token = custom_token_generator.check_token(user, token)
        if is_valid_token:
            user.is_active = True
            user.save()
        return render(request, "registration/activation_account.html",
                      context={"is_valid_token": is_valid_token})


class ActivationAccountResendView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        form = ActivationAccountResendForm()
        return render(request, "registration/activation_account_resend.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ActivationAccountResendForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user", None)
            email_obj = EmailMessage('email/activation_account.tpl',
                                     context={'email_name': user.email[:user.email.find("@")],
                                              'domain': f'{request.get_host()}',
                                              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                              'token': custom_token_generator.make_token(user),
                                              'protocol': 'http'}, to=[user.email])

            messages.success(request, _("Check your email to activate your account."))
            EmailThread(email_obj).start()
            return redirect("pages:home")
        return render(request, "registration/activation_account_resend.html", {"form": form})

    def test_func(self):
        return not self.request.user.is_authenticated


class PasswordResetView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomPasswordResetForm()
        return render(request, "registration/password_reset.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user", None)
            email_obj = EmailMessage('email/password_reset.tpl',
                                     context={'email': user.email,
                                              'email_name': user.email[:user.email.find("@")],
                                              'domain': f'{request.get_host()}',
                                              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                              'token': custom_token_generator.make_token(user),
                                              'protocol': 'http'}, to=[user.email])

            EmailThread(email_obj).start()

            messages.info(request, _("An email with password reset instructions has been sent to your email address"))
            return render(request, "registration/password_reset_done.html")
        return render(request, "registration/password_reset.html", context={"form": form})

    def test_func(self):
        return not self.request.user.is_authenticated


class CustomPasswordResetConfirmView(View):
    def get(self, request, uid, token, *args, **kwargs):
        user_id = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, pk=user_id)
        is_valid_token = custom_token_generator.check_token(user, token)
        form = CustomSetPasswordForm(user=user)
        return render(request, "registration/password_reset_confirm.html",
                      context={"form": form, "is_valid_token": is_valid_token})

    def post(self, request, uid, token, *args, **kwargs):
        user_id = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, pk=user_id)
        is_valid_token = custom_token_generator.check_token(user, token)
        form = CustomSetPasswordForm(user, data=request.POST)
        if is_valid_token and form.is_valid():
            form.save()
            messages.info(request, _("Your password has been successfully reset."))
            return redirect("pages:home")
        return render(request, "registration/password_reset_confirm.html",
                      context={"form": form, "is_valid_token": is_valid_token})


class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(request.user)
        return render(request, "registration/password_change.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, _("Your password has been changed successfully."))
            return redirect("pages:home")
        return render(request, "registration/password_change.html", context={"form": form})
