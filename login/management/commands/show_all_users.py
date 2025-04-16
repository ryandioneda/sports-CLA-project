from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()

        if users.count() > 0:
            for user in users:
                self.stdout.write(self.style.SUCCESS(f"{user}"))
        else:
            self.stdout.write(self.style.ERROR("No users found."))