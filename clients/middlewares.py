from django.shortcuts import HttpResponseRedirect


class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        if request.COOKIES.get('token') is None and request.path != '/user/login' and request.path != '/user/register':
            return HttpResponseRedirect('/user/login')

        # Code to be executed for each request/response after
        # the view is called.

        return response