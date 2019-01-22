from django.db import models


class StadiumManager(models.Manager):
    def is_ready(self):
        pass

class Stadium(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=217)
    price = models.IntegerField()
    bank_num = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()
    custom_objects = StadiumManager()

    class Meta:
        app_label = 'myapp'
