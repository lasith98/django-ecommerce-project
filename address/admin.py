from django.contrib import admin

# Register your models here.
from address.models import Address


class CustomAddressAdmin(admin.ModelAdmin):
    search_fields = ['billing_profile__email', 'billing_profile__phone', 'address1', 'town_city']
    list_filter = ['address_type']


admin.site.register(Address, CustomAddressAdmin)
