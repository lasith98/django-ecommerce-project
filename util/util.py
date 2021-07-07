import string
from random import choice
from threading import Thread
from uuid import uuid4

from django.core.mail import send_mail
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(choice(chars) for _ in range(size))


def scramble_upload_filename(instance, filename):
    return "{0}.{1}".format(uuid4(), filename.split('.')[-1]).replace('-', '')


def unique_slug_generator(model_instance, title, slug_field):
    slug = slugify(title, allow_unicode=True)
    model_class = model_instance.__class__
    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1
        slug = "{0}-{1}".format(slug, object_pk)
    return slug


def unique_order_id_generator(model_instance):
    order_new_id = random_string_generator()
    model_class = model_instance.__class__
    while model_class._default_manager.filter(order_id=order_new_id).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1
        order_new_id = order_new_id.join(object_pk)
    return order_new_id.upper()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class SendEmail(Thread):
    def __init__(self, subject, message, from_email, recipient_list,
                 fail_silently=False, auth_user=None, auth_password=None,
                 connection=None, html_message=None):
        Thread.__init__(self)
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.auth_user = auth_user
        self.auth_password = auth_password
        self.connection = connection
        self.html_message = html_message

    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.recipient_list,
                  self.fail_silently, self.auth_user, self.auth_password,
                  self.connection, self.html_message)
