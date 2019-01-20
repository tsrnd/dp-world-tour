from django.core import validators
from rest_framework import serializers

class ListStadium(serializers.Serializer):
    time_from = serializers.IntegerField(required=False)
    time_to = serializers.IntegerField(required=False)
    price = serializers.IntegerField(required=False)
    result_limit = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
