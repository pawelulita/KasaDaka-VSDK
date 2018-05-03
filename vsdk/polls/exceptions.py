from django.http import Http404


class NoCallerIDError(Http404):
    """
    This exception is thrown when there's no caller ID in the GET parameters
    of the request, and caller ID is required.
    """