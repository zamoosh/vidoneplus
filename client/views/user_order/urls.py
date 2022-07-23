from django.urls import path
from .views import *

app_name = 'user_order'

urlpatterns = [
    path('', user_orders, name='user_order'),
    path('user/order/active/', user_order_active, name='user_order_active'),
    path('user/order/inactive/', user_order_inactive, name='user_order_inactive')
]
