from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic.base import ContextMixin

from .cart import Cart
from .forms import AddToCartProductForm
from products.models import Product


class CartDetailView(ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_to_cart_form"] = AddToCartProductForm(initial={"is_replace": True})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, "cart/cart_detail.html", context=context)


class AddToCartProductView(View):
    def post(self, request, pk, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        form = AddToCartProductForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data.get("quantity")
            cart.add_product(product, quantity=quantity)
            return redirect("cart:cart_detail")


class RemoveFromCartProductView(View):
    def post(self, request, pk, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        cart.remove_product(product)
        return redirect("cart:cart_detail")


class ClearCartView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        messages.success(request, _("Your shopping cart has been cleared successfully."))
        return redirect("cart:cart_detail")
