import inject, json, logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from myapp.stadium.usecases import *
from shared.base_handler import *
from myapp.serializer.stadium_serializer import StadiumSerializer
from rest_framework.response import Response
from myapp.stadium.request import ListStadiumSerializer
import datetime
from rest_framework.generics import GenericAPIView
from datetime import datetime, date, time, timedelta
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import ListStadiumResponse
from django.db.models import Q

from datetime import timedelta

logger = logging.getLogger(__name__)


class StadiumHandler(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = ListStadiumSerializer

    def get(self, request, *args, **kwargs):
        request_data = {k: (lambda x: int(x))(v) for k, v in request.query_params.items() if v is not None and v != ''}
        # request_data = {k: v for k, v in request.query_params.items() if v != '' and v is not None}
        serializer = self.get_serializer(data=request.query_params)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        timestamp_time_from = datetime.fromtimestamp(request_data['time_from'])
        time_from_dt = timestamp_time_from.strftime('%Y-%m-%d %H:%M:%S+00')
        timestamp_time_to = datetime.fromtimestamp(request_data['time_to'])
        time_to_dt = timestamp_time_to.strftime('%Y-%m-%d %H:%M:%S+00')
        stadium_registed_list = StadiumRegister.objects.filter((Q(time_from__lt=time_from_dt) & Q(time_to__gt=time_from_dt) | Q(time_from__lt=time_to_dt) & Q(time_to__gt=time_to_dt)) & ~Q(status='Cancel')).values_list('stadium_id').all()
        stadium_available = Stadium.objects.exclude(id__in=stadium_registed_list)
        response_stadium_list = []
        for stadium_list in stadium_available:
            stadium = ListStadiumResponse(
                stadium_list.id,
                stadium_list.name,
                stadium_list.lat,
                stadium_list.lng,
                stadium_list.phone_number,
                stadium_list.email,
                stadium_list.price,
                stadium_list.bank_num,
                )
            response_stadium_list.append(stadium)
        serializer = StadiumSerializer(response_stadium_list, many=True)
        response_data = {
            "stadium": serializer.data,
        }
        print("-=-=-=-=-=-=-====-", response_data)
        return Response(response_data)
        