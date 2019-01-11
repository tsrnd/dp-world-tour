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
        (PD, 'Peding'),
        (PA, 'Paid'),
        (CA, 'Cancel'),
    )
    id_stadium = models.ForeignKey('Stadium', on_delete=models.DO_NOTHING)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    status = models.CharField(
        max_length=2,
        choices=REGISTER_STATUS,
        default=PD
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(blank=True)

    objects = models.Manager()
    custom_objects = StadiumRegisterManager()
