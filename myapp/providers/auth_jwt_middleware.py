import jwt
from datetime import datetime, timedelta
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse


class JwtAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print ("Middleware executed")
        try:
            authorization = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            return HttpResponse(
                json.dumps({"message": "Authorization not in header"}),
                status=401,
                content_type='application/json'
            )
        auth = authorization.split(" ")
        if not auth or auth[0].lower() != 'bearer':
            return None
        token = auth[1]
        try:
            decoded_dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            return HttpResponse(
                json.dumps({"message": "Token invalid"}),
                status=401,
                content_type='application/json'
            )
        id = decoded_dict.get('id', None)
        exp = decoded_dict.get('exp', None)
        print(id)
        if id == None:
            return HttpResponse(
                json.dumps({"message": "Token invalid"}),
                status=401,
                content_type='application/json'
            )
        try:
            usr = User.objects.get(id=id)
        except User.DoesNotExist as e:
            raise e

        if not usr.is_active:
            raise Exception('User inactive or deleted.')
        dt = datetime.now()
        if exp < int(dt.strftime('%s')):
            raise Exception('Token Expired.')
        request.user = usr
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response