from products.models import Product


class RecentVisits:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        recent_visits = self.session.get("recent_visits")
        if not recent_visits:
            recent_visits = self.session["recent_visits"] = {}
        self.recent_visits = recent_visits

    def add_product(self, product, maximum_product=10):
        product_id = str(product.id)

        if product_id not in self.recent_visits.keys():
            if len(self.recent_visits) == maximum_product:
                self.recent_visits.pop(dict(reversed(self.recent_visits.items())).popitem()[0])
            self.recent_visits[product_id] = {"product_id": product.id}
        else:
            self.recent_visits = {key: value for key, value in
                                  self.recent_visits.items() if
                                  key != product_id} | {product_id: self.recent_visits[product_id]}
            self.session["recent_visits"] = self.recent_visits

        self.save()

    def remove_product(self, product):
        product_id = str(product.id)

        if product_id in self.recent_visits.keys():
            del self.recent_visits[product_id]
        self.save()

    def clear(self):
        del self.session["recent_visits"]

    def __iter__(self):
        recent_visits_copy = self.recent_visits.copy()

        product_ids = recent_visits_copy.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            recent_visits_copy[str(product.id)]["product"] = product
            recent_visits_copy[str(product.id)]["category"] = product.category.category_name

        for item in dict(reversed(recent_visits_copy.items())).values():
            yield item

    def __len__(self):
        return len(self.recent_visits.keys())

    def save(self):
        """
        modify session when any change occurs in the session
        """
        self.session.modified = True
