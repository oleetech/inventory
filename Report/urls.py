from django.urls import path
from . import views

urlpatterns = [

    
    #Report
    path('',views.index,name='report'),
    

    path('receipt_from_production_between_date/', views.receipt_from_production_between_date, name='receipt_from_production_between_date'),
    path('receipt_from_production_based_on_order_no/', views.receipt_from_production_based_on_order_no, name='receipt_from_production_based_on_order_no'),
    path('receipt_from_production_total_quantity_by_department_by_order/', views.receipt_from_production_total_quantity_by_department_by_order, name='receipt_from_production_total_quantity_by_department_by_order'),
    path('receipt_from_production_department_summary_by_dates/', views.receipt_from_production_department_summary_by_dates, name='receipt_from_production_department_summary_by_dates'),
    
    # ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল প্রোডাকশন   
    path('receipt_from_production_department_summary_by_month_based_on_date/', views.receipt_from_production_department_summary_by_month_based_on_date, name='receipt_from_production_department_summary_by_month_based_on_date'),
    
    path('receipt_from_production_monthly_data_view/', views.receipt_from_production_monthly_data_view, name='receipt_from_production_monthly_data_view'),
    
    path('receipt_from_production_monthly_data_by_department_view/', views.receipt_from_production_monthly_data_by_department_view, name='receipt_from_production_monthly_data_by_department_view'),
    
    #ডেট অনুযায়ী প্রোডাক্ট সামারি 
    path('receipt_from_production_total_by_name_between_dates/', views.receipt_from_production_total_by_name_between_dates, name='receipt_from_production_total_by_name_between_dates'),


]