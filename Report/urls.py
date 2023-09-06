from django.urls import path
from . import views
from . import salesemployeeviews

urlpatterns = [

    
    #Report
    path('',views.index,name='report'),
    
 # ____                       _                  _     _                 
 #|  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 #| |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 #|  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 #|_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                                                        
    
    
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
    
    # অর্ডার অনুযায়ী প্রোডাকশন রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে ডিটেলস রিপোর্ট
    path('receipt_from_production_based_on_order_no_filter_by_department/', views.receipt_from_production_based_on_order_no_filter_by_department, name='receipt_from_production_based_on_order_no_filter_by_department'),
    
   
    # ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল প্রোডাকশন ডেট সিলেক্ট করে  
    path('receipt_from_production_department_summary_by_month_based_on_date/', views.receipt_from_production_department_summary_by_month_based_on_date, name='receipt_from_production_department_summary_by_month_based_on_date'),
    
    

    #ডেট অনুযায়ী প্রোডাক্ট সামারি 
    path('receipt_from_production_total_by_name_between_dates/', views.receipt_from_production_total_by_name_between_dates, name='receipt_from_production_total_by_name_between_dates'),
    
    #ডেট অনুযায়ী প্রোডাক্ট সামারি ডিপার্টমেন্ট সিলেক্ট করে     
    path('receipt_from_production_total_by_name_between_dates_and_department/', views.receipt_from_production_total_by_name_between_dates_and_department, name='receipt_from_production_total_by_name_between_dates_and_department'),













#         ____            _                  _____                       _                               
#        / ___|    __ _  | |   ___   ___    | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___ 
#        \___ \   / _` | | |  / _ \ / __|   |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \
#         ___) | | (_| | | | |  __/ \__ \   | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/
#        |____/   \__,_| |_|  \___| |___/   |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___|
#                                                               |_|                  |___/               

    path('sales_employee_data/', salesemployeeviews.sales_employee_data, name='sales_employee_data'),
    path('all_sales_employee_data/', salesemployeeviews.all_sales_employee_data, name='all_sales_employee_data'),



]