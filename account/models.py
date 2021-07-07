from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from address.models import Address
from customer.models import WishList


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    billing = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="profile_billing_address", null=True,
                                blank=True)
    shipping = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="profile_shipping_address", null=True,
                                 blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        WishList.objects.create(user=instance)
    instance.profile.save()
