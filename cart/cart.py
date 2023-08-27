from django.contrib import messages
from django.utils.translation import gettext as _

from copy import deepcopy

from products.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request
        self.session = request.session

        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add_product(self, product, quantity=1):
        """
        Add product to cart with specific quantity. if product exist in cart, product quantity add with quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {"product_id": product_id, "quantity": quantity}
        else:
            self.cart[product_id]["quantity"] += quantity

        messages.success(self.request, _("Product has been successfully added to the cart."))
        self.save()

    def remove_product(self, product):
        """
        Remove product form cart if exist in cart.
        """
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()
            messages.success(self.request, _("Product has been successfully removed from the cart."))

    def get_total_price(self):
        """
        Get amount of total price products
        """
        return sum([product_obj["product"].price * product_obj["quantity"] for product_obj in self.cart.values()])

    def clear(self):
        """
        Clear all of cart
        """
        del self.session["cart"]

    def __len__(self):
        """
        Return count of product in cart
        """
        return len(self.cart.keys())

    def __iter__(self):
        cart_copy = self.cart.copy()
        product_ids = cart_copy.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            cart_copy[str(product.id)]["product"] = product

        for item in cart_copy.values():
            item["total_price"] = item["product"].price * item["quantity"]
            yield item

    def save(self):
        """
        modify session when any change occurs in the session
        """
        self.session.modified = True

