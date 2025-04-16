from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):

        User.objects.all().delete()
        users = User.objects.all()

        if users.count() == 0:
            self.stdout.write(self.style.SUCCESS("Successfully deleted all users."))
        else:
            self.stdout.write(self.style.ERROR("Failed to delete all users."))