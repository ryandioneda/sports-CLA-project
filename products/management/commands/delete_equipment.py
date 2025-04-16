from django.core.management import BaseCommand
from products.models import Equipment

class Command(BaseCommand):
    def handle(self, *args, **options):

        Equipment.objects.all().delete()

        if Equipment.objects.all().count() == 0:
            self.stdout.write(self.style.SUCCESS("Successfully deleted all equipment objects."))
        else:
            self.stdout.write(self.style.ERROR("Failed to delete all equipment objects."))