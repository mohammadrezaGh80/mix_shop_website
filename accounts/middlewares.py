from django.shortcuts import reverse


class ClearSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls_name = ["accounts:register_step_one", "accounts:register_step_two"]

        if request.path not in [reverse(url_name) for url_name in exempt_urls_name] and \
                request.session.get("info_user"):
            del request.session["info_user"]
        response = self.get_response(request)

        return response
