
from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister
from myapp.serializer.stadium_serializer import StadiumSerializer


class BookingDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    stadium = StadiumSerializer(
        {'exclude_fields': ['created_at', 'updated_at', 'deleted_at']})
    time_from = serializers.DateTimeField(format='%s')
    time_to = serializers.DateTimeField(format='%s')
    status = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'stadium', 'time_from', 'time_to', 'status')

    def validate(self, data):
        print('validate---------')
        print(data)
        return data
