from django.contrib import admin
from .models import Equipment, Review, Borrow_Request, Rental
# Register your models here.
admin.site.register(Equipment)
admin.site.register(Review)
admin.site.register(Borrow_Request)
admin.site.register(Rental)