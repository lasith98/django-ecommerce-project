from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import DetailView, ListView

from product.models import Product, Category
from store.models import Carousel, ContactMessage, Offer


def index(request):
    context = {
        'products': Product.objects.filter(is_active=True, discount_available=False,availability='In Stock').order_by('create_date').all()[:10],
        'discount_products': Product.objects.filter(is_active=True, discount_available=True,availability='In Stock').distinct(),

        'offers': Offer.objects.filter(expired__gte=datetime.today()).order_by('create_date').all(),
        'carousel': Carousel.objects.filter(active=True).all()
    }
    return render(request, 'index.html', context=context)


def quick_view(request, pk):
    return render(request, 'quick-view.html', context={'object': Product.objects.get(pk=pk)})


@csrf_exempt
def contact_us(request):
    if request.method == "POST":
        message = ContactMessage()
        message.message = request.POST['message']
        message.email = request.POST['email']
        message.mobile_no = request.POST['mobile_no']
        message.subject = request.POST['subject']
        message.name = request.POST['name']
        message.save()
        return HttpResponse('Thank you! Your message has been successfully sent. We will contact you very soon!')
    return render(request, 'contact_us.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = Product.objects.filter(category=context['object'].category).exclude(
            pk=context['object'].id).all()[:20]
        return context


class ProductListView(ListView):
    model = Product
    template_name = "list.html"
    paginate_by = 10
    allow_empty = True
    ordering = ['create_date']

    def get_ordering(self):
        ordering = self.request.GET.get('orderby', 'create_date')
        # validate ordering here
        return [ordering]

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by(*self.get_ordering())

    def post(self, request, *args, **kwargs):
        query = request.POST['query']
        category_id = request.POST['category']
        category_name = None
        if category_id == "all":
            query_set = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) |
                                               Q(category__name__icontains=query) | Q(search_text__icontains=query),
                                               is_active=True).order_by(*self.get_ordering())
        else:
            category_name = Category.objects.filter(id=int(category_id)).first().name
            query_set = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) |
                                               Q(category__name__icontains=query), is_active=True,
                                               category_id=int(category_id)).order_by(*self.get_ordering())

        page_size = self.get_paginate_by(query_set)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(query_set, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset,
                'categories': Category.objects.all(),
                'category_name': category_name
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': query_set,
                'categories': Category.objects.all(),
                'category_name': category_name
            }
        return render(request, 'list.html', context)


class CategoryWiseProductListView(ListView):
    template_name = "list.html"
    paginate_by = 10
    allow_empty = True
    ordering = ['create_date']

    def get_queryset(self):
        if 'category_id' in self.kwargs:
            return Product.objects.filter(category_id=self.kwargs['category_id'], is_active=True)
        return Product.objects
