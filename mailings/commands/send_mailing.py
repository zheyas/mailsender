from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from mailings.models import Mailing


class Command(BaseCommand):

    help = "Send all scheduled mailings"

    def handle(self, *args, **kwargs):
        for mailing in Mailing.objects.filter(status="Запущена"):
            for client in mailing.recipients.all():
                send_mail(
                    mailing.message.subject, mailing.message.body, None, [client.email]
                )
            mailing.status = "Завершена"
            mailing.save()
