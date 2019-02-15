import time
from django.utils import timezone
from django.db import DatabaseError, transaction
from django.db.models import Q
import logging
import sys
from myapp.models.find_matches import FindMatch
from myapp.models.matches import Match
from myapp.models.cronjob import CronjobModel

logger = logging.getLogger('cronjob')
JOB_NAME = 'REMOVE_FIND_MATCHS'

def remove_find_matchs():
    try:
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=1, updated_at=timezone.now())
        logger.info(f"Start {JOB_NAME}")
        
        with transaction.atomic():
            Match.objects.filter(date_match__lt=timezone.now()).filter(Q(status='WAITING') | Q(status='PENDING')).delete()
            FindMatch.objects.filter(date_match__lt=timezone.now()).filter(Q(status='WAITING') | Q(status='PENDING')).delete()
            CronjobModel.objects.filter(job_name=JOB_NAME).update(status=2, updated_at=timezone.now())

        logger.info(f'{JOB_NAME} successful')
        pass
    except Exception as err:
        logger.error(f'{JOB_NAME} failed {err}')
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=4, updated_at=timezone.now())

        