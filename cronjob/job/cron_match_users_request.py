import time
from datetime import timedelta
from django.utils import timezone
from django.db import DatabaseError, transaction
from django.contrib.contenttypes.models import ContentType
import logging
from cronjob.job import job_const
import sys
from myapp.models.find_matches import FindMatch
from myapp.models.matches import Match
from myapp.models.cronjob import CronjobModel
from django.db import models
from django.core.mail import send_mail

logger = logging.getLogger('cronjob')
JOB_NAME = 'MATCH_USER_REQUESTS'

class FindMatchResult(models.Model):
    email = models.EmailField(blank=True)
    date_match = models.DateTimeField()
    find_match_id = models.IntegerField()
def match_users_request():
    try:
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=1, updated_at=timezone.now())
        logger.info(f"Start {JOB_NAME}")
        find_match_rqs = FindMatchResult.objects.raw('''
            SELECT 1 as id, a.id as find_match_id, a.date_match, auth_user.email
            FROM
            (SELECT myapp_findmatch.*,
                    tmpJoin2.max,
                    rank() OVER (PARTITION BY myapp_findmatch.date_match
                                ORDER BY created_at,
                                            id ASC) AS ranking
            FROM myapp_findmatch
            INNER JOIN
                (SELECT date_match
                FROM myapp_findmatch
                WHERE status = 'PD'
                GROUP BY date_match
                HAVING count(date_match) > 1 AND date_match > current_date) AS tmpJoin ON tmpJoin.date_match = myapp_findmatch.date_match
            INNER JOIN
                (SELECT date_match,
                        max(ranking)
                FROM
                    (SELECT myapp_findmatch.*, 
                            rank() OVER (PARTITION BY myapp_findmatch.date_match
                                        ORDER BY created_at,
                                                id ASC) AS ranking
                    FROM myapp_findmatch) AS tmptbl
                GROUP BY date_match) AS tmpJoin2 ON tmpJoin2.date_match = myapp_findmatch.date_match) AS a
                INNER JOIN myapp_userteam ON myapp_userteam.team_id = a.team_id
                    AND myapp_userteam.roll = 'CN'
                INNER JOIN auth_user ON auth_user.id = myapp_userteam.user_id
            WHERE (MOD(a.max,2) = 0
                AND a.ranking <= 10)
            OR (MOD(a.max,2) = 1
                AND a.ranking < a.max)
        ''')
        list_id_find_match = []
        arr_match = []
        for i in range(0, len(find_match_rqs), 2):
            arr_match.append(Match(
                date_match=find_match_rqs[i].date_match,
                status='PD',
                find_match_a_id=find_match_rqs[i].find_match_id,
                find_match_b_id=find_match_rqs[i+1].find_match_id,
            ))
            list_id_find_match.extend([find_match_rqs[i].find_match_id, find_match_rqs[i+1].find_match_id])
            # send_mail(
            #     'Subject here',
            #     'Here is the message.',
            #     'sender@gmail.com',
            #     ['reciever@gmail.com'],
            #     fail_silently=False,
            # )
        
        with transaction.atomic():
            FindMatch.objects.filter(pk__in=list_id_find_match).update(status='WA', updated_at=timezone.now())
            Match.objects.bulk_create(arr_match)
            CronjobModel.objects.filter(job_name=JOB_NAME).update(status=2, updated_at=timezone.now())

        logger.info(f'{JOB_NAME} successful')
        pass
    except Exception as err:
        logger.error(f'{JOB_NAME} failed {err}')
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=4, updated_at=timezone.now())

        