from django.core.management.base import BaseCommand
from allauth.account.models import EmailAddress

class Command(BaseCommand):
    def handle(self, *args, **options):

        emails = EmailAddress.objects.all()

        if emails.count() > 0:
            for email in emails:
                self.stdout.write(self.style.SUCCESS(f"{email}"))
        else:
            self.stdout.write(self.style.ERROR("No emails found."))