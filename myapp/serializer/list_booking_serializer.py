from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium


class ListBookingSerializer(serializers.Serializer):

    result_count = serializers.SerializerMethodField()
    next_page_flg = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()

    class Meta:
        fields = ('result_count', 'next_page_flg', 'bookings')

    def get_result_count(self, data):
        return self.filteredBookings.count()

    def get_next_page_flg(self, data):
        user_id = self.request.user.id
        all_bookings = StadiumRegister.objects.filter(user=user_id)
        return all_bookings[self.page * self.result_limit:(self.page+1)*self.result_limit].count() > 0

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
            return int(self.request.GET.get('page'))
        except:
            raise serializers.ValidationError({'error': 'page is not valid'})

    @property
    def result_limit(self):
        try:
            return int(self.request.GET.get('result_limit'))
        except:
            raise serializers.ValidationError(
                {'error': 'result_limit is not valid'})

    @property
    def filteredBookings(self):
        user_id = self.request.user.id
        all_bookings = StadiumRegister.objects.filter(user=user_id)
        bookings = all_bookings[(self.page-1) *
                                self.result_limit:self.page*self.result_limit]
        return bookings


class BookingSerializer(serializers.ModelSerializer):

    stadium = serializers.SerializerMethodField()

    class Meta:
        model = StadiumRegister
        fields = ('id', 'stadium', 'time_from', 'time_to', 'status')

    def get_stadium(self, data):
        stadium_id = data.stadium_id
        stadium = Stadium.objects.get(pk=stadium_id)
        return {
            'id': stadium_id,
            'name': stadium.name,
            'phone_number': stadium.phone_number,
            'email': stadium.email,
            'price': stadium.price,
        }
