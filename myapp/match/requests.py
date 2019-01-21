from rest_framework import serializers
from myapp.models.user_teams import UserTeam
from myapp.models.find_matches import FindMatch
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


class FindMatchSerializer(serializers.Serializer):
    date_match = serializers.IntegerField(max_value=9999999999)
    team_id = serializers.IntegerField()
    default_error_messages = {
        'date_match_exist': _('Date match exist'),
    }

    def __init__(self, *args, **kwargs):
        super(FindMatchSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        dt = datetime.utcfromtimestamp(
            attrs.get('date_match')).strftime('%Y-%m-%d')
        findmatch = FindMatch.objects.filter(date_match__date = dt, team__pk = attrs.get('team_id')).exclude(status = "REJECTED")
        if len(findmatch) <= 0:
            return attrs
        else:
            raise serializers.ValidationError(
                self.error_messages['date_match_exist'])

    def create(self, validated_data):
        findMatch = FindMatch(
            date_match=datetime.utcfromtimestamp(validated_data['date_match']),
            team_id=validated_data['team_id']
        )
        findMatch.save()
        return findMatch
