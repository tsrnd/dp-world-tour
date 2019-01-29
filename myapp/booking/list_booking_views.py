from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models.stadium_registers import StadiumRegister
from myapp.serializer.list_booking_serializer import ListBookingSerializer
from myapp.serializer.stadium_serializer import StadiumSerializer


class ListBookingView(GenericAPIView):

    def get(self, request):
        print('user=', request.user.id)
        # Get user id
        user_id = request.user.id
        # Get page
        page = int(request.GET.get('page'))
        print('page=', page)
        # Get result_limit
        result_limit = int(request.GET.get('result_limit'))
        print('result_limit=', result_limit)
        # Get all object in database with user_id
        all_bookings = StadiumRegister.objects.filter(user=user_id)
        # Get object with page and result_limit
        bookings = all_bookings[(page-1)*result_limit:page*result_limit]
        # Get next page flag
        next_page_flg = all_bookings[page *
                                     result_limit:(page+1)*result_limit].count() > 0
        if bookings.count() == 0:
            return Response({'bookings': []}, status=status.HTTP_200_OK)
        serializer = ListBookingSerializer(bookings, many=True)
        context = {
            'result_count': bookings.count(),
            'next_page_flg': next_page_flg,
            "bookings": serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)
