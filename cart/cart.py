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
            self.cart[product_id]["quantity"] = quantity

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
        Return amount of total price products
        """
        return sum([product_obj["product"].price * product_obj["quantity"] for product_obj in self])

    def get_count_items(self):
        """
        Return count of all items
        """
        return sum([product_obj["quantity"] for product_obj in self])

    def is_exist_product_in_cart(self, product):
        """
        Check product exist in cart, if exist return True otherwise False
        """
        product_id = str(product.id)
        return True if self.cart.get(product_id) else False

    def get_quantity_of_product_in_cart(self, product):
        """
        Return quantity of specific product in cart, if product doesn't exist in cart return 0
        """
        product_id = str(product.id)
        if self.is_exist_product_in_cart(product):
            return self.cart[product_id]["quantity"]
        return 0

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
        cart_copy = deepcopy(self.cart)
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

