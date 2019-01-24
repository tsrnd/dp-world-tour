from rest_framework import serializers
from myapp.models.stadiums import Stadium


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('__all__')
