from django.urls import path
from . import views,salesemployeeviews,inventoryviews,salesorderviews,businesspartnerview,purchasingview,bankingview


urlpatterns = [

    path('', views.post_list, name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),    

    
 # ____                       _                  _     _                 
 #|  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 #| |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 #|  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 #|_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                                                        

    #ডেট অনুযায়ী প্রোডাকশন রিপোর্ট 
    path('Production/receipt_from_production_between_date/', views.receipt_from_production_between_date, name='receipt_from_production_between_date'),
    
    #ডেট অনুযায়ী ডিপার্টমেন্ট  প্রোডাকশন টোটাল সামারি  রিপোর্ট
    path('Production/receipt_from_production_department_summary_by_dates/', views.receipt_from_production_department_summary_by_dates, name='receipt_from_production_department_summary_by_dates'),
    
    #ডেট অনুযায়ী প্রোডাকশন রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে বিস্তারিত 
    path('Production/receipt_from_production_between_date_by_department/', views.receipt_from_production_between_date_by_department, name='receipt_from_production_between_date_by_department'),

    
    # ১ বছরের মাস অনুযায়ী রিপোর্ট     
    path('Production/receipt_from_production_monthly_data_view/', views.receipt_from_production_monthly_data_view, name='receipt_from_production_monthly_data_view'),
   
    # ১ বছরের মাস অনুযায়ী রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে         
    path('Production/receipt_from_production_monthly_data_by_department_view/', views.receipt_from_production_monthly_data_by_department_view, name='receipt_from_production_monthly_data_by_department_view'),
    
           
    # অর্ডার অনুযায়ী প্রোডাকশন রিপোর্ট   
    path('Production/receipt_from_production_based_on_order_no/', views.receipt_from_production_based_on_order_no, name='receipt_from_production_based_on_order_no'),
    
    # অর্ডার অনুযায়ী ডিপার্টমেন্ট প্রোডাকশন রিপোর্ট   
    path('Production/receipt_from_production_total_quantity_by_department_by_order/', views.receipt_from_production_total_quantity_by_department_by_order, name='receipt_from_production_total_quantity_by_department_by_order'),
    
    # অর্ডার অনুযায়ী প্রোডাকশন রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে ডিটেলস রিপোর্ট
    path('Production/receipt_from_production_based_on_order_no_filter_by_department/', views.receipt_from_production_based_on_order_no_filter_by_department, name='receipt_from_production_based_on_order_no_filter_by_department'),
    
    #অর্ডার অনুযায়ী সব ডিপার্টমেন্ট প্রোডাকশন ব্যালেন্স রিপোর্ট  
    path('Production/production_balance_based_on_orderNo_every_department/', views.production_balance_based_on_orderNo_every_department, name='production_balance_based_on_orderNo_every_department'),
   
   
    # ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল প্রোডাকশন ডেট সিলেক্ট করে  
    path('Production/receipt_from_production_department_summary_by_month_based_on_date/', views.receipt_from_production_department_summary_by_month_based_on_date, name='receipt_from_production_department_summary_by_month_based_on_date'),
    
    

    #ডেট অনুযায়ী প্রোডাক্ট সামারি 
    path('Production/receipt_from_production_total_by_name_between_dates/', views.receipt_from_production_total_by_name_between_dates, name='receipt_from_production_total_by_name_between_dates'),
    
    #ডেট অনুযায়ী প্রোডাক্ট সামারি ডিপার্টমেন্ট সিলেক্ট করে     
    path('Production/receipt_from_production_total_by_name_between_dates_and_department/', views.receipt_from_production_total_by_name_between_dates_and_department, name='receipt_from_production_total_by_name_between_dates_and_department'),



#         ____            _                  _____                       _                               
#        / ___|    __ _  | |   ___   ___    | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___ 
#        \___ \   / _` | | |  / _ \ / __|   |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \
#         ___) | | (_| | | | |  __/ \__ \   | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/
#        |____/   \__,_| |_|  \___| |___/   |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___|
#                                                               |_|                  |___/               


    # একজন মার্কেটিং এর ডেটা দেখা 
    path('Marketing/sales_employee_data/', salesemployeeviews.sales_employee_data, name='sales_employee_data'),
    # সব  মার্কেটিং এর ডেটা দেখা    
    path('Marketing/all_sales_employee_data/', salesemployeeviews.all_sales_employee_data, name='all_sales_employee_data'),

#  ___                                  _                          
# |_ _|  _ __   __   __   ___   _ __   | |_    ___    _ __   _   _ 
#  | |  | '_ \  \ \ / /  / _ \ | '_ \  | __|  / _ \  | '__| | | | |
#  | |  | | | |  \ V /  |  __/ | | | | | |_  | (_) | | |    | |_| |
# |___| |_| |_|   \_/    \___| |_| |_|  \__|  \___/  |_|     \__, |
#                                                            |___/ 


    #ডেট অনুযায়ী আইটেম  রিপোর্ট 
    path('Inventory/item_receipt_between_date/', inventoryviews.item_receipt_between_date, name='item_receipt_between_date'),
    path('Inventory/item_delivery_between_date/', inventoryviews.item_delivery_between_date, name='item_delivery_between_date'),
    path('Inventory/item_stock_between_date/', inventoryviews.item_stock_between_date, name='item_stock_between_date'),
    path('Inventory/issue_for_production_between_date/', inventoryviews.issue_for_production_between_date, name='issue_for_production_between_date'),
  
    #ডেট অনুযায়ী আইটেম  রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে     
    path('Inventory/item_delivery_between_date_by_department/', inventoryviews.item_delivery_between_date_by_department, name='item_delivery_between_date_by_department'),
    path('Inventory/item_receipt_between_date_by_department/', inventoryviews.item_receipt_between_date_by_department, name='item_receipt_between_date_by_department'),
    path('Inventory/issue_for_production_between_date_by_department/', inventoryviews.issue_for_production_between_date_by_department, name='issue_for_production_between_date_by_department'),

    #ডেট অনুযায়ী ডিপার্টমেন্ট  আইটেম টোটাল সামারি  রিপোর্ট
    path('Inventory/item_receipt_department_summary_by_dates/', inventoryviews.item_receipt_department_summary_by_dates, name='item_receipt_department_summary_by_dates'),
    path('Inventory/item_delivery_department_summary_by_dates/', inventoryviews.item_delivery_department_summary_by_dates, name='item_delivery_department_summary_by_dates'),
    path('Inventory/issue_for_production_department_summary_by_dates/', inventoryviews.issue_for_production_department_summary_by_dates, name='issue_for_production_department_summary_by_dates'),

    
    # ১ বছরের মাস অনুযায়ী রিপোর্ট     
    path('Inventory/item_receipt_monthly_data/', inventoryviews.item_receipt_monthly_data, name='item_receipt_monthly_data'),
    path('Inventory/item_delivery_monthly_data/', inventoryviews.item_delivery_monthly_data, name='item_delivery_monthly_data'),
    path('Inventory/issue_for_production_monthly_data/', inventoryviews.issue_for_production_monthly_data, name='issue_for_production_monthly_data'),
    
    # ১ বছরের মাস অনুযায়ী রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে       
    path('Inventory/item_receipt_monthly_data_by_department/', inventoryviews.item_receipt_monthly_data_by_department, name='item_receipt_monthly_data_by_department'),
    path('Inventory/item_delivery_monthly_data_by_department/', inventoryviews.item_delivery_monthly_data_by_department, name='item_delivery_monthly_data_by_department'),
   
   # ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল আইটেম ডেট সিলেক্ট করে  
    path('Inventory/item_receipt_department_summary_by_month_based_on_date/', inventoryviews.item_receipt_department_summary_by_month_based_on_date, name='item_receipt_department_summary_by_month_based_on_date'),
    path('Inventory/item_delivery_department_summary_by_month_based_on_date/', inventoryviews.item_delivery_department_summary_by_month_based_on_date, name='item_delivery_department_summary_by_month_based_on_date'),

    #ডেট অনুযায়ী প্রোডাক্ট সামারি  
    path('Inventory/item_receipt_total_by_name_between_dates/', inventoryviews.item_receipt_total_by_name_between_dates, name='item_receipt_total_by_name_between_dates'),
    path('Inventory/item_delivery_total_by_name_between_dates/', inventoryviews.item_delivery_total_by_name_between_dates, name='item_delivery_total_by_name_between_dates'),
    
    #ডেট অনুযায়ী প্রোডাক্ট সামারি ডিপার্টমেন্ট সিলেক্ট করে 
    path('Inventory/item_receipt_total_by_name_between_dates_and_department/', inventoryviews.item_receipt_total_by_name_between_dates_and_department, name='item_receipt_total_by_name_between_dates_and_department'),
    path('Inventory/item_delivery_total_by_name_between_dates_and_department/', inventoryviews.item_delivery_total_by_name_between_dates_and_department, name='item_delivery_total_by_name_between_dates_and_department'),

    #নির্দিষ্ট আইটেমের ডেট অনুযায়ী রিপোর্ট 
    path('Inventory/item_receipt_between_date_by_name/', inventoryviews.item_receipt_between_date_by_name, name='item_receipt_between_date_by_name'),
    path('Inventory/item_delivery_between_date_by_name/', inventoryviews.item_delivery_between_date_by_name, name='item_delivery_between_date_by_name'),
    path('Inventory/issue_for_production_balance_report/', inventoryviews.issue_for_production_balance_report, name='issue_for_production_balance_report'),
    path('Inventory/ledger_entry_view/', inventoryviews.ledger_entry_view, name='ledger_entry_view'),

  
#  ____            _                   ___               _               
# / ___|    __ _  | |   ___   ___     / _ \   _ __    __| |   ___   _ __ 
# \___ \   / _` | | |  / _ \ / __|   | | | | | '__|  / _` |  / _ \ | '__|
#  ___) | | (_| | | | |  __/ \__ \   | |_| | | |    | (_| | |  __/ | |   
# |____/   \__,_| |_|  \___| |___/    \___/  |_|     \__,_|  \___| |_|   
#  
    path('Sales/sales_quotation_between_date/', salesorderviews.sales_quotation_between_date, name='sales_quotation_between_date'),
    path('Sales/sales_order_between_date/', salesorderviews.sales_order_between_date, name='sales_order_between_date'),
    path('Sales/delivery_between_date/', salesorderviews.delivery_between_date, name='delivery_between_date'),
    path('Sales/ar_invoice_between_date/', salesorderviews.ar_invoice_between_date, name='ar_invoice_between_date'),
    path('Sales/ar_invoice_between_date_without_item/', salesorderviews.ar_invoice_between_date_without_item, name='ar_invoice_between_date_without_item'),
    
    #কাস্টমার অর্ডার সামারি রিপোর্ট 
    path('Sales/customer_summary/', salesorderviews.customer_summary, name='customer_summary'),
    #সেলস অর্ডার এর বয়স দেখা     
    path('Sales/sales_order_aging_report/', salesorderviews.sales_order_aging_report, name='sales_order_aging_report'),
    #বয়স অনুযায়ী  সেলস অর্ডার দেখা     
    path('Sales/filter_orders_by_age/', salesorderviews.filter_orders_by_age, name='filter_orders_by_age'),
    #স্ট্যাটাস অনুযায়ী  সেলস অর্ডার দেখা     
    path('Sales/sales_order_status_filter/', salesorderviews.sales_order_status_filter, name='sales_order_status_filter'),
    #প্রোডাক্ট অনুযায়ী  সেলস অর্ডার     
    path('Sales/sales_order_by_product_report/', salesorderviews.sales_order_by_product_report, name='sales_order_by_product_report'),
    #সাইজ অনুযায়ী প্রোডাকশন ব্যালেন্স 
    path('Sales/production_balance_line_wise/', salesorderviews.production_balance_line_wise, name='production_balance_line_wise'),
    #সাইজ অনুযায়ী প্রোডাকশন ও ডেলিভারি ব্যালেন্স    
    path('Sales/order_balance_production_delivery_line_wise/', salesorderviews.order_balance_production_delivery_line_wise, name='order_balance_production_delivery_line_wise'),
    #অর্ডার অনুযায়ী ডেলিভারি চালান বিস্তারিত   
    path('Sales/delivery_items_by_order/', salesorderviews.delivery_items_by_order, name='delivery_items_by_order'),
    
    # আইটেম ব্যালেন্স ডিপার্টমেন্ট অনুযায়ী  
    path('Sales/balance_report_view/', salesorderviews.balance_report_view, name='balance_report_view'),
    #অর্ডার অনুযায়ী চালান লিস্ট 
    path('Sales/delivery_challan_list_based_on_order/', salesorderviews.delivery_challan_list_based_on_order, name='delivery_challan_list_based_on_order'),
    
    # পেন্ডিং পার্টিকুলার  অর্ডার অনুযায়ী    
    path('Sales/pending_particular_based_on_order_no/', salesorderviews.pending_particular_based_on_order_no, name='pending_particular_based_on_order_no'),
    #পেন্ডিং পার্টিকুলার  ডেট অনুযায়ী     
    path('Sales/pending_particular_between_on_date/', salesorderviews.pending_particular_between_on_date, name='pending_particular_between_on_date'),
    #পেন্ডিং পার্টিকুলার  আইটেম অনুযায়ী
    path('Sales/sum_quantity_by_name/', salesorderviews.sum_quantity_by_name, name='sum_quantity_by_name'),
    
    #অর্ডার অনুযায়ী ডেলিভারি ও চালান রেসিভ দেখা
    path('Sales/check_delivery_status/', salesorderviews.check_delivery_status, name='check_delivery_status'),
    
    #অর্ডার অনুযায়ী ডেলিভারি পার্সেন্টেজ 
    path('Sales/calculate_delivery_percentage/', salesorderviews.calculate_delivery_percentage, name='calculate_delivery_percentage'),
    
    # আইটেম group সিলেক্ট করে আইটেম group  অনুযায়ী টোটাল সেলস quantity এবং  এমাউন্ট     
    path('Sales/calculate_summary/', salesorderviews.calculate_summary, name='calculate_summary'),
    #আইটেম অনুযায়ী অর্ডার টোটাল আইটেম quantity, এমাউন্ট সামারি 
    path('Sales/sales_order_item_wise_summary/', salesorderviews.sales_order_item_wise_summary, name='sales_order_item_wise_summary'),
    


# ____                  _                              ____                   _                               
# | __ )   _   _   ___  (_)  _ __     ___   ___   ___  |  _ \    __ _   _ __  | |_   _ __     ___   _ __   ___ 
# |  _ \  | | | | / __| | | | '_ \   / _ \ / __| / __| | |_) |  / _` | | '__| | __| | '_ \   / _ \ | '__| / __|
# | |_) | | |_| | \__ \ | | | | | | |  __/ \__ \ \__ \ |  __/  | (_| | | |    | |_  | | | | |  __/ | |    \__ \
# |____/   \__,_| |___/ |_| |_| |_|  \___| |___/ |___/ |_|      \__,_| |_|     \__| |_| |_|  \___| |_|    |___/
#                                                                                                              
 
    #কাস্টমার অনুযায়ী সেলস অর্ডার লিস্ট 
    path('Businesspartner/sales_order_based_on_customer_name/', businesspartnerview.sales_order_based_on_customer_name, name='sales_order_based_on_customer_name'),
    #সকল কাস্টমারের সেলস ডেলিভারি রিপোর্ট    
    path('Businesspartner/customer_sales_report/', businesspartnerview.customer_sales_report, name='customer_sales_report'),
                                                                      
#  ____                          _                                          
# |  _ \   _   _   _ __    ___  | |__     __ _   ___    ___     
# | |_) | | | | | | '__|  / __| | '_ \   / _` | / __|  / _ \   
# |  __/  | |_| | | |    | (__  | | | | | (_| | \__ \ |  __/   
# |_|      \__,_| |_|     \___| |_| |_|  \__,_| |___/  \___|    
#



# Datewise
    path('purchasing/purchase_quotation_between_date/', purchasingview.purchase_quotation_between_date, name='purchase_quotation_between_date'),
    path('purchasing/purchase_order_between_date/', purchasingview.purchase_order_between_date, name='purchase_order_between_date'),
    path('purchasing/goods_receipt_po_between_date/', purchasingview.goods_receipt_po_between_date, name='goods_receipt_po_between_date'),
    path('purchasing/ap_invoice_between_date_without_item/', purchasingview.ap_invoice_between_date_without_item, name='ap_invoice_between_date_without_item'),
    path('purchasing/ap_invoice_between_date/', purchasingview.ap_invoice_between_date, name='ap_invoice_between_date'),


#  ____                    _      _                   
# | __ )    __ _   _ __   | | __ (_)  _ __     __ _   
# |  _ \   / _` | | '_ \  | |/ / | | | '_ \   / _` |  
# | |_) | | (_| | | | | | |   <  | | | | | | | (_| |  
# |____/   \__,_| |_| |_| |_|\_\ |_| |_| |_|  \__, |  
#                                             |___/   
    path('banking/incoming_payment_info_between_date/', bankingview.incoming_payment_info_between_date, name='incoming_payment_info_between_date'),
    path('banking/outgoing_payment_info_between_date/', bankingview.outgoing_payment_info_between_date, name='outgoing_payment_info_between_date'),
   
]


