from django.urls import path
from . import views

urlpatterns = [

    
    #Report
    path('receipt_from_production_between_date/', views.receipt_from_production_between_date, name='receipt_from_production_between_date'),
    path('receipt_from_production_based_on_order_no/', views.receipt_from_production_based_on_order_no, name='receipt_from_production_based_on_order_no'),
    path('total_quantity_by_department/', views.total_quantity_by_department, name='total_quantity_by_department'),
    

]