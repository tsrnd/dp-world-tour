from django.db import models


class FindMatchManager(models.Manager):
    def is_accepted(self):
        pass

class FindMatch(models.Model):
    PD = 'PENDING'
    WA = 'WAITING'
    AC = 'ACCEPTED'
    RJ = 'REJECTED'
    REQUEST_STATUS = (
        (PD, 'Pending'),
        (AC, 'Accepted'),
        (RJ, 'Rejected'),
        (WA, 'Waiting'),
    )
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING)
    date_match = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=REQUEST_STATUS,
        default=PD
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        app_label = 'myapp'
        unique_together = ('team', 'date_match', 'status', )

    objects = models.Manager()
    custom_objects = FindMatchManager()
