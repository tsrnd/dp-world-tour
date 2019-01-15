from django.db import models
from django.conf import settings


class UserTeamManager(models.Manager):
    def is_my_team(self):
        pass

class UserTeam(models.Model):
    PD = 'PENDING'
    AC = 'ACCEPTED'
    RJ = 'REJECTED'
    INVITE_STATUS = (
        (PD, 'Pending'),
        (AC, 'Accepted'),
        (RJ, 'Rejected'),
    )
    MB = 'MEMBER'
    CN = 'CAPTION'
    ROLE_STATUS = (
        (MB, 'Member'),
        (CN, 'Caption'),
    )
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    id_team = models.ForeignKey('Team', on_delete=models.DO_NOTHING)
    roll = models.CharField(
        max_length=10,
        choices=ROLE_STATUS,
        default=MB,
    )
    status = models.CharField(
        max_length=10,
        choices=INVITE_STATUS,
        default=PD
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()
    custom_objects = UserTeamManager()
