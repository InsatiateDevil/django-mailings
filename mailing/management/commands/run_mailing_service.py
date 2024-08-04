from datetime import timedelta

from django.core.management import BaseCommand
from mailing.tasks import create_mailing_task
from mailing.models import Mailing
from mailing.services import get_datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        current_datetime = get_datetime()
        mailings = Mailing.objects.filter(status__in=[0, 1])
        for mailing in mailings:
            if mailing.status == 0 and mailing.next_send_datetime < current_datetime:
                mailing.status = 1
            if mailing.next_send_datetime < current_datetime:
                mailing.next_send_datetime = current_datetime + timedelta(minutes=1)
            mailing.save()
            if mailing.status == 1:
                create_mailing_task.apply_async(
                    (mailing.id,),
                    eta=mailing.next_send_datetime
                )
