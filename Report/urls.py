from django.urls import path
from . import views

urlpatterns = [

    
    #Report
    path('',views.index,name='report'),
    
    #ডেট অনুযায়ী প্রোডাকশন রিপোর্ট 
    path('receipt_from_production_between_date/', views.receipt_from_production_between_date, name='receipt_from_production_between_date'),
    
    #ডেট অনুযায়ী ডিপার্টমেন্ট  প্রোডাকশন রিপোর্ট
    path('receipt_from_production_department_summary_by_dates/', views.receipt_from_production_department_summary_by_dates, name='receipt_from_production_department_summary_by_dates'),
    
    # ১ বছরের মাস অনুযায়ী রিপোর্ট     
    path('receipt_from_production_monthly_data_view/', views.receipt_from_production_monthly_data_view, name='receipt_from_production_monthly_data_view'),
   
    # ১ বছরের মাস অনুযায়ী রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে         
    path('receipt_from_production_monthly_data_by_department_view/', views.receipt_from_production_monthly_data_by_department_view, name='receipt_from_production_monthly_data_by_department_view'),
    
           
    # অর্ডার অনুযায়ী প্রোডাকশন রিপোর্ট   
    path('receipt_from_production_based_on_order_no/', views.receipt_from_production_based_on_order_no, name='receipt_from_production_based_on_order_no'),
    
    # অর্ডার অনুযায়ী ডিপার্টমেন্ট প্রোডাকশন রিপোর্ট   
    path('receipt_from_production_total_quantity_by_department_by_order/', views.receipt_from_production_total_quantity_by_department_by_order, name='receipt_from_production_total_quantity_by_department_by_order'),
    
   
    # ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল প্রোডাকশন ডেট সিলেক্ট করে  
    path('receipt_from_production_department_summary_by_month_based_on_date/', views.receipt_from_production_department_summary_by_month_based_on_date, name='receipt_from_production_department_summary_by_month_based_on_date'),
    
    

    #ডেট অনুযায়ী প্রোডাক্ট সামারি 
    path('receipt_from_production_total_by_name_between_dates/', views.receipt_from_production_total_by_name_between_dates, name='receipt_from_production_total_by_name_between_dates'),
    
    #ডেট অনুযায়ী প্রোডাক্ট সামারি ডিপার্টমেন্ট সিলেক্ট করে     
    path('receipt_from_production_total_by_name_between_dates_and_department/', views.receipt_from_production_total_by_name_between_dates_and_department, name='receipt_from_production_total_by_name_between_dates_and_department'),



]