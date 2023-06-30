from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Category, Product, Comment
from profiles.recent_visits import RecentVisits
from .forms import CommentForm


class ProductCategoryView(View):
    def get(self, request, category_name, *args, **kwargs):
        category = get_object_or_404(Category, category_name=category_name)
        if not category.sub_categories.exists():
            raise Http404()

        sub_categories = category.sub_categories.all()

        return render(request, "products/product_category.html",
                      context={"category_name": category_name, "sub_categories": sub_categories})


class ProductSubCategoryListView(View):
    def get(self, request, category_name, *args, **kwargs):
        category = get_object_or_404(Category, category_name=category_name)
        if category.sub_categories.exists():
            raise Http404()

        products = Product.objects.filter(category=category).order_by("-modified_datetime")

        return render(request, "products/product_sub_category_list.html",
                      context={"category_name": category_name, "products": products})


class ProductDetailView(View):
    def get(self, request, category_name, pk, *args, **kwargs):
        recent_visits = RecentVisits(request)
        category = get_object_or_404(Category, category_name=category_name)
        product = get_object_or_404(Product, category=category, pk=pk)
        recent_visits.add_product(product)
        comments = Comment.objects.filter(product=product).order_by("-modified_datetime")

        if request.user.is_authenticated:
            comment = Comment.objects.filter(user=request.user, product=product)
            form = CommentForm(instance=comment.first()) if comment.exists() else CommentForm()
        else:
            form = CommentForm()

        return render(request, "products/product_detail.html",
                      context={"product": product, "form": form, "comments": comments})

    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, category_name=kwargs["category_name"])
        product = get_object_or_404(Product, category=category, pk=kwargs["pk"])

        comment = Comment.objects.filter(user=request.user, product=product)
        form = CommentForm(request.POST, instance=comment.first())
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = product
            if "is_anonymous" in request.POST:
                new_comment.is_anonymous = True
            new_comment.save()
            messages.success(request, _("Your comment was successfully submitted."))
            return redirect("products:product_detail", kwargs["category_name"], kwargs["pk"])
        return render(request, "products/product_detail.html", context={"product": product, "form": form})
