"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetView, PasswordChangeDoneView, PasswordChangeView
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .sitemaps import StaticViewSitemap, StoreSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'store': StoreSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('account/password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('account/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='cached-sitemap'),
    path('robots.txt', include('robots.urls')),

    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('customer/account/', include('account.urls')),
    path('customer/account/data/', include('customer.urls')),
    path('core/system/', include('core.urls')),
    path('customer/address/', include('address.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
