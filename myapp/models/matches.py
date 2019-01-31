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
    find_match_a = models.ForeignKey('FindMatch', on_delete=models.DO_NOTHING, related_name='team_a')
    find_match_b = models.ForeignKey('FindMatch', on_delete=models.DO_NOTHING, related_name='team_b')
    date_match = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=MATCH_STATUS,
        default=PD
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        app_label = 'myapp'
        unique_together = ('find_match_a', 'find_match_b', 'date_match', 'status')

    objects = models.Manager()
    custom_objects = MatchManager()
