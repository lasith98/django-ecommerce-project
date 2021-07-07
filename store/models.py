from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from util.util import scramble_upload_filename, SendEmail


class Carousel(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=scramble_upload_filename)
    title = models.CharField(max_length=50, default='', blank=True)
    sub_title = models.CharField(max_length=50, default='', blank=True)
    content = models.CharField(max_length=50, default='', blank=True)
    sub_content = models.CharField(max_length=50, default='', blank=True)
    link = models.URLField(null=True, blank=True)
    link_text = models.CharField(max_length=50, default='shop now', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Replay(models.Model):
    text = models.TextField()
    message = models.ForeignKey(ContactMessage, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Offer(models.Model):
    image = models.ImageField(upload_to=scramble_upload_filename, blank=False)
    title = models.CharField(max_length=50)
    valid_message = models.CharField(max_length=10, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    create_date = models.DateField(auto_now_add=True)
    expired = models.DateField(blank=False)

    def __str__(self):
        return self.title


@receiver(post_save, sender=ContactMessage)
def notify_admin(sender, **kwargs):
    if kwargs['created']:
        model = kwargs['instance']
        body = """
        Name : {0}
        Subject : {1}
        mobile No : {2}
        Email :{3}
        message : {4}
        """.format(model.name, model.subject, model.mobile_no, model.email, model.message)
        SendEmail('New customer message - {0}'.format(model.subject), body, settings.EMAIL_HOST_USER,
                  [settings.ADMIN_EMAIL_ADDRESS]).start()
