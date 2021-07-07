from django.contrib.auth.decorators import login_required
from django.urls import path

from customer.views import OrderListView, OrderDetailView, DownloadListView, account_details, UpdateAddressView, \
    WishListView, remove_wish_list_product, add_to_wish_list_product

LOGIN_REDIRECT_URL = "/account/login"
app_name = 'customer_data'
urlpatterns = [
    path('', login_required(OrderListView.as_view(), login_url=LOGIN_REDIRECT_URL), name='index'),
    path('order_view/<int:pk>', login_required(OrderDetailView.as_view(), login_url=LOGIN_REDIRECT_URL),
         name='order-view'),
    path('download', login_required(DownloadListView.as_view(), login_url=LOGIN_REDIRECT_URL),
         name='download'),
    path('details', login_required(account_details, login_url=LOGIN_REDIRECT_URL),
         name='details'),
    path('update_address_view', login_required(UpdateAddressView.as_view(), login_url=LOGIN_REDIRECT_URL),
         name='update_address_view'),
    path('wish_list/<int:pk>', login_required(WishListView.as_view(), login_url=LOGIN_REDIRECT_URL),
         name='wish_list'),
    path('remove_wish_list_product', login_required(remove_wish_list_product, login_url=LOGIN_REDIRECT_URL),
         name='remove_wish_list_product'),
    path('add_to_wish_list_product', login_required(add_to_wish_list_product, login_url=LOGIN_REDIRECT_URL),
         name='add_to_wish_list_product'),

]
