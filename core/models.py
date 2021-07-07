from django.db import models


# Create your models here.
class MetaTag(models.Model):
    title = models.TextField()
    description = models.TextField()
    keyword = models.TextField()
