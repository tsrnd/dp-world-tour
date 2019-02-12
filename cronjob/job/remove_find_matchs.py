import time
from django.utils import timezone
from django.db import DatabaseError, transaction
import logging
import sys
from myapp.models.find_matches import FindMatch
from myapp.models.cronjob import CronjobModel

logger = logging.getLogger('cronjob')
JOB_NAME = 'REMOVE_FIND_MATCHS'

def remove_find_matchs():
    try:
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=1, updated_at=timezone.now())
        logger.info(f"Start {JOB_NAME}")
        
        with transaction.atomic():
            FindMatch.objects.filter(date_match__lt=timezone.now()).delete()
            CronjobModel.objects.filter(job_name=JOB_NAME).update(status=2, updated_at=timezone.now())

        logger.info(f'{JOB_NAME} successful')
        pass
    except Exception as err:
        logger.error(f'{JOB_NAME} failed {err}')
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=4, updated_at=timezone.now())

        