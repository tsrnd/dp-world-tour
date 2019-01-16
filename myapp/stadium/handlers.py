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
from datetime import timedelta

logger = logging.getLogger(__name__)


class StadiumHandler(APIView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    def get(self, request):
        response = self.bh.validate(ListStadium, request.GET)
        if response is not None:
            return response
        request_data = request.POST.dict()
        time_from = request_data.get('time_from')
        time_to = request_data.get('time_to')
        price = request_data.get('price')
        result_limit = request_data.get('result_limit', 20)
        page = request_data.get('page', 1)
        r1 = {
            'time_from': time_from,
            'time_to': time_to,
            'price': price,
            'result_limit': result_limit,
            'page': page,
        }
        print("-=-=-=--=-=",r1)
        r2 = {k: v for k, v in r1.items() if v is not None and v != ''}
        print("------------", r2)
        stadium_list = self.usecase.get_list_stadium(r2)
        serializer = StadiumSerializer(stadium_list, many=True)
        return Response(serializer.data)
        