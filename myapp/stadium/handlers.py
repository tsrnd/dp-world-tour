import inject, json, logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from myapp.stadium.usecases import *
from shared.base_handler import *
from myapp.serializers import StadiumSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class StadiumHandler(APIView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    def get(self, request):
            stadium_list = self.usecase.get_list_stadium()
            serializer = StadiumSerializer(stadium_list, many=True)
            return Response(data=serializer.data)
            # serializer.data
        # return render(request, 'stadium/stadium_list.html', context=serializer.data)
        
