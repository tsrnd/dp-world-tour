from django.db import models


class MatchManager(models.Manager):
    def is_accepted(self):
        pass

class Match(models.Model):
    PD = 'PENDING'
    AC = 'ACCEPTED'
    RJ = 'REJECTED'
    MATCH_STATUS = (
        (PD, 'Pending'),
        (AC, 'Accepted'),
        (RJ, 'Rejected'),
    )
    id_find_match_a = models.ForeignKey('FindMatch', on_delete=models.DO_NOTHING, related_name='team_a')
    id_find_match_b = models.ForeignKey('FindMatch', on_delete=models.DO_NOTHING, related_name='team_b')
    date_match = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=MATCH_STATUS,
        default=PD
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    objects = models.Manager()
    custom_objects = MatchManager()
