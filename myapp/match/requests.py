from rest_framework import serializers
from myapp.models.matches import Match
from myapp.models.user_teams import UserTeam
from myapp.models.find_matches import FindMatch
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.mail import send_mail


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

class MatchAcceptSerializer(serializers.ModelSerializer):
    match_id = serializers.IntegerField()

    class Meta:
        model = Match
        fields = ['id', 'status', 'match_id', 'find_match_a', 'find_match_a']

    def validate(self, data):
        team_id = self.context['request'].data['team_id']
        find_match = self.instance.find_match_a
        other_find_match = self.instance.find_match_b
        if self.instance.find_match_b.team.id == team_id:
            find_match = self.instance.find_match_b
            other_find_match = self.instance.find_match_a
        
        # check match id is of team of current user
        if find_match.team.id != team_id and other_find_match.team.id != team_id:
            raise serializers.ValidationError({"permission": "This match request is not your team"})
        
        if self.instance.status == 'ACCEPTED':
            raise serializers.ValidationError({"status": "You and another team already accepted this match"})

        if self.instance.status == 'REJECTED' or find_match.status == 'REJECTED':
            raise serializers.ValidationError({"status": "You or another team already reject this matching"})

        if find_match.status == 'PENDING':
            raise serializers.ValidationError({"status": "This request findmatch is pending to match"})

        return data

    def update(self, instance, validated_data):
        team_id = self.context['request'].data['team_id']
        find_match = instance.find_match_a
        other_find_match = instance.find_match_b
        find_match_is_a = True
        if instance.find_match_b.team.id == team_id:
            find_match_is_a = False
            find_match = instance.find_match_b
            other_find_match = instance.find_match_a

        find_match.status = validated_data['status']
        find_match.save()

        if validated_data['status'] == 'REJECTED':
            instance.status = validated_data['status']
            if other_find_match.status != 'REJECTED':
                other_caption = UserTeam.custom_objects.my_caption(other_find_match.team_id)
                other_find_match.status = 'PENDING'
                other_find_match.save()
                # sendmail to notify for other team
                send_mail('Your rival has rejected this match',
                    'Your rival has rejected this match, please wait until we make new match for your team',
                    'noreply@worldtour.vn',
                    [other_caption.email,]
                )
        else:
            if other_find_match.status == 'ACCEPTED':
                other_caption = UserTeam.custom_objects.my_caption(other_find_match.team_id)
                instance.status = 'ACCEPTED'
                # sendmail to 2 team
                send_mail('Your rival has accepted this match',
                    'Your rival has accepted this match, This match has been create',
                    'noreply@worldtour.vn',
                    [self.context['request'].user.email, other_caption.email]
                )
        instance.save()

        return instance
