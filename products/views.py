from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import Category, Product


class ProductCategoryView(View):
    def get(self, request, category_name, *args, **kwargs):
        category = get_object_or_404(Category, category_name=category_name)
        if category.parent:
            raise Http404()

        sub_categories = category.sub_categories.all()

        return render(request, "products/product_category.html",
                      context={"category_name": category_name, "sub_categories": sub_categories})


class ProductSubCategoryListView(View):
    def get(self, request, category_name, *args, **kwargs):
        category = get_object_or_404(Category, category_name=category_name)
        if not category.parent:
            raise Http404()

        products = Product.objects.filter(category=category)

        return render(request, "products/product_sub_category_list.html",
                      context={"category_name": category_name, "products": products})


class ProductDetailView(View):
    def get(self, request, category_name, pk, *args, **kwargs):
        category = get_object_or_404(Category, category_name=category_name)
        product = get_object_or_404(Product, category=category, pk=pk)

        return render(request, "products/product_detail.html", context={"product": product})

