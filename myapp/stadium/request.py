from django.core import validators
from rest_framework import serializers

class ListStadiumSerializer(serializers.Serializer):
    time_from = serializers.IntegerField(required=True)
    time_to = serializers.IntegerField(required=True)
    price = serializers.IntegerField(required=False)
    result_limit = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
