from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium
from myapp.stadium.booking_serializer import BookingStadiumSerializer
from shared.base_handler import BaseHandler


class BookingView(APIView, BaseHandler):

    def post(self, request, stadiumID):
        # time_from from request
        timeFrom = request.POST.get('time_from')
        # time_to from request
        timeTo = request.POST.get('time_to')
        # when stadium is valid, get stadium registered
        stadiumsRegister = StadiumRegister.objects.filter(
            Q(time_from__lt=timeFrom, time_to__gt=timeFrom)
            | Q(time_from__lt=timeTo, time_to__gt=timeTo)
            & Q(stadium_id=stadiumID)).exclude(status="CANCEL")

        if len(stadiumsRegister) > 0:
            # Please check error response later
            return self.not_found_response()
        else:
            serializer = BookingStadiumSerializer(
                timeFrom, timeTo, stadiumID, request.user.id)
            if serializer.is_valid():
                # Save data when serializer is valid
                serializer.save()
                return HttpResponse(status=200)
            else:
                return self.not_found_response()
