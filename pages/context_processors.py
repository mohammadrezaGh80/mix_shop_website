from django.contrib.sessions.models import Session

from itertools import groupby

from .search_history import SearchHistory


def search_history(request):
    return {"search_history": SearchHistory(request)}


def popular_searches(request):
    sessions = Session.objects.all()
    list_searches = []
    for session in sessions:
        if session.get_decoded().get("search_history"):
            list_searches.extend(session.get_decoded().get("search_history").values())
    list_popular_searches_with_count = list(
        sorted([(key, len(list(group))) for key, group in groupby(sorted(list_searches))][:5],
               key=lambda group: group[1], reverse=True)
    )

    return {"popular_searches": [group[0] for group in list_popular_searches_with_count]}
