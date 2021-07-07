from django.db import models

# Create your models here.
from django.utils.html import format_html
from model_utils import Choices


class Address(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address_type = models.CharField(max_length=120, choices=Choices('Billing', 'Shipping'))
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    town_city = models.CharField(max_length=50)

    def __str__(self):
        return """
                {0} {1}
                {2}
                {3}
                {4}
                """.format(self.first_name, self.last_name, self.address1,
                           self.address2 if self.address2 is not None else '', self.town_city)

    def address_only(self):
        return """{0}
                  {1}
                  {2}
                   """.format(self.address1,
                              self.address2 if self.address2 is not None else '', self.town_city)

    def html(self):
        if self.address_type == "Billing":
            if self.address2 is None:
                return format_html("""
                            <address>
                                   <p><strong>{0} {1}</strong></p>
                                   <p>{2} <br>
                                      {3}<br>
                                      
                                   <p>Phone: {4}</p>
                                   <p>Email:{5} </p>
                               </address>
                               """.format(self.first_name, self.last_name, self.address1,
                                          self.town_city, self.phone, self.email))

            return format_html("""
                 <address>
                        <p><strong>{0} {1}</strong></p>
                        <p>{2} <br>
                           {3}<br>
                           {4}</p>
                        <p>Phone: {5}</p>
                        <p>Email:{6} </p>
                    </address>
                    """.format(self.first_name, self.last_name, self.address1,
                               self.address2, self.town_city, self.phone, self.email))
        else:
            if self.address2 is None:
                return format_html("""
                            <address>
                                   <p><strong>{0} {1}</strong></p>
                                   <p>{2} <br>
                                      {3}<br>
                               </address>
                               """.format(self.first_name, self.last_name, self.address1,
                                          self.town_city))

            return format_html("""
                 <address>
                        <p><strong>{0} {1}</strong></p>
                        <p>{2} <br>
                           {3}<br>
                           {4}</p>
                
                    </address>
                    """.format(self.first_name, self.last_name, self.address1,
                               self.address2, self.town_city))
