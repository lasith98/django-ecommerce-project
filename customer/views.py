from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, DeleteView

# Create your views here.
from address.models import Address
from customer.models import WishList
from order.models import Order
from product.models import Product


class OrderListView(ListView):
    model = Order
    paginate_by = 5
    template_name = 'account/customer-orders.html'
    ordering = ['order_date']

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).all().order_by(*self.get_ordering())


class OrderDetailView(DetailView):
    model = Order
    template_name = 'account/view-order.html'


class DownloadListView(ListView):
    model = Order
    paginate_by = 5
    template_name = 'account/download.html'
    ordering = ['order_date']

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user, status='Completed').all().order_by(
            *self.get_ordering())


def account_details(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user)
        if request.POST.get('old_password', '') != '':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Please correct the error below.')
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.profile.display_name = request.POST['display_name']
        user.email = request.POST['email']
        user.save()

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/account-details.html', {
        'form': form
    })


class UpdateAddressView(TemplateView):
    template_name = 'account/account-address.html'


def add_to_wish_list_product(request):
    context = {'add': False}
    if request.POST:
        if request.user.is_authenticated:
            try:
                wish_list = request.user.wishlist
                product_id = request.POST.get('product_id', 0)
                product = Product.objects.get(pk=product_id)
                wish_list.product.add(product)
                wish_list.save()
                context['wish_list_count'] = wish_list.product.count()
                context['add'] = True
            except Product.DoesNotExist:
                pass
        if request.is_ajax():
            return JsonResponse(context)
        render(request, 'wishlist.html', context={'object': request.user.wishlist})

    else:
        return redirect('store:index')


def remove_wish_list_product(request):
    if request.POST:
        if request.user.is_authenticated:

            try:
                product = Product.objects.get(pk=request.POST.get('product_id', None))
                request.user.wishlist.product.remove(product)
                request.user.wishlist.save()
            except Product.DoesNotExist:
                pass
            return render(request, 'wishlist.html', context={'object': request.user.wishlist})
        else:
            return redirect('account:login')

    else:
        return redirect('store:index')


class WishListView(DetailView):
    model = WishList
    template_name = 'wishlist.html'
