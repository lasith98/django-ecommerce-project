from cart.models import Cart
from cart.views import CART_ID
from customer.models import WishList
from product.models import Category
from django.conf import settings


def cart_processor(request):
    cart = None
    wish_list_count = 0
    if request.session.has_key(CART_ID):
        try:
            cart = Cart.objects.get(pk=request.session.get(CART_ID), active=True)
        except Cart.DoesNotExist:
            pass
    if request.user.is_authenticated:
        try:
            wish_list_count = WishList.objects.get(user=request.user).product.count()
        except WishList.DoesNotExist:
            pass

    context = {
        'cart': cart,
        'categories': Category.objects.all(),
        'wish_list_count': wish_list_count,
        'currency': settings.CURRENCY_TYPE
    }
    return context
