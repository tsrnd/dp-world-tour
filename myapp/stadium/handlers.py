import inject, json, logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from myapp.stadium.usecases import *
from shared.base_handler import *
from myapp.serializers import StadiumSerializer
from rest_framework.response import Response
from myapp.stadium.request import ListStadium
import datetime

logger = logging.getLogger(__name__)


class StadiumHandler(APIView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    def get(self, request):
        response = self.bh.validate(ListStadium, request.GET)
        if response is not None:
            return response
        time_from = self.request.query_params.get('time_from', datetime.datetime.now().strftime('%s'))
        time_to = self.request.query_params.get('time_to')
        price = self.request.query_params.get('price')
        stadium_list = self.usecase.get_list_stadium()
        serializer = StadiumSerializer(stadium_list, many=True)
        return Response(serializer.data)
        