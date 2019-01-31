from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium
from myapp.serializer.stadium_serializer import StadiumSerializer
from django.core.paginator import Paginator


class ListBookingSerializer(serializers.Serializer):

    result_count = serializers.SerializerMethodField()
    next_page_flg = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()

    class Meta:
        fields = ('result_count', 'next_page_flg', 'bookings')

    def get_result_count(self, data):
        return self.filteredBookings.count()

    def get_next_page_flg(self, data):
        return self.paginator.page(self.page).has_next()

    def get_bookings(self, data):
        booking_serializer = BookingSerializer(
            self.filteredBookings, many=True, read_only=True)
        return booking_serializer.data

    @property
    def request(self):
        return self.context['request']

    @property
    def page(self):
        try:
            page = int(self.request.GET.get('page'))
        except:
            raise serializers.ValidationError({'error': 'page is not valid'})
        if page <= 0:
            raise serializers.ValidationError(
                {'error': 'page must be positive number'})
        return page

    @property
    def result_limit(self):
        try:
            limit = int(self.request.GET.get('result_limit'))
        except:
            raise serializers.ValidationError(
                {'error': 'result_limit is not valid'})
        if limit < 0:
            raise serializers.ValidationError(
                {'error': 'limit must be positive number'})
        return limit

    @property
    def all_bookings(self):
        user_id = self.request.user.id
        return StadiumRegister.objects.filter(user=user_id, deleted_at__isnull=True)

    @property
    def paginator(self):
        return Paginator(self.all_bookings, self.result_limit)

    @property
    def filteredBookings(self):
        return self.paginator.page(self.page).object_list


class BookingSerializer(serializers.ModelSerializer):

    stadium = StadiumSerializer(
        {'exclude_fields': ['created_at', 'updated_at', 'deleted_at']})

    class Meta:
        model = StadiumRegister
        fields = ('id', 'stadium', 'time_from',
                  'time_to', 'status', 'total_price')
