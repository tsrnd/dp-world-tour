from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium


def convert(time):
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S+00').timestamp()


class BookingView(APIView):

    def post(self, request, stadiumID):
        # time_from from request
        timeFrom = request.POST.get('time_from')
        # time_to from request
        timeTo = request.POST.get('time_to')
        # get stadium from database
        stadium = get_object_or_404(Stadium, pk=stadiumID)
        # when stadium is valid, get stadium registered
        stadiumsRegister = StadiumRegister.objects.filter(
            Q(time_from__lt=timeFrom, time_to__gt=timeFrom)
            | Q(time_from__lt=timeTo, time_to__gt=timeTo)
            & Q(stadium_id=stadiumID)).exclude(status="CANCEL")

        if len(stadiumsRegister) > 0:
            # Please check error response later
            return HttpResponse(status=400)
        else:
            # fake user from request
            user = get_object_or_404(User, pk=196)
            newRegister = StadiumRegister()
            newRegister.stadium = stadium
            newRegister.user = user
            newRegister.time_from = timeFrom
            newRegister.time_to = timeTo
            newRegister.total_price = (
                convert(timeTo) - convert(timeFrom))/3600*stadium.price  # 1 hour = 3600s
            newRegister.save()
            return HttpResponse(status=200)
