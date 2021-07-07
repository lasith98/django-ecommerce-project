from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import GenerateInvoiceView, generate_view

LOGIN_REDIRECT_URL = "/account/login"
app_name = 'core'
urlpatterns = [
    path('generate-invoice/<int:pk>', GenerateInvoiceView.as_view(),
         name='generate-invoice'),
    path('generate-invoice-view/<int:id>', login_required(generate_view), name='generate-invoice-view')
]
