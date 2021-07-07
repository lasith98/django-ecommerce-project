from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from product.models import Product, Discount, Category


class CustomProductAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'search_text')
    list_per_page = 5
    list_display = (
        'picture', 'title', 'price', 'availability', 'is_active')
    list_editable = ('price', 'availability', 'is_active')
    list_filter = ('availability', 'is_active')
    list_display_links = ('title', 'picture')
    exclude = ('slug','discount_available')

    def picture(self, obj):
        return format_html('<img src="{}" height="90" width="90" />'.format(obj.image.url))


admin.site.register(Product, CustomProductAdmin)
admin.site.register(Category)
admin.site.register(Discount)
