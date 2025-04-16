from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class Collection(models.Model):

    collection_name = models.CharField(max_length=100)
    collection_description = models.TextField()

    LENDER_PRIVACY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]
    BORROWER_PRIVACY_CHOICES = [
        ("public", "Public"),
    ]
    collection_privacy = models.CharField(
        max_length=20, choices=LENDER_PRIVACY_CHOICES, default="public"
    )

    collection_private_userlist = models.ManyToManyField(
        User, blank=True, related_name="productCollections_private_userlist"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="productCollections_owned_collections",
    )

    def __str__(self):
        return self.collection_name


class Collection_Request(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["collection", "user"], name="request_collection_once"
            )
        ]
