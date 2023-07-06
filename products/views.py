from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Category, Product, Comment, CommentLike, CommentDislike
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
        comments = product.comments.order_by("-modified_datetime")

        paginator = Paginator(comments, 2)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)

        LAST_PAGE_NUMBER = page_obj.paginator.num_pages
        BEFORE_AND_AFTER_PAGE_COUNT = 1
        list_range_pages = range(1, LAST_PAGE_NUMBER + 1)
        list_show_pages = [1, page_obj.paginator.num_pages]

        if LAST_PAGE_NUMBER - (2 * BEFORE_AND_AFTER_PAGE_COUNT) > 2 * BEFORE_AND_AFTER_PAGE_COUNT:
            if page_obj.number == 1:
                list_show_pages[1:1] = [2, 3]
            elif page_obj.number == LAST_PAGE_NUMBER:
                list_show_pages[-1:-1] = [LAST_PAGE_NUMBER - 2, LAST_PAGE_NUMBER - 1]
            else:
                list_between_pages = []
                for index in range(-BEFORE_AND_AFTER_PAGE_COUNT, BEFORE_AND_AFTER_PAGE_COUNT + 1):
                    if page_obj.number + index not in list_show_pages:
                        list_between_pages.append(page_obj.number + index)
                list_show_pages[1:1] = list_between_pages
        else:
            list_show_pages = list_range_pages

        if request.user.is_authenticated:
            comment = Comment.objects.filter(user=request.user, product=product)
            form = CommentForm(instance=comment.first()) if comment.exists() else CommentForm()
        else:
            form = CommentForm()

        return render(request, "products/product_detail.html",
                      context={"product": product, "form": form, "comments": comments,
                               "page_obj": page_obj, "list_show_pages": list_show_pages,
                               "range_pages": list_range_pages})

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


class ProductLikeComment(View):
    def post(self, request, category_name, id_product, id_comment, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=id_comment)
        try:
            comment_like = CommentLike.objects.get(user=request.user, comment=comment)
        except CommentLike.DoesNotExist:
            CommentLike.objects.create(user=request.user, comment=comment)
            return JsonResponse({"status": "liked"})
        else:
            comment_like.delete()
            return JsonResponse({"status": "retake_liked"})


class ProductDislikeComment(View):
    def post(self, request, category_name, id_product, id_comment, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=id_comment)
        try:
            comment_dislike = CommentDislike.objects.get(user=request.user, comment=comment)
        except CommentDislike.DoesNotExist:
            CommentDislike.objects.create(user=request.user, comment=comment)
            return JsonResponse({"status": "disliked"})
        else:
            comment_dislike.delete()
            return JsonResponse({"status": "retake_disliked"})
