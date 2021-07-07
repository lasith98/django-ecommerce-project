from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.

from cart.models import Cart
from cart.views import CART_ID, CART_ITEM_COUNT
from order.models import Order, Address
from util.util import get_client_ip


def _load_billing_address(request):
    billing_address, created = Address.objects.get_or_create(address1=request.POST["address1"],
                                                             address2=request.POST["address2"],
                                                             town_city=request.POST["town_city"],
                                                             email=request.POST["email"],
                                                             phone=request.POST["phone"],
                                                             first_name=request.POST["first_name"],
                                                             last_name=request.POST["last_name"],
                                                             address_type='Billing'
                                                             )
    return billing_address


def _load_shipping_address(request):
    if request.POST.get('ship_to_different', '') != '':
        shipping_address, created = Address.objects.get_or_create(address1=request.POST["s_address1"],
                                                                  address2=request.POST["s_address2"],
                                                                  town_city=request.POST["s_town_city"],
                                                                  first_name=request.POST["s_first_name"],
                                                                  last_name=request.POST["s_last_name"],
                                                                  address_type='Shipping'
                                                                  )
        return shipping_address


def place_order(request):
    if request.method == "POST":
        if request.session.has_key(CART_ID):
            try:
                order = Order()
                if request.user.is_authenticated:
                    order.customer = request.user
                    if request.user.profile.billing:
                        order.billing_address = request.user.profile.billing
                    else:
                        order.billing_address = _load_billing_address(request)

                    if request.user.profile.shipping and request.POST.get('ship_to_different', '') == '':
                        order.shipping_address = request.user.profile.shipping
                    else:
                        order.shipping_address = _load_shipping_address(request)
                else:
                    order.billing_address = _load_billing_address(request)
                    order.shipping_address = _load_shipping_address(request)

                order.ip_address = get_client_ip(request)
                cart = Cart.objects.get(pk=request.session.get(CART_ID))
                order.save()
                for item in cart.item.all():
                    order.orderitem_set.create(quantity=item.quantity, product=item.product)
                order.save()
                request.session.pop(CART_ID)
                request.session.pop(CART_ITEM_COUNT)
                cart.active = False
                cart.save()
            except Cart.DoesNotExist:
                pass
    return render(request, 'cart/thank-you.html')
