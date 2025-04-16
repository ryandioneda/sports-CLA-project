from django.db import models
from django.contrib.auth.models import User
from productCollections.models import Collection
from datetime import timedelta
from django.db.models import UniqueConstraint

import uuid


class Equipment(models.Model):
    CONDITION_CHOICES = [
        ("new", "New"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    CATEGORY_CHOICES = [
        ("ball", "Ball Sports"),
        ("racket", "Racket Sports"),
        ("fitness", "Fitness Equipment"),
        ("indoor", "indoor Sports"),
        ("water", "Water Sports"),
        ("winter", "Winter Sports"),
        ("extreme", "extreme Sports"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("unavailable", "unavailable"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="media/")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    collections = models.ManyToManyField(
        Collection, related_name="equipment", blank=True
    )

    def __str__(self):
        return self.name


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

def due_date(self):
    return self.rental_date + timedelta(days=7)

class Review(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Borrow_Request(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["equipment", "user"], name="request_only_once")
        ]

    # STATUS_CHOICES = [
    #     ("pending", "Pending"),
    #     ("approved", "Approved"),
    #     ("denied", "Denied")
    # ]
