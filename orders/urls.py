

from django.urls import path
from orders import views

urlpatterns = [
    
    path('place_order/',views.place_order, name='place_order'),
    path('payments/',views.payment, name='payments'),
    path('order_completion/',views.order_completion, name='order_completion'),

               
               
               
               ]
