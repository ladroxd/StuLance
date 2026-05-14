from django.utils.translation import get_language


class TrackUserLanguageMiddleware:
    """Persist the active language on the user record so notifications can be
    translated into the recipient's preferred language at creation time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            lang = get_language() or ''
            if lang and request.user.language != lang:
                request.user.language = lang
                request.user.save(update_fields=['language'])
        return response
