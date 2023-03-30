from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import LoginForm, CustomUserCreationForm


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
            user = authenticate(request, username=cleaned_data["email"], password=cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("pages:home")
            else:
                messages.error(request, _("Email and Password is incorrect!"))

        return render(request, "registration/login.html", {"form": form})


class LogoutView(View):
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
