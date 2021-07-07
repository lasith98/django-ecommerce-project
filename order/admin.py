from django.contrib import admin
from django.shortcuts import resolve_url, reverse
# Register your models here.
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price', 'discount', 'total',)
    raw_id_fields = ['product']


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_date', 'shipping', 'total', 'status', ]
    list_per_page = 5
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ('id', 'order_id',)
    inlines = [OrderItemInline]
    readonly_fields = ['order_id', 'order_date', 'order_note', 'sub_total', 'email', 'phone',
                       'shipping_cost', 'total', 'export']
    fields = ['order_id', 'status', 'order_date', 'order_note', 'billing_address', 'shipping_address', 'email', 'phone',
              'sub_total',
              'shipping_cost', 'total', 'export']

    def shipping(self, obj):
        return obj.shipping_address if obj.shipping_address else obj.billing_address

    def email(self, obj):
        return obj.billing_address.email

    def phone(self, obj):
        return obj.billing_address.phone

    def export(self, obj):
        return format_html(
            '<a href="{0}" target="_blank"><b><h4>Invoice</h4></b></a>'.format(
                reverse('core:generate-invoice-view', kwargs={'id': obj.id})))


admin.site.register(Order, CustomOrderAdmin)
