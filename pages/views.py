from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import activate, get_language
from django.conf import settings


def home_page_view(request):
    return render(request, "home.html")


def change_language_view(request):
    next_page = request.GET.get("next_page")
    language_code = request.GET.get("lang", get_language())
    if language_code not in list(map(lambda lang: lang[0], settings.LANGUAGES)):
        language_code = get_language()

    response = HttpResponseRedirect(next_page)

    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    activate(language_code)

    return response
