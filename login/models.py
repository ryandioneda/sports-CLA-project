from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now

# Create your models here.


class ReviewField:
    review_text = models.CharField()
    review_rating = models.IntegerField()
    profile = models.ForeignKey(
        "Profile", related_name="reviews", on_delete=models.CASCADE
    )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(null=True, max_length=64)
    lname = models.CharField(null=True, max_length=64)
    birth_date = models.DateField(null=True)
    email = models.EmailField()
    date_joined = models.DateTimeField(default=now)
    address = models.CharField(null=True, max_length=128)
    city = models.CharField(null=True, max_length=64)
    state = models.CharField(null=True, max_length=5)
    zip_code = models.CharField(null=True, max_length=5)
    image = models.FileField(upload_to="media/")


class CustomPerms(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        default_permissions = ()  # disable "add", "change", "delete"
        # and "view" default permissions

        permissions = (
            ("borrower_perms", "Global borrower permissions"),
            ("lender_perms", "Global lender permissions"),
        )
