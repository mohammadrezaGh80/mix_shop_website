from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect

from .forms import LoginForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
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
