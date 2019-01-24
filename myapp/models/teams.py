from django.db import models
from django.conf import settings


class TeamManager(models.Manager):
    def get_name(self):
        pass
    
    def is_exist(self, team_name):
        try:
            _ = Team.objects.get(team_name=team_name, deleted_at__isnull=True)
            return True
        except Team.DoesNotExist:
            return False

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_profile_image_url = models.CharField(max_length=217, null=True)
    acronym = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()
    custom_objects = TeamManager()

    class Meta:
        app_label = 'myapp'
