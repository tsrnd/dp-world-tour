import inject
from myapp.models.teams import Team
from myapp.models.user_teams import UserTeam
from shared.storage import Storage
from shared.utils import detect_content_of_file, gen_file_name, get_storage_file_url
from django.conf import settings
from rest_framework.serializers import (
        HyperlinkedIdentityField,
        ModelSerializer,
        SerializerMethodField,
        ValidationError,
        CurrentUserDefault,
        DateTimeField,
        BooleanField,
    )
from django.contrib.auth.models import User
from rest_framework import serializers

class TeamCreateSerializer(ModelSerializer):
    storage = inject.attr(Storage)
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'team_profile_image_url',
            'acronym',
            'created_at',
        ]

    def validate(self, data):
        # check current user is a leader
        if UserTeam.custom_objects.is_caption(self.context['request'].user.id):
            raise ValidationError({"user": "Current user login is a leader of another team"})
        
        # check team name is exist
        if Team.custom_objects.is_exist(data["team_name"]):
            raise ValidationError({"team_name":"This team_name is already existed"})

        return data
    

    def create(self, validated_data):
        from django.db import transaction
        with transaction.atomic():
            f = self.context['request'].data['file']
            file_name = None
            if f:
                file_name = gen_file_name(f.name)
                content_type = detect_content_of_file(f)                
            team = Team.objects.create(
                team_name=validated_data['team_name'],
                acronym=validated_data['acronym'],
                team_profile_image_url=file_name,
            )
            UserTeam.objects.create(
                user=self.context['request'].user,
                team=team,
                status='ACCEPTED',
                roll='CAPTION',
            )
            if f:
                with f.open() as file_data:
                        self.storage.put_object(settings.STORAGE['bucket_name'], file_name,
                            file_data, f.size, content_type)
            return team

class TeamSerializer(ModelSerializer):
    profile_url = SerializerMethodField()
    def get_profile_url(self, obj):
        return get_storage_file_url(obj.team_profile_image_url, settings.STORAGE['bucket_name'])
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'profile_url',
            'acronym',
            'created_at',
        ]

class InviteSerializer(ModelSerializer):
    date_joined_format = serializers.DateTimeField(source='date_joined', format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = User
        fields = ('id','username','email','date_joined_format')
    

class UserTeamSerializer(ModelSerializer):
    is_caption = SerializerMethodField()
    team = TeamSerializer(read_only=True)
    
    def get_is_caption(self, obj):
        return obj.roll == 'CAPTION' 
    class Meta:
        model = UserTeam
        fields = ['id', 'is_caption', 'team']

class InvitationListSerializer(ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = UserTeam
        ordering = ('created_at',)
        fields = ['id', 'status', 'team', 'created_at']

class InvitationUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserTeam
        fields = ['id', 'status', 'user']

    def validate(self, data):
        # check invitation id is of current user

        if self.instance.user.id != self.context['request'].user.id:
            raise ValidationError({"permission": "This invitation is not your invitation"})
        
        if self.instance.status == 'REJECTED':
                raise ValidationError({"status": "You've already rejected this invitation"})
        elif self.instance.status == 'ACCEPTED':
                raise ValidationError({"status": "You've already accepted this invitation"})

        return data
