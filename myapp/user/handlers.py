import inject
import json
import logging

from django.http import HttpResponse
from django.views import View
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *
from myapp.models.users import UserApp
from django.conf import settings
from myapp.user.requests import UserGetToken

logger = logging.getLogger(__name__)


class AuthHandler(View):
    usecase = inject.attr(UserUsecase)
    bh = inject.attr(BaseHandler)

    def post(self, request):
        response = self.bh.validate(UserRegister, request.POST)
        if response is not None:
            return response

        return HttpResponse(
            json.dumps({"message": "validate success"}),
            status=200,
            content_type='application/json'
        )


class AuthenticateUser(View):
    usecase = inject.attr(UserUsecase)
    bh = inject.attr(BaseHandler)

    def post(self, request):
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = UserApp.objects.first()
            if user:
                try:
                    user_details = {}
                    user_details['name'] = user.username
                    user_details['token'] = user.token
                    user_details['expire_time'] = settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
                    return HttpResponse(
                        json.dumps(user_details),
                        status=200,
                        content_type='application/json'
                    )

                except Exception as e:
                    raise e
            else:
                res = {
                    'error':
                    'can not authenticate with the given credentials or the account has been deactivated'
                }
                return HttpResponse(
                    json.dumps(res),
                    status=200,
                    content_type='application/json'
                )
        except UserApp.DoesNotExist:
            res = {'error': 'please provide a email and a password'}
            return HttpResponse(
                json.dumps(res),
                status=200,
                content_type='application/json'
            )
