from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import Order
from .custom import generate_random_reference


@receiver(pre_save, sender=Order)
def create_order(sender, instance, **kwargs):

    # check if order is being created for the first
    # time
    if instance.pk is None:
        # create a reference token for the order.
        instance.reference = generate_random_reference()
        return instance


# @receiver(pre_save, sender=Order)
# def update_order(sender, instance, **kwargs):
#
#     # check if order is being created for the first
#     # time
#     # if instance.pk is not None:
#     print(instance.pk, 'this is pk')
#         # create a reference token for the order.
#         # previous_products = instance.products.all()
#         # print(previous_products, 'these are the previous products')


@receiver(pre_delete, sender=Order)
def delete_order_products(sender, instance, **kwargs):
    """
    This instantly deletes all order products, if the
    order is deleted
    """
    order_products = instance.products.all()

    for product in order_products:
        product.delete()

