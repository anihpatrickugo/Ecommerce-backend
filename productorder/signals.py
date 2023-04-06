from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import Order, Payment
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


@receiver(post_save, sender=Payment)
def send_email_to_user_after_payment(sender, instance, **kwargs):
    """
       This instantly sends an email to the user
       when a payment is being made.
    """
    subject = "Order Payment confirmation"
    context = {'username': instance.user.username,
               'amount': instance.order.amount,
               "order_reference": instance.order.reference,
               "payment reference": instance.reference}

    html_content = render_to_string('emails/order_payment.html', context=context)
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_SENDER
    recipient_list = [instance.user.email]

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


