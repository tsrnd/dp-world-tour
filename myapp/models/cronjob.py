from django.db import models
from django.conf import settings

status_choices = (
    (0, 'init'),
    (1, 'running'),
    (2, 'success'),
    (3, 'fail'),
)

class CronjobManager(models.Manager):
    
    def is_exist(self, job_hash):
        try:
            _ = CronjobModel.objects.get(job_hash=job_hash, deleted_at__isnull=True)
            return True
        except CronjobModel.DoesNotExist:
            return False

class CronjobModel(models.Model):
    job_hash = models.CharField(max_length=100, unique=True, null=True, blank=True)
    job_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    job_schedule = models.CharField(max_length=20)
    job_path = models.CharField(max_length=500)
    last_run_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=status_choices, default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()
    custom_objects = CronjobManager()

    class Meta:
        app_label = 'myapp'
        db_table = "cronjob"
