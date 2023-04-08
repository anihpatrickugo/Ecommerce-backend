from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.conf import settings
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


@receiver(pre_delete, sender=Order)
def delete_order_products(sender, instance, **kwargs):
    """
    This instantly deletes all order products, if the
    order is deleted
    """
    order_products = instance.products.all()

    for product in order_products:
        product.delete()


# @receiver(post_save, sender=Order)
# def send_email_to_user_after_payment(sender, instance, **kwargs):
#     """
#        This instantly sends an email to the user
#        when a payment is being made.
#     """
#     if instance.payment:
#


