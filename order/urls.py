from django.urls import path
from .views import place_order

app_name = 'order'
urlpatterns = [
    path('place_order', place_order, name='place_order'),

]
