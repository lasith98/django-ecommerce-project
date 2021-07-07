from django.contrib.auth.decorators import login_required
from django.urls import path

from address.views import UpdateAddress, CreateAddress

LOGIN_REDIRECT_URL = "/account/login"
app_name = 'address'
urlpatterns = [

    path('update_address/<int:pk>', login_required(UpdateAddress.as_view(), login_url=LOGIN_REDIRECT_URL),
         name='update_address'),
    path('create_address', login_required(CreateAddress.as_view(), login_url=LOGIN_REDIRECT_URL),
         name='create_address'),


]
