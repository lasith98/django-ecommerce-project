from django.urls import path
from .views import view_cart, remove_item, add_to_cart, checkout_view, view_cart_item

app_name = 'cart'
urlpatterns = [
    path('', view_cart, name='index'),
    path('remove/<int:pk>', remove_item, name='remove'),
    path('add', add_to_cart, name='add'),
    path('checkout', checkout_view, name='checkout'),
    path('cart_item', view_cart_item, name='cart_item'),

]
