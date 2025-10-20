from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceOrder
from parts.models import Part

@receiver(post_save, sender=ServiceOrder)
def update_parts_stock_on_completion(sender, instance, created, **kwargs):
    """
    When a service order is marked as 'completed', decrease part stock.
    """
    # If the order was just created, skip
    if created:
        return

    # Only act if status changed to 'completed'
    if instance.status == "completed":
        for part in instance.parts.all():
            if part.in_stock > 0:
                part.in_stock -= 1  # simple logic: subtract 1 per part used
                part.save()