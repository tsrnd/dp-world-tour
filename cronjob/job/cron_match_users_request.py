import time
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
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from threading import Thread
from django.template.loader import render_to_string
RECORDS_PER_THREAD = 50
logger = logging.getLogger('cronjob')
JOB_NAME = 'MATCH_USER_REQUESTS'
User = get_user_model()
class FindMatchResult(models.Model):
    email = models.EmailField(blank=True)
    username = models.CharField(blank=True)
    date_match = models.DateTimeField()
    find_match_id = models.IntegerField()
def match_users_request():
    try:
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=1, updated_at=timezone.now())
        logger.info(f"Start {JOB_NAME}")
        find_match_rqs = FindMatchResult.objects.raw('''
            SELECT 1 as id, a.id as find_match_id, a.date_match, auth_user.email, auth_user.username
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
                WHERE status = 'PENDING'
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
                    AND myapp_userteam.roll = 'CAPTION'
                INNER JOIN auth_user ON auth_user.id = myapp_userteam.user_id
            WHERE (MOD(a.max,2) = 0
                AND a.ranking <= 10)
            OR (MOD(a.max,2) = 1
                AND a.ranking < a.max)
            ORDER BY a.date_match
        ''')
        list_id_find_match = []
        arr_match = []
        index_loop = 0
        custom_find_match = []
        while index_loop < len(find_match_rqs)-1:
            if find_match_rqs[index_loop].date_match == find_match_rqs[index_loop+1].date_match:
                custom_find_match.extend([find_match_rqs[index_loop], find_match_rqs[index_loop+1]])
                index_loop = index_loop + 2
            else:
                index_loop = index_loop + 1

        for i in range(0, len(custom_find_match), 2):
            arr_match.append(Match(
                date_match=custom_find_match[i].date_match,
                status='PENDING',
                find_match_a_id=custom_find_match[i].find_match_id,
                find_match_b_id=custom_find_match[i+1].find_match_id,
            ))
            list_id_find_match.extend([custom_find_match[i].find_match_id, custom_find_match[i+1].find_match_id])
        with transaction.atomic():
            FindMatch.objects.filter(pk__in=list_id_find_match).update(status='WAITING', updated_at=timezone.now())
            Match.objects.bulk_create(arr_match)
            CronjobModel.objects.filter(job_name=JOB_NAME).update(status=2, updated_at=timezone.now())

        threads = []
        for k in range(0, len(custom_find_match), RECORDS_PER_THREAD):
            threads.append(Thread(target=sendEmail, args=(custom_find_match[k:k+RECORDS_PER_THREAD],)))
            threads[-1].start()
        for thread in threads:
            thread.join()
        logger.info(f'{JOB_NAME} successful')
        pass
    except Exception as err:
        logger.error(f'{JOB_NAME} failed {err}')
        CronjobModel.objects.filter(job_name=JOB_NAME).update(status=4, updated_at=timezone.now())

        
def sendEmail(list):
    for i in range(0, len(list), 2):
        mess1 = render_to_string('confirm_email.html', {
            'username': list[i].username,
            'opponent': list[i+1].username,
            'link': 'http://localhost:8001/match/' + str(list[i].find_match_id) + '/detail',
            'date_match': list[i].date_match,
        })
        mess2 = render_to_string('confirm_email.html', {
            'username': list[i+1].username,
            'opponent': list[i].username,
            'link': 'http://localhost:8001/match/' + str(list[i+1].find_match_id) + '/detail',
            'date_match': list[i].date_match,
        })
        print("here1ldjsalkdjsalkdjsalkdjsal")
        EmailMessage('Confirm request find match', mess1, "noreply@worldtour.vn", to=[list[i].email]).send()
        EmailMessage('Confirm request find match', mess2, "noreply@worldtour.vn",to=[list[i+1].email]).send()
