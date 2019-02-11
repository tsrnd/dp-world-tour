from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from shared.base_handler import BaseHandler
from myapp.serializer.booking_detail_serializer import BookingDetailSerializer
from myapp.models.stadium_registers import StadiumRegister
import inject
from shared import utils
from datetime import datetime, timedelta
from django.db.models import Q

DATE_FORMAT = '%Y-%m-%d %H:%M:%S+00'


class BookingDetail(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = BookingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_booking):
        user_id = self.request.user.id
        try:
            time_from = int(self.request.GET.get('time_from'))
        except:
            return Response({'error': 'time_from must be timestamp'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            time_to = int(self.request.GET.get('time_to'))
        except:
            return Response({'error': 'time_to must be timestamp'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            stadium = StadiumRegister.objects.get(
                Q(time_from__lte=utils.convertTimestampToString(
                    time_from, dateFormat=DATE_FORMAT))
                & Q(time_to__gte=utils.convertTimestampToString(time_to, dateFormat=DATE_FORMAT))
                & Q(user=user_id)
                & Q(stadium=id_booking)
                & Q(deleted_at__isnull=True))
        except:
            return Response({'error': 'stadium is not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingDetailSerializer(stadium, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
