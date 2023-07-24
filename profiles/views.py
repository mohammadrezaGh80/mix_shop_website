from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.views.generic.base import ContextMixin

from accounts.forms import CustomUserChangeForm
from products.models import Product
from .recent_visits import RecentVisits
from products.forms import CommentForm
from products.models import Comment
from products.paginator import CustomPaginator


class ProfilePageTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/profile_page.html"


class OrdersTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/orders.html"


class FavoritesTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/favorites.html"


class ManageCommentView(LoginRequiredMixin, ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.request.user.comments.all().order_by("-modified_datetime")
        context["comments"] = comments

        paginator = CustomPaginator(comments, 5)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        range_pages_comment = page_obj.paginator.get_elided_page_range(number=page, on_each_side=1)
        context["page_obj"] = page_obj
        context["range_pages"] = range_pages_comment
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        comment_form = CommentForm()
        context["comment_form"] = comment_form
        return render(request, "profiles/comments.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        comment = get_object_or_404(Comment, pk=int(request.POST.get("id_comment")))
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            if "is_anonymous" in request.POST:
                new_comment.is_anonymous = True
            else:
                new_comment.is_anonymous = False
            new_comment.save()
            messages.success(request, _("Your comment was successfully changed."))
            return redirect("profiles:comments")
        context["comment_form"] = comment_form
        return render(request, "profiles/comments.html", context)


class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        messages.success(request, _("Your comment was successfully deleted."))
        return redirect("profiles:comments")


class AddressesTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/addresses.html"


class RecentVisitsTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/recent_visits.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_visits"] = RecentVisits(self.request)
        return context


class ClearRecentVisits(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recent_visits = RecentVisits(request)
        recent_visits.clear()
        return redirect("profiles:recent_visits")


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


class DeleteProductOfRecentVisits(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        recent_visits = RecentVisits(request)

        product_id = int(request.POST["delete_id"])
        product = get_object_or_404(Product, pk=product_id)

        recent_visits.remove_product(product)
        return redirect("profiles:recent_visits")

