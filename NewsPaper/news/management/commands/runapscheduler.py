import logging
import os
import time as timesleep

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from news.models import Subscribers, Post
from django.utils import timezone
from datetime import datetime, time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def sending_email_to_subscribers():
    end_week = datetime.combine(timezone.now().date() - timezone.timedelta(days=1), time.max)
    start_week = datetime.combine(end_week - timezone.timedelta(days=7),time.min)

    subscribers = Subscribers.objects.exclude(user__email='')
    for subscriber in subscribers:
        user_name = subscriber.user.username
        user_mail = subscriber.user.email
        posts = Post.objects.filter(categories__in=subscriber.news_category.all(),
                                         time_create__range=(start_week, end_week))

        context = {'username': user_name, 'posts':posts,
                    'link':f'http://127.0.0.1:8000/news/'}
        html_content = render_to_string('mails_per_week.html', context)
        email = EmailMultiAlternatives(
            subject='Еженедельная рассылка новостей',
                body='',
                from_email=os.getenv('E_MAIL_FULL'),
                to=[user_mail]
            )
        email.attach_alternative(html_content, "text/html")
        email.send()
        timesleep.sleep(30)

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            sending_email_to_subscribers,
            trigger=CronTrigger(day_of_week='mon', hour='07', minute='00'),
            id="sending_email_to_subscribers",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'sending_email_to_subscribers'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week=1, hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")