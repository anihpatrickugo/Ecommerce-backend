from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Order
from .custom import generate_random_reference

@receiver(pre_save, sender=Order)
def create_order_reference_number(sender, instance, **kwargs):
    """
    This instantly creates an order reference_number
    for new orders.
    """

    if instance.pk is None:
        instance.reference = generate_random_reference()
        return instance