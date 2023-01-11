from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import Order
from .custom import generate_random_reference


@receiver(pre_save, sender=Order)
def create_or_edit_order(sender, instance, **kwargs):

    # check if order is being created for the first
    # time
    if instance.pk is None:
        # create a reference token for the order.
        instance.reference = generate_random_reference()
        return instance

    else:

        # then this is definitely an update
        # delete the initial products in the data base
        initial_products = instance.products.all()
        for product in initial_products:
            product.delete()

@receiver(pre_delete, sender=Order)
def delete_order_products(sender, instance, **kwargs):
    """
    This instantly deletes all order products, if the
    order is deleted
    """
    order_products = instance.products.all()

    for product in order_products:
        product.delete()

