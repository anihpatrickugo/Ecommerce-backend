from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

@receiver(post_save, sender=Order)
def create_order_reference_number(sender, instance, created, **kwargs):
    """
    This instantly creates an order reference_number
    for new orders.
    """
    pass
    #
    # if created:
    #     print(instance.date)
    # else:
    #     print(instance.date)
