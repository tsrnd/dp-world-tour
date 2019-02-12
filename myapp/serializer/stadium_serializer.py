from rest_framework import serializers
from myapp.models.stadiums import Stadium
from collections.abc import Iterable


class StadiumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stadium
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(StadiumSerializer, self).__init__(*args, **kwargs)
        if isinstance(args[0], Iterable) and len(args[0]) > 0 and 'exclude_fields' in args[0]:
            fields = args[0]
            for field_name in fields['exclude_fields']:
                self.fields.pop(field_name)
