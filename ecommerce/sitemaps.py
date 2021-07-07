from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from product.models import Product


class BaseSitemap(Sitemap):
    changefreq = 'daily'
    priority = "1"
    protocol = "https"


class StaticViewSitemap(BaseSitemap):
    changefreq = 'monthly'

    def items(self):
        return ['store:shop', 'store:contact_us', 'store:index']

    def location(self, obj):
        return reverse(obj)


class StoreSitemap(BaseSitemap):

    def items(self):
        return Product.objects.all()
