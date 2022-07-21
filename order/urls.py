from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('', orders, name='orders'),
    path('order/create/', order_create, name='order_create'),
    path('order/edit/<int:order_id>/', order_edit, name='order_edit'),
    path('order/delete/<int:order_id>/', order_delete, name='order_delete'),
    path('order/detail/<int:order_id>/', order_detail, name='order_detail'),
    path('order/buy/<int:order_id>/', order_buy, name='order_buy'),

    path('static/files/<int:order_id>/', static_files, name='static_files')
]
