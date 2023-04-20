from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfilePageTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/profile_page.html"
