from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
# Create your models here.
from product.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=100, default=settings.SHIPPING_COST)
    active = models.BooleanField(default=True)

    def total(self):
        total = 0.0
        for item in self.item.all():
            total += float(item.get_total())
        return total

    def total_with_shipping(self):
        return self.total() + float(self.shipping_cost)

    def sub_total(self):
        total = 0.0
        for item in self.item.all():
            total += float(item.get_sub_total())
        return total

    def total_item(self):
        return self.item.count()

    def is_empty(self):
        return self.total_item() == 0

    @property
    def item(self):
        return self.cartitem_set


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_sub_total(self):
        return self.product.get_price * self.quantity

    def get_total(self):
        return self.product.get_price * self.quantity

    @property
    def get_total_text(self):
        return '{0} {1}'.format(settings.CURRENCY_TYPE, self.get_total())

    @property
    def get_net_amount_text(self):
        return '{0} {1}'.format(settings.CURRENCY_TYPE, self.get_sub_total())
