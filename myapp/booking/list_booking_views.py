from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models.stadium_registers import StadiumRegister
from myapp.serializer.list_booking_serializer import ListBookingSerializer
from rest_framework.permissions import IsAuthenticated
from shared.base_handler import BaseHandler
import inject


class ListBookingView(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = ListBookingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        return Response(serializer.data, status=status.HTTP_200_OK)
