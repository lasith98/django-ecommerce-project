from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

from address.models import Address


class UpdateAddress(UpdateView):
    template_name = 'account/account-address.html'
    model = Address
    fields = '__all__'

    def get_success_url(self):
        return reverse('customer_data:update_address_view')


class CreateAddress(CreateView):
    template_name = 'account/account-address.html'
    model = Address
    fields = '__all__'

    def get_success_url(self):
        return reverse('customer_data:update_address_view')

    def form_valid(self, form):
        self.object = form.save()
        profile = self.request.user.profile
        if self.object.address_type == "Billing":
            profile.billing = self.object
        else:
            profile.shipping = self.object
        profile.save()
        return super().form_valid(form)
