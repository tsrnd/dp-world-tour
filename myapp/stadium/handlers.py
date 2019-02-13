import inject, json, logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from myapp.models.stadiums import Stadium
from shared.base_handler import *
from myapp.serializer.stadium_serializer import StadiumSerializer
from rest_framework.response import Response
from myapp.stadium.request import ListStadiumSerializer
import datetime
from rest_framework.generics import GenericAPIView
from datetime import datetime, date, time, timedelta
from myapp.models.stadium_registers import StadiumRegister
from myapp.stadium.request import ListStadiumResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import timedelta

logger = logging.getLogger(__name__)

RESULT_LIMIT_DEFAULT = 20
PAGE_DEFAULT = 1


class StadiumHandler(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = ListStadiumSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        request_data = {
            k: (lambda x: int(x))(v)
            for k, v in request.query_params.items()
            if v is not None and v != ''
        }
        timestamp_time_from = datetime.fromtimestamp(request_data['time_from'])
        time_from_dt = timestamp_time_from.strftime('%Y-%m-%d %H:%M:%S+00')
        timestamp_time_to = datetime.fromtimestamp(request_data['time_to'])
        time_to_dt = timestamp_time_to.strftime('%Y-%m-%d %H:%M:%S+00')
        stadium_registed_list = StadiumRegister.objects.filter(
            (Q(time_from__lt=time_from_dt) & Q(time_to__gt=time_from_dt)
             | Q(time_from__lt=time_to_dt) & Q(time_to__gt=time_to_dt)
             ) & ~Q(status='Cancel')).values_list('stadium_id').all()
        stadium_available = Stadium.objects.exclude(
            id__in=stadium_registed_list).order_by('id')
        if ('min_price' in request_data) & ('max_price' in request_data):
            stadium_available = stadium_available.filter(price__range=(request_data['min_price'],request_data['max_price']))
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
        result_limit = request.GET.get('result_limit', RESULT_LIMIT_DEFAULT)
        page = request.GET.get('page', PAGE_DEFAULT)
        paginator = Paginator(stadium_available, result_limit)
        try:
            stadiums = paginator.page(page)
        except PageNotAnInteger:
            stadiums = paginator.page(PAGE_DEFAULT)
        except EmptyPage:
            stadiums = paginator.page(paginator.num_pages)

        serializer = StadiumSerializer(stadiums, many=True)
        response_data = {
            "result_count": stadium_available.count(),
            "page": int(page),
            "next_page_flg": stadiums.has_next(),
            "stadium": serializer.data,
        }
        return Response(response_data)
