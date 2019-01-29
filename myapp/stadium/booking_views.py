import inject
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium
from myapp.stadium.booking_serializer import BookingStadiumSerializer
from shared.base_handler import BaseHandler
from rest_framework.permissions import (
    IsAuthenticated,
)
from myapp.permission.user_permission import (
    IsNormalUser,
)


class BookingView(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = BookingStadiumSerializer
    permission_classes = [IsAuthenticated, IsNormalUser, ]
    queryset = StadiumRegister.objects.all()
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        request_data = request.POST.copy()
        request_data['stadium'] = kwargs['pk']
        serializer = self.get_serializer(data=request_data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        serializer.save()
        context = {
            "message": "Create request booking successfully"
        }
        return Response(
            context,
            status=201,
        )
