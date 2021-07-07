from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from model_utils import Choices

from address.models import Address
from cart.models import Cart
from product.models import Product
from util.util import unique_order_id_generator, SendEmail


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    order_note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=120, choices=Choices('Canceled', 'In Progress', 'Completed', 'Created'),
                              default='Created')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="billing_address")
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="shipping_address", null=True,
                                         blank=True)
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=100, default=settings.SHIPPING_COST)
    sub_total = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    order_date = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return "{} IP : {}".format(self.order_id, self.ip_address)

    def update_total(self):
        self.sub_total = self.get_item_total()
        self.total = self.sub_total + float(self.shipping_cost)

    def get_item_total(self):
        total = 0.0
        for item in self.orderitem_set.all():
            total += float(item.total)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0.0, editable=False)
    discount = models.CharField(max_length=250, editable=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=100, default=0.0, editable=False)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} X {1}".format(self.product.title, self.quantity)


def create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(create_order_id, sender=Order)


@receiver(post_save, sender=Order)
def order_update(sender, **kwargs):
    model = kwargs['instance']

    if model.status == 'Created':
        html_message = render_to_string('email/invoice.html', {'object': model})
        plain_message = strip_tags(html_message)
        SendEmail('Order : {0} status'.format(model.order_id), plain_message, settings.EMAIL_HOST_USER,
                  [model.billing_address.email]).start()


@receiver(pre_save, sender=OrderItem)
def update_order_item_pre_save(sender, **kwargs):
    model = kwargs['instance']
    if not model.total:
        model.price = model.product.price
        model.sale_price = model.product.get_price
        model.discount = model.product.discount_text
    model.total = model.sale_price * model.quantity


@receiver(post_save, sender=OrderItem)
def update_order_item_post_save(sender, **kwargs):
    model = kwargs['instance']
    model.order.update_total()
    model.order.save()


@receiver(post_delete, sender=OrderItem)
def update_order_item_post_delete(sender, **kwargs):
    model = kwargs['instance']
    model.order.update_total()
    model.order.save()
