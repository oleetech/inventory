from django.urls import path
from . import views

urlpatterns = [
    path('custom_print_view/', views.custom_print_view, name='custom_print_view'),

    path('ajax/', views.ajax_view, name='ajax_view'),
    path('receiptproduction/', views.ajax_view_receipt, name='receiptproduction'),
    


]