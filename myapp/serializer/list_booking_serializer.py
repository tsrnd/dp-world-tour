from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium
from myapp.serializer.stadium_serializer import StadiumSerializer


class ListBookingSerializer(serializers.Serializer):

    result_count = serializers.SerializerMethodField()
    next_page_flg = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()

    class Meta:
        fields = ('result_count', 'next_page_flg', 'bookings')

    def get_result_count(self, data):
        return self.filteredBookings.count()

    def get_next_page_flg(self, data):
        return self.all_bookings[self.page * self.result_limit:(self.page+1)*self.result_limit].count() > 0

    def get_bookings(self, data):
        serial = BookingSerializer(
            self.filteredBookings, many=True, read_only=True)
        return serial.data

    @property
    def request(self):
        return self.context['request']

    @property
    def page(self):
        try:
            page = int(self.request.GET.get('page'))
        except:
            raise serializers.ValidationError({'error': 'page is not valid'})
        if page == 0:
            raise serializers.ValidationError({'error': 'page is zero'})
        return page

    @property
    def result_limit(self):
        try:
            return int(self.request.GET.get('result_limit'))
        except:
            raise serializers.ValidationError(
                {'error': 'result_limit is not valid'})

    @property
    def all_bookings(self):
        user_id = self.request.user.id
        return StadiumRegister.objects.filter(user=user_id, deleted_at__isnull=True)

    @property
    def filteredBookings(self):
        bookings = self.all_bookings[(self.page-1) *
                                     self.result_limit:self.page*self.result_limit]
        return bookings


class BookingSerializer(serializers.ModelSerializer):

    stadium = StadiumSerializer(
        {'exclude_fields': ['created_at', 'updated_at', 'deleted_at']})

    class Meta:
        model = StadiumRegister
        fields = ('id', 'stadium', 'time_from',
                  'time_to', 'status', 'total_price')
