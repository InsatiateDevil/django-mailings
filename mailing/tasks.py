import smtplib
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, MailingTry


@shared_task
def create_mailing_task(mailing_id):
    mailing = Mailing.objects.filter(pk=mailing_id).first()
    if mailing:
        mailing.next_send_datetime += timedelta(minutes=mailing.period)
        if mailing.next_send_datetime > mailing.last_send_datetime:
            mailing.status = 4
        else:
            create_mailing_task.apply_async(
                (mailing.id,),
                eta=mailing.next_send_datetime
            )
        mailing.save()
        for client in mailing.clients.all():
            try:
                response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                MailingTry.objects.create(
                    status=True,
                    response=response,
                    mailing=mailing,
                    client=client
                )
            except smtplib.SMTPException as e:
                MailingTry.objects.create(
                    status=True,
                    response=str(e),
                    mailing=mailing,
                    client=client
                )
    else:
        print('ATTENTION!!!!! Mailing not found!!! create_mailing_task()')
        # TODO: add error handling


@shared_task
def activate_mailings(mailing_id):
    mailing = Mailing.objects.filter(pk=mailing_id).first()
    if mailing:
        mailing.status = 1
        mailing.save()
        create_mailing_task.apply_async(
            (mailing.id,),
            eta=mailing.next_send_datetime
        )
    else:
        print('ATTENTION!!!!! Mailing not found!!! activate_mailings()')
        # TODO: add error handling


