from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from product.models import Product


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
