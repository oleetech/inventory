from django.urls import path
from . import views

urlpatterns = [

    
    #Report
    path('',views.index,name='report'),
    

    path('receipt_from_production_between_date/', views.receipt_from_production_between_date, name='receipt_from_production_between_date'),
    path('receipt_from_production_based_on_order_no/', views.receipt_from_production_based_on_order_no, name='receipt_from_production_based_on_order_no'),
    path('total_quantity_by_department/', views.total_quantity_by_department, name='total_quantity_by_department'),
    path('department_summary_by_dates/', views.department_summary_by_dates, name='department_summary_by_dates'),
    path('department_summary_by_month/', views.department_summary_by_month, name='department_summary_by_month'),
    
    path('receipt_from_production_monthly_data_view/', views.receipt_from_production_monthly_data_view, name='receipt_from_production_monthly_data_view'),
    
    path('receipt_from_production_monthly_data_by_department_view/', views.receipt_from_production_monthly_data_by_department_view, name='receipt_from_production_monthly_data_by_department_view'),


]