import time
from datetime import timedelta
from django.utils import timezone
from django.db import DatabaseError, transaction
from django.contrib.contenttypes.models import ContentType
import logging
from cronjob.job import job_const
logger = logging.getLogger('cronjob')
import sys
RESULT_LIMIT = 10000
def match_users_request():
    JOB_NAME = sys._getframe().f_code.co_name
    try:
        logger.info(f"Start {JOB_NAME}")
        logger.info(f'{JOB_NAME} successful')
        pass
    except Exception as err:
        logger.error(f'{JOB_NAME} failed {err}')
        