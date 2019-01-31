from django.db import models
from django.conf import settings
from myapp.models.stadiums import Stadium
from django.db.models import Q


class StadiumRegisterManager(models.Manager):
    def is_paid(self):
        pass

    def is_ready(self, time_from, time_to, stadium_id):
        try:
            _ = StadiumRegister.objects.exclude(status="CANCEL").get(
            Q(time_from__lt=time_from, time_to__gt=time_from)
            | Q(time_from__lt=time_to, time_to__gt=time_to)
            | Q(time_from__gt=time_from, time_from__lt=time_to)
            | Q(time_to__gt=time_from, time_to__lt=time_to)
            | Q(time_to=time_to, time_from=time_from)
            & Q(stadium_id=stadium_id))
            return False
        except StadiumRegister.DoesNotExist:
            return True

    def get_total_price(self, time_from, time_to, stadium_id):
        try:
            stadium = Stadium.objects.get(id=stadium_id)
        except Stadium.DoesNotExist:
            return None
        hours = (time_to - time_from)
        total_price = hours.total_seconds()//3600*stadium.price
        return total_price

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
