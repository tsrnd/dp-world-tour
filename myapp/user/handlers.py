import inject, json, logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *

logger = logging.getLogger(__name__)


class AuthHandler(TemplateView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    def post(self, request):
        response = self.bh.validate(UserRegister, request.POST)
        if response is not None:
            return response
        context = {"message": "validate success"}
        return render(request, 'base.html', context)

    def get(self, request):
        # response = self.bh.validate(UserRegister, request.POST)
        context = {"message": "validate success"}
        return render(request, 'authen/register.html', context)
