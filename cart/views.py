from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from cart.models import Cart, CartItem
from product.models import Product
from util.js_message import JSMessage

CART_ID = 'cart_id'
CART_ITEM_COUNT = 'cart_item_count'


def view_cart(request):
    return render(request, 'cart/cart.html')


def add_to_cart(request):
    messages = JSMessage.success('', False)
    if request.method == "POST":
        if request.session.has_key(CART_ID):
            try:
                cart = Cart.objects.get(pk=int(request.session.get(CART_ID)))
            except Cart.DoesNotExist:
                cart = Cart()
                cart.save()
                request.session[CART_ID] = cart.id
        else:
            cart = Cart()
            cart.save()
            request.session[CART_ID] = cart.id

        if cart is not None:
            try:
                product = Product.objects.get(pk=request.POST['product_id'])
                if product.is_available():
                    if request.user.is_authenticated:
                        request.user.wishlist.product.remove(product)
                        request.user.wishlist.save()

                    # TODO add max oder limit
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                    cart_item.quantity = int(request.POST['quantity'])
                    cart_item.save()
                    cart.item.add(cart_item)
                    cart.save()
                    messages = JSMessage.success('"{0}" has been added to your cart.'.format(product.title))
                else:
                    messages = JSMessage.error('You cannot add another "{0}" to your cart.'.format(product.title))
            except Product.DoesNotExist:
                pass
        request.session[CART_ITEM_COUNT] = cart.total_item()
        if request.is_ajax():
            return JsonResponse({CART_ITEM_COUNT: cart.total_item(), 'js_data': messages})
    return redirect('cart:index')


def remove_item(request, pk):
    if request.session.has_key(CART_ID):
        try:
            cart = Cart.objects.get(pk=int(request.session.get(CART_ID)))
            item = cart.item.get(pk=pk)
            item.delete()
            if cart.is_empty():
                cart.delete()
                request.session.pop(CART_ID)
                request.session.pop(CART_ITEM_COUNT)
            else:
                request.session[CART_ITEM_COUNT] = cart.total_item()
        except Cart.DoesNotExist or CartItem.DoesNotExist:
            pass
    return redirect('cart:index')


def checkout_view(request):
    return render(request, 'cart/checkout.html')


def view_cart_item(request):
    return render(request, 'cart/cart_item.html')
