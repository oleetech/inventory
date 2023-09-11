from django.urls import path
from . import views

urlpatterns = [

    path('delivery/', views.ajax_view, name='delivery'),
    path('get_sales_order_info/', views.get_sales_order_info, name='get_sales_order_info'),
    path('orderline_by_data/', views.orderline_by_data, name='orderline_by_data'),
    path('deliveryinfo/', views.deliveryinfo, name='deliveryinfo'),


]