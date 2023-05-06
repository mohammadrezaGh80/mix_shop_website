from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from accounts.forms import CustomUserChangeForm


class ProfilePageTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/profile_page.html"


class OrdersTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/orders.html"


class FavoritesTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/favorites.html"


class AddressesTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/addresses.html"


class RecentVisitsTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/recent_visits.html"


class PersonalInfoUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, "profiles/personal_info.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=request.user.pk)
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your information has been edited successfully."))
        return render(request, "profiles/personal_info.html", context={"form": form, "user": user})
