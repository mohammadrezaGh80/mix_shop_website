from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import Category, Product
from profiles.recent_visits import RecentVisits


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
        return render(request, "products/product_detail.html", context={"product": product})

