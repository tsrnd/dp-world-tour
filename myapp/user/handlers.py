import inject, json, logging

from django.http import HttpResponse
from django.views import View
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *

logger = logging.getLogger(__name__)


class AuthHandler(View):
    usecase = inject.attr(UsecaseInterface)
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

