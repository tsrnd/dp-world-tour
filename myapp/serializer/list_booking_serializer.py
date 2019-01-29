from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.stadiums import Stadium


class ListBookingSerializer(serializers.ModelSerializer):

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
