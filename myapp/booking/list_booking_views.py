from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models.stadium_registers import StadiumRegister
from myapp.serializer.list_booking_serializer import ListBookingSerializer
from rest_framework.permissions import IsAuthenticated


class ListBookingView(GenericAPIView):

    serializer_class = ListBookingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
