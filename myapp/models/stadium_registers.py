from django.db import models
from django.conf import settings


class StadiumRegisterManager(models.Manager):
    def is_paid(self):
        pass

class StadiumRegister(models.Model):
    PD = 'PENDING'
    PA = 'PAID'
    CA = 'CANCEL'
    REGISTER_STATUS = (
        (PD, 'Pending'),
        (PA, 'Paid'),
        (CA, 'Cancel'),
    )
    stadium = models.ForeignKey('Stadium', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=REGISTER_STATUS,
        default=PD
    )
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        app_label = 'myapp'
        unique_together = ('user', 'stadium', 'time_from', )

    objects = models.Manager()
    custom_objects = StadiumRegisterManager()
