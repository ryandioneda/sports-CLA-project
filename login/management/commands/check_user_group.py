from django.core.management.base import BaseCommand
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    """Check which group a user is in using their email"""

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **kwargs):
        email = kwargs['email']

        try:
            email_object = EmailAddress.objects.get(email=email)

            user = email_object.user

            groups = user.groups.all()

            if groups.exists():
                for group in groups:
                    self.stdout.write(self.style.SUCCESS(f"{email_object} ({user}) is in {group} group."))
            else:
                self.stdout.write(self.style.ERROR(f"{email_object} ({user}) is not in any groups."))
        except:
            self.stdout.write(self.style.ERROR(f"No user found with the email {email}."))

        