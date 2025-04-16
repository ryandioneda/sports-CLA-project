from products.models import Equipment
from django.dispatch import receiver
from django.db.models.signals import post_delete

@receiver(post_delete, sender=Equipment)
def delete_image(sender, instance, **kwargs):
    if instance.image is not None:
        instance.image.delete(False)