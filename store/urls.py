from django.urls import path
from store.views import index, ProductDetailView, ProductListView, contact_us, CategoryWiseProductListView, quick_view

app_name = 'store'
urlpatterns = [
    path('', index, name='index'),
    path('contact_us', contact_us, name='contact_us'),
    path('shop', ProductListView.as_view(), name='shop'),
    path('category_list/<int:category_id>', CategoryWiseProductListView.as_view(), name='category_list'),
    path('product/<str:slug>', ProductDetailView.as_view(), name='product'),
    path('quick_view/<int:pk>', quick_view, name='quick_view'),
]
