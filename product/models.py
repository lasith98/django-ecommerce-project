import datetime

from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from model_utils import Choices
from util.util import scramble_upload_filename, unique_slug_generator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=100)
    discount_type = models.CharField(max_length=30, choices=Choices('Amount', 'Percentage'),
                                     default='Percentage')
    expired_type = models.CharField(max_length=30, choices=Choices('On Date', 'Date Range', 'No Expired'),
                                    default='No Expired')
    expired = models.DateTimeField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def is_discount(self):

        if self.is_active and not self.amount.is_zero():
            if self.expired_type == "On Date":
                return self.expired > timezone.now()
            elif self.expired_type == "Date Range":
                return self.expired >= timezone.now() >= self.expired
            else:
                return True

        return False


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=scramble_upload_filename)
    slug = models.SlugField(max_length=100, unique=True, null=True, allow_unicode=True)
    title = models.CharField(max_length=100)
    search_text = models.TextField(max_length=100, null=True)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=100)
    maximum = models.IntegerField(default=10)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    availability = models.CharField(max_length=30, choices=Choices('In Stock', 'Out of Stock'), default='In Stock')
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    discount_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product', kwargs={'slug': self.slug})

    def is_available(self):
        return self.availability == 'In Stock'

    @property
    def get_availability_color(self):
        return "availability" if self.availability == "In Stock" else "no-availability "

    @property
    def price_text(self):
        return '{0} {1}'.format(settings.CURRENCY_TYPE, self.price)

    @property
    def discount_price_text(self):
        return '{0} {1}'.format(settings.CURRENCY_TYPE, self.discount_price)

    @property
    def discount_text(self):
        if self.is_discount:
            if self.discount.discount_type == 'Amount':
                return '-{0}'.format(self.discount.amount)
            return '{0} %'.format(int(self.discount.amount))
        return '-'

    @property
    def discount_price(self):
        if self.is_discount:
            if self.discount.discount_type == 'Amount':
                return self.price - self.discount.amount
            else:
                return self.price - (round((self.discount.amount / 100) * self.price, 2))
        return 0.0

    @property
    def is_discount(self):
        if self.discount is not None:
            if self.discount.is_active and not self.discount.amount.is_zero():
                if self.discount.expired_type == "On Date":
                    return self.discount.expired > timezone.now()
                elif self.discount.expired_type == "Date Range":
                    return self.discount.expired >= timezone.now() >= self.discount.expired
                else:
                    return True

        return False

    @property
    def get_price(self):
        return self.discount_price if self.is_discount else self.price

    @property
    def is_new(self):
        return (self.create_date + datetime.timedelta(days=15)) > timezone.now()


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.title, instance.slug)
    instance.discount_available = instance.is_discount


pre_save.connect(slug_save, sender=Product)


@receiver(post_save, sender=Product)
def update_product_discount_post_save(sender, **kwargs):
    model = kwargs['instance']
    model.discount_available = model.is_discount


@receiver(post_save, sender=Discount)
def update_discount_post_save(sender, **kwargs):
    model = kwargs['instance']
    model.product_set.update(discount_available=model.is_discount)
