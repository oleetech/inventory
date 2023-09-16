from django.urls import path
from . import views

urlpatterns = [
    path('custom_print_view/', views.custom_print_view, name='custom_print_view'),

    path('ajax/', views.ajax_view, name='ajax_view'),
    path('receiptproduction/', views.ajax_view_receipt, name='receiptproduction'),
    path('get_production_order_info/', views.get_production_order_info, name='get_production_order_info'),
    path('orderline_by_data/', views.orderline_by_data, name='orderline_by_data'),    


]