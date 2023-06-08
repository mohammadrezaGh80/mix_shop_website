from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import activate, get_language
from django.conf import settings
from django.views import View

from products.models import Product
from profiles.recent_visits import RecentVisits
from itertools import groupby
from math import ceil


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        COUNT_OF_SUGGESTION = 10

        recent_visits = RecentVisits(request)
        list_category_with_count = sorted(
            [(key, len(list(group)))
             for key, group in groupby(recent_visits, key=lambda recent_visit: recent_visit["category"])],
            key=lambda category: category[1],
            reverse=True
        )
        count_recent_visits_product = sum([group[1] for group in list_category_with_count])
        list_category_with_count_suggestion = [
            (list_category_with_count[index][0], list_category_with_count[index][1] +
             ceil((COUNT_OF_SUGGESTION - count_recent_visits_product - index) / len(list_category_with_count)))
            for index in range(len(list_category_with_count))
        ]

        suggestion_products = []
        for category_group in list_category_with_count_suggestion:
            products = Product.objects.filter(category__category_name=category_group[0])[:category_group[1]]
            suggestion_products.extend(products)

        return render(request, "home.html", context={"suggestion_products": suggestion_products})


def change_language_view(request):
    next_page = request.GET.get("next_page")
    language_code = request.GET.get("lang", get_language())
    if language_code not in list(map(lambda lang: lang[0], settings.LANGUAGES)):
        language_code = get_language()

    response = HttpResponseRedirect(next_page)

    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    activate(language_code)

    return response
