from django.shortcuts import render, get_object_or_404, redirect
from django.views import View


from .cart import Cart
from .forms import AddToCartProductForm
from products.models import Product


class CartDetailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "cart/cart_detail.html")

    def post(self, request, *args, **kwargs):
        return render(request, "cart/cart_detail.html")


class AddToCartProductView(View):
    def post(self, request, pk, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)

        form = AddToCartProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get("quantity")
            cart.add_product(product, quantity=quantity)
            return redirect("cart:cart_detail")

