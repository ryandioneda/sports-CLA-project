from django.core.management import BaseCommand
from products.models import Rental

class Command(BaseCommand):
    def handle(self, *args, **options):

        rentals = Rental.objects.all()

        if rentals.count() > 0:
            for rental in rentals:
                rental_data = {
                    "User": rental.user,
                    "Equipment": rental.equipment,
                    "Rental Date": rental.rental_date,
                    "Return Date": rental.return_date,
                    "Is Active": rental.active
                }
                self.stdout.write(self.style.SUCCESS(f"{rental_data}"))
        else:
            self.stdout.write(self.style.ERROR("No rentals found."))

