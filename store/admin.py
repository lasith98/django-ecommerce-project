from django.contrib import admin


from store.models import Carousel, ContactMessage, Offer, Replay


class CustomCarouselAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('name', 'active')
    list_editable = ('active',)


class ReplayTabularInline(admin.TabularInline):
    model = Replay
    extra = 1


class CustomContactMessageAdmin(admin.ModelAdmin):
    search_fields = ('date', 'name', 'subject', 'mobile_no', 'email', 'message')
    list_display = ('date', 'name', 'subject', 'mobile_no', 'email', 'message')
    list_per_page = 5
    list_display_links = ('date', 'name', 'subject', 'mobile_no', 'email', 'message')
    ordering = ('date',)
    inlines = [ReplayTabularInline]


class CustomOfferAdmin(admin.ModelAdmin):
    search_fields = ('title', 'valid_message', 'description', 'expired')
    list_display = ('title', 'valid_message', 'description', 'expired')
    list_filter = ('create_date', 'expired')
    list_per_page = 5


admin.site.register(Offer, CustomOfferAdmin)
admin.site.register(Carousel, CustomCarouselAdmin)
admin.site.register(ContactMessage, CustomContactMessageAdmin)
